#We will write this story generation function based on the new flowchart.

from copy import deepcopy
import random
from components.RelChange import RelChange
from components.RewriteRuleWithWorldState import JoiningJointRule, JointType

from components.StoryGraphTwoWS import StoryGraph
from components.StoryNode import StoryNode
from components.UtilFunctions import permute_actor_list_for_joint, permute_actor_list_for_joint_with_range_and_freesize, permute_actor_list_for_joint_with_variable_length
from components.UtilityEnums import ChangeAction, GenericObjectNode

DEFAULT_HOLD_EDGE_NAME = "holds"
DEFAULT_ADJACENCY_EDGE_NAME = "connects"
DEFAULT_WAIT_NODE = StoryNode(name="Wait", biasweight=0, tags= {"Type":"Placeholder"}, charcount=1)

#Actually yeah making Verbose would make testing this way, way easier than it needs to be. So we're going to make Verbose
#...head in hands. This is so bad. This is a bad system I have created.
#Like for real for real there's no way I can realistically test this without a Verbose letting us know what's going on where.
#TODO (Extra Features): Make Verbose, so that we can read what's going on while the generation is being done.
def generate_story_from_starter_graph(init_storygraph: StoryGraph, list_of_rules, required_story_length, top_n = 5, extra_attempts=5, score_mode=0, verbose=False):

    #make a copy of the graph
    if verbose:
        print("Creating a copy of the Storygraph")
    final_story_graph = deepcopy(init_storygraph)

    while True:

        #check the shortest story length
        shortest_path_length = final_story_graph.get_shortest_path_length_from_all()

        #If the path length is equal to or greater than the required length, we're done
        if shortest_path_length >= required_story_length:
            #return result
            if verbose:
                print("Shortest path of story has reached desired length, terminating generation and returning result.")
            return final_story_graph
    
        #Make a list of all characters' path lengths.
        #Reduce this list to only the ones with the shortest path length.
        if verbose:
            print("Getting the names of characters with shortest path...")    
        shortest_path_character_names_list = final_story_graph.get_characters_with_shortest_path_length()

        #Randomly pick one name from that list. That will be the character we generate stories for in this step. 
        current_charname = random.choice(shortest_path_character_names_list)
        if verbose:
            print("Chosen current character:", current_charname)
        latest_state = final_story_graph.make_latest_state()

        current_character = latest_state.node_dict[current_charname]

        action_for_character_found = False

        if verbose:
            print("Making list of Acceptable Rules")
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
        if verbose:
            print("Checking for acceptable actions...")
        for rule in acceptable_rules:
            for rule_insert_index in range(0, final_story_graph.get_longest_path_length_by_character(current_character)):
                rule_score = final_story_graph.calculate_score_from_rule_char_and_cont(actor=current_character, insert_index=rule_insert_index, rule = rule, mode=0)

                #We can use the rule score itself to test whether or not a rule is suitable.
                #In the event of a normal rule, if one node is invalid the entire sequence will return -999, which lets us know the rule isn't valid.
                #In the event of a joint rule, -999 will only be returned if all the available slots are -999, which means that this rule cannot be applied to this character and thus is invalid.
                if rule_score != -999:
                    
                    if verbose:
                        print("Found Acceptable Rule", rule.rule_name, "at", rule_insert_index)
                    rule_container = StoryGenerationActionContainer(action_name="Apply Rule", action_object=rule, action_score=rule_score, perform_index=rule_insert_index)
                    acceptable_rules_with_absolute_step_and_score.append(rule_container)

        acceptable_rules_with_absolute_step_and_score = sorted(acceptable_rules_with_absolute_step_and_score, key=get_action_score, reverse=True)
        if verbose:
            print("Acceptable rules found:", len(acceptable_rules_with_absolute_step_and_score))

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
                            action_chosen = "Advance Task"
                        case 'task_step_already_failed':
                            action_chosen = "Cancel Task"
                            default_task_score = -999
                            cancel_count += 1
                        case 'task_step_can_advance':
                            action_chosen = "Perform Task"
                            default_task_score = final_story_graph.calculate_score_from_next_task_in_task_stack(actor_name=current_charname, task_stack_name=task_name, task_perform_index=attempt_index, mode=score_mode)
                        case _:
                            default_task_score = -999
                    
                    if action_chosen != "Do Nothing":

                        task_container = StoryGenerationActionContainer(action_name=action_chosen, action_object=task_name, action_score=default_task_score, perform_index=attempt_index)
                        list_of_available_tasks.append(task_container)

        if verbose:
            print("Acceptable task-related actions found:", len(list_of_available_tasks))


        #Fill in this list with valid actions to take, pointing towards either the acceptable rules or the tasks that can be advanced
        list_of_valid_actions = []
        for rule_container in acceptable_rules_with_absolute_step_and_score:
            list_of_valid_actions.append(rule_container)

        force_move_towards_quest_into_top_n = False

        #Checking the number of things that say "Cancel".
        task_count = len(list_of_available_tasks)
        cancel_count = len([x for x in list_of_available_tasks if x[3] == "Cancel"])

        #So if there is not a task or if everything is a cancel, we add a move towards quest action
        if len(list_of_available_tasks) < 0 or task_count == cancel_count:
            if verbose:
                print("No valid tasks found. We will add a move towards task location action to Top N.")
                print("We will also add a wait action.")
            force_move_towards_quest_into_top_n = True
        
        if len(list_of_available_tasks) > 0:
            if verbose:
                print("Some tasks are found. We will add task actions to the list of valid actions.")            
            for task_container in list_of_available_tasks:
                list_of_valid_actions.append(task_container)

        if verbose:
            print("Acceptable total actions found:", len(list_of_valid_actions))                

        #Modify the following part so that it picks top 5 from both the acceptable rules and the available tasks instead.
        #
        #If the list of available tasks is empty, then insert "Advance Towards Task Location" into the Top 5
        #Here, we will choose from top n rules.
        #Also, if none of these actions are valid, we either advance towards task location or wait. 1/2 chance for either one.
        # TODO (Important): No Valid Actions will essentially never happen because Move Towards Task Location is always valid. :thinking:
        # You know what, I'm fine with this. We can make characters move around if there are no valid actions, with staying and waiting being the "last resort" option in the event that there are no possible actions.

        sorted_list_of_valid_actions = sorted(list_of_valid_actions, key=get_action_score, reverse=True)
        top_pick_count = top_n
        if len(list_of_valid_actions) < top_n:
            if verbose:
                print("Picking Top", top_n, "Actions...")            
            top_pick_count = len(sorted_list_of_valid_actions)

        top_n_valid_actions = sorted_list_of_valid_actions[:top_pick_count]
        extra_actions = sorted_list_of_valid_actions[top_pick_count:]

        #Since we don't want to clog top_n_valid_actions, we're just going to insert this action as-is.
        #We will randomly pick one valid spot to move to that location here, although it will most likely be the last step so might as well as make that the only option?
        
        # TODO (Important): There's a lot of redundant waiting in the testing. How will we be able to eliminate that?
        # The solution might lie in checking the attempt move towards quest
        if force_move_towards_quest_into_top_n:
            final_abs_step = final_story_graph.get_longest_path_length_by_character(character=current_character) -1
            move_towards_quest_container = StoryGenerationActionContainer(action_name="Move Towards Task Location", action_object=None, action_score=0, perform_index=final_abs_step)
            top_n_valid_actions.append(move_towards_quest_container)

        if verbose:
            print("Top N Total (This number will be 1 more than Top N if Move Towards Task Loc exists):", len(top_n_valid_actions))     

        # if len(acceptable_rules_with_absolute_step_and_score) < top_n:
        #     top_pick_count = len(acceptable_rules_with_absolute_step_and_score)

        # top_n_acceptable_rules = acceptable_rules_with_absolute_step_and_score[:top_pick_count]
        # extra_rules = acceptable_rules_with_absolute_step_and_score[top_pick_count:]

        # if len()
        extra_attempts_left = extra_attempts        

        if verbose:
            print("Choosing action to do...")
        while not action_for_character_found:

            if verbose:
                print("Extra Attempts Left:", extra_attempts_left)

            # #Check the length of the list now. Do we have enough? If this is blank or if we're out of attempts, we must make our character wait.
            if len(top_n_valid_actions) == 0 or extra_attempts_left == 0:
                if verbose and len(top_n_valid_actions) == 0:
                    print("No valid actions found! This character will wait.")
                if verbose and extra_attempts_left == 0:
                    print("Out of extra attempts! This character will wait.")                     
                latest_action = final_story_graph.get_latest_story_node_from_character(current_character)
                final_story_graph.add_story_part(part=DEFAULT_WAIT_NODE, character=current_character, timestep=latest_action.timestep)
                action_for_character_found = True

            # #From the valid options, we pick from the rule we will use randomly.
            chosen_action_container = random.choice(top_n_valid_actions)
            top_n_valid_actions.remove(chosen_action_container)

            action_type = chosen_action_container.action_name

            # What is this action? We check the first element to find out.
            #Each action will return a true/false value. If the apply is successful, True is returned. If not, False is returned.
            match action_type:
                case "Apply Rule":
                    if verbose:
                        print("Attempting to apply a rule:",chosen_action_container.action_object.rule_name,"at abs_step",chosen_action_container.perform_index,"for",current_charname)
                    action_for_character_found = attempt_apply_rule(rule_object=chosen_action_container.action_object, perform_index=chosen_action_container.perform_index, target_story_graph=final_story_graph, character_object=current_character, shortest_path_charname_list=shortest_path_character_names_list)
                case "Advance Task":
                    if verbose:
                        print("Attempting to advance task:",chosen_action_container.action_object,"at",chosen_action_container.perform_index,"for",current_charname)
                    action_for_character_found = attempt_apply_task(stack_name=chosen_action_container.action_object, attempt_index=chosen_action_container.perform_index, target_story_graph=final_story_graph, current_character=current_character)
                case "Perform Task":
                    if verbose:
                        print("Attempting to perform task:",chosen_action_container.action_object,"at",chosen_action_container.perform_index,"for",current_charname)
                    action_for_character_found = attempt_apply_task(stack_name=chosen_action_container.action_object, attempt_index=chosen_action_container.perform_index, target_story_graph=final_story_graph, current_character=current_character)
                case "Cancel Task":
                    if verbose:
                        print("Attempting to cancel task:",chosen_action_container.action_object,"at",chosen_action_container.perform_index,"for",current_charname)
                    action_for_character_found = attempt_apply_task(stack_name=chosen_action_container.action_object, attempt_index=chosen_action_container.perform_index, target_story_graph=final_story_graph, current_character=current_character)
                case "Move Towards Task Location":
                    if verbose:
                        print("Attempting to move towards task location:")

                    #We can make a list of index and randomly pick from it until it gives us a positive result
                    #Let's do it in the function
                    #Actually, I think it would be better to always call this function from the latest step.
                    action_for_character_found = attempt_move_towards_task_loc(target_story_graph=final_story_graph, current_character=current_character, movement_index=final_abs_step)
                case "Wait":
                    pass
                case _:
                    pass

            if verbose:
                print("Chosen action validity:", action_for_character_found)
                if action_for_character_found:
                    print("The action is valid, so the action was performed.")

            #If we don't find the rule to apply yet, we might need to add new rules to top_n. Suitable rules might be clogged behind invalid joint rules.
            if not action_for_character_found:
                if extra_attempts_left == -1 or extra_attempts > 0:
                    if verbose:
                        print("We still have extra attempts, so we'll keep trying.")
                    #Check if we have any attempts left, if we do, then add the first thing from the extra rules if there are still more extra rules
                    if len(extra_actions) > 0:
                        top_n_valid_actions.append(extra_actions.pop(0))
                    if extra_attempts_left > 0:
                        extra_attempts_left -= 1
            else:
                #If we did find the rule to apply we should update the story graph so that the locations show up in the story.

                #Temporary Print
                # for part in final_story_graph.story_parts.values():
                #     print(part.name)
                #     print("prev",part.previous_nodes)
                #     print("next",part.next_nodes)
                #     print("-----")

                final_story_graph.fill_in_locations_on_self()

        #Finally, we fill in the locations on self and update the list of changes.
        final_story_graph.update_list_of_changes()
        final_story_graph.fill_in_locations_on_self()

