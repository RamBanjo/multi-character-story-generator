#We will make a few storygraphs to test the function where we calculate the score from the rules.
#Character for all cases: Alice
#Case 1: Normal rule, no purging (A(BC)D -> A(BCEF)D (If BC then append EF))
#Case 2: Normal rule with purging (A(BC)D -> A(EF)D (If BC then purge and append EF))

#For these cases, we will introduce Bob, who is going to be waiting and will perform C at the same step where Alice is.
#Case 3: JoiningJointRule (AB(C) -> AB(CX) (If there is someone doing C, then all of them can do X))
#Case 4: ContJointRule (ABC(X) -> ABC(XY), (Cont X with XY))
#Case 5: SplitJointRule (ABCX(Y) -> ABCX(YG, YH) (Cont Y with G and H, for two different characters. Value for Alice is max between G and H.))

#If this isn't broken, we should be able to substitute all the conditions in the story nodes with the equivalent test objects and be done with this file.
import sys
sys.path.insert(0,'')

from application.components.ConditionTest import HasTagTest, InBiasRangeTest
from application.components.StoryObjects import LocationNode, CharacterNode
from application.components.StoryNode import StoryNode
from application.components.WorldState import WorldState
from application.components.StoryGraphTwoWS import StoryGraph
from application.components.RewriteRuleWithWorldState import *
from application.components.RelChange import RelChange, TagChange
from application.components.UtilityEnums import *

alice = CharacterNode("Alice", biases={"lawbias": 20, "moralbias":50}, tags={"Type":"Character", "Job":"Swordmaster", "Wealth":"Average"})
bob = CharacterNode("Bob", biases={"lawbias": 0, "moralbias":40}, tags={"Type":"Character", "Job":"Fighter", "Wealth":"Poor"})

somewhere = LocationNode("Somewhere")

default_ws = WorldState("Default WS", [alice, bob, somewhere])
default_ws.connect(from_node=somewhere, edge_name=default_ws.DEFAULT_HOLD_EDGE_NAME, to_node=alice)
default_ws.connect(from_node=somewhere, edge_name=default_ws.DEFAULT_HOLD_EDGE_NAME, to_node=bob)

#These nodes are for testing all cases. They are one character nodes.
DEFAULT_WAIT_NODE = StoryNode(name="Wait", biasweight=0, tags= {"Type":"Placeholder"}, charcount=1)

#Node A and Node B will add tags which makes Node E have more score than Node F, while C and D will remove it. If Purging works correctly, then we can expect to see the score for Node E for Rule 2 if purging works correctly.
node_a = StoryNode(name="Node A", biasweight=1, tags= {"Type":"Placeholder"}, charcount=1, effects_on_next_ws=[TagChange(name="Actor Becomes Wanted", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="Wanted", value="Theft", add_or_remove=ChangeAction.ADD)])
node_b = StoryNode(name="Node B", biasweight=1, tags= {"Type":"Placeholder"}, charcount=1)
node_c = StoryNode(name="Node C", biasweight=1, tags= {"Type":"Placeholder"}, charcount=1, effects_on_next_ws=[TagChange(name="Actor No Longer Wanted", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="Wanted", value="Theft", add_or_remove=ChangeAction.REMOVE)])
node_d = StoryNode(name="Node D", biasweight=1, tags= {"Type":"Placeholder"}, charcount=1)
node_e = StoryNode(name="Node E", biasweight=3, tags= {"Type":"Placeholder"}, charcount=1) 

is_swordmaster = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Job", value="Swordmaster")
is_swordmaster_target = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Job", value="Swordmaster")
not_swordmaster = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Job", value="Swordmaster", inverse=True)
not_swordmaster_target = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Job", value="Swordmaster", inverse=True)
is_warrior = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Job", value="Warrior")
is_fighter = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Job", value="Fighter")
is_fighter_target = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Job", value="Fighter")
is_cook = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Job", value="Cook")
average_wealth_target = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Wealth", value="Average")

not_wanted_for_theft = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Wanted", value="Theft", inverse=True)
non_negative_law_bias = InBiasRangeTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, bias_axis="lawbias", min_accept=0, max_accept=100)
greater_than_30_moral_bias = InBiasRangeTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, bias_axis="moralbias", min_accept=30, max_accept=100)

