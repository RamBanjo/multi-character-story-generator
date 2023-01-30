#We will write this story generation function based on the new flowchart.

import copy
import random

from components.StoryGraphTwoWS import StoryGraph
from components.StoryNode import StoryNode

DEFAULT_HOLD_EDGE_NAME = "holds"
DEFAULT_ADJACENCY_EDGE_NAME = "connect"
DEFAULT_WAIT_NODE = StoryNode("Wait", 0, {"Type":"Placeholder"}, 1)

def generate_story_from_starter_graph(actor_list, location_list, object_list, init_storygraph: StoryGraph, list_of_storynodes, list_of_rules, required_story_length, top_n = 5):

    #make a copy of the graph
    final_story_graph = copy(init_storygraph)

    while True:

        #check the shortest story length
        shortest_path_length = final_story_graph.get_shortest_path_length_from_all()

        #If the path length is equal to or greater than the required length, we're done
        if shortest_path_length >= required_story_length:
            #return result
            return final_story_graph

        #Make a list of all characters' path lengths.
        path_length_list = final_story_graph.get_all_path_length_with_charname()

        #Reduce this list to only the ones with the shortest path length.
        shortest_path_character_names_list = [x[1] for x in path_length_list if x[0] == shortest_path_length]

        #Randomly pick one name from that list. That will be the character we generate stories for in this step. 
        current_charname = random.choice(shortest_path_character_names_list)

        latest_state = final_story_graph.make_latest_state()

        current_character = latest_state.node_dict[current_charname]

        node_for_this_character_found = False

        #Only pick the acceptable rules
        acceptable_rules = [rule for rule in list_of_rules if final_story_graph.check_rule_validity(current_character, rule)]

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
                pass
                #TODO: This is the part where we check if we have enough valid characters to apply the joint rule.
                #TODO: If we do, then apply it.
                #TODO: If we don't, then, remove this rule from the top n acceptable rules. We'd have to choose again from the top n list.

        #Finally, we fill in the locations on self and update the list of changes.
        final_story_graph.update_list_of_changes()
        final_story_graph.fill_in_locations_on_self()

def get_biasweight(e):
    return e.biasweight