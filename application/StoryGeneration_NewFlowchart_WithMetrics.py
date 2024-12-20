#We will write this story generation function based on the new flowchart.
import statistics
import sys

sys.path.insert(0,'')

from copy import deepcopy
import random
from application.components.ConditionTest import HasEdgeTest
from application.components.RelChange import RelChange, TaskChange
from application.components.RewriteRuleWithWorldState import JoiningJointRule, JointType

from application.components.StoryGraphTwoWS import StoryGraph
from application.components.StoryNode import StoryNode
from application.components.UtilFunctions import permute_actor_list_for_joint, permute_actor_list_for_joint_with_range_and_freesize, permute_actor_list_for_joint_with_variable_length, scrambled_sort
from application.components.UtilityEnums import ChangeAction, GenericObjectNode
from application.components.CharacterTask import TaskStack

# DEFAULT_HOLD_EDGE_NAME = "holds"
# DEFAULT_ADJACENCY_EDGE_NAME = "connects"
DEFAULT_WAIT_NODE = StoryNode(name="Wait", biasweight=0, tags= {"Type":"Placeholder"}, charcount=1)

# TODO: Add Metric Requirements
# While choosing potential actions, if metric_requirements is not an empty list, then we will check for metric information.
# If a potential action would cause a metric requirement to be violated, then that action should be excluded from the list of possible actions.
#
# Some metrics that can be used:
#
# uniqueness (character_name, value from 0 to 100, metric mode) (Uniqueness is measured by unique nodes / total nodes)
# preference (character_name, value from 0 to 100, metric mode) (Preference is measured by Important Nodes / total nodes)
# jointability (character_name, value from 0 to 100, metric mode) (Jointability is measured by Joint Nodes / total nodes)
# cost (character_name, value from 0 to 100, metric mode) (Cost is measured by Costly Nodes / total nodes)
#
# Remember:
# If an action causes an object to be removed from the game world, the cost is 1. (According to ReGEN)
# I suppose we can count the number of costly nodes if that's the case, then?
# 
# There are three modes. Keep lower, keep higher, and keep stable
# Keep Lower: If the value of the following metric isn't already lower than the specified percentage, it will try to make it lower. If it's already lower, it will try to keep it low.
# - Increase points for nodes that would cause the value to decrease, and decrease points for nodes that would cause the value to increase
#
# Keep Higher: Opposite of Keep Lower. Try to get a high percentage and keep the percentage high.
# - Increase points for nodes that would cause the value to increase, and decrease points for nodes that would cause the value to decrease.
#
# Keep Stable: A mix of both. If drastically higher or lower, will try to get +-5% within the range of the percentage.
# - Increase points for nodes that would make it the case. Decrease points otherwise.
#
# (The only exception is the wait node. You just can't do more fillers if you've waited for quite a bit.)

