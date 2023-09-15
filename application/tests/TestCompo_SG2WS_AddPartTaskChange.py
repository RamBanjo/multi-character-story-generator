# testing add_story_part_at_step here
# modify_taskchange_object_on_add can also be tested here since it's called by add_story_part_at_step

# The Scenario: Alice takes a task from Bob to kill someone Bob Hates (again, wow, Bob has a lot of people to kill)
# Bob will give Alice a task on Absolute Step 0. Therefore, if we look at the Worldstate after that Timestep, we should see that the task is already filled in, even though it didn't go in filled in.
import sys
sys.path.insert(0,'')

from application.components.CharacterTask import CharacterTask, TaskStack
from application.components.ConditionTest import HasEdgeTest
from application.components.RelChange import TaskChange
from application.components.StoryGraphTwoWS import StoryGraph
from application.components.StoryNode import StoryNode
from application.components.StoryObjects import CharacterNode, LocationNode
from application.components.UtilityEnums import GenericObjectNode
from application.components.WorldState import WorldState


alice = CharacterNode("Alice")
bob = CharacterNode("Bob")
charlie = CharacterNode("Charlie")
daniel = CharacterNode("Daniel")
eve = CharacterNode("Eve")

townsquare = LocationNode("TownSquare")

test_ws = WorldState("TestWS", objectnodes=[alice, bob, charlie, daniel, eve, townsquare])
test_ws.connect(from_node=townsquare, edge_name="holds", to_node=alice)
test_ws.connect(from_node=townsquare, edge_name="holds", to_node=bob)
test_ws.connect(from_node=townsquare, edge_name="holds", to_node=charlie)
test_ws.connect(from_node=townsquare, edge_name="holds", to_node=daniel)
test_ws.connect(from_node=townsquare, edge_name="holds", to_node=eve)
test_ws.connect(from_node=bob, edge_name="hates", to_node=charlie)
test_ws.connect(from_node=bob, edge_name="hates", to_node=daniel)

#Since Bob hates Charlie and Daniel, when Alice gets the quest to kill someone Bob hates, the quest's placeholder should be replaced by either of those hated person.

task_owner_hates_hated_person = HasEdgeTest(object_from_test=GenericObjectNode.TASK_GIVER, edge_name_test="hates", object_to_test="hated_person", soft_equal=True)

kill_hated_task = CharacterTask(task_name="Kill Hated Character Task", task_actions=[], task_location_name="TownSquare", actor_placeholder_string_list=["hated_person"])
kill_hated_stack = TaskStack(stack_name="Kill Hated Stack", task_stack=[kill_hated_task], task_stack_requirement=[task_owner_hates_hated_person])

give_kill_hated_stack = TaskChange(name="Give Kill Hated Stack", task_giver_name=GenericObjectNode.GENERIC_ACTOR, task_owner_name=GenericObjectNode.GENERIC_TARGET, task_stack=kill_hated_stack)

give_kill_hated_stack_action = StoryNode(name="Give Kill Hated Stack Action", biasweight=0, charcount=1, target_count=1, tags=[{"Type":"Give_Quest"}], effects_on_next_ws=[give_kill_hated_stack])

test_sg = StoryGraph("Test SG", character_objects=[alice, bob, charlie, daniel], location_objects=[townsquare], starting_ws=test_ws)

test_sg.insert_joint_node(joint_node=give_kill_hated_stack_action, main_actor=alice, other_actors=[bob], location=townsquare, targets=[], absolute_step=0, make_main_actor_a_target=True)

#At this point, we should be able to grab the final world state and see if Alice has the task, and who Alice is supposed to kill in the task.

# first_node = test_sg.story_parts[("Alice", 0)]

# change_object = first_node.effects_on_next_ws[0]

# task_stack_gained = change_object.task_stack

# print(task_stack_gained.stack_giver_name)
# print(task_stack_gained.stack_owner_name)
        # print(new_part.effects_on_next_ws[0].task_stack.stack_giver_name)
        # print(new_part.effects_on_next_ws[0].task_stack.stack_owner_name)
latest_ws = test_sg.make_latest_state()

# #Next, get Alice from Latest WS. Then we get the Kill Hated Stack from Alice to see if the dict is properly assigned.

latest_alice = latest_ws.node_dict["Alice"]
latest_stack = latest_alice.get_task_stack_by_name("Kill Hated Stack")

print(latest_stack)

print(latest_stack.placeholder_info_dict)

print(test_sg.placeholder_dicts_of_tasks)