#check_joint_continuity_validity

from copy import deepcopy
from components.ConditionTest import HasTagTest
from components.RewriteRuleWithWorldState import ContinuousJointRule, JoiningJointRule, SplittingJointRule
from components.StoryGraphTwoWS import StoryGraph
from components.StoryNode import StoryNode
from components.StoryObjects import CharacterNode, LocationNode
from components.UtilityEnums import GenericObjectNode
from components.WorldState import WorldState


alice = CharacterNode(name="Alice", tags={"Type":"Character", "Job":"Swordmaster"})
bob = CharacterNode(name="Bob", tags={"Type":"Character", "Job":"Warrior"})
charlie = CharacterNode(name="Charlie", tags={"Type":"Character", "Job":"Paladin"})
daniel = CharacterNode(name="Daniel", tags={"Type":"Character", "Job":"Archer"})
eve = CharacterNode(name="Eve", tags={"Type":"Character", "Job":"Sorcerer"})

town = LocationNode(name="TownSquare")

test_ws = WorldState(name="Test State", objectnodes=[alice, bob, charlie, daniel, town])

test_ws.connect(from_node=town, edge_name="holds", to_node=alice)
test_ws.connect(from_node=town, edge_name="holds", to_node=bob)
test_ws.connect(from_node=town, edge_name="holds", to_node=charlie)
test_ws.connect(from_node=town, edge_name="holds", to_node=daniel)
test_ws.connect(from_node=town, edge_name="holds", to_node=eve)

#Eve doesn't exist in this world state nor does she exist in the story graph. Oops!
test_sg = StoryGraph(name="Test SG", character_objects=[alice, bob, charlie, daniel], location_objects=[town], starting_ws=test_ws)
test_sg_2 = deepcopy(test_sg)
test_sg_3 = deepcopy(test_sg)

node_x = StoryNode(name="Action X", biasweight=1, tags={"Type":"Placeholder"}, charcount=-1)
node_y = StoryNode(name="Action Y", biasweight=1, tags={"Type":"Placeholder"}, charcount=-1)
node_z = StoryNode(name="Action Z", biasweight=1, tags={"Type":"Placeholder"}, charcount=-1, target_count=-1)

#This action doesn't want people with the job Swordmaster to do, therefore Alice shouldn't be allowed to do it.
test_not_swordmaster = HasTagTest(object_to_test=GenericObjectNode.ALL_ACTORS, tag="Job", value="Swordmaster", inverse=True)
node_w = StoryNode(name="Action W", biasweight=1, tags={"Type":"Placeholder"}, charcount=-1, required_test_list=[test_not_swordmaster])
node_v = StoryNode(name="Action V", biasweight=1, tags={"Type":"Placeholder"}, charcount=3, target_count=1)

test_sg.insert_joint_node(joint_node=node_x, main_actor=alice, other_actors=[bob, charlie, daniel], location=town)
test_sg_2.insert_joint_node(joint_node=node_x, main_actor=alice, other_actors=[bob, charlie], location=town)
test_sg_2.insert_joint_node(joint_node=node_z, main_actor=daniel, location=town)
test_sg_3.insert_story_part(part=node_x, character=alice, location=town)
test_sg_3.insert_story_part(part=node_x, character=bob, location=town)
test_sg_3.insert_story_part(part=node_y, character=charlie, location=town)
test_sg_3.insert_story_part(part=node_y, character=daniel, location=town)
#Grouping Split are formatted as a Dict in the form of [{"actor_group":[(list of character objects)] and "target_group":[(list of character objects)]}, etc...] showing each split. If it's a Cont or Join, then there will be only one member.

#The rule is that X can be followed by Y. That's a Cont Joint Rule!
if_x_then_y_cont = ContinuousJointRule(base_joint=node_x, joint_node=node_y, rule_name="If X then Y")
if_x_then_y_join = JoiningJointRule(base_actions=[node_x], joint_node=node_y, rule_name="If X or Z then Y")
if_x_then_split_into_wz_split = SplittingJointRule(base_joint=node_x, split_list=[node_w, node_z], rule_name="If X then Split into WZ")
if_x_then_split_into_yz_split = SplittingJointRule(base_joint=node_x, split_list=[node_y, node_z], rule_name="If X then Split into YZ")
if_x_then_v_cont = ContinuousJointRule(base_joint=node_x, joint_node=node_v, rule_name="If X then V")
if_xy_then_w_join = JoiningJointRule(base_actions=[node_x, node_y], joint_node=node_w, rule_name="If XY then W")
if_xy_then_z_join = JoiningJointRule(base_actions=[node_x, node_y], joint_node=node_z, rule_name="If XY then Z")

#Test Case 1: Try to call check_joint_continuity_validity while mentioning Eve as one of the characters. This should be False, because Eve doesn't exist.
grouping_split_tc1 = [{"actor_group":[alice, bob, charlie, eve], "target_group":[]}]
print("Test Case 1: Eve doesn't exist in Story Graph.")
validity = test_sg.check_joint_continuity_validity(joint_rule=if_x_then_y_cont, main_character=alice, grouping_split=grouping_split_tc1, insert_index=1, verbose=True)
print("Validity is", validity)
print()

