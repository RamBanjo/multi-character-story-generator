#We will write this story generation function based on the new flowchart.

import copy
import random
from components.RelChange import RelChange
from components.RewriteRuleWithWorldState import JoiningJointRule, JointType

from components.StoryGraphTwoWS import StoryGraph
from components.StoryNode import StoryNode
from components.UtilFunctions import permute_actor_list_for_joint, permute_actor_list_for_joint_with_range_and_freesize, permute_actor_list_for_joint_with_variable_length
from components.UtilityEnums import ChangeAction, GenericObjectNode

DEFAULT_HOLD_EDGE_NAME = "holds"
DEFAULT_ADJACENCY_EDGE_NAME = "connect"
DEFAULT_WAIT_NODE = StoryNode(name="Wait", biasweight=0, tags= {"Type":"Placeholder"}, charcount=1)

#TODO (Important): Plot details about how to implement tasks into this function, then add compatibility with the tasks here according to the plot
#TODO (Extra Features): Make Verbose, so that we can read what's going on while the generation is being done.
def generate_story_from_starter_graph(init_storygraph: StoryGraph, list_of_rules, required_story_length, top_n = 5, extra_attempts=5, score_mode=0):

    #make a copy of the graph
    final_story_graph = copy.copy(init_storygraph)

    while True:

        #check the shortest story length
        shortest_path_length = final_story_graph.get_shortest_path_length_from_all()

        #If the path length is equal to or greater than the required length, we're done
        if shortest_path_length >= required_story_length:
            #return result
            return final_story_graph
    
        #Make a list of all characters' path lengths.
        #Reduce this list to only the ones with the shortest path length.
        shortest_path_character_names_list = final_story_graph.get_characters_with_shortest_path_length()

        #Randomly pick one name from that list. That will be the character we generate stories for in this step. 
        current_charname = random.choice(shortest_path_character_names_list)

        latest_state = final_story_graph.make_latest_state()

        current_character = latest_state.node_dict[current_charname]

        action_for_character_found = False

        #acceptable_rules = [r ulefor rule in list_of_rules if final_story_graph.check_rule_validity(current_character, rule)]
        acceptable_rules = [rule for rule in list_of_rules]

        #Give each rule a score according to current graph state and the chosen character.
        acceptable_rules_with_absolute_step_and_score = []

        #Here appears to be where the rules are applied. However, the things we want to apply are no longer all rules, because it now include steps from tasks.
        #How do I add tasks to the list of things that can be done without disrupting the previous architecture? Or do we have to rebuild this function from ground up?
        #Rebuilding will make things work obviously but we need to figure out if this is salvagable first.
        #
        # What do we define a Rewrite Rule as
        # What do we define a Task Advance as
        #
        # Path 1: Convert rules and tasks into a new object
        # In its essence, both things do the same thing: Remove certain number of story nodes from the story (for Task Advance its always 0) and insert certain nodes at the same part
        #
        # In RewriteRule's case, the spots it choose depends on if a pattern exist and if removing/inserting at the spot 
        #
        # Maybe we can use a translator to turn them into the same type of object?
        #
        # Take all the valid spots where we can remove/insert nodes, and then list them as possible changes to the storyline?
        # This will make a lot of things obsolete (like the functions applying the rules or the functions attempting to advance task)
        #
        # In the next section there will be a part where I directly call apply_rewrite_rule and said rule we're applying is from the acceptable_rules list above.
        # Do something about it, maybe?
        #
        # Path No. 2: Make a new object that contains rewrite rule and task advance, use that to signify change in the story at different spots
        #
        # Path No. 3: Make two separate lists. One list is for acceptable rules, the other list is for acceptable task advancement/cancellations.
        # This way, we can prioritize advancing tasks over cancelling tasks.
        # Advancing Tasks should have the same priority as applying rewrite rules in that cancelling tasks can only be done if there's really no other choices.
        # 
        # GeneratorAction where the action is to apply rule, advance task, or cancel task? And then that action object can point to the Rule/Advance that's occuring
        # Or the things being added/removed from the story
        #
        # Only rules have a score, but can we give score to task advancement the same way? Rules are being scored by calculate_score_from_rule_char_and_cont so we should make a function that scores each step of the task too
        #
        # In the event that the character is not in the right location to perform the task, moving towards the task location will be worth some score as well
        # The Task Location Function don't really return any specific task location but it does give the optimal location to travel towards to be closer to a task.
        # In that case, what score should be given? Also there is no task representation or rewrite rule representation for such an action
        # Could be a secret third thing?
        #
        # Secret Third Thing it is!
        #
        # The choosing will be like this:
        # 1. From List of Valid Rewrite Rules: Top 5 Rules
        # 2. From List of Valid Task Advancements: Top 5 Advancements (Task Cancels also go here)
        # 3. If List 2 is empty, We will throw a "Advance towards task location" as one of the possible outcomes in addition to List 1
        # "Advance Towards Task Location" has no score but will always be included along with the Top 5 of the Valid Rewrite Rules
        # It can be weighted to make it more likely in settings
        # Discussed this algorithm with Professor

        #Append the absolute step and score next to rule into the list acceptable rules with score. Watch out for special cases in joint rules:
        # Join Joint and Cont Joint: The score is the max between the actor slot and the target slot. If any slot doesn't allow character placement, the score if the other allowed slot. If both slots are unallowed, the score is -999.
        # Split Joint: The score is the max among all the given splits, excluding the split that doesn't allow the character. If none of the splits allow the character on any slots, the score is -999.
        #
        # Format: (Rule, Insert Index, Score)
        for rule in acceptable_rules:
            for rule_insert_index in range(0, final_story_graph.get_longest_path_length_by_character(current_character)):
                rule_score = final_story_graph.calculate_score_from_rule_char_and_cont(actor=current_character, insert_index=rule_insert_index, score_mode=0)

                #We can use the rule score itself to test whether or not a rule is suitable.
                #In the event of a normal rule, if one node is invalid the entire sequence will return -999, which lets us know the rule isn't valid.
                #In the event of a joint rule, -999 will only be returned if all the available slots are -999, which means that this rule cannot be applied to this character and thus is invalid.
                if rule_score != -999:
                    acceptable_rules_with_absolute_step_and_score.append((rule, rule_insert_index, rule_score))

        acceptable_rules_with_absolute_step_and_score = sorted(acceptable_rules_with_absolute_step_and_score, key=get_element_2, reverse=True)

        #Sort it by biasweight. Python sorts ascending by default, so we must reverse it.
        #acceptable_rules.sort(key=get_biasweight, reverse=True)

        #As seen above, we have created a list of Rewrite Rules. We should create a list of valid Advancements too.
        # Then, from that list of valid task advancements, sort by score.

        #Populate this list with all the tasks that the character can do. If this list is empty, add "Advance Towards Task Location" as one of the actions in the list of valid actions.
        #Format for valid tasks tuple: (Task Stack Name, Task Advance Index, Score, Task Action)
        #(Don't need actor name because actor is already chosen a long time ago)
        available_task_name_list = final_story_graph.get_list_of_task_stack_names_from_latest_step(current_charname)
        
        list_of_available_tasks = []
        cancel_count = 1

        for task_name in available_task_name_list:
            for attempt_index in range(0, final_story_graph.longest_path_length):

                task_completeness = final_story_graph.test_task_completeness()
                task_valid = final_story_graph.test_task_stack_advance_validity(task_stack_name=task_name, actor_name=current_charname, abs_step=task_name)

                if task_valid:
                    default_task_score = 0
                    action_chosen = "Do Nothing"
                    match task_completeness:
                        case 'task_step_already_completed':
                            action_chosen = "Advance"
                        case 'task_step_already_failed':
                            action_chosen = "Cancel"
                            default_task_score = -999
                            cancel_count += 1
                        case 'task_step_incomplete':
                            action_chosen = "Perform"
                            default_task_score = final_story_graph.calculate_score_from_next_task_in_task_stack(actor_name=current_charname, task_stack_name=task_name, task_perform_index=attempt_index, mode=score_mode)
                        case _:
                            default_task_score = -999
                    
                    if action_chosen != "Do Nothing":
                        task_tuple = (task_name, attempt_index, default_task_score, action_chosen)
                        list_of_available_tasks.append(task_tuple)

        #Fill in this list with valid actions to take, pointing towards either the acceptable rules or the tasks that can be advanced
        list_of_valid_actions = []
        for rule_tuple in acceptable_rules:
            action_tuple = ("Apply Rule", rule_tuple, rule_tuple[2])
            list_of_valid_actions.append(action_tuple)

        force_move_towards_quest_into_top_n = False

        #Checking the number of things that say "Cancel".
        task_count = len(list_of_available_tasks)
        cancel_count = len([x for x in list_of_available_tasks if x[3] == "Cancel"])

        #So if there is not a task or if everything is a cancel, we add a move towards quest action
        if len(list_of_available_tasks) < 0 or task_count == cancel_count:
            force_move_towards_quest_into_top_n = True
        
        if len(list_of_available_tasks) > 0:
            for task_tuple in list_of_available_tasks:
                action_tuple = ("Apply Task", task_tuple, task_tuple[2])
                list_of_valid_actions.append(action_tuple)

        #Modify the following part so that it picks top 5 from both the acceptable rules and the available tasks instead.
        #
        #If the list of available tasks is empty, then insert "Advance Towards Task Location" into the Top 5
        #Here, we will choose from top n rules.
        #Also, if none of these actions are valid, we either advance towards task location or wait. 1/2 chance for either one.
        #TODO (Important): No Valid Actions will essentially never happen because Move Towards Task Location is always valid. :thinking:
        
        sorted_list_of_valid_actions = sorted(list_of_valid_actions, key=get_element_2, reverse=True)
        top_pick_count = top_n
        if len(list_of_valid_actions) < top_n:
            top_pick_count = len(sorted_list_of_valid_actions)

        top_n_valid_actions = sorted_list_of_valid_actions[:top_pick_count]
        extra_actions = sorted_list_of_valid_actions[top_pick_count:]

        #Since we don't want to clog top_n_valid_actions, we're just going to insert this action as-is.
        #We will randomly pick one valid spot to move to that location here, although it will most likely be the last step so might as well as make that the only option?
        if force_move_towards_quest_into_top_n:
            top_n_valid_actions.append(("Move Towards Task Location", None, 0))

        

        # if len(acceptable_rules_with_absolute_step_and_score) < top_n:
        #     top_pick_count = len(acceptable_rules_with_absolute_step_and_score)

        # top_n_acceptable_rules = acceptable_rules_with_absolute_step_and_score[:top_pick_count]
        # extra_rules = acceptable_rules_with_absolute_step_and_score[top_pick_count:]

        # if len()
        extra_attempts_left = extra_attempts        

        #TODO (Important): Edit this entire loop to make it work with Task Advancements
        while not action_for_character_found:

            # #Check the length of the list now. Do we have enough? If this is blank, we must make our character wait.
            if len(top_n_valid_actions) == 0 or extra_attempts_left == 0:
                 latest_action = final_story_graph.get_latest_story_node_from_character()
                 final_story_graph.add_story_part(part=DEFAULT_WAIT_NODE, character=current_character, timestep=latest_action.timestep)
                 action_for_character_found = True

            # #From the valid options, we pick from the rule we will use randomly.
            chosen_action = random.choice(top_n_valid_actions)
            top_n_valid_actions.remove(chosen_action)

            # What is this action? We check the first element to find out.
            #Each action will return a true/false value. If the apply is successful, True is returned. If not, False is returned.
            match chosen_action[0]:
                case "Apply Rule":
                    action_for_character_found = attempt_apply_rule(chosen_rule=chosen_action[1], target_story_graph=final_story_graph, character_object=current_character, shortest_path_charname_list=shortest_path_character_names_list)
                case "Apply Task":
                    action_for_character_found = attempt_apply_task(task_tuple=chosen_action[1], target_story_graph=final_story_graph, current_character=current_character)
                case "Move Towards Task Location":

                    #We can make a list of index and randomly pick from it until it gives us a positive result
                    #Let's do it in the function

                    action_for_character_found = attempt_move_towards_task_loc(target_story_graph=final_story_graph, current_character=current_character)
                case _:
                    pass
            
            #If we don't find the rule to apply yet, we might need to add new rules to top_n. Suitable rules might be clogged behind invalid joint rules.
            if not action_for_character_found:
                if extra_attempts_left == -1 or extra_attempts > 0:
                    #Check if we have any attempts left, if we do, then add the first thing from the extra rules if there are still more extra rules
                    if len(extra_actions) > 0:
                        top_n_valid_actions.append(extra_actions.pop(0))
                    if extra_attempts_left > 0:
                        extra_attempts_left -= 1
            else:
                #If we did find the rule to apply we should update the story graph so that the locations show up in the story.
                final_story_graph.fill_in_locations_on_self()

        #Finally, we fill in the locations on self and update the list of changes.
        final_story_graph.update_list_of_changes()
        final_story_graph.fill_in_locations_on_self()



