from components.StoryGraph import StoryGraph
from components.WorldState import WorldState


class RewriteRule:
    
    '''
    Based on ReGEN
    There should be four parts
    
    Story Precondition: Part of the graph.
    Relationship Precondition: Part of the graph.

    These story graphs will only contain one storyline with no character assigned to them

    TODO: Add a function in StoryGraph and WorldState that checks for subgraph in terms of story condition and relationship condition respectively
    
    Story Change
    Relationship Change (already included in story_changes and story_condition thanks to timesteps coming pre-included with world states)
    '''
    
    def __init__(self, story_condition: StoryGraph, story_change: StoryGraph, dummychar, name="", required_tags=[], unwanted_tags=[], bias=None):
        self.rule_name = name
        self.story_condition = story_condition
        self.story_change = story_change
        self.dummychar = dummychar

    def check_character_compatibility(self, character_node):
        #TODO: Check if the character contains tags in Required Tags (not compatible if false)

        #TODO: Check if character contains tags in Unwanted Tags (not compatible if true)
        
        #TODO: Check if character's bias is within the acceptable range (not compatible if false)

        #If the character passes all three tests, then return true. Otherwise, return false
        return True
'''        
Hey wait a second Ram, this method of rewriting rules might not work for our purpose
Consider: This method will not preserve the previous state of the story map
Nor will it work well with the timestep method, as replacing things pushes it further in the timestep

This is how it will go, if we try to make it work

1. Base story
A-B-C
1-2-3

2. Replacement Rules
B-C can be replaced with B-D-C
B-D can be replaced with B-E-F

3. Start replacing, while pushing timesteps up
A-B-E-F-C
1-2-3-4-5

We'll also need to handle stuff like the location where the story should be replaced, as the same thing coudl happen more than once in the storyline.

Some options:
- It should replace the first occurance it finds
- It should replace a random occurance
- It should replace all occurances (which is what I assume what happens if applyonce is false)

Chosen Options:

depending on if applyonce is true or false, it does different things

applyonce True: it replaces a random occurance.
applyonce False: it replaces every occurance.
'''