#We will make a few storygraphs to test the function where we calculate the score from the rules.
#Character for all cases: Alice
#Case 1: Normal rule, no purging (A(BC)D -> A(BCEF)D (If BC then append EF))
#Case 2: Normal rule with purging (A(BC)D -> A(EF)D (If BC then purge and append EF))

#For these cases, we will introduce Bob, who is going to be waiting and will perform C at the same step where Alice is.
#Case 3: JoiningJointRule (AB(C) -> AB(CX) (If there is someone doing C, then all of them can do X))
#Case 4: ContJointRule (ABC(X) -> ABC(XY), (Cont X with XY))
#Case 5: SplitJointRule (ABCX(Y) -> ABCX(YG, YH) (Cont Y with G and H, for two different characters. Value for Alice is max between G and H.))

from components.StoryObjects import LocationNode, CharacterNode
from components.StoryNode import StoryNode
from components.WorldState import WorldState
from components.StoryGraphTwoWS import StoryGraph
from components.RewriteRuleWithWorldState import *
from components.RelChange import RelChange, TagChange
from components.UtilityEnums import *

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
node_f = StoryNode(name="Node F", biasweight=1, tags= {"Type":"Placeholder"}, charcount=1, suggested_included_tags=[("Job","Swordmaster")], suggested_excluded_tags=[("Wanted","Theft")], suggested_bias_range={"lawbias":(0,100), "moralbias":(30,100)})

#Alice should be able to proc up all the checks in the suggested includes in Node F, which means Node E will add 3 to the score and Node F will add 5 to the score. For both Case 1 and Case 2, Max Mode should return 5, and Avg Mode should return 4.

#The following nodes are going to be used in Joint Rules, because they may allow more than one characters to partake.
node_x = StoryNode(name="Node X", biasweight=1, tags={"Type":"Placeholder"}, charcount=2, suggested_included_tags=[("Job","Swordmaster"), ("Job","Warrior"), ("Job","Fighter")])
node_y = StoryNode(name="Node Y", biasweight=1, tags={"Type":"Placeholder"}, charcount=2, suggested_included_tags=[("Wealth","Average"), ("Living",True), ("Job","Fighter")])

#These two are for splits. Max between these should be 3. Average between these should be 2.5.
node_g = StoryNode(name="Node G", biasweight=1, tags={"Type":"Placeholder"}, charcount=1, suggested_included_tags=[("Job","Swordmaster")])
node_h = StoryNode(name="Node H", biasweight=1, tags={"Type":"Placeholder"}, charcount=3, suggested_included_tags=[("Job","Cook")])

#Okay, here are rules.
rule_1 = RewriteRule(story_condition=[node_b, node_c], story_change=[node_e, node_f], remove_before_insert=False)
rule_2 = RewriteRule(story_condition=[node_b, node_c], story_change=[node_e, node_f], remove_before_insert=True)

#Then, the joint rules.
rule_3 = JoiningJointRule(base_actions=[node_c], joint_node=node_x)
rule_4 = ContinuousJointRule(base_joint=node_x, joint_node=node_y)
rule_5 = SplittingJointRule(base_joint=node_x, split_list=[node_g, node_h])

graph_1 = StoryGraph("Graph 1", [alice, bob], [somewhere], default_ws)
graph_1.insert_multiple_parts([node_a, node_b, node_c, node_d], alice, [somewhere, somewhere, somewhere, somewhere], 0)

# graph_1.apply_rewrite_rule(rule=rule_1, character=alice)
# for thing in graph_1.make_story_part_list_of_one_character(character_to_extract=alice):
#     print(thing)

#Need to change the logic of apply rewrite rule in cases where there's no purging, so that we append the new nodes *after* the pattern we want instead of before.
print("Graph 1 Rule 1 Index 1 Mode 0 (Expect 5)", graph_1.calculate_score_from_rule_char_and_cont(actor=alice, insert_index=1, rule=rule_1, mode=0))
print("Graph 1 Rule 1 Index 1 Mode 1 (Expect 4)", graph_1.calculate_score_from_rule_char_and_cont(actor=alice, insert_index=1, rule=rule_1, mode=1))
print("Graph 1 Rule 2 Index 1 Mode 0 (Expect 4)", graph_1.calculate_score_from_rule_char_and_cont(actor=alice, insert_index=1, rule=rule_2, mode=0))
print("Graph 1 Rule 2 Index 1 Mode 1 (Expect 3.5)", graph_1.calculate_score_from_rule_char_and_cont(actor=alice, insert_index=1, rule=rule_2, mode=1))

#TODO: Continue testing the Joint Rules