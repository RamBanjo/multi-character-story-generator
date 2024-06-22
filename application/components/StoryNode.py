import sys
sys.path.insert(0,'')

from copy import deepcopy
from statistics import mean

from application.components.UtilFunctions import get_actor_object_from_list_with_actor_name, replace_multiple_placeholders_with_multiple_change_havers, replace_multiple_placeholders_with_multiple_test_takers, replace_pair_value_with_actual_actors

#, required_tags_list = [], unwanted_tags_list = [], bias_range = dict(), required_test_list = [], suggested_test_list = [], required_tags_list_target = [], unwanted_tags_list_target = [], bias_range_target = dict(), suggested_included_tags = [], suggested_excluded_tags = [], suggested_bias_range = dict(), suggested_included_tags_target = [], suggested_excluded_tags_target = [], suggested_bias_range_target = dict(), condition_tests = [],

'''
name: The name of this action.
biasweight: The score that the StoryGenerator will get if a character performs this action. The higher it is, the more likely this action will be performed.
tags: Tags that describe this StoryNode. Some important tags to note are as follow:
    'costly':True: Marks the StoryNode as Costly, which makes Cost StoryMetric count this StoryNode as Costly.
    'important_action':True: Marks the StoryNode as an Important Action, which makes the Preference StoryMetric count this StoryNode as Important
charcount: How many characters can perform this action. 1 by default. Can be set as a tuple of 2 ints (inclusive range) or -1 (freesized)
target_count: How many CharacterNode can be targeted by this action. 0 by default. Similarly to charcount, can be set as a tuple of 2 ints or -1.
timestep: The timestep that this StoryNode is in. When the StoryGraph looks for a pattern of certain storynodes being in a certain order, it will ignore the pattern if there is a timestep difference in one of the storynodes being checked.
actor: List of actors performing this action. Length should be equal to charcount.
target: List of targets this action is being performed on. Length should be equal to target_count.
effects_on_next_ws: List of Changes that will occur after this action was taken.
required_test_list: List of ConditionTests that must return True for this action to be valid.
suggested_test_list: List of ConditionTests that will grant extra points (likeliness to be chosen) if they return True.
'''
class StoryNode:
    def __init__(self, name:str, biasweight:int = 0, tags:dict = {"Type":"Placeholder"}, charcount = 1, target_count = 0, timestep = 0, actor = [], target = [], effects_on_next_ws = [], required_test_list = [], suggested_test_list = [], internal_id:int = 0, **kwargs):
        
        #the name of this action.
        self.name = name

        #bias weight. How much this action will affect the bias of the character performing it. For now, this will also affect how likely it is a character will perform this node.
        self.biasweight = biasweight
        
        #tags for searching actions of a specific type.
        #If it's an end node, it will be among the tags.
        self.tags = tags
        
        #charcount will be 1 if it's single char node, if it's joint then it will be more than 1, equal to the number of actors expected here.
        #If the char count is -1, it means that the amount is not fixed and can by any amount as long as it is a non-negative integer.
        self.charcount = charcount

        #target count is the number of characters that's allowed to be the target (exact count). Non-actor targets such as locations and objects do not care about this, but actors do.
        #Similarly to charcount, if this is -1, the amount is not fixed and can be any amount as long as it is a non-negative integer.
        self.target_count = target_count
        
        #set of characters acting. if it's a template, then it should be blank
        self.actor = actor
        
        #set of targets of this action. if it's a template, then it should be blank.
        self.target = target

        #the location where this story happens. If it's a template, then it should be None.
        self.location = None

        #timestep property. For template storynodes it will be 0. But once it is assigned to the story the number will never change.
        #This will prevent stories from different timestep from being blended together.
        self.timestep = timestep

        #Effects on next World State. We will use RelChange objects to represent the changes that this node will do to the next world state.
        self.effects_on_next_ws = effects_on_next_ws

        #Absolute Step is for the Joint Rules, so that the rules know which nodes to join together
        self.abs_step = 0

        #For consistency, all required/unwanteds are now lists of tuples instead.
        #Required Tags List, Unwanted Tags List, and Bias Range are taken from RewriteRule.
        self.required_test_list = required_test_list
        self.suggested_test_list = suggested_test_list

        self.internal_id = internal_id

    def get_name(self):
        return self.name
    
    def set_name(self, new_name):
        self.name = new_name

    def get_location(self):
        return self.location

    def set_location(self, new_location):
        self.location = new_location

    def add_actor(self, new_actor):
        if new_actor not in self.actor:
            self.actor.append(new_actor)

    def remove_actor(self, remove_actor):
        self.actor.remove(remove_actor)

    def remove_all_actors(self):
        self.actor = []

    def add_target(self, new_target):
        if new_target not in self.target:
            self.target.append(new_target)
    
    def remove_target(self, remove_target):
        self.target.remove(remove_target)

    def check_if_character_exists_in_node(self, actor):
        return actor in self.actor or actor in self.target

    def get_actor_names(self):
        actornamestring = ""
        for actorobject in self.actor:

            if actorobject is not None:
                actornamestring += actorobject.get_display_name()
            else:
                actornamestring += "None"
                

            actornamestring += ", "
        return actornamestring[:-2]

    def get_target_names(self):
        targetnamestring = ""
        for targetobject in self.target:

            if targetobject is not None:
                targetnamestring += targetobject.get_display_name()
            else:
                targetnamestring += "None"
                

            targetnamestring += ", "
        return targetnamestring[:-2]

    def __str__(self) -> str:
        return self.get_name() + " (Actors: " + self.get_actor_names() + ")"

    def __eq__(self, rhs):

        if rhs is None:
            return False

        return self.get_name() == rhs.get_name() and sorted(self.actor) == sorted(rhs.actor) and sorted(self.target) == sorted(rhs.target)

    def __ge__(self, rhs):
        return self.get_name() >= rhs.get_name()

    def check_if_joint_node(self):
        
        if type(self.charcount) == tuple() or type(self.target_count) == tuple():
            return True

        #If this node allows more than 1 character or allows more than 1 target which is an actor then it is a joint node.
        return self.charcount > 1 or self.target_count > 0 or self.charcount == -1 or self.target_count == -1
    
    def export_object_as_dict(self) -> dict:
        return_dict = dict()

        return_dict["name"] = self.name
        return_dict["biasweight"] = self.biasweight
        return_dict["tags"] = self.tags
        return_dict["charcount"] = self.charcount
        return_dict["target_count"] = self.target_count
        return_dict["timestep"] = self.timestep

        return_dict["required_test_ids"] = []
        for test in self.required_test_list:
            return_dict["required_test_ids"].append(test.internal_id)

        return_dict["suggested_test_ids"] = []
        for test in self.suggested_test_list:
            return_dict["suggested_test_ids"].append(test.internal_id)

        return_dict["change_ids"] = []
        for change in self.effects_on_next_ws:
            return_dict["change_ids"].append(change.internal_id)

        return_dict["internal_id"] = self.internal_id

        return return_dict
    
    def return_stripped_story_node(self):

        nodecopy = deepcopy(self)
        nodecopy.effects_on_next_ws = []
        nodecopy.required_test_list = []
        nodecopy.suggested_test_list = []

        return nodecopy
    
