# Testing the Main Function. Here are the things we need to test:

# 1. Testing if replacement rules are recognized. (COMPLETED!)
# Graph starts with A-B-C. We have rules that say B -> DE and C -> FG. If we make the graph continue generating until the shortest path length of 5 is reached we would get ADEFG.
# There are also invalid rules that the main character can't do. We want to make sure the program is able to ignore those as well. B -> Bad_1 and C -> Bad_2 are invalid because those nodes are invalid for the character.
#
# 2. Testing if task is recognized. (COMPLETED!)
# Graph starts with A-B-C, where A contains a TaskChange Object. The task consists of two steps, each step has 1 action: Action D and Action E.
# ...performing the task would potentially put you in a different location. What if B or C travels to another node? Would doing a chart break that? I don't like the sound of this.
# I mean, it *would* make the option invalid at least if we put the proper requirements in the traveling nodes...
#
# 3. Testing if joint rules are recognized. (COMPLETED!)
# Graph starts with A-B-C for two characters. There is a rule where C -> Joint Node X, Joint Node X -> Joint Node Y, and Joint Node Y -> D or E. Both characters should have the same chart.
#
# 4. Testing if scores are recognized
# Graph is A-B-C. There are 10 rules, each trying to continue C with 10 different nodes. If the scores are properly recognized, we would be able to get Top 5 only.
#
# 5. Testing if task locations are recognized
# Graph is A-B-C. Player gets a Task Stack with only one task in Location X, but they are currently in Location Z. They must travel from Z to Y and then X to do that task.
#
# 6. Like a ReGEN
# Rules, characters, and objects are based of ReGEN. There are two main characters, Alice and Bob.
# All the rules specify that they can only be done by Main Characters, so other characters will do a lot of waiting.
import sys
sys.path.insert(0,'')

from application.StoryGeneration_NewFlowchart import attempt_apply_rule, generate_story_from_starter_graph
from application.components.CharacterTask import CharacterTask, TaskStack
from application.components.ConditionTest import HasEdgeTest, HasTagTest, InBiasRangeTest, SameLocationTest
from application.components.RelChange import RelChange, TagChange, TaskChange
from application.components.RewriteRuleWithWorldState import *
from application.components.StoryGraphTwoWS import StoryGraph
from application.components.StoryNode import StoryNode
from application.components.StoryObjects import CharacterNode, LocationNode, ObjectNode
from application.components.UtilityEnums import ChangeAction, GenericObjectNode
from application.components.WorldState import WorldState

node_a = StoryNode(name="Node A")
node_b = StoryNode(name="Node B")
node_c = StoryNode(name="Node C")
node_d = StoryNode(name="Node D")
node_e = StoryNode(name="Node E")
node_f = StoryNode(name="Node F")
node_g = StoryNode(name="Node G")

not_warrior_tag = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Job", value="Warrior", inverse=True)
bad_1 = StoryNode(name="Bad_1", required_test_list=[not_warrior_tag])
bad_2 = StoryNode(name="Bad_2", required_test_list=[not_warrior_tag])

alice = CharacterNode(name="Alice", tags={"Type":"Character", "Job":"Warrior", "Alive":True})
bob = CharacterNode(name="Bob", tags={"Type":"Character", "Job":"Fighter", "Alive":True})
charlie = CharacterNode(name="Charlie", tags={"Type":"Character", "Job":"Bard", "Alive":True})
town = LocationNode(name = "Town")

#Test 1: Recognization of Replacement Rules
# Graph starts with A-B-C. We have rules that say B -> DE and C -> FG. If we make the graph continue generating until the shortest path length of 5 is reached we would get ADEFG.

#BEGIN TEST 1
# state_1 = WorldState(name="State 1", objectnodes=[alice, town])
# state_1.connect(from_node=town, edge_name="holds", to_node=alice)

# graph_1 = StoryGraph(name="Graph 1", character_objects=[alice], location_objects=[town], starting_ws = state_1)

# graph_1.insert_multiple_parts(part_list=[node_a, node_b, node_c], character=alice, location_list=[town, town, town])

