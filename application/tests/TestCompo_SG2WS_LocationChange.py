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

alice = CharacterNode(name="Alice", tags={"Type":"Character", "Job":"Warrior", "Alive":True})
bob = CharacterNode(name="Bob", tags={"Type":"Character", "Job":"Fighter", "Alive":True})
charlie = CharacterNode(name="Charlie", tags={"Type":"Character", "Job":"Bard", "Alive":True})
town_a = LocationNode("Town A")
town_b = LocationNode("Town B")
town_c = LocationNode("Town C")

ws5 = WorldState(name="World State", objectnodes=[alice, bob, charlie, town_a, town_b, town_c])

ws5.doubleconnect(nodeA=town_a, edge_name="connects", nodeB=town_b)
ws5.doubleconnect(nodeA=town_b, edge_name="connects", nodeB=town_c)
ws5.connect(from_node=town_a, edge_name="holds", to_node=alice)
ws5.connect(from_node=town_a, edge_name="holds", to_node=bob)
ws5.connect(from_node=town_c, edge_name="holds", to_node=charlie)


sg5 = StoryGraph(name="Story Graph 5", character_objects=[alice, bob, charlie], location_objects=[town_a, town_b, town_c], starting_ws=ws5)


node_a = StoryNode(name="Node A")

sg5.add_story_part(part=node_a, character=alice, location=town_a)

go_to_new_location_change = RelChange(name="Go To Task Loc", node_a=town_b, edge_name="holds", node_b=GenericObjectNode.GENERIC_ACTOR, value=None, add_or_remove=ChangeAction.ADD)

# not_be_in_current_location_change = RelChange("Leave Current Loc", node_a=GenericObjectNode.GENERIC_LOCATION, edge_name=current_ws.DEFAULT_HOLD_EDGE_NAME, node_b=character_at_step, add_or_remove=ChangeAction.REMOVE)
not_be_in_current_location_change = RelChange(name="Leave Current Loc", node_a=GenericObjectNode.GENERIC_LOCATION, edge_name="holds", node_b=GenericObjectNode.GENERIC_ACTOR, add_or_remove=ChangeAction.REMOVE, soft_equal=True, value=None)

target_location_adjacent_to_current_location = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_LOCATION, edge_name_test="connects", object_to_test=town_b, soft_equal=True)

move_towards_task_location_node = StoryNode(name="Move Towards Town B", biasweight=0, tags={"Type":"Movement"}, charcount=1, effects_on_next_ws=[not_be_in_current_location_change, go_to_new_location_change], required_test_list=[target_location_adjacent_to_current_location])

sg5.add_story_part(part=move_towards_task_location_node, character=alice)
sg5.fill_in_locations_on_self()
sg5.add_story_part(part=node_a, character=alice)
sg5.fill_in_locations_on_self()

sg5.print_all_node_beautiful_format()
latest_state = sg5.make_latest_state()
print(latest_state.get_actor_current_location(alice))