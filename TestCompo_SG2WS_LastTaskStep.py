
from components.CharacterTask import CharacterTask, TaskStack
from components.RelChange import TaskAdvance
from components.StoryGraphTwoWS import StoryGraph
from components.StoryNode import StoryNode
from components.StoryObjects import CharacterNode, LocationNode
from components.UtilityEnums import GenericObjectNode
from components.WorldState import WorldState


alice = CharacterNode("Alice")
bob = CharacterNode("Bob")
charlie = CharacterNode("Charlie")
daniel = CharacterNode("Danniel")
eve = CharacterNode("Eve")

town = LocationNode("Town")
castle = LocationNode("Castle")
jail = LocationNode("Jail")

test_ws = WorldState(name="World State", objectnodes=[alice, bob, charlie, daniel, eve, town, castle, jail])

test_ws.connect(from_node=town, edge_name="holds", to_node=alice)
test_ws.connect(from_node=town, edge_name="holds", to_node=bob)
test_ws.connect(from_node=town, edge_name="holds", to_node=charlie)
test_ws.connect(from_node=town, edge_name="holds", to_node=daniel)
test_ws.connect(from_node=town, edge_name="holds", to_node=eve)

adv1 = TaskAdvance(name="Adv1", actor_name="Alice", task_stack_name="Test Stack")
story_node_1 = StoryNode("Story Node 1", biasweight=0, tags={"Type":"Placeholder"}, charcount=1, effects_on_next_ws=[adv1])

story_node_2 = StoryNode("Story Node 2", biasweight=0, tags={"Type":"Placeholder"}, charcount=1, effects_on_next_ws=[])

placeholder_dict = {GenericObjectNode.TASK_OWNER: "Alice", GenericObjectNode.TASK_GIVER: "Bob"}

task_1 = CharacterTask(task_name="Task 1", task_actions=[], task_location_name="Town", task_giver_name="Bob", task_owner_name="Alice")
task_2 = CharacterTask(task_name="Task 2", task_actions=[], task_location_name="Town", task_giver_name="Bob", task_owner_name="Alice")
task_3 = CharacterTask(task_name="Task 3", task_actions=[], task_location_name="Town", task_giver_name="Bob", task_owner_name="Alice")
task_4 = CharacterTask(task_name="Task 4", task_actions=[], task_location_name="Town", task_giver_name="Bob", task_owner_name="Alice")

teststack = TaskStack(stack_name="Test Stack", task_stack=[task_1, task_2, task_3, task_4], stack_giver_name="Bob", stack_owner_name="Alice")

alice.add_task_stack(teststack)

test_sg = StoryGraph(name="Test SG", character_objects=[alice, bob, charlie, daniel, eve], location_objects=[town, castle, jail], starting_ws=test_ws)

print(test_sg.find_last_step_of_task_stack_from_actor(task_stack_name="Test Stack", actor_name="Alice"))

test_sg.add_story_part(story_node_1, character=alice, location=town)

print(test_sg.find_last_step_of_task_stack_from_actor(task_stack_name="Test Stack", actor_name="Alice"))

test_sg.add_story_part(story_node_1, character=alice, location=town)

print(test_sg.find_last_step_of_task_stack_from_actor(task_stack_name="Test Stack", actor_name="Alice"))

test_sg.add_story_part(story_node_1, character=alice, location=town)

print(test_sg.find_last_step_of_task_stack_from_actor(task_stack_name="Test Stack", actor_name="Alice"))

test_sg.add_story_part(story_node_2, character=alice, location=town)
test_sg.add_story_part(story_node_2, character=alice, location=town)
test_sg.add_story_part(story_node_2, character=alice, location=town)
test_sg.add_story_part(story_node_2, character=alice, location=town)
test_sg.add_story_part(story_node_2, character=alice, location=town)

test_sg.add_story_part(story_node_1, character=alice, location=town)

print(test_sg.find_last_step_of_task_stack_from_actor(task_stack_name="Test Stack", actor_name="Alice"))