node_f = StoryNode(name="Node F", biasweight=3, tags= {"Type":"Placeholder"}, charcount=1, required_test_list=[is_swordmaster, not_wanted_for_theft], suggested_test_list=[non_negative_law_bias, greater_than_30_moral_bias])

#Alice should be able to proc up all the checks in the suggested includes in Node F, which means Node E will add 3 to the score and Node F will add 5 to the score. For both Case 1 and Case 2, Max Mode should return 5, and Avg Mode should return 4.

#The following nodes are going to be used in Joint Rules, because they may allow more than one characters to partake.
node_x = StoryNode(name="Node X", biasweight=1, tags={"Type":"Placeholder"}, charcount=2, suggested_test_list=[is_swordmaster, is_warrior, is_fighter])
node_y = StoryNode(name="Node Y", biasweight=3, tags={"Type":"Placeholder"}, charcount=1, target_count=1, suggested_test_list=[average_wealth_target, is_fighter_target])
node_w = StoryNode(name="Node W", biasweight=5, tags={"Type":"Placeholder"}, charcount=1, target_count=1, required_test_list=[not_swordmaster_target])
node_z = StoryNode(name="Node Z", biasweight=4, tags={"Type":"Placeholder"}, charcount=1, target_count=1, required_test_list=[not_swordmaster_target])
node_v = StoryNode(name="Node V", biasweight=7, tags={"Type":"Placeholder"}, charcount=1, target_count=1, required_test_list=[not_swordmaster, not_swordmaster_target])

#These two are for splits. Max between these should be 3. Average between these should be 2.5.
node_g = StoryNode(name="Node G", biasweight=1, tags={"Type":"Placeholder"}, charcount=1, suggested_test_list=[is_swordmaster])
node_h = StoryNode(name="Node H", biasweight=1, tags={"Type":"Placeholder"}, charcount=3, suggested_test_list=[is_cook])

#Okay, here are rules.
rule_1 = RewriteRule(story_condition=[node_b, node_c], story_change=[node_e, node_f], remove_before_insert=False)
rule_2 = RewriteRule(story_condition=[node_b, node_c], story_change=[node_e, node_f], remove_before_insert=True)

#Then, the joint rules.
rule_3 = JoiningJointRule(base_actions=[node_c], joint_node=node_x)
rule_4 = ContinuousJointRule(base_joint=node_x, joint_node=node_y)
rule_4a = ContinuousJointRule(base_joint=node_x, joint_node=node_w)
rule_4b = ContinuousJointRule(base_joint=node_x, joint_node=node_z)
rule_4c = ContinuousJointRule(base_joint=node_x, joint_node=node_v)

rule_5 = SplittingJointRule(base_joint=node_x, split_list=[node_g, node_h])

graph_1 = StoryGraph("Graph 1", [alice, bob], [somewhere], default_ws)
graph_1.insert_multiple_parts([node_a, node_b, node_c, node_d], alice, [somewhere, somewhere, somewhere, somewhere], 0)

# graph_1.apply_rewrite_rule(rule=rule_1, character=alice)
# for thing in graph_1.make_story_part_list_of_one_character(character_to_extract=alice):
#     print(thing)

#Need to change the logic of apply rewrite rule in cases where there's no purging, so that we append the new nodes *after* the pattern we want instead of before.
print("Graph 1 Rule 1 Index 1 Mode 0 (Expect 5)", graph_1.calculate_score_from_rule_char_and_cont(actor=alice, insert_index=1, rule=rule_1, mode=0))
print("Graph 1 Rule 1 Index 1 Mode 1 (Expect 4)", graph_1.calculate_score_from_rule_char_and_cont(actor=alice, insert_index=1, rule=rule_1, mode=1))

#These two tests will return -999 because the step where Alice stops being wanted for Theft is no longer there. Node D requires that the actor is not wanted for Theft.
print("Graph 1 Rule 2 Index 1 Mode 0 (Expect -999)", graph_1.calculate_score_from_rule_char_and_cont(actor=alice, insert_index=1, rule=rule_2, mode=0))
print("Graph 1 Rule 2 Index 1 Mode 1 (Expect -999)", graph_1.calculate_score_from_rule_char_and_cont(actor=alice, insert_index=1, rule=rule_2, mode=1))

