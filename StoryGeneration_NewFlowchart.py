#We will write this story generation function based on the new flowchart.

import copy
import random
from components.RewriteRuleWithWorldState import JointType

from components.StoryGraphTwoWS import StoryGraph
from components.StoryNode import StoryNode
from components.UtilFunctions import permute_actor_list_for_joint, permute_actor_list_for_joint_with_variable_length

DEFAULT_HOLD_EDGE_NAME = "holds"
DEFAULT_ADJACENCY_EDGE_NAME = "connect"
DEFAULT_WAIT_NODE = StoryNode(name="Wait", biasweight=0, tags= {"Type":"Placeholder"}, charcount=1)

#TODO: In order to make life easier for myself during testing, I should convert this into multiple functions.
def generate_story_from_starter_graph(init_storygraph: StoryGraph, list_of_rules, required_story_length, top_n = 5):

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

        node_for_this_character_found = False

        #Only pick the acceptable rules
        acceptable_rules = [rule for rule in list_of_rules if final_story_graph.check_rule_validity(current_character, rule)]

        #Give each rule a score according to current graph state and the chosen character.
        acceptable_rules_with_score = []

        #TODO: Append score next to rule into the list acceptable rules with score. Watch out for special cases in joint rules:
        # Join Joint and Cont Joint: The score is the max between the actor slot and the target slot.
        # Split Joint: The score is the max among all the given splits.
        for rule in acceptable_rules:
            pass

        #Sort it by biasweight. Python sorts ascending by default, so we must reverse it.
        acceptable_rules.sort(key=get_biasweight, reverse=True)

        #Here, we will choose from top n rules.
        top_pick_count = top_n
        if len(acceptable_rules) < top_n:
            top_pick_count = len(acceptable_rules)

        top_n_acceptable_rules = acceptable_rules[:top_pick_count]

        while not node_for_this_character_found:

            #Check the length of the list now. Do we have enough? If this is blank, we must make our character wait.
            if len(top_n_acceptable_rules) == 0:
                latest_action = final_story_graph.get_latest_story_node_from_character()
                final_story_graph.add_story_part(part=DEFAULT_WAIT_NODE, character=current_character, timestep=latest_action.timestep)
                node_for_this_character_found = True
                final_story_graph.fill_in_locations_on_self()

            #From the valid options, we pick from the rule we will use randomly.
            chosen_rule = random.choice(top_n_acceptable_rules)
            top_n_acceptable_rules.remove(chosen_rule)

            #If it's just a normal rewrite rule, we can instantly apply it because we don't need to check its validity with other nodes. We'll apply it to one random good spot.
            if not chosen_rule.is_joint_rule:
                final_story_graph.apply_rewrite_rule(chosen_rule, current_character, applyonce=True)
            else:

                #Here, we are going to make all the possible character groups. First, we get all the characters who can be added to the joint node.

                #TODO: WAIT WAIT WAIT WE NEED TO CLARIFY FURTHER
                #Applicable character names should be taken from shortest path character names list, correct
                #HOWEVER, if this is a cont rule or a split rule, then we can just simply use the characters currently sharing a node with that character.
                #In addition to that, if this is a join rule, we should look for characters who are indeed doing the nodes specified in the join pattern and are within the shortest path.
                #Now that I'm a bit more awake, we don't know yet where the nodes will be applied. At least, we already have the functions of the cont rule and the split rule to be only valid if the given characters are in the previous node together.

                #Before we can do this, we should clarify whether we would be doing 
                applicable_character_names = []
                applicable_character_names += shortest_path_character_names_list
                applicable_character_names.remove(current_charname)

                # Once we have decided which characters are applicable, we need to look for spots that this rule can fit, and the list of characters whose story will be extended if we use that absolute step.
                # For example, if we're doing a continuing joint, we must find the places where the "main character" performs the continuing joint. Then, return each absolute step with the list of characters in that joint.
                # Like this:
                # 
                # [(2, ["Alice, Bob, Charlie, David"]),
                # (6, ["Alice, Bob, Harry, Irina"])]
                # 
                # This allows us to instantly have a list of characters to use. We limit the possibilities 
                #
                # This same method can be done to determine the suitable characters and spots that the joint rule can take. However, before we can do that, we would need to determine the method that we will use for our Joining Joint.
                # Write the function in the StoryGraph that does exactly this. We can handle the single joint node case, but for the other case we need to decide joining joint style first
                #
                # Update: We have completed this function in SG2WS. We just need to run SG2WS.check_if_abs_step_has_joint_pattern for all the steps in our current character's line.
                #
                # TODO: Additionally from that, we can use the available character information along with the required character information (actor/target) in the consecutive joint node and/or splits to determine how many actors can be applied, and prune the list of acceptable actors groups down to that.

                list_of_possible_char_groups = []

                characters_wanted_count = chosen_rule.get_character_count()
                minimum_actor_count = 2

                if chosen_rule.joint_type == JointType.SPLIT:
                    minimum_actor_count = len(chosen_rule.split_list)

                if type(characters_wanted_count) == tuple:
                    list_of_possible_char_groups += permute_actor_list_for_joint_with_variable_length(current_charname, applicable_character_names, characters_wanted_count[0], characters_wanted_count[1])
                elif characters_wanted_count == -1:
                    list_of_possible_char_groups += permute_actor_list_for_joint_with_variable_length(current_charname, applicable_character_names, minimum_actor_count, characters_wanted_count[1])
                else:
                    list_of_possible_char_groups += permute_actor_list_for_joint(current_charname, applicable_character_names, characters_wanted_count)

                #Find all locations where this rule can be applied.



                pass
                #TODO: This is the part where we check if we have enough valid characters to apply the joint rule.
                #If we do, then apply it.
                #If we don't, then, remove this rule from the top n acceptable rules. We'd have to choose again from the top n list.

        #Finally, we fill in the locations on self and update the list of changes.
        final_story_graph.update_list_of_changes()
        final_story_graph.fill_in_locations_on_self()

def get_biasweight(e):
    return e.biasweight