'''
init_storygraph: The initial Story Graph that the generation will be based on.
list_of_rules: The list of rules that the generator can apply to the graph.
required_story_length: How long the resulting StoryGraph should at least be (in nodes). Result may be greater than this value, but it will not be lesser.
top_n: When choosing an action to do, the generator will pick from the best scoring n actions.
extra_attempts: How many times the generator will attempt to find a valid action before giving up and having the character do nothing (wait). If set to -1 it will never give up.
score_mode: There are two score modes. Score Mode 0 will pick the highest node in the rule as that rule's score. Score Mode 1 will average the scores of all nodes in the rule.
verbose: If set to True, the console will print what the generator is currently doing.
extra_movement_requirement_list: List of ConditionTests that a character must fulfill in order to perform a move action. You can use GenericObjectNode.GENERIC_ACTOR to refer to the moving character, GenericObjectNode.GENERIC_LOCATION to refer to the current location, and GenericObjectNode.GENERIC_TARGEt to refer to the target location that is being moved into.
suggested_movement_requirement_list: Same as above, but passing the tests grand the score listed in the test. The highest score movements will be prioritized.
minimum_move_req_score: If set to None, then there is no minimum score. Otherwise, it will use the score from suggested_movement_requirement_list score and exclude certain movements that don't score enough.
action_repeat_penalty: This amount of points will be deducted if the same rule is applied multiple itmes in the same storyline.
metrics_requirements: List of StoryMetrics. The metric requirements that controls how the characters choose their actions.
metric_reward: Extra points granted for following the metrics_requirements. For reaching the Metric Goal, max reward is given. If the action chosen does not reach the Metric Goal, The amount given will be ratio between the max distance and the current distance. (EX. If goal is 20 or Higher and an action would cause a score to be 19, we would have 19/20 * metric_reward.)
metric_penalty: Points deducted for not following the metrics_requirements. For not completing the Metric Goal, max penalty is given. Penalty is increased the further the result is from the Metric Goal. (EX. 20 or Higher and an action would cause it to go from 22 to 19, we would have 21/20 * metric_reward.)
task_movement_random: If set to True, when a character is attempting to move, they will choose randomly. If set to False it will always choose the first available location.
'''
def generate_story_from_starter_graph(init_storygraph: StoryGraph, list_of_rules, required_story_length, top_n = 5, extra_attempts=5, score_mode=0, verbose=False, extra_movement_requirement_list = [], suggested_movement_requirement_list=[], extra_move_changes = [], minimum_move_req_score = None , action_repeat_penalty = -10, metrics_requirements = [], metric_reward = 50, metric_penalty = -50, previous_graph_list = [], metric_retention=0, task_movement_random = False, charname_extra_prob_dict : dict = dict(), metric_leniency = 5, metric_allow_equal = False):

    #make a copy of the graph
    if verbose:
        print("Creating a copy of the Storygraph")
    final_story_graph = deepcopy(init_storygraph)

    dict_of_taken_actions = dict()

    for actor in final_story_graph.character_objects:
        dict_of_taken_actions[actor.get_name()] = list()

    while True:

        if verbose:
            print("===== BEGIN LOOP =====")

        final_story_graph.refresh_longest_path_length()

        #check the shortest story length
        shortest_path_length = final_story_graph.get_shortest_path_length_from_all()
        if verbose:
            print("Shortest Path Length:", shortest_path_length)
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
        if verbose:
            print(shortest_path_character_names_list)
            
        #Randomly pick one name from that list. That will be the character we generate stories for in this step.
        
        current_charname = random.choice(shortest_path_character_names_list)
        if verbose:
            print("Chosen current character:", current_charname)
        latest_state = final_story_graph.make_latest_state()

        current_character = latest_state.node_dict[current_charname]
        # final_story_graph.print_all_nodes_from_characters_storyline(current_character)
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
        # TODO: Is it possible to accumulate task cancels into one big cancel task that cancels all failed tasks?
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
            print("Checking for acceptable rules...")
        for rule in acceptable_rules:
            for rule_insert_index in range(0, final_story_graph.get_longest_path_length_by_character(current_character)+1):
                if verbose:
                    print("Currently evaluating:", rule.rule_name, "at", rule_insert_index)
                rule_score = final_story_graph.calculate_score_from_rule_char_and_cont(actor=current_character, insert_index=rule_insert_index, rule = rule, mode=0)
                
                #We can use the rule score itself to test whether or not a rule is suitable.
                #In the event of a normal rule, if one node is invalid the entire sequence will return -999, which lets us know the rule isn't valid.
                #In the event of a joint rule, -999 will only be returned if all the available slots are -999, which means that this rule cannot be applied to this character and thus is invalid.
                if rule_score != -999:
                
                    if verbose:
                        print("Found Acceptable Rule", rule.rule_name, "at", rule_insert_index)

                    rule_container = StoryGenerationActionContainer(action_name="Apply Rule", action_object=rule, action_descriptor=rule.rule_name, action_score=rule_score, perform_index=rule_insert_index)
                    rule_application_count = dict_of_taken_actions[current_charname].count(rule_container.scoreless_string())
                    
                    if rule_application_count > 0:
                        if verbose:
                            print("The rule",rule.rule_name,"was already repeated",str(rule_application_count),"time(s), so we will deduct some score.")
                        rule_container.action_score += (rule_application_count * action_repeat_penalty)

                    for metric in metrics_requirements:

                        test_splitjoint = False

                        if metric.character_object == current_character:
                            
                            purge_count = 0
                            followup_nodes_list = []
                            if not rule.is_joint_rule:
                                # print("accessed")
                                followup_nodes_list = rule.story_change
                                if rule.remove_before_insert:
                                    purge_count = len(rule.story_change)

                            else:
                                match rule.joint_type:
                                    case JointType.SPLIT:
                                        test_splitjoint = True
                                    case _:
                                        followup_nodes_list = [rule.joint_node]
                            
                            pass_metric_test = False
                            distance_from_new_value_to_goal = 0.0
                            distance_from_worst_case_to_goal = 100.0
                            goal_distance_ratio = 1.0

                            # print(followup_nodes_list)
                            if not test_splitjoint:
                                #The formula for reward multiplier is 1 - (distance_from_new_value_to_goal / distance_from_worst_case_to_goal). For example, reaching 15 when the goal is 20 makes it so that the distance to goal is 5. Therefore, the multiplier would be (1 - (5 / 20)) = 15/20.
                                #The formula for penalty multiplier is 1 + (distance_from_new_value_to_goal / distance_from_worst_case_to_goal). For example, falling down to 15 when the goal is 20 makes it so the distance to goal is 5. Therefore, the multiplier would be 1 + (5/20) = 25/20.
                                test_result = final_story_graph.test_if_given_node_list_will_follow_metric_rule(metric=metric, node_list=followup_nodes_list, step=rule_insert_index, purge_count=purge_count, score_retention=metric_retention, previous_graphs=previous_graph_list, leniency_window=metric_leniency, accept_equal=metric_allow_equal, verbose=verbose)
                                pass_metric_test = test_result[0]
                                distance_from_new_value_to_goal = test_result[1]
                                distance_from_worst_case_to_goal = abs(test_result[2] - metric.value)

                                goal_distance_ratio  = float(distance_from_new_value_to_goal) / float(distance_from_worst_case_to_goal)
                            
                            else:
                                #We consider the splitting joint rule to be following the metric if at least one of the continuations follow the metric.
                                #For the purpose of reward calculation, we take the average of all passing cases.
                                #For the purpose of penalty calculation, we take the average of all cases, whether it passes or fails.
                                follow_metric_exists = False
                                list_of_passing_ratios = []
                                list_of_all_ratios = []

                                for node in rule.split_list:
                                    check_result = final_story_graph.test_if_given_node_list_will_follow_metric_rule(metric=metric, node_list=[node], step=rule_insert_index, purge_count=purge_count, score_retention=metric_retention, previous_graphs=previous_graph_list, leniency_window=metric_leniency, accept_equal=metric_allow_equal, verbose=verbose)                                    
                                    list_of_passing_ratios.append(check_result[1] / abs(check_result[2] - metric.value))

                                    if check_result[0]:
                                        follow_metric_exists = True
                                        list_of_all_ratios.append(check_result[1] / abs(check_result[2] - metric.value))

                                pass_metric_test = follow_metric_exists
                                if pass_metric_test:
                                    goal_distance_ratio = statistics.mean(list_of_passing_ratios)
                                else:
                                    goal_distance_ratio = statistics.mean(list_of_all_ratios)

                            if pass_metric_test:
                                if verbose:
                                    print("The rule",rule.rule_name,"follows the metrics:", str(metric), "(Some score will be awarded.)")

                                rule_container.action_score += (metric_reward * (1.0 - goal_distance_ratio))
                            else:
                                if verbose:
                                    print("The rule",rule.rule_name,"violates the metrics.", str(metric), "(Some score will be deducted.)")
                                rule_container.action_score += (metric_penalty * (1.0 + goal_distance_ratio))


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

        current_character_pathlength = final_story_graph.get_longest_path_length_by_character(current_character)

        if verbose:
            print("Checking for acceptable tasks...")
        for task_name in available_task_name_list:

            
            for attempt_index in range(0, current_character_pathlength+1):
                if verbose:
                    print("Evaluating:", task_name, "at", attempt_index)
                
                #TODO: Hey, since we already have the task_stack_advance_validity test task_completeness, why do we have to test for both again?
                
                # task_completeness = final_story_graph.test_task_completeness(task_stack_name=task_name, actor_name=current_charname, abs_step=attempt_index)
                task_valid, task_completeness = final_story_graph.test_task_stack_advance_validity(task_stack_name=task_name, actor_name=current_charname, abs_step=attempt_index)

