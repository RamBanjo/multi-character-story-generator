from datetime import datetime
import os
import sys
sys.path.insert(0,'')

from application.components.StoryObjects import *
from application.components.WorldState import *
from application.components.CharacterTask import *
from application.components.StoryGraphTwoWS import *
from application.components.StoryNode import *
from application.components.RelChange import *
from application.components.UtilityEnums import *
from application.components.RewriteRuleWithWorldState import *
from application.components.StoryMetrics import *

from application.StoryGeneration_NewFlowchart_WithMetrics import generate_story_from_starter_graph, make_base_graph_from_previous_graph, generate_multiple_graphs, attempt_move_towards_task_loc

alice = CharacterNode(name="Alice", internal_id=0)

hub = LocationNode(name="Hub", internal_id=10)

#Alice can do two types of actions: Take a W and Take an L. Taking a W is a Main Character Action.

take_w = StoryNode(name="Take a W", tags={"Type":"Action", "important_action":True})
take_l = StoryNode(name="Take an L", tags={"Type":"Action", "important_action":False})

tiny_ws = WorldState(name="Really Small WS", objectnodes=[alice, hub])
tiny_ws.connect(from_node=hub, edge_name="holds", to_node=alice)

init_graph = StoryGraph(name="Initial Graph", character_objects=[alice], starting_ws=tiny_ws)

patternless_into_taking_w = RewriteRule(story_condition=[], story_change=[take_w], name="Patternless Take W")
patternless_into_taking_l = RewriteRule(story_condition=[], story_change=[take_l], name="Patternless Take L")

alice_main_character_more_than_50 = StoryMetric(metric_type=MetricType.PREFER, value=50, metric_mode=MetricMode.HIGHER, character_object=alice)

retention = 1

init_graph.insert_story_part(part=take_l, character=alice, location=hub, absolute_step=0)
init_graph.insert_story_part(part=take_l, character=alice, location=hub, absolute_step=1)
init_graph.insert_story_part(part=take_l, character=alice, location=hub, absolute_step=2)

test_result = init_graph.test_if_given_node_list_will_follow_metric_rule(metric=alice_main_character_more_than_50, node_list=[take_l], step=3, verbose=True)
pass_metric_test = test_result[0]
distance_from_new_value_to_goal = test_result[1]
distance_from_worst_case_to_goal = abs(test_result[2] - alice_main_character_more_than_50.value)
goal_distance_ratio  = float(distance_from_new_value_to_goal) / float(distance_from_worst_case_to_goal)
print(goal_distance_ratio)

# print(init_graph.test_if_given_node_list_will_follow_metric_rule(metric=alice_main_character_more_than_50, node_list=[take_l], step=3, verbose=True))

test_result = init_graph.test_if_given_node_list_will_follow_metric_rule(metric=alice_main_character_more_than_50, node_list=[take_w], step=3, verbose=True)
pass_metric_test = test_result[0]
distance_from_new_value_to_goal = test_result[1]
distance_from_worst_case_to_goal = abs(test_result[2] - alice_main_character_more_than_50.value)
goal_distance_ratio  = float(distance_from_new_value_to_goal) / float(distance_from_worst_case_to_goal)
print(goal_distance_ratio)
# print(init_graph.test_if_given_node_list_will_follow_metric_rule(metric=alice_main_character_more_than_50, node_list=[take_w], step=3, verbose=True))

# start_gen_time = datetime.now()
# generated_graph_list = generate_multiple_graphs(initial_graph=init_graph, list_of_rules=[patternless_into_taking_l, patternless_into_taking_w], metric_requirements=[alice_main_character_more_than_50], required_story_length=25, max_storynodes_per_graph=5, metric_retention=retention, verbose=True)

# finish_gen_time = datetime.now()

# print("xxx")
# print("Generation Time:", str(finish_gen_time-start_gen_time))

# base_folder_name = "Alice Taking Ws and Ls"
# base_directory = "application/tests/test_output/"

# graphcounter = 1

# for generated_graph in generated_graph_list:
#     print("Cycle Number:", str(graphcounter))
#     fullpath = base_directory + base_folder_name + "/" + str(graphcounter) + "/"
#     metric_path = fullpath + "/metrics/"

#     if not os.path.exists(fullpath):
#         os.makedirs(fullpath)
#     if not os.path.exists(metric_path):
#         os.makedirs(metric_path)

#     generated_graph.print_graph_nodes_to_text_file(directory=fullpath, verbose=True)
#     generated_graph.print_metric_of_each_character_to_text_file(directory=metric_path, previous_graphs=generated_graph_list[:graphcounter-1], verbose=True, retention=retention)
#     latest_ws = generated_graph.make_latest_state()
#     latest_ws.print_wsedges_to_text_file(directory=fullpath, verbose=True)

#     graphcounter += 1

# fullpath = base_directory + base_folder_name + "/final_metrics_retention_1/"
# if not os.path.exists(fullpath):
#     os.makedirs(fullpath)
# generated_graph_list[-1].print_metric_of_each_character_to_text_file(directory=fullpath, previous_graphs=generated_graph_list[:-1], verbose=True, retention=1, include_true_uniqueness = True)

# fullpath = base_directory + base_folder_name + "/final_metrics_retention_based_on_graph/"
# if not os.path.exists(fullpath):
#     os.makedirs(fullpath)
# generated_graph_list[-1].print_metric_of_each_character_to_text_file(directory=fullpath, previous_graphs=generated_graph_list[:-1], verbose=True, retention=retention, include_true_uniqueness = True)

# print("Generation Complete! Yippee!!")
