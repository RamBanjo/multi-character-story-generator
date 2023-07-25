from components.StoryGraphTwoWS import *
from components.CharacterTask import CharacterTask, TaskStack
from components.ConditionTest import HasEdgeTest
from components.RelChange import RelChange, TagChange, TaskChange
from components.StoryNode import StoryNode
from components.StoryObjects import CharacterNode, LocationNode, ObjectNode
from components.UtilityEnums import ChangeAction, GenericObjectNode
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

#If we give tasks to characters, then they should show up. Let's give empty task stacks to Alice and Charlie.

test_stack_1 = TaskStack(stack_name="Test Stack 1", task_stack=[], task_stack_requirement=[], stack_giver_name="Bob", stack_owner_name="Alice")
test_stack_2 = TaskStack(stack_name="Test Stack 2", task_stack=[], task_stack_requirement=[], stack_giver_name="Bob", stack_owner_name="Alice")
test_stack_3 = TaskStack(stack_name="Test Stack 3", task_stack=[], task_stack_requirement=[], stack_giver_name="Bob", stack_owner_name="Charlie")
test_stack_4 = TaskStack(stack_name="Test Stack 4", task_stack=[], task_stack_requirement=[], stack_giver_name="Bob", stack_owner_name="Charlie")
test_stack_5 = TaskStack(stack_name="Test Stack 5", task_stack=[], task_stack_requirement=[], stack_giver_name="Bob", stack_owner_name="Charlie")
test_stack_6 = TaskStack(stack_name="Test Stack 6", task_stack=[], task_stack_requirement=[], stack_giver_name="Bob", stack_owner_name="Alice")

alice.add_task_stack(task_stack=test_stack_1)
alice.add_task_stack(task_stack=test_stack_2)
charlie.add_task_stack(task_stack=test_stack_3)
charlie.add_task_stack(task_stack=test_stack_4)
charlie.add_task_stack(task_stack=test_stack_5)

print("Alice Task Stack Names", test_sg.get_list_of_task_stack_names_from_latest_step("Alice"))
print("Bob Task Stack Names", test_sg.get_list_of_task_stack_names_from_latest_step("Bob"))
print("Charlie Task Stack Names", test_sg.get_list_of_task_stack_names_from_latest_step("Charlie"))

snode1 = StoryNode(name="Action 1", biasweight=0, tags={"Type":"Placeholder"}, charcount=1)
snode2 = StoryNode(name="Action 2", biasweight=0, tags={"Type":"Placeholder"}, charcount=1)
snode3 = StoryNode(name="Action 3", biasweight=0, tags={"Type":"Placeholder"}, charcount=1)
snode4 = StoryNode(name="Action 4", biasweight=0, tags={"Type":"Placeholder"}, charcount=1)


task_change_object = TaskChange("Get TS6", task_giver_name="Bob", task_owner_name="Alice", task_stack=test_stack_6)
snode5 = StoryNode(name="Action 5", biasweight=0, tags={"Type":"Placeholder"}, charcount=1, effects_on_next_ws=[task_change_object])

test_sg.add_story_part(part=snode1, character=alice, location=town)
test_sg.add_story_part(part=snode2, character=alice, location=town)
test_sg.add_story_part(part=snode3, character=alice, location=town)
test_sg.add_story_part(part=snode4, character=alice, location=town)
test_sg.add_story_part(part=snode5, character=alice, location=town)
test_sg.refresh_longest_path_length()

test_sg.make_latest_state()
print("Alice Task Stack Names (After adding Story Parts)", test_sg.get_list_of_task_stack_names_from_latest_step("Alice"))

# Test these things as well
# find_last_step_of_task_stack_from_actor
# attempt_advance_task_stack
# test_task_completeness
# calculate_score_from_next_task_in_task_stack