# START: Checking to see if doing this task would ruin the story length. Remove if this breaks the code.
# Do I really need Length Verification? I mean, we didn't do length verification for regular rules, and we did say it's the *minimum* story length
                if task_valid and task_completeness == 'task_step_can_advance':

                    current_state = final_story_graph.make_state_at_step(stopping_step=attempt_index)[0]
                    current_task_stack = current_state.node_dict[current_charname].get_task_stack_by_name(task_name)
                    current_task = current_task_stack.get_current_task()

                    number_of_nodes_in_current_task = len(current_task.task_actions)
                    task_valid = task_valid and number_of_nodes_in_current_task + current_character_pathlength <= required_story_length
# END of Length Verification

                # if task_valid:
                default_task_score = 0
                action_chosen = "Do Nothing"
                match task_completeness:
                    case 'task_step_already_completed':
                        action_chosen = "Advance Task"
                    case 'task_step_already_failed':
                        action_chosen = "Cancel Task"
                        default_task_score = 999
                        cancel_count += 1
                    case 'task_step_can_advance':
                        if task_valid:
                            action_chosen = "Perform Task"
                            default_task_score = final_story_graph.calculate_score_from_next_task_in_task_stack(actor_name=current_charname, task_stack_name=task_name, task_perform_index=attempt_index, mode=score_mode)
                    case _:
                        default_task_score = -999
                    
                if action_chosen != "Do Nothing":

                    task_container = StoryGenerationActionContainer(action_name=action_chosen, action_object=task_name, action_descriptor=task_name, action_score=default_task_score, perform_index=attempt_index)
                    list_of_available_tasks.append(task_container)

                    if verbose:
                        print("Found acceptable Task-related action:", task_container.scoreless_string())

        if verbose:
            print("Acceptable task-related actions found:", len(list_of_available_tasks))


        #Fill in this list with valid actions to take, pointing towards either the acceptable rules or the tasks that can be advanced
        list_of_valid_actions = []
        for rule_container in acceptable_rules_with_absolute_step_and_score:
            list_of_valid_actions.append(rule_container)

        force_move_towards_quest_into_top_n = False

        #Checking the number of things that say "Cancel".
        task_count = len(list_of_available_tasks)
        cancel_count = len([x for x in list_of_available_tasks if x.action_name == "Cancel Task"])

        #So if there is not a task or if everything is a cancel, we add a move towards quest action
        if len(list_of_available_tasks) < 0 or task_count == cancel_count:
            if verbose:
                print("No valid tasks found. We will add a move towards task location action to Top N.")
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

        sorted_list_of_valid_actions = scrambled_sort(list_of_valid_actions, key=get_action_score, reverse=True)
        top_pick_count = top_n
        if len(list_of_valid_actions) < top_n:
            if verbose:
                print("Picking Top", top_n, "Actions...")            
            top_pick_count = len(sorted_list_of_valid_actions)

        top_n_valid_actions = sorted_list_of_valid_actions[:top_pick_count]
        extra_actions = sorted_list_of_valid_actions[top_pick_count:]

        if verbose:
            print("---")
            print("Top Actions Chosen:")
            if len(top_n_valid_actions) > 0:
                for thing in top_n_valid_actions:
                    print(thing) 
            else:
                print("(No Valid Actions)")
            print("---")

        #Since we don't want to clog top_n_valid_actions, we're just going to insert this action as-is.
        #We will randomly pick one valid spot to move to that location here, although it will most likely be the last step so might as well as make that the only option?
        
        # TODO (Important): There's a lot of redundant waiting in the testing. How will we be able to eliminate that?
        # The solution might lie in checking the attempt move towards quest
        if force_move_towards_quest_into_top_n:
            final_abs_step = final_story_graph.get_longest_path_length_by_character(character=current_character)

            move_towards_quest_container = StoryGenerationActionContainer(action_name="Move Towards Task Location", action_descriptor="Default", action_object=None, action_score=0, perform_index=final_abs_step)
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
                waiting_step = 0
                if latest_action is not None:
                    waiting_step = latest_action.timestep

                waiting_abs_step = final_story_graph.get_longest_path_length_by_character(character=current_character)
                final_story_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=current_character, absolute_step=waiting_abs_step, timestep=waiting_step)
                chosen_action_container = None
                action_for_character_found = True
            else:
                # #From the valid options, we pick from the rule we will use randomly.
                chosen_action_container = random.choice(top_n_valid_actions)
                top_n_valid_actions.remove(chosen_action_container)

                action_type = chosen_action_container.action_name

                # What is this action? We check the first element to find out.
                #Each action will return a true/false value. If the apply is successful, True is returned. If not, False is returned.
                if verbose:
                    print("Performing Action:", str(chosen_action_container))
                match action_type:
                    case "Apply Rule":
                        action_for_character_found = attempt_apply_rule(rule_object=chosen_action_container.action_object, perform_index=chosen_action_container.perform_index, target_story_graph=final_story_graph, character_object=current_character, shortest_path_charname_list=shortest_path_character_names_list, verbose=verbose)
                    case "Advance Task":
                        action_for_character_found = attempt_apply_task(stack_name=chosen_action_container.action_object, attempt_index=chosen_action_container.perform_index, target_story_graph=final_story_graph, current_character=current_character)
                    case "Perform Task":
                        action_for_character_found = attempt_apply_task(stack_name=chosen_action_container.action_object, attempt_index=chosen_action_container.perform_index, target_story_graph=final_story_graph, current_character=current_character)
                    case "Cancel Task":
                        action_for_character_found = attempt_apply_task(stack_name=chosen_action_container.action_object, attempt_index=chosen_action_container.perform_index, target_story_graph=final_story_graph, current_character=current_character)
                    case "Move Towards Task Location":

                        #We can make a list of index and randomly pick from it until it gives us a positive result
                        #Let's do it in the function
                        #Actually, I think it would be better to always call this function from the latest step.
                        wait_probability = charname_extra_prob_dict.get(current_charname, 0)
                        action_for_character_found = attempt_move_towards_task_loc(target_story_graph=final_story_graph, current_character=current_character, movement_index=final_abs_step, extra_movement_requirements=extra_movement_requirement_list, suggested_movement_requirements=suggested_movement_requirement_list, score_calc_mode=score_mode, minimum_action_score_for_valid_movement=minimum_move_req_score, random_optimal_pick=task_movement_random, extra_changes=extra_move_changes, extra_wait_prob=wait_probability)
                    case "Wait":
                        pass
                    case _:
                        pass

            if verbose:
                print("Chosen action validity:", action_for_character_found)
                if action_for_character_found:
                    print("The action is valid, so the action was performed.")
                else:
                    print("This action is not valid, so nothing was performed.")

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
                if chosen_action_container is not None:
                    dict_of_taken_actions[current_charname].append(chosen_action_container.scoreless_string())
                #If we did find the rule to apply we should update the story graph so that the locations show up in the story.

                #Temporary Print
                # for part in final_story_graph.story_parts.values():
                #     print(part.name)
                #     print("prev",part.previous_nodes)
                #     print("next",part.next_nodes)
                #     print("-----")

                # final_story_graph.fill_in_locations_on_self()

        #Finally, we fill in the locations on self and update the list of changes.
        final_story_graph.update_list_of_changes()
        final_story_graph.fill_in_locations_on_self()

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

        # current_purge_count = 0

        # if current_rule.remove_before_insert:
        #     current_purge_count = len(current_rule.story_condition)

        #TODO (Extra Features): apply_rewrite_rule already has continuation validity thing going on, so why are we checking it twice here? Read into this.
        # nonjoint_cont_valid = target_story_graph.check_continuation_validity(actor=character_object, abs_step_to_cont_from=current_index, cont_list=current_rule.story_change, target_list=current_rule.target_list, purge_count=current_purge_count)

        # if nonjoint_cont_valid:
            #Get the locations where this pattern can be applied, set everything as banned except the location that we want.
            #At no point in apply rewrite rule or check for pattern in storyline does the continuation validity get checked so we need to check for continuation validity.
            #If the application of the rule is successful, then this should return true.
            #Checking for continuation validity already exists within Apply Rewrite Rule, so we don't have to do anything extra here.
        apply_rule_success = target_story_graph.apply_rewrite_rule(rule=current_rule, character=character_object, abs_step=current_index, verbose=verbose)

    else:
        applicable_character_names = []
        all_possible_character_list = []
        character_count = current_rule.get_character_count()

        if current_rule.joint_type == JointType.JOIN:
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
            if len(all_possible_character_list) > 0:
                
                chosen_grouping = random.choice(all_possible_character_list)
                all_possible_character_list.remove(chosen_grouping)

                if current_rule.joint_type == JointType.SPLIT:
                    nodesplit = current_rule.split_list
                else:
                    nodesplit = [current_rule.joint_node]

                current_state = target_story_graph.make_state_at_step(current_index)[0]

                chosen_grouping_with_character_objects = []

                for actor_name in chosen_grouping:
                    chosen_grouping_with_character_objects.append(current_state.node_dict[actor_name])

                chosen_grouping_split = target_story_graph.pick_one_random_valid_character_grouping_from_all_valid_groupings(continuations=nodesplit, abs_step=current_index, character_list=chosen_grouping_with_character_objects)

                #If there are no valid splits here at all, it's skipped.
                if chosen_grouping_split is None:
                    continue
                
                split_copy = deepcopy(chosen_grouping_split)
                rule_validity = target_story_graph.check_joint_continuity_validity(joint_rule=current_rule, main_character=character_object, grouping_split=split_copy, insert_index=current_index)
                del(split_copy)

                if rule_validity:
                    valid_character_grouping = chosen_grouping_split
                    grouping_choose_complete = True
            else:
                valid_character_grouping = None
                grouping_choose_complete = True

        #If the combination is valid, then we need to apply the specified node/continuations and then mark that we have found a proper continuation.
        if valid_character_grouping is not None:
            
            #Apply the continuation based on whether the rule was a split rule.
            if current_rule.joint_type == JointType.SPLIT:
                target_story_graph.split_continuation(split_list=current_rule.split_list, chargroup_list=valid_character_grouping, abs_step=current_index)
            else:
                target_story_graph.joint_continuation(abs_step=current_index, joint_node=current_rule.joint_node, actors=valid_character_grouping[0]["actor_group"], target_list=valid_character_grouping[0]["target_group"])

            apply_rule_success = True

    return apply_rule_success

