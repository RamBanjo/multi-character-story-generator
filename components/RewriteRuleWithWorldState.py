from components.StoryGraphTwoWS import StoryGraph
from components.WorldState import WorldState

class RewriteRule:


    
    # ...do we really need World State Change, if all of the world state changes will be stated in the change to world states in the story parts?
    # We probably don't.
    # With the same logic, we don't need World State Condition either, since we can put all the conditions in the 


    def __init__(self, story_condition, story_change, world_state_condition, world_state_change, dummychar, name=""):
        self.rule_name = name
        self.story_condition = story_condition
        self.story_change = story_change
        self.dummychar = dummychar
        self.is_joint_rule = False
        self.world_state_condition = world_state_condition
        self.world_state_change = world_state_change

    #TODO: Make it account for all the past world states, by inputting list of changes from the story graph
    def check_character_compatibility(self, character_node, init_world_state, list_of_changes, start_of_check):

        compatibility = True

        #Instead of checking directly with this thing, we'll need to check with each individual node in story_change.

        for story_node in self.story_change:
            compatibility = compatibility and story_node.check_character_compatibility(character_node)

        return compatibility

'''
JointRule needs 2 dummy characters and joints in one of three ways:
(JointRule feels more like a grammar rule than a replacement rule...)

Two into one (Joining Joint), where two characters join into one node
    - This one takes an input of two (or more). Character A should be doing Action X, and Character B should be doing Action Y.
        - Possibly, use a list to handle this? So long as everything in the list is satisfied...
    - If this condition is met, then add the next node, Joint Action Z, which will involve A and B doing something together OR A acting on B.

one into one (Continuous Joint), where two characters continue to act as one group
    - Takes an input of one joint node.
    - If this joint node exists with the specified characters, join it with another joint node with the same characters.

one into two (Splitting Joint), where two characters previously joined together split up
    - Takes an input of one joint node.
    - If this joint node exists with the specified characters, split the characters off into different branches.
'''


'''
Base Joint Rule containing common properties between all the aforementioned joint rules

Rule Name: What the rule is referred to.
Merge Count: How many characters are merging here. Minimum is 2.
Dummy Chars: The dummies used for the purpose of replacing. Dummies are consistent.
    - For example, if there are two Dummies in the rule, and the rule is used on a graph with Alice and Bob as input chars in that order,
    Dummy A will always be replaced by Alice and Dummy B will always be replaced by Bob.
Required Tags List, unwanted tags list, and bias range list are the same as normal rules, but written in a list so that characters can
have separate values if needs be. If a particular slot has no prerequisites, it should be an empty dict if it's tags, or None if it's a bias range.
'''
class JointRule:
    def __init__(self, merge_count, joint_type, rule_name="", required_tags_list=[], unwanted_tags_list=[], bias_range_list=[]):
        self.rule_name = rule_name
        self.merge_count = merge_count
        self.joint_type = joint_type
        self.required_tags_list = required_tags_list
        self.unwanted_tags_list = unwanted_tags_list
        self.bias_range_list = bias_range_list
        self.is_joint_rule = True

    def check_compatibilities(self, character_list):
        #This function should be the same as the function that checks compatibilities in the normal rewrite rules but it checks for each character
        compatibility = True

        #This part below is lifted from regular rules.
        for i in range (0, len(character_list)):
            #TODO: Check if the character contains tags in Required Tags (not compatible if false)

            if self.required_tags_list[i] is not None:
                for tag in self.required_tags_list[i].values():
                    compatibility = compatibility and tag in character_list[i].tags.values()

            #TODO: Check if character contains tags in Unwanted Tags (not compatible if true)
            if self.unwanted_tags_list[i] is not None:
                for tag in self.unwanted_tags_list[i].values():
                    compatibility = compatibility and tag not in character_list[i].tags.values()
        
            #TODO: Check if character's bias is within the acceptable range (not compatible if false)
            if self.bias_range_list[i] is not None:
                for bias in self.bias_range_list[i]:
                    char_bias_value = character_list[i].biases[bias]
                    compatibility = compatibility and char_bias_value >= self.bias_range_list[i][bias][0]
                    compatibility = compatibility and char_bias_value <= self.bias_range_list[i][bias][1]
                
        #If the character passes all three tests, then return true. Otherwise, return false
        return compatibility

'''
Joining Joint Rule!

Joining Joint's base is a list of nodes for each of the character intending to join in.
'''
class JoiningJointRule(JointRule):
    def __init__(self, merge_count, base_actions, joint_node, rule_name="", required_tags_list=[], unwanted_tags_list=[], bias_range_list=[]):

        super().__init__(merge_count, "joining", rule_name, required_tags_list, unwanted_tags_list, bias_range_list)

        self.base_actions = base_actions
        self.joint_node = joint_node

'''
Continuous Joint Rule!

Cont. Joint's base is a joint itself, and then a joint would connect to it.
'''
class ContinuousJointRule(JointRule):
    def __init__(self, merge_count, base_joint, joint_node, rule_name="", required_tags_list=[], unwanted_tags_list=[], bias_range_list=[]):

        super().__init__(merge_count, "continuous", rule_name, required_tags_list, unwanted_tags_list, bias_range_list)

        self.base_joint = base_joint
        self.joint_node = joint_node

'''
Splitting Joint Rule!

Splitting Joint Rule's base would be the joint node where dummy chars will go separate ways.
'''
class SplittingJointRule(JointRule):
    def __init__(self, merge_count, base_joint, split_list, rule_name="", required_tags_list=[], unwanted_tags_list=[], bias_range_list=[]):

        super().__init__(merge_count, "splitting", rule_name, required_tags_list, unwanted_tags_list, bias_range_list)

        self.base_joint = base_joint
        self.split_list = split_list