def replace_placeholders_in_story_node(story_node:StoryNode, placeholder_dict:dict, list_of_actor_objects=[]):
    #Things that must be replaced:
    # - Actors
    # - Targets 
    # - Relationship Changes
    # - Requirement Tests
    story_node_copy = deepcopy(story_node)

    new_actor_list = []
    new_target_list = []

    new_ws_effect_list = []

    new_req_test_list = []
    new_suggest_test_list = []

    for actor in story_node_copy.actor:
        if actor in list(placeholder_dict.keys()):
            new_actor = get_actor_object_from_list_with_actor_name(actor_name=placeholder_dict[actor], actor_list=list_of_actor_objects)
            new_actor_list.append(new_actor)
        else:
            new_actor_list.append(actor)

   
    for target in story_node_copy.target:
        if target in list(placeholder_dict.keys()):
            new_actor = get_actor_object_from_list_with_actor_name(actor_name=placeholder_dict[target], actor_list=list_of_actor_objects)
            # print(new_actor)
            new_target_list.append(new_actor)
        else:
            new_target_list.append(target)

    replaced_kv = replace_pair_value_with_actual_actors(kv_pair_list=placeholder_dict.items(), actor_list=list_of_actor_objects)

    for test in story_node_copy.required_test_list:
        new_req_test_list.append(replace_multiple_placeholders_with_multiple_test_takers(test=test, placeholder_tester_pair_list=replaced_kv))

    for test in story_node_copy.suggested_test_list:
        new_suggest_test_list.append(replace_multiple_placeholders_with_multiple_test_takers(test=test, placeholder_tester_pair_list=replaced_kv))

    for change in story_node_copy.effects_on_next_ws:
        new_ws_effect_list.append(replace_multiple_placeholders_with_multiple_change_havers(change=change, placeholder_tester_pair_list=replaced_kv))

    story_node_copy.actor = new_actor_list
    story_node_copy.target = new_target_list
    story_node_copy.required_test_list = new_req_test_list
    story_node_copy.suggested_test_list = new_suggest_test_list
    story_node_copy.effects_on_next_ws = new_ws_effect_list

    # print(new_actor_list, new_target_list, new_req_test_list, new_suggest_test_list, new_ws_effect_list)

    return story_node_copy