#TODO (Testing): Test this function
def attempt_apply_task(stack_name, attempt_index, target_story_graph, current_character):

    #Since the action is already determined by the function within SG2WS, theres no need to split this into three like I thought I had to.
    # TODO (Testing): HOWEVER we need to ensure that this function works as intended. Test this.
    # TODO: haha guess what happens when we try to advance a task that's doomed to be cancelled
    advance_success = target_story_graph.attempt_advance_task_stack(task_stack_name=stack_name, actor_name=current_character.get_name(), abs_step=attempt_index)
    return advance_success

# TODO (Testing): Test this function
# TODO (Optimization): This function takes quite a while to run, we need to figure out why.
# Will return True if changes are made to the story graph and False if not.
def attempt_move_towards_task_loc(target_story_graph:StoryGraph, current_character, movement_index, extra_movement_requirements = [], suggested_movement_requirements=[], extra_changes = [], minimum_action_score_for_valid_movement = None, score_calc_mode=0, random_optimal_pick = False, extra_wait_prob = 0):

    current_ws = target_story_graph.make_state_at_step(movement_index)[0]
    char_from_ws = current_ws.node_dict.get(current_character.get_name())
    optimal_location_object_list = []
    best_score_so_far = -999
    optimal_move_actions_with_best_score = []
    optimal_location_object_list.extend(current_ws.get_optimal_location_towards_task(actor=current_character, return_all_possibilities=True, extra_probability_to_wait_if_no_valid=extra_wait_prob))
    # current_location_of_character = current_ws.get_actor_current_location(current_character)

    #If we're in the same location then we don't need to do the things below. Since we don't want to move locations this should return False.
    
    # print(optimal_location_object_list)
    # if current_location_of_character in optimal_location_object_list:
    #     # print("Already In Current Place:", current_location_of_character.get_name())
    #     return False

    #Repeat until we find valid location or if we run out of locations
    while len(optimal_location_object_list) > 0:
        
        choice_no = 0
        if random_optimal_pick and len(optimal_location_object_list) > 1:
            choice_no = random.randint(0, len(optimal_location_object_list)-1)

        optimal_location_object = optimal_location_object_list[choice_no]
        optimal_location_name = optimal_location_object.get_name()

        go_to_new_location_change = RelChange(name="Go To Task Loc", node_a=GenericObjectNode.GENERIC_TARGET, edge_name=current_ws.DEFAULT_HOLD_EDGE_NAME, node_b=GenericObjectNode.GENERIC_ACTOR, value=None, add_or_remove=ChangeAction.ADD)
        not_be_in_current_location_change = RelChange(name="Leave Current Loc", node_a=GenericObjectNode.GENERIC_LOCATION, edge_name=current_ws.DEFAULT_HOLD_EDGE_NAME, node_b=GenericObjectNode.GENERIC_ACTOR, add_or_remove=ChangeAction.REMOVE, soft_equal=True, value=None)

        all_changes = deepcopy(extra_changes)
        all_changes.append(go_to_new_location_change)
        all_changes.append(not_be_in_current_location_change)

        target_location_adjacent_to_current_location = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_LOCATION, edge_name_test=current_ws.DEFAULT_ADJACENCY_EDGE_NAME, object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True)
        
        all_requirements = deepcopy(extra_movement_requirements)
        all_requirements.append(target_location_adjacent_to_current_location)
        
        # move_towards_task_location_node = StoryNode("Move Towards Task Location", biasweight=0, tags={"Type":"Movement"}, charcount=1, effects_on_next_ws=[go_to_new_location_change, not_be_in_current_location_change], required_test_list=[target_location_adjacent_to_current_location])
        
        # TODO: Since we want to make the scores matter here... What are some things we are able to do to make the scores matter? As of now, scores don't seem to matter much.
        # 1. Add a score requirement + a chance to fail if the score doesn't meet requirement? (Harder to test)
        # 2. Score Negative = Fail, thats it (Not very customizable)
        # 3. Score under given threshold (Requires an extra parameter)

        # Will make it 3 for now but will discuss with Professor later

        move_towards_task_location_node = StoryNode(name="Move Towards " + optimal_location_name, biasweight=0, tags={"Type":"Movement"}, target=[optimal_location_object], charcount=1, effects_on_next_ws=all_changes, required_test_list=all_requirements, suggested_test_list=suggested_movement_requirements)

        # TODO: why not translate the stuff here to something valid

        #We have made our custom move towards task location node. We will check to see if it's a valid move to move to that location.
        movement_validity = target_story_graph.check_continuation_validity(actor=char_from_ws, abs_step_to_cont_from=movement_index, cont_list=[move_towards_task_location_node])    
        # print("Movement Success:", movement_validity, current_location_of_character.get_name(), optimal_location_name)
        # print(movement_validity)
        # if char_from_ws.get_name() == "Alien God":
        #     for item in all_requirements:
        #         print(item)
        #     print("Alien God Movement Valid (Should be False):", movement_validity)

        calc_score = -999

        if len(suggested_movement_requirements) > 0:
            calc_score = target_story_graph.calculate_score_from_char_and_cont(actor=char_from_ws, insert_index=movement_index, contlist=[move_towards_task_location_node], purge_count=0, mode=score_calc_mode, target_list=[[optimal_location_object]])
            if minimum_action_score_for_valid_movement is not None:
                movement_validity = movement_validity and calc_score >= minimum_action_score_for_valid_movement

        if movement_validity:
            if len(suggested_movement_requirements) <= 0:
                target_story_graph.insert_story_part(part=move_towards_task_location_node, character=char_from_ws, absolute_step=movement_index, targets=[optimal_location_object])
                target_story_graph.fill_in_locations_on_self()
                return True
            else:
                if calc_score > best_score_so_far:
                    best_score_so_far = calc_score
                    optimal_move_actions_with_best_score.clear()

                if calc_score >= best_score_so_far:
                    optimal_move_actions_with_best_score.append(move_towards_task_location_node)

        optimal_location_object_list.pop(0)
    
    if len(suggested_movement_requirements) > 0 and len(optimal_move_actions_with_best_score) > 0:
        
        final_chosen_action_node = random.choice(optimal_move_actions_with_best_score)
        target_story_graph.insert_story_part(part=final_chosen_action_node, character=char_from_ws, absolute_step=movement_index)
        target_story_graph.fill_in_locations_on_self()
        return True

    return False
    
