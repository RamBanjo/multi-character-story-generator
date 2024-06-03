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

from application.StoryGeneration_NewFlowchart_WithMetrics import generate_multiple_graphs, generate_story_from_starter_graph, make_base_graph_from_previous_graph

papabear = CharacterNode(name="Papa Bear", tags={"Type":"Character", "Age":"Adult", "Alive":True, "CanKill":"Claws", "OwnsForestHome":True}, internal_id=8)
protection_pillar = ObjectNode(name="Protection Pillar", tags={"Type":"Object", "ProtectsHomes":True, "Active":False}, internal_id=12)

magic_temple = LocationNode(name="Magic Temple", tags={"Type":"Location", "Home":True, "Demolished":False}, internal_id=26)
bear_house = LocationNode(name="Bear House", tags={"Type":"Location", "Home":True, "Demolished":False}, internal_id=16)

list_of_objects = [papabear, protection_pillar, magic_temple, bear_house]
reds_world_state = WorldState(name="Reds World State", objectnodes=list_of_objects)

reds_world_state.connect(from_node=bear_house, edge_name="holds", to_node=papabear)
reds_world_state.doubleconnect(from_node=bear_house, edge_name="connects", to_node=magic_temple)
reds_world_state.connect(from_node=magic_temple, edge_name="holds", to_node=protection_pillar)
reds_world_state.connect(from_node=papabear, edge_name="owns", to_node=bear_house)

actor_shares_location_with_rod = SameLocationTest(list_to_test=[GenericObjectNode.GENERIC_ACTOR, protection_pillar])
rod_is_not_active_check = HasTagTest(object_to_test=protection_pillar, tag="Active", value=True, inverse=True)
actor_holds_rod = RelChange(name="Actor Hold Rod", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="holds", node_b=protection_pillar, add_or_remove=ChangeAction.ADD)
location_no_longer_holds_rod = RelChange(name="Location Stop Hold Rod", node_a=GenericObjectNode.GENERIC_LOCATION, edge_name="holds", node_b=protection_pillar, add_or_remove=ChangeAction.REMOVE)

take_rod = StoryNode(name="Take Rod", tags={"Type":"Find Rod"}, charcount=1, actor=[GenericObjectNode.TASK_OWNER], location = magic_temple, target=[protection_pillar], required_test_list=[rod_is_not_active_check, actor_shares_location_with_rod], effects_on_next_ws=[actor_holds_rod, location_no_longer_holds_rod])

actor_holds_rod_check = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="holds", object_to_test=protection_pillar)
actor_owns_home = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="owns", object_to_test=GenericObjectNode.GENERIC_LOCATION)
actor_stops_holding_rod = RelChange(name="Actor Stop Holds Rod", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="holds", node_b=protection_pillar, add_or_remove=ChangeAction.REMOVE)
location_starts_holding_rod = RelChange(name="Location Holds Rod", node_a=GenericObjectNode.GENERIC_LOCATION, edge_name="holds", node_b=protection_pillar, add_or_remove=ChangeAction.ADD)
rod_becomes_active = TagChange(name="Rod is Activated", object_node_name=protection_pillar, tag="Activated", value=True, add_or_remove=ChangeAction.ADD)

install_rod = StoryNode(name="Install Rod", type={"Type":"Defense"}, charcount=1, actor=[GenericObjectNode.TASK_OWNER], required_test_list=[actor_holds_rod_check], effects_on_next_ws=[actor_stops_holding_rod, location_starts_holding_rod, rod_becomes_active])


def create_rod_task_node_for_homeowner(character_object, character_home_location_object):

    character_object_name = character_object.get_name()
    character_home_location_name = character_home_location_object.get_name()

    magical_temple_not_hold_rod = HasEdgeTest(object_from_test=magic_temple, edge_name_test="holds", object_to_test=protection_pillar, inverse=True)
    magical_temple_hold_rod = HasEdgeTest(object_from_test=magic_temple, edge_name_test="holds", object_to_test=protection_pillar)

    my_home_is_destroyed_check = HasTagTest(object_to_test=character_home_location_object, tag="Demolished", value=True)

    take_rod_from_temple_task = CharacterTask(task_name="Take Rod from Temple", task_actions=[take_rod], task_location_name="Magic Temple", avoidance_state=[magical_temple_not_hold_rod])
    install_rod_at_my_home_task = CharacterTask(task_name="Install Rod at My Home", task_actions=[install_rod], task_location_name=character_home_location_name, avoidance_state=[my_home_is_destroyed_check])

    take_rod_and_install_stack = TaskStack(stack_name="Rod Quest", task_stack=[take_rod_from_temple_task,install_rod_at_my_home_task])

    take_rod_and_install_stackchange = TaskChange(name="Rod Quest Change", task_giver_name=GenericObjectNode.GENERIC_ACTOR, task_owner_name=GenericObjectNode.GENERIC_ACTOR, task_stack=take_rod_and_install_stack)

    personal_rod_quest_name = "Get Rod Quest for " + character_object_name
    my_get_rod_quest_action = StoryNode(name=personal_rod_quest_name, tags={"Type":"GetTask"}, effects_on_next_ws=[take_rod_and_install_stackchange], required_test_list=[magical_temple_hold_rod])
    
    return my_get_rod_quest_action

papa_bear_rod_quest_node = create_rod_task_node_for_homeowner(character_object=papabear, character_home_location_object=bear_house)

initial_graph = StoryGraph(name="Test Graph", character_objects=[papabear], starting_ws=reds_world_state)
initial_graph.insert_story_part(part = papa_bear_rod_quest_node, character=papabear, location=bear_house, absolute_step=0)

start_gen_time = datetime.now()
generated_graph = generate_story_from_starter_graph(init_storygraph=initial_graph, list_of_rules=[], required_story_length=10, verbose=True, extra_attempts=-1)

finish_gen_time = datetime.now()

print("xxx")
print("Generation Time:", str(finish_gen_time-start_gen_time))

base_directory = "application/tests/test_output/"
base_folder_name = "bear_rod_test"


fullpath = base_directory + base_folder_name
if not os.path.exists(fullpath):
    os.makedirs(fullpath)

generated_graph.print_graph_nodes_to_text_file(directory=fullpath, verbose=True)

generated_graph.make_latest_state().print_all_edges()

print("Generation Complete! Yippee!!")
