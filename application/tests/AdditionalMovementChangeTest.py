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

from application.StoryGeneration_NewFlowchart_WithMetrics import attempt_move_towards_task_loc
import os

#Alice keeps track of how many times she has moved in her step counter, which is stored in her tag.

alice = CharacterNode(name="Alice", tags={"Type":"Character", "StepCounter":0}, internal_id=0)
hub = LocationNode(name="Hub", internal_id=1)
arcade = LocationNode(name="Arcade", tags={"Type":"Location","FunPlace":True}, internal_id = 2)
pool = LocationNode(name="Swimming Pool", tags={"Type":"Location","FunPlace":True, "ExercisePlace":True}, internal_id = 3)
museum = LocationNode(name="Museum", tags={"Type":"Location","ArtPlace":True}, internal_id = 4)
concert = LocationNode(name="Concert Hall", tags={"Type":"Location", "ArtPlace":True, "FunPlace":True}, internal_id=5)
gym = LocationNode(name="Gym", tags={"Type":"Location", "ExercisePlace":True}, internal_id=6)

testws = WorldState(name="Test WS", objectnodes=[alice, hub, arcade, pool, museum, concert, gym])

testws.connect(from_node=hub, edge_name="holds", to_node=alice)
testws.doubleconnect(from_node=arcade, edge_name="connects", to_node=hub)
testws.doubleconnect(from_node=pool, edge_name="connects", to_node=hub)
testws.doubleconnect(from_node=museum, edge_name="connects", to_node=hub)
testws.doubleconnect(from_node=concert, edge_name="connects", to_node=hub)
testws.doubleconnect(from_node=gym, edge_name="connects", to_node=hub)

increment_step_counter_change = RelativeTagChange(name="Increment Step Counter", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="StepCounter", value_delta=1)
movement_extra_change = [increment_step_counter_change]

testsg = StoryGraph(name="Test SG", character_objects=[alice], starting_ws=testws)

attempt_move_towards_task_loc(target_story_graph=testsg, current_character=alice, movement_index=0, extra_changes=[increment_step_counter_change])
attempt_move_towards_task_loc(target_story_graph=testsg, current_character=alice, movement_index=1, extra_changes=[increment_step_counter_change])
attempt_move_towards_task_loc(target_story_graph=testsg, current_character=alice, movement_index=2, extra_changes=[increment_step_counter_change])

testsg.print_all_node_beautiful_format()

latest_alice = testsg.make_latest_state().node_dict["Alice"]
print("Latest Alice Step Counter", latest_alice.tags["StepCounter"])