# # for part in graph_1.story_parts.values():
# #     print(part.name)
# #     print("prev",part.previous_nodes)
# #     print("next",part.next_nodes)
# #     print("-----")

# rule_b_to_de = RewriteRule(name="b->de",story_condition=[node_b], story_change=[node_d, node_e], remove_before_insert=True)
# rule_c_to_fg = RewriteRule(name="c->fg",story_condition=[node_c], story_change=[node_f, node_g], remove_before_insert=True)
# rule_b_to_bad1 = RewriteRule(name="b->bad1",story_condition=[node_b], story_change=[bad_1])
# rule_c_to_bad2 = RewriteRule(name="c->bad2",story_condition=[node_c], story_change=[bad_2])

# # graph_1.print_all_node_beautiful_format()
# # graph_1.refresh_longest_path_length()
# # print(graph_1.get_longest_path_length_by_character(character=alice))
# # print(graph_1.get_latest_story_node_from_character(character=alice))

# graph_1_modded = generate_story_from_starter_graph(init_storygraph=graph_1, list_of_rules=[rule_b_to_bad1, rule_b_to_de, rule_c_to_bad2, rule_c_to_fg], required_story_length=5, top_n=5, extra_attempts=-1, verbose=True)

# print("We expect the story following Story Graph to contain the following nodes for Alice: A-D-E-F-G.")
# graph_1_modded.print_all_node_beautiful_format()
#END TEST 1

#Test 2: Recognition of Tasks
#

#BEGIN TEST 2

# reward = ObjectNode(name="Reward", tags={"Type":"Object", "Value":"Expensive"})

# target_is_alive = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Alive", value=True)
# target_dies = TagChange(name="Target Dies",object_node_name=GenericObjectNode.GENERIC_TARGET, tag="Alive", value=False, add_or_remove=ChangeAction.ADD)

# task_giver_holds_reward = HasEdgeTest(object_from_test=GenericObjectNode.TASK_GIVER, edge_name_test="holds", object_to_test=reward, soft_equal=True)
# bob_holds_reward = HasEdgeTest(object_from_test=bob, edge_name_test="holds", object_to_test=reward, soft_equal=True)

# task_giver_and_owner_share_loc = SameLocationTest(list_to_test=[GenericObjectNode.TASK_GIVER, GenericObjectNode.TASK_OWNER])
# task_giver_loses_reward = RelChange(name="Task Giver Lose Reward", node_a=GenericObjectNode.TASK_GIVER, edge_name="holds", node_b=reward, value=None,add_or_remove=ChangeAction.REMOVE, soft_equal=True)
# task_owner_gets_reward = RelChange(name="Task Owner Gets Reward", node_a=GenericObjectNode.TASK_OWNER, edge_name="holds", node_b=reward, value=None,add_or_remove=ChangeAction.ADD)

# kill_target = StoryNode(name="Kill Target", actor=[GenericObjectNode.TASK_OWNER],target=["kill_target"],required_test_list=[target_is_alive], effects_on_next_ws=[target_dies], charcount=1, target_count=1)
# get_reward = StoryNode(name="Get Reward", actor=[GenericObjectNode.TASK_GIVER, GenericObjectNode.TASK_OWNER], effects_on_next_ws=[task_giver_loses_reward, task_owner_gets_reward], required_test_list=[task_giver_holds_reward, task_giver_and_owner_share_loc], charcount=1, target_count=1)

# task_giver_hates_kill_target = HasEdgeTest(object_from_test=GenericObjectNode.TASK_GIVER, edge_name_test="hates", object_to_test="kill_target")

# kill_target_task = CharacterTask(task_name="Kill Target Task", task_actions=[kill_target], task_location_name="Town", actor_placeholder_string_list=["kill_target"])
# get_reward_task = CharacterTask(task_name="Get Reward Task", task_actions=[get_reward], task_location_name="Town")
# kill_target_task_stack = TaskStack(stack_name="Kill and Get Rewarded", task_stack=[kill_target_task, get_reward_task], task_stack_requirement=[task_giver_hates_kill_target], stack_giver_name=GenericObjectNode.GENERIC_ACTOR, stack_owner_name=GenericObjectNode.GENERIC_TARGET)

