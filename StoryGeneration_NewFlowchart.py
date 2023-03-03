#We will write this story generation function based on the new flowchart.

import copy
import random
from components.RewriteRuleWithWorldState import JoiningJointRule, JointType

from components.StoryGraphTwoWS import StoryGraph
from components.StoryNode import StoryNode
from components.UtilFunctions import permute_actor_list_for_joint, permute_actor_list_for_joint_with_variable_length

DEFAULT_HOLD_EDGE_NAME = "holds"
DEFAULT_ADJACENCY_EDGE_NAME = "connect"
DEFAULT_WAIT_NODE = StoryNode(name="Wait", biasweight=0, tags= {"Type":"Placeholder"}, charcount=1)

#TODO: In order to make life easier for myself during testing, I should convert this into multiple functions.
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

        rule_for_this_character_found = False

        #acceptable_rules = [rule for rule in list_of_rules if final_story_graph.check_rule_validity(current_character, rule)]
        acceptable_rules = [rule for rule in list_of_rules]

        #Give each rule a score according to current graph state and the chosen character.
        acceptable_rules_with_absolute_step_and_score = []

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

        #Here, we will choose from top n rules.
        top_pick_count = top_n
        if len(acceptable_rules_with_absolute_step_and_score) < top_n:
            top_pick_count = len(acceptable_rules_with_absolute_step_and_score)

        top_n_acceptable_rules = acceptable_rules_with_absolute_step_and_score[:top_pick_count]
        extra_rules = acceptable_rules_with_absolute_step_and_score[top_pick_count:]
        extra_attempts_left = extra_attempts

        while not rule_for_this_character_found:

            #Check the length of the list now. Do we have enough? If this is blank, we must make our character wait.
            if len(top_n_acceptable_rules) == 0 or extra_attempts_left == 0:
                latest_action = final_story_graph.get_latest_story_node_from_character()
                final_story_graph.add_story_part(part=DEFAULT_WAIT_NODE, character=current_character, timestep=latest_action.timestep)
                rule_for_this_character_found = True

            #From the valid options, we pick from the rule we will use randomly.
            chosen_rule = random.choice(top_n_acceptable_rules)
            top_n_acceptable_rules.remove(chosen_rule)
            #Keep in mind that the the chosen rule is a tuple. Index 0 is the node itself, Index 1 is the location to apply to, Index 2 is the score (which we won't use here.)

            #If it's just a normal rewrite rule, we can instantly apply it because we don't need to check its validity with other nodes. We'll apply it to one random good spot.

            #TODO: Apply rewrite rule, but we can choose the specific spot? Or maybe just use insert function here because we already did the checks above and we know the rule can be applied because it passes the tests.
            # Maybe use the banned subgraph locs to ban everything that's not the chosen index?
            if not chosen_rule[0].is_joint_rule:

                pattern_check_result = final_story_graph.check_for_pattern_in_storyline(chosen_rule[0].story_condition, current_character)
                banned_locs = pattern_check_result[1]
                banned_locs.remove(chosen_rule[1])

                final_story_graph.apply_rewrite_rule(chosen_rule, current_character, applyonce=True, banned_subgraph_locs=banned_locs)
                rule_for_this_character_found = True
            else:

                applicable_character_names = []
                applicable_character_names += shortest_path_character_names_list
                applicable_character_names.remove(current_charname)

                # TODO: Most of the functions we have to write here are already taken care of in SG2WS.

                # TODO: Need to work the applicable character names further.
                # Joining Joint: Don't modify this, it's perfect.
                # Continuous Joint and Splitting Joint: Instead of doing this, use the names of the characters currently sharing the node with the current character at the current absolute step, ignoring their length.

                # TODO: Once we have the list of characters, we test the validity here. If it's not valid we don't add anything and make this part loop again.
                # If it's valid then it can be applied, so we should attempt to apply it.
                # For Joining Joint: We will test validity by first creating a list of all possible character combinations. Then, we'll remove any bad character combination from this list.
                # For Continuous Joint and Splitting Joint: There is no need to test validity because the only combination we know of is valid.

                # TODO: To apply the rules, we would do the following:
                # We can use generate_valid_actor_and_target_split for Joining Joint and Continuous Joint.
                # We can use generate_valid_character_grouping for Splitting Joint.
                # We will loop this until we find a valid character combination or there's no more character combinations to choose from.
                # Both of theese functions will return None if there are not enough valid characters, so we know to not set rule_for_this_character_found to True yet and make the program look for a new rule.

                # TODO: If we have found a good character combination, we'll apply it here.
            
            #If we don't find the rule to apply yet, we might need to add new rules to top_n. Suitable rules might be clogged behind invalid joint rules.
            if not rule_for_this_character_found:
                if extra_attempts_left == -1 or extra_attempts > 0:
                    #Check if we have any attempts left, if we do, then add the first thing from the extra rules if there are still more extra rules
                    if len(extra_rules) > 0:
                        top_n_acceptable_rules.append(extra_rules.pop(0))
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
