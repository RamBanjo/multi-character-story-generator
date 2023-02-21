from enum import Enum
import statistics
from components.UtilFunctions import actor_count_sum
from components.UtilityEnums import JointType

#TODO: Rewrite this class so instead of replacing things, it *inserts* things after the condition.

class RewriteRule:
    # ...do we really need World State Change, if all of the world state changes will be stated in the change to world states in the story parts?
    # We probably don't.
    # With the same logic, we don't need World State Condition either, since we can put all the conditions in the story nodes


    def __init__(self, story_condition, story_change, name="", remove_before_insert = False, target_list = None):
        self.rule_name = name
        self.story_condition = story_condition
        self.story_change = story_change
        self.is_joint_rule = False
        self.remove_before_insert = remove_before_insert
        self.target_list = target_list

    #Figure out how to choose the best node
    #Maybe use the metrics?

    # This is going to be a separate thing from the metrics. We'll take care of how we handle metrics later
    # For now, this is how we will handle the story rewrite rules' character fitness values.
    # 1. Do steps 2-4 for each of the nodes:
    # 2. Add the raw Bias Value.
    # 3. After we get the sum score from each node, average it.
    # (This is a placeholder calculation formula and will be subject to change)
    # As a failsafe, if the character is not suitable for that node, return -999 (arbitarily large negative number to put it at the bottom of the top n list)
    def get_character_fitness_value(self, character):

        total_bias_list = []
        for story_node in self.story_change:

            if story_node.check_character_compatibility(character):
                total_bias_list.append(story_node.biasweight)
            else:
                return -999
                
        return statistics.mean(total_bias_list)

    #TODO: This probably is no longer needed considering that we have moved all these checks to the Nodes themselves?
    # def check_character_compatibility(self, character_node, init_world_state, list_of_changes, start_of_check):

    #     compatibility = True

    #     #Instead of checking directly with this thing, we'll need to check with each individual node in story_change.

    #     for story_node in self.story_change:
    #         compatibility = compatibility and story_node.check_character_compatibility(character_node)

    #     return compatibility

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
    def __init__(self, joint_type, rule_name="", target_list=None):
        self.rule_name = rule_name
        self.joint_type = joint_type
        self.is_joint_rule = True
        self.target_list = target_list

'''
Joining Joint Rule!

Joining Joint's base is a list of nodes for each of the character intending to join in.
'''

#Handling base action for Joining Joint Rule: All the nodes mentioned in base actions must exist in some way, though depending on the number of characters allowed in the joint node, we might allow extras.
class JoiningJointRule(JointRule):
    def __init__(self, base_actions, joint_node, rule_name="", target_list=None):

        super().__init__(JointType.JOIN, rule_name, target_list=target_list)

        self.base_actions = base_actions
        self.joint_node = joint_node

    def get_character_fitness_value(self, character):
        if self.joint_node.check_character_compatibility(character):
            return self.joint_node.biasweight
        else:
            return -999

    def get_character_count(self):
        return actor_count_sum(self.joint_node.charcount, self.joint_node.target_count)

'''
Continuous Joint Rule!

Cont. Joint's base is a joint itself, and then a joint would connect to it.
'''

class ContinuousJointRule(JointRule):
    def __init__(self, base_joint, joint_node, rule_name="", target_list=None):

        super().__init__(JointType.CONT, rule_name, target_list=target_list)

        self.base_joint = base_joint
        self.joint_node = joint_node

    def get_character_fitness_value(self, character):
        if self.joint_node.check_character_compatibility(character):
            return self.joint_node.biasweight
        else:
            return -999

    def get_character_count(self):
        return actor_count_sum(self.joint_node.charcount, self.joint_node.target_count)
'''
Splitting Joint Rule!

Splitting Joint Rule's base would be the joint node where dummy chars will go separate ways.
'''

class SplittingJointRule(JointRule):
    def __init__(self, base_joint, split_list, rule_name="", target_list=None):

        super().__init__(JointType.SPLIT, rule_name, target_list=target_list)

        self.base_joint = base_joint
        self.split_list = split_list

    def get_character_fitness_value(self, character):

        eligible_list = []

        for node in self.split_list:
            if node.check_character_compatibility(character):
                eligible_list.append(node)

        if len(eligible_list) > 0:
            biasval_list = [x.biasweight for x in eligible_list]
            return statistics.mean(biasval_list)
        else:
            return -999

    def get_character_count(self):

        current_sum = 0

        for item in self.get_split_character_count():
            current_sum = actor_count_sum(current_sum, item)

        if type(current_sum) == tuple:
            if current_sum[1] > 999:
                current_sum[1] = 999

        return current_sum

    def get_split_character_count(self):
        list_of_cont_counts = []
        
        for cont in self.split_list:
            list_of_cont_counts.append(actor_count_sum(cont.charcount, cont.target_count))

        return list_of_cont_counts
    