# get_kill_target_task_stack = TaskChange(name="Get Task", task_giver_name=GenericObjectNode.GENERIC_ACTOR, task_owner_name=GenericObjectNode.GENERIC_TARGET, task_stack=kill_target_task_stack)

# get_task = StoryNode(name="Get Task", effects_on_next_ws=[get_kill_target_task_stack], charcount=1, target_count=1)
# node_b = StoryNode(name="Node B")
# node_c = StoryNode(name="Node C")
# node_x = StoryNode(name="Node X")

# state_2 = WorldState(name="State 2", objectnodes=[alice, bob, charlie, reward, town])
# state_2.connect(from_node=town, edge_name="holds", to_node=alice)
# state_2.connect(from_node=town, edge_name="holds", to_node=bob)
# state_2.connect(from_node=town, edge_name="holds", to_node=charlie)

# state_2.connect(from_node=bob, edge_name="hates", to_node=charlie)
# state_2.connect(from_node=bob, edge_name="holds", to_node=reward)

# print(state_2.check_connection(node_a=bob, node_b=reward, edge_name="holds", edge_value=None, soft_equal=True))

# sg2 = StoryGraph(name="Graph 2", character_objects=[alice, bob, charlie], location_objects=[town], starting_ws = state_2)

# sg2.insert_joint_node(joint_node=get_task, main_actor=bob, targets=[alice])
# sg2.insert_multiple_parts(part_list=[node_b, node_c], character=alice, location_list=[town, town], absolute_step=1)
# sg2.insert_multiple_parts(part_list=[node_x, node_x, node_x], character=bob, location_list=[town, town, town], absolute_step=1)

# sg2.insert_multiple_parts(part_list=[node_d, node_e, node_f, node_g], character=charlie, location_list=[town, town, town, town])

# sg2.refresh_longest_path_length()


# TODO (Extra Features): Since we have found out that there are some cases where a task is assigned but it isn't possible to do or cancel, we would need a way to prevent that from happening.
# What sort of Error Handling can we do to prevent that? For now, let's sanitize our inputs to make sure that doesn't happen.

# print("---")
# sg2.print_all_nodes_from_characters_storyline_beautiful_format(alice)
# print("---")
# sg2.print_all_nodes_from_characters_storyline_beautiful_format(bob)
# print("---")
# sg2.print_all_nodes_from_characters_storyline_beautiful_format(charlie)
# print("---")

# print(sg2.attempt_advance_task_stack(task_stack_name="Kill and Get Rewarded", actor_name="Alice", abs_step=2, verbose=True))
# print(sg2.attempt_advance_task_stack(task_stack_name="Kill and Get Rewarded", actor_name="Alice", abs_step=3, verbose=True))
# print(sg2.attempt_advance_task_stack(task_stack_name="Kill and Get Rewarded", actor_name="Alice", abs_step=4, verbose=True))

# graph_2_modded = generate_story_from_starter_graph(init_storygraph=sg2, list_of_rules=[], required_story_length=5, top_n=5, extra_attempts=-1, verbose=True)

# print("---")
# graph_2_modded.print_all_nodes_from_characters_storyline_beautiful_format(alice)
# print("---")
# graph_2_modded.print_all_nodes_from_characters_storyline_beautiful_format(bob)
# print("---")
# graph_2_modded.print_all_nodes_from_characters_storyline_beautiful_format(charlie)
# print("---")
# END TEST 2

# Test 3: Recognition of Joint Rules (all three types)
# BEGIN TEST 3
# Graph starts with A-B-C for two characters. There is a rule where C -> Joint Node X, Joint Node X -> Joint Node Y, and Joint Node Y -> D or E. Both characters should have the same chart.

# state_3 = WorldState("Test State 3", objectnodes=[alice, bob, town])
# state_3.connect(from_node=town, edge_name="holds", to_node=alice)
# state_3.connect(from_node=town, edge_name="holds", to_node=bob)

