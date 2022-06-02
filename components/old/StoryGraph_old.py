import random
from numpy import empty
from components.StoryNode import *
from components.StoryObjects import *

'''
Storygraph!

The story graph contains the following things:

List of Timesteps:
Each timestep will contain a group of story nodes,
each one with its own character(s) and 
'''
class StoryGraph:
    def __init__(self, name, character_objects, location_objects):
        self.name = name
        self.timesteps = []
        self.character_objects = character_objects
        self.location_objects = location_objects

    def apply_rewrite_rule(self, rule, character, applyonce=False):
        #Check for that specific character's storyline
        #Check if Rule applies (by checking if the rule is a subgraph of this graph)
        is_subgraph, subgraph_locs = rule.story_condition.is_subgraph(self)
        if is_subgraph:
            #If yes to both, do a replacement
            #Get all instances and replace all of them if ApplyOnce is false
            #If ApplyOnce is true, then replace only one random instance
            print("Rule is subgraph of Self, replacing storyline")

            if not applyonce:
                print("applyonce is false, replacing all instances of this rule")
            else:
                print("applyonce is true, one random instance will be replaced")
                subgraph_locs = [random.choice(subgraph_locs)]
                
            for step in range(0, len(self.timesteps)):
                    if step in subgraph_locs:
                        for substep in range(0, len(rule.story_condition.timesteps)):
                            self.timesteps[step]
                

                

        else:
            print("Nothing is replaced: Rule is not subgraph of Self")
        


    '''
    A story graph is considered to be a subgraph of another storygraph when:
    1) There exists a sequence of timesteps that contains similar nodes
    2) Each of the node mentioned must be performed by the same character

    Oh also. I want this function to return the starting points of each subgraph
    '''
    def is_subgraph(self, other_graph):

        list_of_subgraph_locs = []

        #First of all, this graph can't be the other graph's subgraph if it has more timesteps than the other graph
        if len(self.timesteps) > len(other_graph.timesteps):
            return False, list_of_subgraph_locs

        #Second of all, check each timestep to see if the timestep is in fact a sub timestep of the othergraph's timestep
        #If there are less timesteps remaining in the other graph than there are timesteps in this graph then it can't be subset 
        for x in range(0, len(other_graph.timesteps) - len(self.timesteps) + 1):

            result = True

            #Check all the timesteps of this graph to see if it's contained within the other timestep
            for y in range(0, len(self.timesteps)):

                #For each of the timestep in this graph, we check if it's a subtimestep. If it is, add the coord to the list.
                result = result and self.timesteps[y].is_subgraph(other_graph.timesteps[x+y])
                if result:
                    list_of_subgraph_locs.append(y)

        #If list is empty then it's false. If list is not empty then it's true. Then also return that list.
        return len(list_of_subgraph_locs) > 0, list_of_subgraph_locs
