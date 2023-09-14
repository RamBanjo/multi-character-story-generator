#calculate_score_from_next_task_in_task_stack
import sys
sys.path.insert(0,'')

from application.components.CharacterTask import CharacterTask, TaskStack
from application.components.ConditionTest import HasTagTest
from application.components.RelChange import TaskChange
from application.components.StoryGraphTwoWS import StoryGraph
from application.components.StoryNode import StoryNode
from application.components.StoryObjects import CharacterNode, LocationNode
from application.components.UtilityEnums import GenericObjectNode
from application.components.WorldState import WorldState


alice = CharacterNode(name="Alice", tags={"Type":"Character", "Job":"Archer"})
bob = CharacterNode(name="Bob")
charlie = CharacterNode(name="Charlie")
daniel = CharacterNode(name="Daniel")
eve = CharacterNode(name="Eve")

town = LocationNode(name="TownSquare")

test_ws = WorldState(name="Test State", objectnodes=[alice, bob, charlie, daniel, eve, town])

test_ws.connect(from_node=town, edge_name="holds", to_node=alice)
test_ws.connect(from_node=town, edge_name="holds", to_node=bob)
test_ws.connect(from_node=town, edge_name="holds", to_node=charlie)
test_ws.connect(from_node=town, edge_name="holds", to_node=daniel)
test_ws.connect(from_node=town, edge_name="holds", to_node=eve)

test_sg = StoryGraph(name="Test SG", character_objects=[alice, bob, charlie, daniel, eve], location_objects=[town], starting_ws=test_ws)

#Scenario: Look! It's the Story Nodes from before! Now if only for each task we can have a score... I know! Let's make some scores!

test_is_archer = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Job", value="Archer", score=10)
snodea = StoryNode(name="Action A", biasweight=1, tags={"Type":"Placeholder"}, charcount=1, actor=[GenericObjectNode.TASK_OWNER])

snodeb = StoryNode(name="Action B", biasweight=2, tags={"Type":"Placeholder"}, charcount=1, actor=[GenericObjectNode.TASK_OWNER])
snodec = StoryNode(name="Action C", biasweight=3, tags={"Type":"Placeholder"}, charcount=1, actor=[GenericObjectNode.TASK_OWNER])
snoded = StoryNode(name="Action D", biasweight=4, tags={"Type":"Placeholder"}, charcount=1, actor=[GenericObjectNode.TASK_OWNER])
snodee = StoryNode(name="Action E", biasweight=5, tags={"Type":"Placeholder"}, charcount=1, actor=[GenericObjectNode.TASK_OWNER])
snodef = StoryNode(name="Action F", biasweight=6, tags={"Type":"Placeholder"}, charcount=1, actor=[GenericObjectNode.TASK_OWNER])

test_task_1 = CharacterTask(task_name="Test Task 1", task_actions=[snodea, snodeb], task_location_name="TownSquare", goal_state=[], avoidance_state=[])
test_task_2 = CharacterTask(task_name="Test Task 2", task_actions=[snodec, snoded], task_location_name="TownSquare", goal_state=[], avoidance_state=[])
test_task_3 = CharacterTask(task_name="Test Task 3", task_actions=[snodee, snodef], task_location_name="TownSquare", goal_state=[], avoidance_state=[])


test_stack = TaskStack(stack_name="Test Stack", task_stack=[test_task_1, test_task_2, test_task_3], task_stack_requirement=[], stack_giver_name="Bob", stack_owner_name="Alice")

give_task_to_alice = TaskChange(name="Alice gets Stack", task_giver_name="Bob", task_owner_name="Alice", task_stack=test_stack)
node_x = StoryNode(name="Action X", biasweight=1, tags={"Type":"Placeholder"}, charcount=1, effects_on_next_ws=[give_task_to_alice])

test_sg.add_story_part(part=node_x, character=alice, location=town)

# #The first task should have a score of 2 because Node A has 1 and Node B has 2, which means Node B is the max. However, this can change if we change the score of Node A.
# print("Expecting Score of 2 from this Step:", test_sg.calculate_score_from_next_task_in_task_stack(actor_name="Alice", task_stack_name="Test Stack", task_perform_index=1))

#If we add some optional tests to the tasks, then it should be scored. We'll give it so much score that it is worth more than 2.

#TODO (Extra Features): If we modify the Story Node after it was initialized, then the test won't properly show up. This is prevalent when adding the test after adding a story part to the Story Graph.
#Most likely this is due to the effects_on_next_ws being assigned in Node X, and the List of Changes freezes as it gets added.
#Do we have to fix this? I suppose we don't have to, since when rebuilding the initial world state everything will be run back from the start?

print("Expecting Score of 11 from this Step:", test_sg.calculate_score_from_next_task_in_task_stack(actor_name="Alice", task_stack_name="Test Stack", task_perform_index=1))