# def cycle_attempt_move_towards_task_loc(target_story_graph:StoryGraph, current_character):
    
#     #The path length of the character is the range.

#     path_length_list = target_story_graph.get_all_path_length_with_charname()
#     current_char_path_length = [x[1] for x in path_length_list if x[0] == current_character.get_name()]
#     possible_insert_locs = list(range(0, current_char_path_length))

#     good_insert_loc_found = False

#     while not good_insert_loc_found:
        
#         if len(possible_insert_locs) == 0:
#             return False
        
#         chosen_loc = random.choice(possible_insert_locs)
#         possible_insert_locs.remove(chosen_loc)

#         if attempt_move_towards_task_loc(target_story_graph=target_story_graph, current_character=current_character, movement_index=chosen_loc):
#             return True
#         #Pick a random thing from the possible insert locs, remove it

def perform_wait_action(target_story_graph:StoryGraph, current_character):
    latest_action = target_story_graph.get_latest_story_node_from_character(current_character)

    wait_timestep = 0
    if latest_action is not None:
        wait_timestep = latest_action.timestep

    target_story_graph.add_story_part(part=DEFAULT_WAIT_NODE, character=current_character, timestep=wait_timestep)
    
    return True

def generate_multiple_graphs(initial_graph : StoryGraph, list_of_rules, required_story_length=20, max_storynodes_per_graph=5, top_n = 5, extra_attempts=5, score_mode=0, verbose=False, extra_movement_requirement_list = [], suggested_movement_requirement_list=[], extra_move_changes = [], minimum_move_req_score = 0, action_repeat_penalty = -10, metric_requirements = [], metric_reward=50, metric_penalty=-50, metric_retention=0, task_movement_random=False, charname_extra_prob_dict : dict = dict(), metric_leniency = 5, metric_allow_equal = False):
    
    #NOTE: Max Storynodes per Graph includes the "Recall Tasks" node.

    list_of_completed_story_graphs = []
    
    number_of_graphs_needed = required_story_length // max_storynodes_per_graph
    length_of_last_graph = required_story_length % max_storynodes_per_graph

    if length_of_last_graph > 0:
        number_of_graphs_needed+1

    while len(list_of_completed_story_graphs) < number_of_graphs_needed:
        if verbose:
            print("Graph Generated So Far:", str(len(list_of_completed_story_graphs)))

        if len(list_of_completed_story_graphs) == 0:
            loop_init_graph = initial_graph
        else:
            graph_name = initial_graph.name + " Continuation # " + str(len(list_of_completed_story_graphs))
            loop_init_graph = make_base_graph_from_previous_graph(previous_graph=list_of_completed_story_graphs[-1], graph_name=graph_name)

        loop_graph_length = max_storynodes_per_graph

        if len(list_of_completed_story_graphs) == number_of_graphs_needed-1 and length_of_last_graph != 0:
            loop_graph_length = length_of_last_graph

        new_graph = generate_story_from_starter_graph(init_storygraph=loop_init_graph, list_of_rules=list_of_rules, required_story_length=loop_graph_length, top_n=top_n, extra_attempts=extra_attempts, score_mode=score_mode, verbose=verbose, extra_movement_requirement_list=extra_movement_requirement_list, suggested_movement_requirement_list=suggested_movement_requirement_list, minimum_move_req_score=minimum_move_req_score, action_repeat_penalty=action_repeat_penalty, metrics_requirements=metric_requirements, metric_reward=metric_reward, metric_penalty=metric_penalty, previous_graph_list=list_of_completed_story_graphs, metric_retention=metric_retention, task_movement_random=task_movement_random, extra_move_changes=extra_move_changes, charname_extra_prob_dict = charname_extra_prob_dict, metric_leniency=metric_leniency, metric_allow_equal=metric_allow_equal)

        if verbose:
            print("Current Graph,", str(len(list_of_completed_story_graphs)), "Finished. These are the edges in the latest state of that graph:")
            new_graph.make_latest_state().print_all_edges()

        list_of_completed_story_graphs.append(new_graph)
    return list_of_completed_story_graphs