# sg3 = StoryGraph(name="Graph 3", character_objects=[alice, bob], location_objects=[town], starting_ws=state_3)

# node_a = StoryNode(name="Node A")
# node_b = StoryNode(name="Node B")
# node_c = StoryNode(name="Node C")
# node_d = StoryNode(name="Node D", biasweight=30)
# node_e = StoryNode(name="Node E", biasweight=40)

# joint_x = StoryNode(name="Joint X", charcount=2, biasweight=10)
# joint_y = StoryNode(name="Joint Y", charcount=2, biasweight=20)

# rule_c_to_x = JoiningJointRule(base_actions=[node_c], joint_node=joint_x, rule_name="c->x")
# rule_x_to_y = ContinuousJointRule(base_joint=joint_x, joint_node=joint_y, rule_name="x->y")
# rule_y_to_de = SplittingJointRule(base_joint=joint_y, split_list=[node_d, node_e], rule_name="y->de")

# sg3.insert_multiple_parts(part_list=[node_a, node_b, node_c], character=alice, location_list=[town, town, town])
# sg3.insert_multiple_parts(part_list=[node_a, node_b, node_c], character=bob, location_list=[town, town, town])

# sg3_modded = generate_story_from_starter_graph(init_storygraph=sg3, list_of_rules=[rule_c_to_x, rule_x_to_y, rule_y_to_de], required_story_length=6, top_n=5, extra_attempts=-1, verbose=True)
# sg3_modded.print_all_node_beautiful_format()
# TEST 3 END

# BEGIN TEST 4

# alex = CharacterNode(name="Alex", biases={"lawbias":50, "moralbias":50}, tags={"Job":"Warrior"})

# #base_node that can be continued from
# node_x = StoryNode(name="Node X")

# #No Test, these should be straightforward
# scored_node_a = StoryNode(name="Node A", biasweight=1)
# scored_node_b = StoryNode(name="Node B", biasweight=10)
# scored_node_c = StoryNode(name="Node C", biasweight=30)
# scored_node_d = StoryNode(name="Node D", biasweight=50)
# scored_node_e = StoryNode(name="Node E", biasweight=100)

#Contains Suggested Tests, which means the score will be based on how many tests our main character passses.
#Be sure to put in a cluster of tag test and bias tests as well
# is_warrior = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Job", value="Warrior", score=10)
# non_negative_law_bias = InBiasRangeTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, bias_axis="lawbias", min_accept=0, max_accept=100, score=20)
# greater_than_30_moral_bias = InBiasRangeTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, bias_axis="moralbias", min_accept=30, max_accept=100, score=40)
# is_swordfighter = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Job", value="Swordfighter", score=1000)

# scored_node_f = StoryNode(name="Node F", biasweight=0, suggested_test_list=[is_warrior])
# scored_node_g = StoryNode(name="Node G", biasweight=0, suggested_test_list=[non_negative_law_bias])
# scored_node_h = StoryNode(name="Node H", biasweight=0, suggested_test_list=[greater_than_30_moral_bias])
# scored_node_i = StoryNode(name="Node I", biasweight=0, suggested_test_list=[is_warrior, non_negative_law_bias, is_swordfighter])
# scored_node_j = StoryNode(name="Node J", biasweight=0, suggested_test_list=[is_swordfighter])


# rule_xa = RewriteRule(story_condition=[node_x], story_change=[scored_node_a], name="x->a", remove_before_insert=True)
# rule_xb = RewriteRule(story_condition=[node_x], story_change=[scored_node_b], name="x->b", remove_before_insert=True)
# rule_xc = RewriteRule(story_condition=[node_x], story_change=[scored_node_c], name="x->c", remove_before_insert=True)
# rule_xd = RewriteRule(story_condition=[node_x], story_change=[scored_node_d], name="x->d", remove_before_insert=True)
# rule_xe = RewriteRule(story_condition=[node_x], story_change=[scored_node_e], name="x->e", remove_before_insert=True)
# rule_xf = RewriteRule(story_condition=[node_x], story_change=[scored_node_f], name="x->f", remove_before_insert=True)
# rule_xg = RewriteRule(story_condition=[node_x], story_change=[scored_node_g], name="x->g", remove_before_insert=True)
# rule_xh = RewriteRule(story_condition=[node_x], story_change=[scored_node_h], name="x->h", remove_before_insert=True)
# rule_xi = RewriteRule(story_condition=[node_x], story_change=[scored_node_i], name="x->i", remove_before_insert=True)
# rule_xj = RewriteRule(story_condition=[node_x], story_change=[scored_node_j], name="x->j", remove_before_insert=True)
# rule_list = [rule_xa, rule_xb, rule_xc, rule_xd, rule_xe, rule_xf, rule_xg, rule_xh, rule_xi, rule_xj]