def get_element_2(e):
    return e[2]

def attempt_apply_rule(chosen_rule, target_story_graph, character_object, shortest_path_charname_list):

    apply_rule_success = False

    current_charname = character_object.get_name()
    current_rule = chosen_rule[0]
    current_index = chosen_rule[1]
    #Keep in mind that the the chosen rule is a tuple. Index 0 is the node itself, Index 1 is the location to apply to, Index 2 is the score (which we won't use here.)

    #If it's just a normal rewrite rule, we can instantly apply it because we don't need to check its validity with other nodes. We'll apply it to one random good spot.

    # Apply rewrite rule, but we can choose the specific spot? Or maybe just use insert function here because we already did the checks above and we know the rule can be applied because it passes the tests.
    # Maybe use the banned subgraph locs to ban everything that's not the chosen index?
    if not current_rule.is_joint_rule:

        current_purge_count = 0

        if current_rule.remove_before_insert:
            current_purge_count = len(current_rule.story_condition)

        #TODO (Extra Features): apply_rewrite_rule already has continuation validity thing going on, so why are we checking it twice here? Read into this.
        nonjoint_cont_valid = target_story_graph.check_continuation_validity(actor=target_story_graph, abs_step_to_cont_from=current_index, cont_list=current_rule.story_change, target_list=current_rule.target_list, purge_count=current_purge_count)

        if nonjoint_cont_valid:
            #Get the locations where this pattern can be applied, set everything as banned except the location that we want.
            pattern_check_result = target_story_graph.check_for_pattern_in_storyline(current_rule.story_condition, target_story_graph)
            banned_locs = pattern_check_result[1]
            banned_locs.remove(current_index)
            #At no point in apply rewrite rule or check for pattern in storyline does the continuation validity get checked so we need to check for continuation validity.
            #If the application of the rule is successful, then this should return true.
            #Checking for continuation validity already exists within Apply Rewrite Rule, so we don't have to do anything extra here.
            apply_rule_success = target_story_graph.apply_rewrite_rule(chosen_rule, character_object, applyonce=True, banned_subgraph_locs=banned_locs)

    else:
        applicable_character_names = []
        all_possible_character_list = []
        character_count = current_rule.get_character_count()

        if current_rule.join_type == JointType.JOIN:
            applicable_character_names += shortest_path_charname_list
            applicable_character_names.remove(current_charname)

            all_possible_character_list += permute_actor_list_for_joint_with_range_and_freesize(current_actor=current_charname, other_actors=applicable_character_names, size=character_count)
        else:
            current_node = target_story_graph.story_parts.get((current_charname, current_index-1), None)

            #If the current node is None then there is nothing to continue this Joint Rule from. We need a Joint Node to use a ContinuousJoint or SplittingJoint, so this rule is not valid.

            if current_node is not None:
                applicable_character_names += [actor.get_name() for actor in current_node.actor]
                applicable_character_names += [target.get_name() for target in current_node.target if target in target_story_graph.character_objects]

            all_possible_character_list = [applicable_character_names]
            #If we get into the else, this means the join type isn't a joinjoint therefore we just take everyone in the character's current node.

        valid_character_grouping = None
        grouping_choose_complete = False

        while not grouping_choose_complete:

            if len(chosen_grouping > 0):
                chosen_grouping = random.choice(all_possible_character_list)
                all_possible_character_list.remove(chosen_grouping)

                if current_rule.join_type == JointType.SPLIT:
                    chosen_grouping_split = current_rule.split_list
                else:
                    chosen_grouping_split = [current_rule.joint_node]

                current_state = target_story_graph.make_state_at_step(current_index)
                chosen_grouping_with_character_objects = []

                for actor_name in chosen_grouping:
                    chosen_grouping_with_character_objects.append(current_state.node_dict[actor_name])

                chosen_grouping_split = target_story_graph.pick_one_random_valid_character_grouping_from_all_valid_groupings(continuations=chosen_grouping_split, abs_step=current_index, character_list=chosen_grouping_with_character_objects)

                #If there are no valid splits here at all, it's skipped.
                if chosen_grouping_split is None:
                    continue

                rule_validity = target_story_graph.check_joint_continuity_validity(joint_rule=chosen_rule[0], main_character=character_object, grouping_split=chosen_grouping_split, insert_index=current_index)

                if rule_validity:
                    valid_character_grouping = chosen_grouping_split
                    grouping_choose_complete = True
            else:
                valid_character_grouping = None
                grouping_choose_complete = True

        #If the combination is valid, then we need to apply the specified node/continuations and then mark that we have found a proper continuation.
        if valid_character_grouping is not None:
            
            #Apply the continuation based on whether the rule was a split rule.
            if current_rule.join_type == JointType.SPLIT:
                target_story_graph.split_continuation(split_list=current_rule.split_list, chargroup_list=valid_character_grouping, abs_step=current_index)
            else:
                target_story_graph.joint_continuation(loclist=[current_index], joint_node=current_rule.joint_node, actors=valid_character_grouping[0]["actor_group"], target_list=valid_character_grouping[0]["target_group"], applyonce=True)

            apply_rule_success = True

    return apply_rule_success

