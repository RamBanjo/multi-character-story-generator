#calculate_score_from_next_task_in_task_stack

from components.CharacterTask import CharacterTask, TaskStack
from components.StoryGraphTwoWS import StoryGraph
from components.StoryNode import StoryNode
from components.StoryObjects import CharacterNode, LocationNode
from components.UtilityEnums import GenericObjectNode
from components.WorldState import WorldState


alice = CharacterNode(name="Alice")
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

snodea = StoryNode(name="Action A", biasweight=1, tags={"Type":"Placeholder"}, charcount=1, actor=[GenericObjectNode.TASK_OWNER])
snodeb = StoryNode(name="Action B", biasweight=2, tags={"Type":"Placeholder"}, charcount=1, actor=[GenericObjectNode.TASK_OWNER])
snodec = StoryNode(name="Action C", biasweight=3, tags={"Type":"Placeholder"}, charcount=1, actor=[GenericObjectNode.TASK_OWNER])
snoded = StoryNode(name="Action D", biasweight=4, tags={"Type":"Placeholder"}, charcount=1, actor=[GenericObjectNode.TASK_OWNER])
snodee = StoryNode(name="Action E", biasweight=5, tags={"Type":"Placeholder"}, charcount=1, actor=[GenericObjectNode.TASK_OWNER])
snodef = StoryNode(name="Action F", biasweight=6, tags={"Type":"Placeholder"}, charcount=1, actor=[GenericObjectNode.TASK_OWNER])

test_task_1 = CharacterTask(task_name="Test Task 1", task_actions=[snodea, snodeb], task_location_name="Village", goal_state=[], avoidance_state=[])
test_task_2 = CharacterTask(task_name="Test Task 2", task_actions=[snodec, snoded], task_location_name="Village", goal_state=[], avoidance_state=[])
test_task_3 = CharacterTask(task_name="Test Task 3", task_actions=[snodee, snodef], task_location_name="Village", goal_state=[], avoidance_state=[])
test_stack = TaskStack(stack_name="Test Stack", task_stack=[test_task_1, test_task_2, test_task_3], task_stack_requirement=[], stack_giver_name="Bob", stack_owner_name="Alice")