#Theoratically, the top 5 of these 10 rules should be:
# scored node e: 100 points
# scored node i: 70 points
# scored node d: 50 points
# scored node h: 30 points
# scored node c: 30 points

# ws4 = WorldState(name="World State 4", objectnodes=[alex, town])
# ws4.connect(from_node=town, edge_name="holds", to_node=alex)

# sg4 = StoryGraph(name="Graph 4", character_objects=[alex], location_objects=[town], starting_ws=ws4)
# sg4.add_story_part(part=node_x, character=alex, location=town)

# modded_sg4 = generate_story_from_starter_graph(init_storygraph=sg4, list_of_rules=rule_list, required_story_length=2, top_n=5, verbose=True)

#TEST 4 COMPLETE
#Begin Test 5

#Recognition of Task Locations...it's been a while.

town_a = LocationNode("Town A")
town_b = LocationNode("Town B")
town_c = LocationNode("Town C")

ws5 = WorldState(name="World State", objectnodes=[alice, bob, charlie, town_a, town_b, town_c])

ws5.doubleconnect(nodeA=town_a, edge_name="connects", nodeB=town_b)
ws5.doubleconnect(nodeA=town_b, edge_name="connects", nodeB=town_c)
ws5.connect(from_node=town_a, edge_name="holds", to_node=alice)
ws5.connect(from_node=town_a, edge_name="holds", to_node=bob)
ws5.connect(from_node=town_c, edge_name="holds", to_node=charlie)

share_loc_charlie = SameLocationTest(list_to_test=[GenericObjectNode.TASK_OWNER, charlie])
talk_to_charlie = StoryNode(name="Talk to Charlie", charcount=1, target_count=1, actor=[GenericObjectNode.TASK_OWNER], target=[charlie], required_test_list=[share_loc_charlie])

talk_to_charlie_task = CharacterTask(task_name="Talk to Charlie", task_actions=[talk_to_charlie], task_location_name="Town C")
talk_to_charlie_stack = TaskStack(stack_name="Just Talk to Charlie, Bro", task_stack=[talk_to_charlie_task])

add_talk_charlie_stack = TaskChange(name="Add Talk Charlie Stack", task_giver_name=GenericObjectNode.GENERIC_ACTOR, task_owner_name=GenericObjectNode.GENERIC_TARGET, task_stack=talk_to_charlie_stack)

give_task = StoryNode(name="Give Task", charcount=1, target_count=1, effects_on_next_ws=[add_talk_charlie_stack])

sg5 = StoryGraph(name="Story Graph 5", character_objects=[alice, bob, charlie], location_objects=[town_a, town_b, town_c], starting_ws=ws5)

sg5.insert_joint_node(joint_node=give_task, main_actor=bob, location=town_a, targets=[alice])
sg5.add_story_part(part=node_a, character=charlie, location=town_c)

modded_sg5 = generate_story_from_starter_graph(init_storygraph=sg5, list_of_rules=[], required_story_length=5, verbose=True)

modded_sg5.print_all_node_beautiful_format()
latest_state = modded_sg5.make_latest_state()

print(latest_state.get_actor_current_location(alice))
# Greek Salad
# (Doesn't have to have the same name btw)
# Characters
# - Hercules
# - Sisyphus
# - Zeus
# - Achilles
# - Outis
# - Loki