def attempt_apply_task(task_tuple, target_story_graph, current_character):

    task_stack_name = task_tuple[0]
    attempt_index = task_tuple[1]
    task_action = task_tuple[3]

    #Since the action is already determined by the function within SG2WS, theres no need to split this into three like I thought I had to.
    #TODO (Testing): HOWEVER we need to ensure that this function works as intended. Test this.
    advance_success = target_story_graph.attempt_advance_task_stack(task_stack_name=task_stack_name, actor_name=current_character.get_name(), abs_step=attempt_index)
    return advance_success

#TODO (Testing): Test this function
# Will return True if changes are made and False if not.
def attempt_move_towards_task_loc(target_story_graph:StoryGraph, current_character, movement_index):

    current_ws = target_story_graph.make_state_at_step(movement_index)
    character_at_step = current_ws.node_dict[current_character.get_name()]
    optimal_location_object = current_ws.get_optimal_location_towards_task(current_character)
    current_location_of_character = current_ws.get_actor_current_location(current_character)

    #if we're in the same location then we don't need to do the things below. Since we don't want to move locations this should return False.
    if optimal_location_object.get_name() == current_location_of_character.get_name():
        return False
    
    go_to_new_location_change = RelChange("Go to Task Loc", node_a=optimal_location_object, edge_name=DEFAULT_HOLD_EDGE_NAME, node_b=character_at_step, add_or_remove=ChangeAction.ADD)
    not_be_in_current_location_change = RelChange("Leave Current Loc", node_a=GenericObjectNode.GENERIC_LOCATION, edge_name=DEFAULT_HOLD_EDGE_NAME, node_b=character_at_step, add_or_remove=ChangeAction.REMOVE)
    move_towards_task_location_node = StoryNode("Move Towards Task Location", biasweight=0, tags={"Type":"Movement"}, charcount=1, effects_on_next_ws=[go_to_new_location_change, not_be_in_current_location_change])

    #We have made our custom move towards task location node. We will check to see if it's a valid move to move to that location.
    movement_validity = target_story_graph.check_continuation_validity(actor=current_character, abs_step_to_cont_from=movement_index, cont_list=[move_towards_task_location_node])
    if movement_validity:
        target_story_graph.insert_story_part(part=move_towards_task_location_node, character=current_character, absolute_step=movement_index)
        return True
    
