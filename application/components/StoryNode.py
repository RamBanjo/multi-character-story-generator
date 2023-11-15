import sys
sys.path.insert(0,'')

from copy import deepcopy
from statistics import mean

from application.components.UtilFunctions import get_actor_object_from_list_with_actor_name, replace_multiple_placeholders_with_multiple_change_havers, replace_multiple_placeholders_with_multiple_test_takers, replace_pair_value_with_actual_actors

#, required_tags_list = [], unwanted_tags_list = [], bias_range = dict(), required_test_list = [], suggested_test_list = [], required_tags_list_target = [], unwanted_tags_list_target = [], bias_range_target = dict(), suggested_included_tags = [], suggested_excluded_tags = [], suggested_bias_range = dict(), suggested_included_tags_target = [], suggested_excluded_tags_target = [], suggested_bias_range_target = dict(), condition_tests = [],
class StoryNode:
    def __init__(self, name, biasweight=0, tags={"Type":"Placeholder"}, charcount=1, target_count = 0, timestep = 0, actor = [], target = [], effects_on_next_ws = [], required_test_list = [], suggested_test_list = [], **kwargs):
        
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
        
        #dict of nodes that leads to this node. Each entry has character's unique ID as key and points to
        #the node that character performed before arriving at this node.
        # self.previous_nodes = dict()
        
        #dict of nodes that continue from here. Each entry has character's unique ID as key and points to
        #the node that character will perform after leaving this node.
        # self.next_nodes = dict()

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

    def get_name(self):
        return self.name
    
    def set_name(self, new_name):
        self.name = new_name

    def get_location(self):
        return self.location

    def set_location(self, new_location):
        self.location = new_location

    def add_actor(self, new_actor):
        self.actor.append(new_actor)

    def remove_actor(self, remove_actor):
        self.actor.remove(remove_actor)

    def remove_all_actors(self):
        self.actor = []

    def add_target(self, new_target):
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
    '''
    This function adds next_node as the next node for the character object character_reference

    It will also add self as one of next_node's previous nodes! Convenient!
    '''
    # def add_next_node(self, next_node, character_reference):

    #     char_name = None

    #     if character_reference is not None:
    #         char_name = character_reference.get_name()

    #     self.next_nodes[char_name] = next_node

    #     next_node.previous_nodes[char_name] = self
    #     #next_node.add_actor(character_reference)


    '''
    First, it removes itself from next_node's previous nodes

    Then, it removes next_node from its own next nodes
    '''
    # def remove_next_node(self, character_reference):
        
    #     char_name = None

    #     if character_reference is not None:
    #         char_name = character_reference.get_name()

    #     next_node = self.next_nodes[char_name]

    #     del next_node.previous_nodes[char_name]
    #     del self.next_nodes[char_name]

    # This will test the tests in the required_tests that feature the character's name after replacing all actor placeholders with the character themself.
    # Deprecation of this function???
    # def check_character_compatibility(self, character_node):

    #     compatibility = True

    #     #Check if the character contains tags in Required Tags (not compatible if false)

    #     #print("Before All Tests", compatibility)
    #     # if self.required_tags_list is not None:
    #     #     for tag_tuple in self.required_tags_list:
    #     #         compatibility = compatibility and (character_node.tags.get(tag_tuple[0], None) == tag_tuple[1])

    #     # #Check if character contains tags in Unwanted Tags (not compatible if true)

    #     # #print("After Req Tags Test", compatibility)
    #     # if self.unwanted_tags_list is not None:
    #     #     for tag_tuple in self.unwanted_tags_list:
    #     #         compatibility = compatibility and (character_node.tags.get(tag_tuple[0], None) != tag_tuple[1])
        
    #     # #print("After Unwanted Tags Test", compatibility)
    #     # #Check if character's bias is within the acceptable range (not compatible if false)
    #     # if self.bias_range is not None:
    #     #     for bias in self.bias_range:
    #     #         char_bias_value = character_node.biases[bias]
    #     #         compatibility = compatibility and char_bias_value >= self.bias_range[bias][0]
    #     #         compatibility = compatibility and char_bias_value <= self.bias_range[bias][1]
        
    #     #print("After Bias Range Test", compatibility)
    #     #If the character passes all three tests, then return true. Otherwise, return false
    #     return compatibility
        
    # def check_character_compatibility_for_many_characters(self, list_of_chars):
    #     compatibility = True

    #     for character_node in list_of_chars:
    #         compatibility = compatibility and self.check_character_compatibility(character_node)

    #     return compatibility

    # def check_target_compatibility(self, character_node, verbose = False):
        
    #     compatibility = True

    #     #Check if the character contains tags in Required Tags (not compatible if false)

    #     if self.required_tags_list_target is not None:
    #         for tag_tuple in self.required_tags_list_target:
    #             compatibility = compatibility and (character_node.tags.get(tag_tuple[0], None) == tag_tuple[1])
    #             if verbose:
    #                 print("Result of required tags test", compatibility)

    #     #Check if character contains tags in Unwanted Tags (not compatible if true)

    #     if self.unwanted_tags_list_target is not None:
    #         for tag_tuple in self.unwanted_tags_list_target:
    #             compatibility = compatibility and (character_node.tags.get(tag_tuple[0], None) != tag_tuple[1])
    #             if verbose:
    #                 print("Result of unwanted tags test", compatibility)
        
    #     #Check if character's bias is within the acceptable range (not compatible if false)
    #     if self.bias_range_target is not None:
    #         for bias in self.bias_range_target:
    #             char_bias_value = character_node.biases[bias]
    #             compatibility = compatibility and char_bias_value >= self.bias_range_target[bias][0]
    #             if verbose:
    #                 print("Result of lower bound bias test", compatibility)
    #                 print(compatibility)
    #             compatibility = compatibility and char_bias_value <= self.bias_range_target[bias][1]
    #             if verbose:
    #                 print("Result of upper bound bias test", compatibility)
    #                 print(compatibility)

    #     #If the character passes all three tests, then return true. Otherwise, return false
    #     return compatibility 

    # def check_target_compatibility_for_many_characters(self, list_of_chars):
    #     compatibility = True

    #     for character_node in list_of_chars:
    #         compatibility = compatibility and self.check_target_compatibility(character_node)

    #     return compatibility

    # def calculate_bonus_weight_score(self, character_node):

    #     if not self.check_character_compatibility(character_node=character_node):
    #         return -999
        
    #     score = 0

    #     if self.suggested_included_tags is not None:
    #         for tag_tuple in self.suggested_included_tags:
    #             if (character_node.tags.get(tag_tuple[0], None) == tag_tuple[1]):
    #                 score += 1

    #     if self.suggested_excluded_tags is not None:
    #         for tag_tuple in self.suggested_excluded_tags:
    #             if (character_node.tags.get(tag_tuple[0], None) != tag_tuple[1]):
    #                 score += 1

    #     if self.suggested_bias_range is not None:
    #         for bias in self.suggested_bias_range:
    #             char_bias_value = character_node.biases[bias]
    #             if char_bias_value >= self.suggested_bias_range[bias][0] and char_bias_value <= self.suggested_bias_range[bias][1]:
    #                 score += 1

    #     return score
    
    # def calculate_bonus_weight_score_target(self, character_node):

    #     if not self.check_target_compatibility(character_node=character_node):
    #         return -999

    #     score = 0

    #     if self.suggested_included_tags_target is not None:
    #         for tag_tuple in self.suggested_included_tags_target:
    #             if (character_node.tags.get(tag_tuple[0], None) == tag_tuple[1]):
    #                 score += 1

    #     if self.suggested_excluded_tags_target is not None:
    #         for tag_tuple in self.suggested_excluded_tags_target:
    #             if (character_node.tags.get(tag_tuple[0], None) != tag_tuple[1]):
    #                 score += 1

    #     if self.suggested_bias_range_target is not None:
    #         for bias in self.suggested_bias_range_target:
    #             char_bias_value = character_node.biases[bias]
    #             if char_bias_value >= self.suggested_bias_range_target[bias][0] and char_bias_value <= self.suggested_bias_range_target[bias][1]:
    #                 score += 1

    #     return score

    # def calculate_weight_score(self, character_node, involve_target=False, mode=0):
    #     '''
    #     If max_between_actor_target is set to True AND there are slots for the target, then instead of only doing the bonus weight score for the actor part, it will also calculate the target part and choose max between the two.
    #     '''

    #     if involve_target and self.target_count > 0:

    #         if self.calculate_bonus_weight_score(character_node) == -999 and self.calculate_bonus_weight_score_target(character_node) == -999:
    #             return -999
            
    #         if self.calculate_bonus_weight_score(character_node) == -999:
    #             return self.calculate_bonus_weight_score_target(character_node) + self.biasweight
            
    #         if self.calculate_bonus_weight_score_target(character_node) == -999:
    #             return self.calculate_bonus_weight_score(character_node) + self.biasweight

    #         if mode == 1:
    #             return mean([self.calculate_bonus_weight_score(character_node), self.calculate_bonus_weight_score_target(character_node)]) + self.biasweight
            
    #         return max(self.calculate_bonus_weight_score(character_node), self.calculate_bonus_weight_score_target(character_node)) + self.biasweight

    #     return self.calculate_bonus_weight_score(character_node) + self.biasweight

    # #Also, we should probably make a function that returns true if either the target compat gets approved or the actor compat gets approved, for the purposes of joint rules
    # #Use case for this: When we are testing a joint node for a character, we should test if they'd work in either slot because we don't know which slot they would go to.
    # def check_actor_or_target_compatibility(self, character_node):
    #     return self.check_character_compatibility(character_node) or self.check_target_compatibility(character_node)
    
    # def check_actor_or_target_compatibility_for_many_characters(self, list_of_chars):
    #     compatibility = True

    #     for character_node in list_of_chars:
    #         compatibility = compatibility and self.check_actor_or_target_compatibility(character_node)

    #     return compatibility
    
    def check_if_joint_node(self):
        
        #If this node allows more than 1 character or allows more than 1 target which is an actor then it is a joint node.
        return self.charcount > 1 or self.target_count > 0
    
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