#TODO (Testing): Test this function to see if it really works because WOW I think it's broken. We have valid rules that didn't get applied!
def attempt_apply_rule(rule_object, perform_index, target_story_graph, character_object, shortest_path_charname_list, verbose=False):

    apply_rule_success = False

    current_charname = character_object.get_name()
    current_rule = rule_object
    current_index = perform_index
    #Keep in mind that the the chosen rule is a tuple. Index 0 is the node itself, Index 1 is the location to apply to, Index 2 is the score (which we won't use here.)

    #If it's just a normal rewrite rule, we can instantly apply it because we don't need to check its validity with other nodes. We'll apply it to one random good spot.

    # Apply rewrite rule, but we can choose the specific spot? Or maybe just use insert function here because we already did the checks above and we know the rule can be applied because it passes the tests.
    # Maybe use the banned subgraph locs to ban everything that's not the chosen index?
    if not current_rule.is_joint_rule:

        current_purge_count = 0

        if current_rule.remove_before_insert:
            current_purge_count = len(current_rule.story_condition)

        #TODO (Extra Features): apply_rewrite_rule already has continuation validity thing going on, so why are we checking it twice here? Read into this.
        nonjoint_cont_valid = target_story_graph.check_continuation_validity(actor=character_object, abs_step_to_cont_from=current_index, cont_list=current_rule.story_change, target_list=current_rule.target_list, purge_count=current_purge_count)

        if nonjoint_cont_valid:
            #Get the locations where this pattern can be applied, set everything as banned except the location that we want.
            #At no point in apply rewrite rule or check for pattern in storyline does the continuation validity get checked so we need to check for continuation validity.
            #If the application of the rule is successful, then this should return true.
            #Checking for continuation validity already exists within Apply Rewrite Rule, so we don't have to do anything extra here.
            apply_rule_success = target_story_graph.apply_rewrite_rule(rule=current_rule, character=character_object, abs_step=current_index)

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

                rule_validity = target_story_graph.check_joint_continuity_validity(joint_rule=current_rule, main_character=character_object, grouping_split=chosen_grouping_split, insert_index=current_index)

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
                target_story_graph.joint_continuation(abs_step=current_index, joint_node=current_rule.joint_node, actors=valid_character_grouping[0]["actor_group"], target_list=valid_character_grouping[0]["target_group"])

            apply_rule_success = True

    return apply_rule_success

#TODO (Testing): Test this function
def attempt_apply_task(stack_name, attempt_index, target_story_graph, current_character):

    #Since the action is already determined by the function within SG2WS, theres no need to split this into three like I thought I had to.
    # TODO (Testing): HOWEVER we need to ensure that this function works as intended. Test this.
    advance_success = target_story_graph.attempt_advance_task_stack(task_stack_name=stack_name, actor_name=current_character.get_name(), abs_step=attempt_index)
    return advance_success

# TODO (Testing): Test this function
# Will return True if changes are made to the story graph and False if not.
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

def perform_wait_action(target_story_graph:StoryGraph, current_character):
    latest_action = target_story_graph.get_latest_story_node_from_character()
    target_story_graph.add_story_part(part=DEFAULT_WAIT_NODE, character=current_character, timestep=latest_action.timestep)
    
    return True
    
    
    

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


class StoryGenerationActionContainer:
    def __init__(self, action_name, action_object, action_score, perform_index) -> None:

        self.action_name = action_name
        self.action_object = action_object
        self.action_score = action_score
        self.perform_index = perform_index

def get_action_score(e: StoryGenerationActionContainer):
    return e.action_score