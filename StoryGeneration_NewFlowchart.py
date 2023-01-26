#We will write this story generation function based on the new flowchart.

import copy
import random

from components.StoryGraphTwoWS import StoryGraph


DEFAULT_HOLD_EDGE_NAME = "holds"
DEFAULT_ADJACENCY_EDGE_NAME = "connect"

def generate_story_from_starter_graph(actor_list, location_list, object_list, init_storygraph: StoryGraph, list_of_storynodes, list_of_rules, required_story_length):

    while True:

        #make a copy of the graph
        final_story_graph = copy(init_storygraph)

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
        character_to_cont = random.choice(shortest_path_length)

        #TODO: Function that ranks all our rules? I have no idea how to do this yet. We'll look into it when I'm more awake and conscious.