#TODO: Maybe there's really a problem with memory allocation... There's a reason why it takes so long to generate everything in one go, there has to be
# Either that or this base graph function is flawed, in which case we should abandon it and do things the hard way (again :skull_emoji:)
def make_base_graph_from_previous_graph(previous_graph: StoryGraph, graph_name):

    init_ws = previous_graph.make_latest_state()
    char_list = init_ws.get_all_actors()
    init_ws.make_all_actors_forget_tasks()

    return_graph = StoryGraph(name=graph_name, character_objects=char_list, starting_ws=init_ws, always_true_tests=previous_graph.always_true_tests)

    for character in char_list:
        new_node = make_recall_task_node_based_on_final_graph_step(story_graph=previous_graph, character_name=character.get_name())

        last_location = init_ws.get_actor_current_location(actor=character)
        return_graph.insert_story_part(part=new_node, character=character, location=last_location, absolute_step=0)
        return_graph.placeholder_dicts_of_tasks = previous_graph.placeholder_dicts_of_tasks
        
        
        #TODO (Important): If the character had a task in the last Timestep, remove it, and modify the task so that only the uncompleted items are added in their initial step of the new graph.
        #Otherwise, have them do a normal wait action.

        #We'll need to write the following functions:

        #Function to translate partially completed tasks into new tasks (Make sure to retain placeholder information)
        # 1. Get the current state of the task
        # 2. Get the steps of the task from the current step to the final step, ignoring already completed steps (These are the new steps)
        # 3. Create a new TaskObject based on the steps we got from 2, 
        # 4. Create a StoryNode called RecallTasks 

        #Creating a new "Recall Tasks" node with no targets. The character just assigns the tasks to themselves but remember where they got the tasks from.

        #TODO: Unfortunately(?) this function has just been moved up to (Very Important) priority. We will also need a way to store previous graph's information (including length and metrics value)

        # Wait let's try another example. Graph A has a length of 5 and a uniqueness score of 20. Graph B has a length of 3 and a uniqueness score of 33.33... Together, the storyline will be 8 long and have a uniqueness score of 25.
        # Okay so it's a *weighted* average. We calculate 25 by doing ((5*20) + (3*33.33...))/(5+3) = 25. So we need to weigh it by the length in case of incomplete graphs.

    return return_graph