# #Continue testing the Joint Rules. Starting with the Joining Joint.
graph_2 = StoryGraph("Graph 2", [alice, bob], [somewhere], default_ws)
graph_2.insert_multiple_parts([node_a, node_b, node_c], alice, [somewhere, somewhere, somewhere], 0)
graph_2.insert_multiple_parts([node_a, node_b, node_c], bob, [somewhere, somewhere, somewhere], 0)

#graph_2.print_all_node_beautiful_format()


print("Graph 2 Rule 3 Index 2 Mode 0 (Expect 2)", graph_2.calculate_score_from_rule_char_and_cont(actor=alice, insert_index=2, rule=rule_3, mode=0))
print("Graph 2 Rule 3 Index 2 Mode 1 (Expect 1.5)", graph_2.calculate_score_from_rule_char_and_cont(actor=alice, insert_index=2, rule=rule_3, mode=1))

# print("")
# #Testing the Continuous Joint Rule.
graph_2.insert_joint_node(joint_node=node_x, main_actor=alice, other_actors=[bob], location=somewhere, absolute_step=3)
# for thing in graph_2.make_story_part_list_of_one_character(character_to_extract=alice):
#     print(thing)
# print("")

# Now that we have the proper graph state we will be able to test Continuous Joint Rule. However, this case is different from the last one because of the actor/target slot having different values for Alice.
# As Actor Alice would have 3 points but as Target Alice would have 4 points. Max Mode calculates this as 4 but Average Mode calculates this as 3.5.
print("Graph 2 Rule 4 Index 3 Mode 0 (Expect 4)", graph_2.calculate_score_from_rule_char_and_cont(actor=alice, insert_index=3, rule=rule_4, mode=0))
print("Graph 2 Rule 4 Index 3 Mode 1 (Expect 3.5)", graph_2.calculate_score_from_rule_char_and_cont(actor=alice, insert_index=3, rule=rule_4, mode=1))

# There may be cases where one of the slots or both slots are bad.

# One bad slot -> Choose the slot that isn't bad. Two bad slots -> Return -999.
print("Graph 2 Rule 4a Index 3 Mode 0 (Expect 5)", graph_2.calculate_score_from_rule_char_and_cont(actor=alice, insert_index=3, rule=rule_4a, mode=0))
print("Graph 2 Rule 4a Index 3 Mode 1 (Expect 5)", graph_2.calculate_score_from_rule_char_and_cont(actor=alice, insert_index=3, rule=rule_4a, mode=1))
print("Graph 2 Rule 4b Index 3 Mode 0 (Expect 4)", graph_2.calculate_score_from_rule_char_and_cont(actor=alice, insert_index=3, rule=rule_4b, mode=0))
print("Graph 2 Rule 4b Index 3 Mode 1 (Expect 4)", graph_2.calculate_score_from_rule_char_and_cont(actor=alice, insert_index=3, rule=rule_4b, mode=1))

#The two slots are pretty bad. We need to exclude both.
print("Graph 2 Rule 4c Index 3 Mode 0 (Expect -999)", graph_2.calculate_score_from_rule_char_and_cont(actor=alice, insert_index=3, rule=rule_4c, mode=0))
print("Graph 2 Rule 4c Index 3 Mode 1 (Expect -999)", graph_2.calculate_score_from_rule_char_and_cont(actor=alice, insert_index=3, rule=rule_4c, mode=1))

# #Finally, the Splits. We'll insert Node Y to prepare to accept Nodes G and H.
# print("")
# #Testing the Continuous Joint Rule.
graph_2.insert_joint_node(joint_node=node_y, main_actor=alice, other_actors=[bob], make_main_actor_a_target=True, location=somewhere, absolute_step=4)
# for thing in graph_2.make_story_part_list_of_one_character(character_to_extract=alice):
#     print(thing) #Please note that Alice won't show up in Node Y because she would be the Target there.
# print("")

print("Graph 2 Rule 5 Index 4 Mode 0 (Expect 2)", graph_2.calculate_score_from_rule_char_and_cont(actor=alice, insert_index=4, rule=rule_5, mode=0))
print("Graph 2 Rule 5 Index 4 Mode 1 (Expect 1.5)", graph_2.calculate_score_from_rule_char_and_cont(actor=alice, insert_index=4, rule=rule_5, mode=1))