def cycle_attempt_move_towards_task_loc(target_story_graph:StoryGraph, current_character):
    
    #The path length of the character is the range.

    path_length_list = target_story_graph.get_all_path_length_with_charname()
    current_char_path_length = [x[1] for x in path_length_list if x[0] == current_character.get_name()]
    possible_insert_locs = list(range(0, current_char_path_length))

    good_insert_loc_found = False

    while not good_insert_loc_found:
        
        if len(possible_insert_locs) == 0:
            return False
        
        chosen_loc = random.choice(possible_insert_locs)
        possible_insert_locs.remove(chosen_loc)

        if attempt_move_towards_task_loc(target_story_graph=target_story_graph, current_character=current_character, movement_index=chosen_loc):
            return True
        #Pick a random thing from the possible insert locs, remove it
    
    
    

                # We have our current character and we have a list of characters whose stories can be extended because they have the shortest paths. We also have the absolute step that we will build from.
                # We would like to find out that, with the given rule, who should be in the grouping.
                #
                # For ContinuousJoint and SplittingJoint, the grouping is simple: just take all the actors from the actor/target slots, from the steps where the base joint is found. If no base joint is found, then the pattern is invalid and the rule should be removed from the list.
                #   We have check_for_jointrule_location_in_storyline for this purpose to look for the base joint in the storyline. It also returns a list of the absolute step where the base joint is.
                # For JoiningJoint is a bit more complex. We need to call check_if_abs_step_has_joint_pattern for all the steps. Then, use list_all_good_combinations_from_joint_join_pattern to make list of possible char groups.
                # For 

                # if type(chosen_rule) == JoiningJointRule:
                #     pass
                # else:
                #     pass

                # list_of_possible_char_groups = []

                # characters_wanted_count = chosen_rule.get_character_count()
                # minimum_actor_count = 2

                # if chosen_rule.joint_type == JointType.SPLIT:
                #     minimum_actor_count = len(chosen_rule.split_list)

                # if type(characters_wanted_count) == tuple:
                #     list_of_possible_char_groups += permute_actor_list_for_joint_with_variable_length(current_charname, applicable_character_names, characters_wanted_count[0], characters_wanted_count[1])
                # elif characters_wanted_count == -1:
                #     list_of_possible_char_groups += permute_actor_list_for_joint_with_variable_length(current_charname, applicable_character_names, minimum_actor_count, characters_wanted_count[1])
                # else:
                #     list_of_possible_char_groups += permute_actor_list_for_joint(current_charname, applicable_character_names, characters_wanted_count)
