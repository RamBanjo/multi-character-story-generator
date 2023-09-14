#Test the Task Change Objects
import sys
sys.path.insert(0,'')

from application.components.CharacterTask import CharacterTask, TaskStack
from application.components.ConditionTest import HasEdgeTest
from application.components.RelChange import TagChange, TaskAdvance, TaskCancel, TaskChange
from application.components.StoryNode import StoryNode
from application.components.StoryObjects import CharacterNode, LocationNode
from application.components.UtilityEnums import ChangeAction, GenericObjectNode
from application.components.WorldState import WorldState

alice = CharacterNode("Alice")
bob = CharacterNode("Bob")
charlie = CharacterNode("Charlie")
daniel = CharacterNode("Daniel")
eve = CharacterNode("Eve")

town_square = LocationNode("Town Square")
castle = LocationNode("Castle")

test_ws = WorldState("TestWS", objectnodes=[alice, bob, charlie, daniel, eve, town_square, castle])

#The test: Bob hates Charlie and Daniel. The Task involves the actor doing the task traveling towards the location of the character hated by the task giver and killing them.

task_giver_hates_target = HasEdgeTest(object_from_test=bob, edge_name_test="hates", object_to_test=charlie, soft_equal=True)
task_giver_not_hate_task_owner = HasEdgeTest(object_from_test=bob, edge_name_test="hates", object_to_test=alice, soft_equal=True, inverse=True)
task_owner_not_like_target = HasEdgeTest(object_from_test=alice, edge_name_test="friends", object_to_test=charlie, soft_equal=True, inverse=True)
task_owner_not_love_target = HasEdgeTest(object_from_test=alice, edge_name_test="loves", object_to_test=charlie, soft_equal=True, inverse=True)

murder_target_dies = TagChange("Murder Target Dies", object_node_name=charlie, tag="Alive", value=False, add_or_remove=ChangeAction.ADD)
kill_murder_target_node = StoryNode(name="Kill Target", charcount=1, target_count=1, biasweight=0, tags={"Type":"Murder"}, effects_on_next_ws=[murder_target_dies])

kill_murder_target_task = CharacterTask(task_name="Kill Murder Target", task_actions=[kill_murder_target_node], task_location_name="Castle")

#TaskStack objects might have to be created on demand if it requires the names of the task giver and task owner
kill_hated_character_task = TaskStack(stack_name="Kill Hated Character", task_stack=[kill_murder_target_task], task_stack_requirement=[task_giver_hates_target, task_giver_not_hate_task_owner, task_owner_not_like_target, task_owner_not_love_target], stack_owner_name="Alice", stack_giver_name="Bob")

task_change_test = TaskChange(name="Obtain Kill Hated Character Task", task_giver_name="Bob", task_owner_name="Alice", task_stack=kill_hated_character_task)

test_ws.apply_task_change(task_change_test)

#Now we check if Alice gets that task, she's the Task Owner

alice_from_testws = test_ws.node_dict["Alice"]
gotten_task_stack = alice_from_testws.get_task_stack_by_name("Kill Hated Character")
print(gotten_task_stack.stack_name)
print(gotten_task_stack.task_stack[0].task_name)

#Since we have a task now we can either advance or cancel it

task_advance_test = TaskAdvance(name="Advance Kill Hated Character", actor_name="Alice", task_stack_name="Kill Hated Character")
task_cancel_test = TaskCancel(name="Advance Kill Hated Character", actor_name="Alice", task_stack_name="Kill Hated Character")

test_ws.apply_task_advance_change(taskadvancechange_object=task_advance_test, abs_step=3)
print("Expected Completion Step (3):", gotten_task_stack.task_stack[0].completion_step)

test_ws.apply_task_cancel_change(taskcancelchange_object=task_cancel_test)
print("Expected Removed From Pool (True):", gotten_task_stack.remove_from_pool)
