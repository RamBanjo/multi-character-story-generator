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

from application.StoryGeneration_NewFlowchart_WithMetrics import attempt_move_towards_task_loc, perform_wait_action
#The Illusion of Free Choice...

alice = CharacterNode(name="Alice", internal_id=0)

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

bonus_points_if_target_location_is_fun_place = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="FunPlace", value=True, score=10)
penalty_if_target_location_is_exercise_place = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="ExercisePlace", value=True, score=-10)

suggested_movements = [bonus_points_if_target_location_is_fun_place, penalty_if_target_location_is_exercise_place]

testsg = StoryGraph(name="Test SG", character_objects=[alice], starting_ws=testws)

perform_wait_action(target_story_graph=testsg, current_character=alice)
testsg.fill_in_locations_on_self()
 
#Since we gave bonus points for fun place and minus points for exercise place, we expect Alice to go to either the Concert or the Arcade.

#In the event that minimum points requirement of more than 10 is needed, we would see that there is no valid options because the points requirement for FunPlace is too low
movement_success = attempt_move_towards_task_loc(target_story_graph=testsg, current_character=alice, movement_index=1, suggested_movement_requirements=suggested_movements, minimum_action_score_for_valid_movement=20)
print("Attempt Movement Success:", movement_success)

testsg.fill_in_locations_on_self()

testsg.print_all_node_beautiful_format()