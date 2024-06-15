from datetime import datetime
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

from application.StoryGeneration_NewFlowchart_WithMetrics import generate_multiple_graphs, generate_story_from_starter_graph, make_base_graph_from_previous_graph
import os

red = CharacterNode(name="Red", tags={"Type":"Character", "Age":"Child", "Alive":True}, internal_id=0)
wolf = CharacterNode(name="Wolf", biases={"moralbias":-50, "lawbias":-50}, tags={"Type":"Character", "Age":"Adult", "EatsChildren":True, "EatsNonChildren":True, "Alive":True, "CanKill":"Fangs"}, internal_id=1)
brick_pig = CharacterNode(name="Brick", biases={"moralbias":50, "lawbias":50}, tags={"Type":"Character", "Age":"Adult", "Pacifist":True, "Alive":True, "LikesTreasure":True, "OwnsForestHome":True}, internal_id=2)
grandma = CharacterNode(name="Grandma", biases={"moralbias":-50, "lawbias":0}, tags={"Type":"Character", "Age":"Adult", "Alive":True, "LikesKnowledge":True, "CanKill":"Knife"}, internal_id=3)

forest_village = LocationNode(name="Forest Village", tags={"Type":"Location"}, internal_id=15)
random_forest = LocationNode(name="Random Forest", tags={"Type":"Location", "PigHomeStanding":True, "BearHomeStanding":True, "WitchHomeStanding":True}, internal_id=20)
forest_path = LocationNode(name="Forest Path", tags={"Type":"Location"}, internal_id=21)
plains_village = LocationNode(name="Plains Village", tags={"Type":"Location"}, internal_id=22)
mountain_valley = LocationNode(name="Mountain Valley", tags={"Type":"Location"}, internal_id=24)
magic_temple = LocationNode(name="Magic Temple", tags={"Type":"Location"}, internal_id=26)

list_of_objects = [red, wolf, brick_pig, grandma, forest_village, random_forest, forest_path, plains_village, mountain_valley, magic_temple]

reds_world_state = WorldState(name="Test WS", objectnodes=list_of_objects)

reds_world_state.doubleconnect(from_node=forest_village, edge_name="connects", to_node=forest_path)
reds_world_state.doubleconnect(from_node=random_forest, edge_name="connects", to_node=forest_path)
reds_world_state.doubleconnect(from_node=plains_village, edge_name="connects", to_node=forest_path)
reds_world_state.doubleconnect(from_node=mountain_valley, edge_name="connects", to_node=forest_path)
reds_world_state.doubleconnect(from_node=mountain_valley, edge_name="connects", to_node=magic_temple)

reds_world_state.connect(from_node=plains_village, edge_name="holds", to_node=red)
reds_world_state.connect(from_node=forest_village, edge_name="holds", to_node=grandma)
reds_world_state.connect(from_node=forest_village, edge_name="holds", to_node=brick_pig)
reds_world_state.connect(from_node=forest_village, edge_name="holds", to_node=wolf)

def destroy_house_taskchanges(home_tag_name, homeowner_object):

    home_tag_destroy_change = TagChange(name="Destroy Someone's Home", object_node_name=GenericObjectNode.GENERIC_LOCATION, tag=home_tag_name, value=False, add_or_remove=ChangeAction.ADD)
    home_tag_destroyed_check = HasTagTest(object_to_test=forest_village, tag=home_tag_name, value=False)

    node_name = "Actor Destroys House" + homeowner_object.get_name()
    actor_destroys_house = StoryNode(name=node_name, actor=[GenericObjectNode.TASK_OWNER], tags={"Type":"Destruction", "costly":True}, required_test_list=[], effects_on_next_ws=[home_tag_destroy_change])

    destroy_home_task = CharacterTask(task_name="Destroy Home Task", task_actions=[actor_destroys_house], task_location_name="Forest Village", goal_state=[home_tag_destroyed_check])

    stackname = "Destroy Home Stack (" + home_tag_name + ")"
    destroy_home_stack = TaskStack(stack_name=stackname, task_stack=[destroy_home_task])
    destroy_home_taskchange = TaskChange(name="Destroy Home TaskChange", task_giver_name=GenericObjectNode.GENERIC_TARGET, task_owner_name=GenericObjectNode.GENERIC_TARGET, task_stack=destroy_home_stack)

    return destroy_home_taskchange

destroy_brickhouse_taskchange = destroy_house_taskchanges(home_tag_name="PigHomeStanding", homeowner_object=brick_pig)
report_scared_forest_memory_gain = TagChange(name="Report Scared Memory", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="ScaredForestReportMemory", value=True, add_or_remove=ChangeAction.ADD)
all_destroyhouse_taskchanges = [destroy_brickhouse_taskchange, report_scared_forest_memory_gain]

actor_has_no_reportscare_memory_check = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="ScaredForestReportMemory", value=True, inverse=True)
target_is_grandma = ObjectEqualityTest(object_list=[grandma, GenericObjectNode.GENERIC_TARGET])

report_scared_forest = StoryNode(name="Report Scared Forest Village", tags={"Type":"GiveTask"}, charcount=1, target_count=1, effects_on_next_ws=all_destroyhouse_taskchanges, biasweight=50, required_test_list=[actor_has_no_reportscare_memory_check, target_is_grandma])

initial_graph = StoryGraph(name="Initial Story Graph", character_objects=[red, wolf, brick_pig, grandma], starting_ws=reds_world_state)

patternless_into_report_scared_forest = JoiningJointRule(base_actions=None, joint_node=report_scared_forest, rule_name="Patternless into Report Scared Forest Village")

# print(initial_graph.calculate_score_from_rule_char_and_cont(actor=wolf, insert_index=0, rule=patternless_into_report_scared_forest))

initial_graph.insert_joint_node(joint_node=report_scared_forest.return_stripped_story_node(), main_actor=wolf)