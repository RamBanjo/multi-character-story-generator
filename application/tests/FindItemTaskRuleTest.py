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

alice = CharacterNode(name="Alice", tags={"Type":"Character","Alive":True, "LikesExercise":True}, internal_id=0)

hub = LocationNode(name="Hub", internal_id=1)
arcade = LocationNode(name="Arcade", tags={"Type":"Location","FunPlace":True}, internal_id = 2)
pool = LocationNode(name="Swimming Pool", tags={"Type":"Location","FunPlace":True, "ExercisePlace":True}, internal_id = 3)
museum = LocationNode(name="Museum", tags={"Type":"Location","ArtPlace":True}, internal_id = 4)
concert = LocationNode(name="Concert Hall", tags={"Type":"Location", "ArtPlace":True, "FunPlace":True}, internal_id=5)
gym = LocationNode(name="Gym", tags={"Type":"Location", "ExercisePlace":True}, internal_id=6)

artwork = ObjectNode(name="Artwork", tags={"Type":"Art"}, internal_id=7)
weights = ObjectNode(name="Weights", tags={"Type":"Exercise"}, internal_id=8)
pool_noodle = ObjectNode(name="PoolNoodle", tags={"Type":"Exercise"}, internal_id=9)

testws = WorldState(name="Test WS", objectnodes=[alice, hub, arcade, pool, museum, concert, gym, artwork, weights, pool_noodle])

testws.connect(from_node=hub, edge_name="holds", to_node=alice)
testws.doubleconnect(from_node=arcade, edge_name="connects", to_node=hub)
testws.doubleconnect(from_node=pool, edge_name="connects", to_node=hub)
testws.doubleconnect(from_node=museum, edge_name="connects", to_node=hub)
testws.doubleconnect(from_node=concert, edge_name="connects", to_node=hub)
testws.doubleconnect(from_node=gym, edge_name="connects", to_node=hub)

testws.connect(from_node=pool, edge_name="holds", to_node=pool_noodle)
testws.connect(from_node=gym, edge_name="holds", to_node=weights)
testws.connect(from_node=museum, edge_name="holds", to_node=artwork)

testws.print_all_edges()

# location_has_item_check = HasEdgeTest(object_from_test=museum, edge_name_test="holds", object_to_test=artwork)
# print(testws.test_story_compatibility_with_conditiontest(location_has_item_check))

actor_is_alive = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Alive", value=True)
actor_is_not_unconscious =HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Unconscious", value=True, inverse=True)
location_stops_holding_target = RelChange(name="Location Stops Holding Target", node_a=GenericObjectNode.GENERIC_LOCATION, edge_name="holds", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.REMOVE)
actor_starts_holding_target = RelChange(name="Actor Starts Holding Target", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="holds", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.ADD)

def make_find_item_rule(item_to_find, item_liking_tag, location_holding_item):
    
    current_location_has_item_check = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_LOCATION, edge_name_test="holds", object_to_test=item_to_find)

    take_quest_item = StoryNode(name="Take Quest Item ("+item_to_find.get_name()+")", tags={"Type":"Collect"}, actor=[GenericObjectNode.TASK_OWNER], target=[item_to_find], required_test_list=[actor_is_alive, actor_is_not_unconscious, current_location_has_item_check], effects_on_next_ws=[actor_starts_holding_target, location_stops_holding_target])

    location_no_longer_has_item_check = HasEdgeTest(object_from_test=location_holding_item, edge_name_test="holds", object_to_test=item_to_find, inverse=True)
    find_item_task = CharacterTask(task_name="Find Item Quest", task_actions=[take_quest_item], task_location_name=location_holding_item.get_name(), avoidance_state=[location_no_longer_has_item_check])

    location_has_item_check = HasEdgeTest(object_from_test=location_holding_item, edge_name_test="holds", object_to_test=item_to_find)
    
    memory_name = item_to_find.get_name() + "Memory"
    character_no_quest_memory_check = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag=memory_name, value=True, inverse=True)
    character_gains_quest_memory_change = TagChange(name="Gain Task Quest Memory", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag=memory_name, value=True, add_or_remove=ChangeAction.ADD)

    find_item_stack = TaskStack(stack_name="Find Item Stack ("+item_to_find.get_name()+")", task_stack=[find_item_task], task_stack_requirement=[])

    find_item_change = TaskChange(name="Find Item TaskChange", task_stack=find_item_stack, task_owner_name=GenericObjectNode.GENERIC_ACTOR, task_giver_name=GenericObjectNode.GENERIC_ACTOR)

    character_likes_item_type_check = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag=item_liking_tag, value=True)
    get_find_item_task_node = StoryNode(name="Gain Find Item Quest ("+item_to_find.get_name()+")", tags={"Type":"GetTask"}, effects_on_next_ws=[find_item_change, character_gains_quest_memory_change], required_test_list=[character_no_quest_memory_check, location_has_item_check, character_likes_item_type_check])

    patternless_into_find_item_node = RewriteRule(story_condition=[], story_change=[get_find_item_task_node], name="Patternless into Find Item Task Node")

    return patternless_into_find_item_node

patternless_into_find_pool_noodle = make_find_item_rule(item_to_find=pool_noodle, item_liking_tag="LikesExercise", location_holding_item=pool)
patternless_into_find_weights = make_find_item_rule(item_to_find=weights, item_liking_tag="LikesExercise", location_holding_item=gym)
patternless_into_find_artwork = make_find_item_rule(item_to_find=artwork, item_liking_tag="LikesArtwork", location_holding_item=museum)

init_sg = StoryGraph(name="Init SG", character_objects=[alice], starting_ws=testws)

all_patternless = [patternless_into_find_artwork, patternless_into_find_pool_noodle, patternless_into_find_weights]
output_story = generate_multiple_graphs(initial_graph=init_sg, list_of_rules=all_patternless, required_story_length=30, max_storynodes_per_graph=5, extra_attempts=-1, verbose=True, task_movement_random=True)

for story in output_story:
    story.print_all_node_beautiful_format()