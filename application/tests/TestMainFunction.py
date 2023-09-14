# Testing the Main Function. Here are the things we need to test:

# 1. Testing if replacement rules are recognized.
# Graph starts with A-B-C. We have rules that say B -> DE and C -> FG. If we make the graph continue generating until the shortest path length of 5 is reached we would get ADEFG.
# There are also invalid rules that the main character can't do. We want to make sure the program is able to ignore those as well. B -> Bad_1 and C -> Bad_2 are invalid because those nodes are invalid for the character.
#
# 2. Testing if task is recognized.
# Graph starts with A-B-C, where A contains a TaskChange Object. The task consists of two steps, each step has 1 action: Action D and Action E.
# ...performing the task would potentially put you in a different location. What if B or C travels to another node? Would doing a chart break that? I don't like the sound of this.
# I mean, it *would* make the option invalid at least if we put the proper requirements in the traveling nodes...
#
# 3. Testing if joint rules are recognized.
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
from application.components.ConditionTest import HasEdgeTest, HasTagTest, SameLocationTest
from application.components.RelChange import RelChange, TagChange, TaskChange
from application.components.RewriteRuleWithWorldState import RewriteRule
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

alice = CharacterNode(name="Alice", tags={"Type":"Character", "Job":"Warrior"})
bob = CharacterNode(name="Bob", tags={"Type":"Character", "Job":"Fighter"})
charlie = CharacterNode(name="Charlie", tags={"Type":"Character", "Job":"Bard"})
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

reward = ObjectNode(name="Reward", tags={"Type":"Object", "Value":"Expensive"})

target_is_alive = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Alive", value=True)
target_dies = TagChange(name="Target Dies",object_node_name=GenericObjectNode.GENERIC_TARGET, tag="Alive", value=False, add_or_remove=ChangeAction.ADD)

task_giver_holds_reward = HasEdgeTest(object_from_test=GenericObjectNode.TASK_GIVER, edge_name_test="holds", object_to_test=reward, soft_equal=True)
task_giver_and_owner_share_loc = SameLocationTest(list_to_test=[GenericObjectNode.TASK_GIVER, GenericObjectNode.TASK_OWNER])
task_giver_loses_reward = RelChange(name="Task Giver Lose Reward", node_a=GenericObjectNode.TASK_GIVER, edge_name="holds", node_b=reward, value=None,add_or_remove=ChangeAction.REMOVE, soft_equal=True)
task_owner_gets_reward = RelChange(name="Task Owner Gets Reward", node_a=GenericObjectNode.TASK_OWNER, edge_name="holds", node_b=reward, value=None,add_or_remove=ChangeAction.ADD)

kill_target = StoryNode(name="Kill Target", actor=[GenericObjectNode.TASK_OWNER],target=["kill_target"],required_test_list=[target_is_alive], effects_on_next_ws=[target_dies])
get_reward = StoryNode(name="Get Reward", actor=[GenericObjectNode.TASK_GIVER, GenericObjectNode.TASK_OWNER], effects_on_next_ws=[task_giver_holds_reward, task_owner_gets_reward], required_test_list=[task_giver_holds_reward, task_giver_and_owner_share_loc])

task_giver_hates_kill_target = HasEdgeTest(object_from_test=GenericObjectNode.TASK_GIVER, edge_name_test="hates", object_to_test="kill_target")

kill_target_task = CharacterTask(task_name="Kill Target Task", task_actions=[kill_target], task_location_name="Town", actor_placeholder_string_list=["kill_target"])
get_reward_task = CharacterTask(task_name="Get Reward Task", task_actions=[get_reward], task_location_name="Town")
kill_target_task_stack = TaskStack(stack_name="Kill and Get Rewarded", task_stack=[kill_target_task, get_reward_task], task_stack_requirement=[task_giver_hates_kill_target], stack_giver_name=GenericObjectNode.GENERIC_ACTOR, stack_owner_name=GenericObjectNode.GENERIC_TARGET)

get_kill_target_task_stack = TaskChange(name="Get Task", task_giver_name=GenericObjectNode.GENERIC_ACTOR, task_owner_name=GenericObjectNode.GENERIC_TARGET, task_stack=kill_target_task_stack)

get_task = StoryNode(name="Get Task", effects_on_next_ws=[get_kill_target_task_stack], charcount=1, target_count=1)
node_b = StoryNode(name="Node B")
node_c = StoryNode(name="Node C")
node_x = StoryNode(name="Node X")

state_2 = WorldState(name="State 2", objectnodes=[alice, bob, charlie, town])
state_2.connect(from_node=town, edge_name="holds", to_node=alice)
state_2.connect(from_node=town, edge_name="holds", to_node=bob)
state_2.connect(from_node=town, edge_name="holds", to_node=charlie)
state_2.connect(from_node=bob, edge_name="hates", to_node=charlie)

sg2 = StoryGraph(name="Graph 1", character_objects=[alice, bob, charlie], location_objects=[town], starting_ws = state_2)

sg2.insert_joint_node(joint_node=get_task, main_actor=bob, targets=[alice])
sg2.insert_multiple_parts(part_list=[node_b, node_c], character=alice, location_list=[town, town], absolute_step=1)
sg2.insert_multiple_parts(part_list=[node_x, node_x, node_x], character=bob, location_list=[town, town, town], absolute_step=1)

sg2.insert_multiple_parts(part_list=[node_x, node_x, node_x, node_x], character=charlie, location_list=[town, town, town, town])

sg2.print_all_node_beautiful_format()
#END TEST 2