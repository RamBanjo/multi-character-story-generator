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


#Alice wants to protect Charlie
#Bob wants to kill Charlie
#Charlie is dead

#Alice's task is auto failed
#Bob's task is auto completed

alice = CharacterNode(name="Alice", internal_id=0)
bob = CharacterNode(name="Bob", internal_id=1)
charlie = CharacterNode(name="Charlie", tags={"Type":"Character", "Alive":False}, internal_id=2)

somewhere = LocationNode(name="Somewhere", internal_id=3)

test_ws = WorldState(name="Test WS", objectnodes=[alice, bob, charlie, somewhere])
test_ws.connect(from_node=somewhere, edge_name="holds", to_node=alice)
test_ws.connect(from_node=somewhere, edge_name="holds", to_node=bob)
test_ws.connect(from_node=somewhere, edge_name="holds", to_node=charlie)

charlie_is_dead = HasTagTest(object_to_test="charlie", tag="Alive", value=False)
charlie_is_charlie = ObjectEqualityTest(object_list=[charlie, "charlie"])

protect = StoryNode(name="Protect", actor=[GenericObjectNode.TASK_OWNER], target=["charlie"])
protect_task = CharacterTask(task_name="Protect Task", task_actions=[protect], task_location_name="Somewhere", actor_placeholder_string_list=["charlie"], avoidance_state=[charlie_is_dead])
protect_stack = TaskStack(stack_name="Protect Stack", task_stack=[protect_task], task_stack_requirement=[charlie_is_charlie])
protect_change = TaskChange(name="Protect Change", task_giver_name=GenericObjectNode.GENERIC_ACTOR, task_owner_name=GenericObjectNode.GENERIC_ACTOR, task_stack=protect_stack)
get_protect_node = StoryNode(name="Get Protection", effects_on_next_ws=[protect_change])

murder = StoryNode(name="Murder", actor=[GenericObjectNode.TASK_OWNER], target=["charlie"])
murder_task = CharacterTask(task_name="Murder Task", task_actions=[murder], task_location_name="Somewhere", actor_placeholder_string_list=["charlie"], goal_state=[charlie_is_dead])
murder_stack = TaskStack(stack_name="Murder Stack", task_stack=[murder_task], task_stack_requirement=[charlie_is_charlie])
murder_change = TaskChange(name="Murder Change", task_giver_name=GenericObjectNode.GENERIC_ACTOR, task_owner_name=GenericObjectNode.GENERIC_ACTOR, task_stack=murder_stack)
get_murder_node = StoryNode(name="Get Murder", effects_on_next_ws=[murder_change])

test_sg = StoryGraph(name="Test SG", character_objects=[alice, bob, charlie], starting_ws=test_ws)
test_sg.insert_story_part(part=get_protect_node, character=alice, location=somewhere)
test_sg.insert_story_part(part=get_murder_node, character=bob, location=somewhere)

test_sg.attempt_advance_task_stack("Protect Stack", actor_name="Alice", abs_step=1, verbose=True)
test_sg.attempt_advance_task_stack("Murder Stack", actor_name="Bob", abs_step=1, verbose=True)

test_sg.print_all_node_beautiful_format()