#Test Case 2: We're going to make Alice the main character of this Split Joint again, but if she's missing from the Grouping Split, then nothing can bee done and we should expect False.
grouping_split_tc2 = [{"actor_group":[bob, charlie, daniel], "target_group":[]}]
print("Test Case 2: Alice as the main actor is missing from the Character grouping.")
validity = test_sg.check_joint_continuity_validity(joint_rule=if_x_then_y_cont, main_character=alice, grouping_split=grouping_split_tc2, insert_index=1, verbose=True)
print("Validity is", validity)
print()

# Test Case 3: If we are trying to do Cont Joint or a Split Joint, then all the actors must be in the same base node
# We return false if they aren't.
grouping_split_tc3 = [{"actor_group":[alice, bob, charlie, daniel], "target_group":[]}]
print("Test Case 3: All characters aren't in the same node for the Cont Joint to be valid.")
validity = test_sg_2.check_joint_continuity_validity(joint_rule=if_x_then_y_cont, main_character=alice, grouping_split=grouping_split_tc3, insert_index=1, verbose=True)
print("Validity is", validity)
print()

#Test Case 4: If we're trying to do a Join Joint, then we need to check if the base of the joint matches
# what it says in the rule with check_if_abs_step_has_joint_pattern. It will be false if the pattern
# doesn't follow.
# Say for example the joint rule says you only want characters from X Node,
# but there are some characters from Y Node.

print("Test Case 4: Joining Joint says that the base node must be X for it to work, but there are some characters in Node Y. No match!")
validity = test_sg_3.check_joint_continuity_validity(joint_rule=if_x_then_y_join, main_character=alice, grouping_split=grouping_split_tc3, insert_index=1, verbose=True)
print("Validity is", validity)
print()

#Test Case 5: New Test Case because I just Thought of It: There is no previous step. Rules can't be applied if there's no previous step!
print("Test Case 5: We can't insert the rule in Index 0, because there's no preceding node.")
validity = test_sg_3.check_joint_continuity_validity(joint_rule=if_x_then_y_join, main_character=alice, grouping_split=grouping_split_tc3, insert_index=0, verbose=True)
print("Validity is", validity)
print()

# Test Case 6: We can then use list_all_good_combinations_from_joint_join_pattern to find all the good combis for each of the split.
# But if our split doesn't exist then it's an oopsie and will be False.
# Stuff like "Actor/Target Split is Bad, and you should feel bad"
# For example, the Joint Node allows 2 Actors and 2 Targets, but we're trying to put 3 Actors and 1 Target there.
grouping_split_tc6 = [{"actor_group":[alice], "target_group":[bob, charlie, daniel]}]
print("Test Case 6: Actor and Target Split doesn't work out here for the Cont or Join.")
validity = test_sg.check_joint_continuity_validity(joint_rule=if_x_then_v_cont, main_character=alice, grouping_split=grouping_split_tc6, insert_index=1, verbose=True)
print("Validity is", validity)
print()

#Test Case 7: Finally we can return Validity itself! As long as the joint/splits are valid (as in, they don't mess up the story continuity) then we can return True. Otherwise, it is false.
#Test Case 7.1: Valid Join

print("Test Case 7.1: Nothing wrong with this Join/Cont Rule. Return True.")
validity = test_sg_3.check_joint_continuity_validity(joint_rule=if_xy_then_z_join, main_character=alice, grouping_split=grouping_split_tc6, insert_index=1, verbose=True)
print("Validity is", validity)
print()

#Test Case 7.2: Invalid Join
print("Test Case 7.2: Alice can't be in this Joint because she has a banned tag. Need to return False.")
validity = test_sg_3.check_joint_continuity_validity(joint_rule=if_xy_then_w_join, main_character=alice, grouping_split=grouping_split_tc6, insert_index=1, verbose=True)
print("Validity is", validity)
print()

#Test Case 7.3: Valid Splits
print("Test Case 7.3: Nothing wrong with this Split Rule. Return True.")
grouping_split_tc7 = [{"actor_group":[alice], "target_group":[]}, {"actor_group":[bob, charlie, daniel], "target_group":[]}]
validity = test_sg.check_joint_continuity_validity(joint_rule=if_x_then_split_into_yz_split, main_character=alice, grouping_split=grouping_split_tc7, insert_index=1, verbose=True)
print("Validity is", validity)
print()

#Test Case 7.4: Invalid Splits
# Actually, this would fall into Invalid Splits in 7.4. We don't need a new specific case to handle this.
print("Test Case 7.4: They want to put Alice in a node that she can't be in. Need to return False.")
validity = test_sg.check_joint_continuity_validity(joint_rule=if_x_then_split_into_wz_split, main_character=alice, grouping_split=grouping_split_tc7, insert_index=1, verbose=True)
print("Validity is", validity)
print()