def make_recall_task_node_based_on_final_graph_step(story_graph : StoryGraph, character_name : str):

    final_ws = story_graph.make_latest_state()
    character_at_final_ws = final_ws.node_dict[character_name]
    equivalent_taskchanges = []

    for stack_found in character_at_final_ws.list_of_task_stacks:
        if not stack_found.stack_is_complete() and not stack_found.remove_from_pool:
            
            new_stack_name = stack_found.stack_name

            # Since we already handled the main generator in such a way that there shouldnt be partial tasks, we can assume that
            # There will be no tasks completed halfway in a way that only some nodes are complete

            # Either all the nodes are done, or no nodes are done at all

            incomplete_task_list = []
            for task in stack_found.task_stack:
                if not task.task_complete_status:
                    incomplete_task_list.append(task)
            new_task_stack = TaskStack(stack_name=new_stack_name, task_stack=incomplete_task_list, task_stack_requirement=stack_found.task_stack_requirement, stack_giver_name=stack_found.stack_giver_name, stack_owner_name=stack_found.stack_owner_name)

            taskchange_with_new_task = TaskChange(name="Recall Stack: "+new_task_stack.stack_name, task_giver_name=new_task_stack.stack_giver_name, task_owner_name=new_task_stack.stack_owner_name, task_stack=new_task_stack)
            equivalent_taskchanges.append(taskchange_with_new_task)


    node_name = "Wait"
    if len(equivalent_taskchanges) > 0:
        node_name = "Recall Tasks"

    new_node = StoryNode(name=node_name, biasweight=0, tags={"Type":"Initialize"}, effects_on_next_ws=equivalent_taskchanges)

    return new_node

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
    def __init__(self, action_name, action_descriptor, action_object, action_score, perform_index) -> None:

        self.action_name = action_name
        self.action_descriptor = action_descriptor
        self.action_object = action_object
        self.action_score = action_score
        self.perform_index = perform_index

    def __str__(self):
        return self.action_name + " (" + self.action_descriptor + ") for " + str(self.action_score) + " Points at Index " + str(self.perform_index)
    
    def scoreless_string(self):
        return self.action_name + " (" + self.action_descriptor + ") at Index " + str(self.perform_index)
    
def get_action_score(e: StoryGenerationActionContainer):
    return e.action_score