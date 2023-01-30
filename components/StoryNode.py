from numpy import character


class StoryNode:
    def __init__(self, name, biasweight, tags, charcount, target_count = 0, timestep = 0, effects_on_next_ws = [], required_tags_list = dict(), unwanted_tags_list = dict(), bias_range = dict(), required_tags_list_target = dict(), unwanted_tags_list_target = dict(), bias_range_target = dict(), condition_tests = [], **kwargs):
        
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
        self.actor = []
        
        #set of targets of this action. if it's a template, then it should be blank.
        self.target = []

        #the location where this story happens. If it's a template, then it should be None.
        self.location = None
        
        #dict of nodes that leads to this node. Each entry has character's unique ID as key and points to
        #the node that character performed before arriving at this node.
        self.previous_nodes = dict()
        
        #dict of nodes that continue from here. Each entry has character's unique ID as key and points to
        #the node that character will perform after leaving this node.
        self.next_nodes = dict()

        #timestep property. For template storynodes it will be 0. But once it is assigned to the story the number will never change.
        #This will prevent stories from different timestep from being blended together.
        self.timestep = timestep

        #Effects on next World State. We will use RelChange objects to represent the changes that this node will do to the next world state.
        self.effects_on_next_ws = effects_on_next_ws

        #Absolute Step is for the Joint Rules, so that the rules know which nodes to join together
        self.abs_step = 0

        #Required Tags List, Unwanted Tags List, and Bias Range are taken from RewriteRule.
        self.required_tags_list = required_tags_list
        self.unwanted_tags_list = unwanted_tags_list
        self.bias_range = bias_range

        self.required_tags_list_target = required_tags_list_target
        self.unwanted_tags_list_target = unwanted_tags_list_target
        self.bias_range_target = bias_range_target

        #condition_tests is a list of ConditionTest objects. In order to perform this story node, the world state must fulfil all the conditions in it.
        self.condition_tests = condition_tests
        
        #TODO: An object that defines the change in relationship for characters and objects in this story node

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

    def get_actor_names(self):
        actornamestring = ""
        for actorobject in self.actor:

            if actorobject is not None:
                actornamestring += actorobject.get_name()
            else:
                actornamestring += "None"
                

            actornamestring += ", "
        return actornamestring[:-2]

    def get_target_names(self):
        targetnamestring = ""
        for targetobject in self.target:

            if targetobject is not None:
                targetnamestring += targetobject.get_name()
            else:
                targetnamestring += "None"
                

            targetnamestring += ", "
        return targetnamestring[:-2]


    def __str__(self) -> str:
        return self.get_name() + " (Actors: " + self.get_actor_names() + ")"

    def __eq__(self, rhs):
        return self.get_name() == rhs.get_name() and sorted(self.actor) == sorted(rhs.actor) and sorted(self.target) == sorted(rhs.target)

    def __ge__(self, rhs):
        return self.get_name() >= rhs.get_name()
    '''
    This function adds next_node as the next node for the character object character_reference

    It will also add self as one of next_node's previous nodes! Convenient!
    '''
    def add_next_node(self, next_node, character_reference):

        char_name = None

        if character_reference is not None:
            char_name = character_reference.get_name()

        self.next_nodes[char_name] = next_node
        next_node.previous_nodes[char_name] = self
        #next_node.add_actor(character_reference)


    '''
    First, it removes itself from next_node's previous nodes

    Then, it removes next_node from its own next nodes
    '''
    def remove_next_node(self, character_reference):

        char_name = None

        if character_reference is not None:
            char_name = character_reference.get_name()

        next_node = self.next_nodes[char_name]

        del next_node.previous_nodes[char_name]
        del self.next_nodes[char_name]

    def check_character_compatibility(self, character_node):

        compatibility = True

        #TODO: Check if the character contains tags in Required Tags (not compatible if false)

        #print("Before All Tests", compatibility)
        if self.required_tags_list is not None:
            for tag in self.required_tags_list.values():
                compatibility = compatibility and tag in character_node.tags.values()

        #TODO: Check if character contains tags in Unwanted Tags (not compatible if true)

        #print("After Req Tags Test", compatibility)
        if self.unwanted_tags_list is not None:
            for tag in self.unwanted_tags_list.values():
                compatibility = compatibility and tag not in character_node.tags.values()
        
        #print("After Unwanted Tags Test", compatibility)
        #TODO: Check if character's bias is within the acceptable range (not compatible if false)
        if self.bias_range is not None:
            for bias in self.bias_range:
                char_bias_value = character_node.biases[bias]
                compatibility = compatibility and char_bias_value >= self.bias_range[bias][0]
                compatibility = compatibility and char_bias_value <= self.bias_range[bias][1]
        
        #print("After Bias Range Test", compatibility)
        #If the character passes all three tests, then return true. Otherwise, return false
        return compatibility
        
    def check_character_compatibility_for_many_characters(self, list_of_chars):
        compatibility = True

        for character_node in list_of_chars:
            compatibility = compatibility and self.check_character_compatibility(character_node)

        return compatibility

    def check_target_compatibility(self, character_node, verbose = False):
        
        compatibility = True

        #TODO: Check if the character contains tags in Required Tags (not compatible if false)

        if self.required_tags_list_target is not None:
            for tag in self.required_tags_list_target.values():
                compatibility = compatibility and tag in character_node.tags.values()
                if verbose:
                    print("Result of required tags test", compatibility)

        #TODO: Check if character contains tags in Unwanted Tags (not compatible if true)

        if self.unwanted_tags_list_target is not None:
            for tag in self.unwanted_tags_list_target.values():
                compatibility = compatibility and tag not in character_node.tags.values()
                if verbose:
                    print("Result of unwanted tags test", compatibility)
        
        #TODO: Check if character's bias is within the acceptable range (not compatible if false)
        if self.bias_range_target is not None:
            for bias in self.bias_range_target:
                char_bias_value = character_node.biases[bias]
                compatibility = compatibility and char_bias_value >= self.bias_range_target[bias][0]
                if verbose:
                    print("Result of lower bound bias test", compatibility)
                    print(compatibility)
                compatibility = compatibility and char_bias_value <= self.bias_range_target[bias][1]
                if verbose:
                    print("Result of upper bound bias test", compatibility)
                    print(compatibility)

        #If the character passes all three tests, then return true. Otherwise, return false
        return compatibility 

    def check_target_compatibility_for_many_characters(self, list_of_chars):
        compatibility = True

        for character_node in list_of_chars:
            compatibility = compatibility and self.check_target_compatibility(character_node)

        return compatibility


