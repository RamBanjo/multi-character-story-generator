from components.StoryGraphTwoWS import *
from components.CharacterTask import CharacterTask, TaskStack
from components.ConditionTest import HasEdgeTest
from components.RelChange import RelChange, TagChange, TaskChange
from components.StoryNode import StoryNode
from components.StoryObjects import CharacterNode, LocationNode, ObjectNode
from components.UtilityEnums import ChangeAction, GenericObjectNode
from components.WorldState import WorldState

# alice = CharacterNode(name="Alice")
# bob = CharacterNode(name="Bob")
# charlie = CharacterNode(name="Charlie")
# daniel = CharacterNode(name="Daniel")
# eve = CharacterNode(name="Eve")

# town = LocationNode(name="TownSquare")

# test_ws = WorldState(name="Test State", objectnodes=[alice, bob, charlie, daniel, eve, town])

# test_ws.connect(from_node=town, edge_name="holds", to_node=alice)
# test_ws.connect(from_node=town, edge_name="holds", to_node=bob)
# test_ws.connect(from_node=town, edge_name="holds", to_node=charlie)
# test_ws.connect(from_node=town, edge_name="holds", to_node=daniel)
# test_ws.connect(from_node=town, edge_name="holds", to_node=eve)

# test_sg = StoryGraph(name="Test SG", character_objects=[alice, bob, charlie, daniel, eve], location_objects=[town], starting_ws=test_ws)

# #If we give tasks to characters, then they should show up. Let's give empty task stacks to Alice and Charlie.

# test_stack_1 = TaskStack(stack_name="Test Stack 1", task_stack=[], task_stack_requirement=[], stack_giver_name="Bob", stack_owner_name="Alice")
# test_stack_2 = TaskStack(stack_name="Test Stack 2", task_stack=[], task_stack_requirement=[], stack_giver_name="Bob", stack_owner_name="Alice")
# test_stack_3 = TaskStack(stack_name="Test Stack 3", task_stack=[], task_stack_requirement=[], stack_giver_name="Bob", stack_owner_name="Charlie")
# test_stack_4 = TaskStack(stack_name="Test Stack 4", task_stack=[], task_stack_requirement=[], stack_giver_name="Bob", stack_owner_name="Charlie")
# test_stack_5 = TaskStack(stack_name="Test Stack 5", task_stack=[], task_stack_requirement=[], stack_giver_name="Bob", stack_owner_name="Charlie")
# test_stack_6 = TaskStack(stack_name="Test Stack 6", task_stack=[], task_stack_requirement=[], stack_giver_name="Bob", stack_owner_name="Alice")

# alice.add_task_stack(task_stack=test_stack_1)
# alice.add_task_stack(task_stack=test_stack_2)
# charlie.add_task_stack(task_stack=test_stack_3)
# charlie.add_task_stack(task_stack=test_stack_4)
# charlie.add_task_stack(task_stack=test_stack_5)

# print("Alice Task Stack Names", test_sg.get_list_of_task_stack_names_from_latest_step("Alice"))
# print("Bob Task Stack Names", test_sg.get_list_of_task_stack_names_from_latest_step("Bob"))
# print("Charlie Task Stack Names", test_sg.get_list_of_task_stack_names_from_latest_step("Charlie"))

# snode1 = StoryNode(name="Action 1", biasweight=0, tags={"Type":"Placeholder"}, charcount=1)
# snode2 = StoryNode(name="Action 2", biasweight=0, tags={"Type":"Placeholder"}, charcount=1)
# snode3 = StoryNode(name="Action 3", biasweight=0, tags={"Type":"Placeholder"}, charcount=1)
# snode4 = StoryNode(name="Action 4", biasweight=0, tags={"Type":"Placeholder"}, charcount=1)


# task_change_object = TaskChange("Get TS6", task_giver_name="Bob", task_owner_name="Alice", task_stack=test_stack_6)
# snode5 = StoryNode(name="Action 5", biasweight=0, tags={"Type":"Placeholder"}, charcount=1, effects_on_next_ws=[task_change_object])

# test_sg.add_story_part(part=snode1, character=alice, location=town)
# test_sg.add_story_part(part=snode2, character=alice, location=town)
# test_sg.add_story_part(part=snode3, character=alice, location=town)
# test_sg.add_story_part(part=snode4, character=alice, location=town)
# test_sg.add_story_part(part=snode5, character=alice, location=town)
# test_sg.refresh_longest_path_length()

# test_sg.make_latest_state()
# print("Alice Task Stack Names (After adding Story Parts)", test_sg.get_list_of_task_stack_names_from_latest_step("Alice"))

# Test these things as well
# attempt_advance_task_stack
# test_task_completeness
# calculate_score_from_next_task_in_task_stack

# Okay, here we're testing Task Stack 7, and how complete this task is.
# We will need to test that all the testcases are working. Aha.
#
# (DONE) not_exist: Task Stack doesn't Exist. We will call a name that's not Test Stack 7 to test this.
# (DONE) task_stack_cleared: The task stack is already complete. We will call Test Stack 7 after it has been marked complete to test this.
# (DONE) incompatible: The task stack is trying to test for completeness at the point before the last update step, where the task can't be updated. We will advance Test Stack 7 then test the abs step before that update to test this.
# (DONE) wrong_location: The task is not in the correct location. We will move Alex to the Castle where the task is not to test this.
# (DONE) task_step_already_completed: The task is already completed according to the goal state given in the task.
# (DONE) task_step_already_failed: The task is already failed according to the fail state given in the task.
# (DONE) task_step_can_advance: None of the other conditions above applies.

#Here's a new world state, story graph, and an entirely new premise to consider upon

alex = CharacterNode("Alex")
bonnie = CharacterNode("Bonnie")
carol = CharacterNode("Carol")
diane = CharacterNode("Diane")
edgar = CharacterNode("Edgar")

village = LocationNode("Village")
castle = LocationNode("Castle")

test_ws_2 = WorldState(name="Test WS 2", objectnodes=[alex, bonnie, carol, diane, edgar, village, castle])

test_ws_2.connect(from_node=village, edge_name="holds", to_node=alex)
test_ws_2.connect(from_node=village, edge_name="holds", to_node=bonnie)
test_ws_2.connect(from_node=village, edge_name="holds", to_node=carol)
test_ws_2.connect(from_node=village, edge_name="holds", to_node=diane)
test_ws_2.connect(from_node=village, edge_name="holds", to_node=edgar)

become_rich = TagChange(name="Become Rich", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="Wealth", value="Rich", add_or_remove=ChangeAction.ADD)

snodea = StoryNode(name="Action A", biasweight=0, tags={"Type":"Placeholder"}, charcount=1, actor=[GenericObjectNode.TASK_OWNER], effects_on_next_ws=[become_rich])
snodeb = StoryNode(name="Action B", biasweight=0, tags={"Type":"Placeholder"}, charcount=1, actor=[GenericObjectNode.TASK_OWNER])
snodec = StoryNode(name="Action C", biasweight=0, tags={"Type":"Placeholder"}, charcount=1, actor=[GenericObjectNode.TASK_OWNER])
snoded = StoryNode(name="Action D", biasweight=0, tags={"Type":"Placeholder"}, charcount=1, actor=[GenericObjectNode.TASK_OWNER])
snodee = StoryNode(name="Action E", biasweight=0, tags={"Type":"Placeholder"}, charcount=1, actor=[GenericObjectNode.TASK_OWNER])
snodef = StoryNode(name="Action F", biasweight=0, tags={"Type":"Placeholder"}, charcount=1, actor=[GenericObjectNode.TASK_OWNER])

advance_stack_7 = TaskAdvance(name="Advance Task 7 on Alex", actor_name="Alex", task_stack_name="Task Stack 7")
snodey = StoryNode(name="Action Y", biasweight=0, tags={"Type":"Placeholder"}, charcount=1, effects_on_next_ws=[])

# Situation: Bonnie wants Alex to do some matchmaking.
# Task is complete if Carol and Diane loves each other.
# Task is failed if Carol hates Diane or if Diane hates Carol

carol_loves_diane_two_way = HasEdgeTest(object_from_test=carol, edge_name_test="loves", object_to_test=diane, soft_equal=True, two_way=True)
carol_hates_diane = HasEdgeTest(object_from_test=carol, edge_name_test="hates", object_to_test=diane, soft_equal=True)
diane_hates_carol = HasEdgeTest(object_from_test=carol, edge_name_test="hates", object_to_test=diane, soft_equal=True)

test_task_1 = CharacterTask(task_name="Test Task 1", task_actions=[snodea, snodeb], task_location_name="Village", goal_state=[carol_loves_diane_two_way], avoidance_state=[carol_hates_diane, diane_hates_carol])
test_task_2 = CharacterTask(task_name="Test Task 2", task_actions=[snodec, snoded], task_location_name="Village", goal_state=[carol_loves_diane_two_way], avoidance_state=[carol_hates_diane, diane_hates_carol])
test_task_3 = CharacterTask(task_name="Test Task 3", task_actions=[snodee, snodef], task_location_name="Village", goal_state=[carol_loves_diane_two_way], avoidance_state=[carol_hates_diane, diane_hates_carol])
test_stack_7 = TaskStack(stack_name="Test Stack 7", task_stack=[test_task_1, test_task_2, test_task_3], task_stack_requirement=[], stack_giver_name="Bonnie", stack_owner_name="Alex")

task_change_object_2 = TaskChange("Get TS7", task_giver_name="Bonnie", task_owner_name="Alex", task_stack=test_stack_7)
snodex = StoryNode(name="Action X", biasweight=0, tags={"Type":"Placeholder"}, charcount=1, target_count=1, effects_on_next_ws=[task_change_object_2])

test_sg_2 = StoryGraph("Test SG 2", character_objects=[alex, bonnie, carol, diane, edgar], location_objects=[village, castle], starting_ws=test_ws_2)

test_sg_2.insert_joint_node(joint_node=snodex, main_actor=alex, targets=[bonnie], location=village)
test_sg_2.print_all_node_beautiful_format()

print("Task Stack Info", test_sg_2.find_last_step_of_task_stack_from_actor(task_stack_name="Test Stack 7", actor_name="Alex", verbose=True))
print("The task should be able to be advanced because there's no other condition:", test_sg_2.test_task_completeness(task_stack_name="Test Stack 7", actor_name="Alex", abs_step=1))

#Here, we will change the world state and make the task already complete / already failed
test_ws_2.doubleconnect(nodeA=carol, edge_name="loves", nodeB=diane)
print("Condition is already complete, so we should see task_already_completed:", test_sg_2.test_task_completeness(task_stack_name="Test Stack 7", actor_name="Alex", abs_step=1))

test_ws_2.disconnect(from_node=carol, edge_name="loves", to_node=diane, soft_equal=True)
test_ws_2.connect(from_node=carol, edge_name="hates", to_node=diane)

print("Since they hate each other, now the task is already failed:", test_sg_2.test_task_completeness(task_stack_name="Test Stack 7", actor_name="Alex", abs_step=1))

#But what if the task doesn't exist???
test_ws_2.disconnect(from_node=diane, edge_name="loves", to_node=carol, soft_equal=True)
test_ws_2.disconnect(from_node=carol, edge_name="hates", to_node=diane, soft_equal=True)
print("This task name doesn't exist:", test_sg_2.test_task_completeness(task_stack_name="Weird Task", actor_name="Alex", abs_step=1))

#Okay, and what if the task wants you to go to the wrong location?
test_ws_2.disconnect(from_node=village, edge_name="holds", to_node=alex, soft_equal=True)
test_ws_2.connect(from_node=castle, edge_name="holds", to_node=alex)
print("Looks like we're having a wrong location here:", test_sg_2.test_task_completeness(task_stack_name="Test Stack 7", actor_name="Alex", abs_step=1))

test_ws_2.connect(from_node=village, edge_name="holds", to_node=alex)
test_ws_2.disconnect(from_node=castle, edge_name="holds", to_node=alex, soft_equal=True)
#And what if we want to advance the task before the final step?

# sg2test = test_sg_2.make_state_at_step(stopping_step=0)
# alex_1 = sg2test.node_dict["Alex"]
# for thing in alex_1.list_of_task_stacks:
#     print("SG0", thing.stack_name)

# sg2test = test_sg_2.make_state_at_step(stopping_step=1)
# alex_1 = sg2test.node_dict["Alex"]
# for thing in alex_1.list_of_task_stacks:
#     print("SG1", thing.stack_name)

# sg2test = test_sg_2.make_state_at_step(stopping_step=2)
# alex_1 = sg2test.node_dict["Alex"]
# for thing in alex_1.list_of_task_stacks:
#     print("SG2", thing.stack_name)

# sg2test = test_sg_2.make_state_at_step(stopping_step=3)
# alex_1 = sg2test.node_dict["Alex"]
# for thing in alex_1.list_of_task_stacks:
#     print("SG2", thing.stack_name)

# test_sg_2.add_story_part(part=snodey, character=alex, location=village)

test_sg_2.attempt_advance_task_stack(task_stack_name="Test Stack 7", actor_name="Alex", abs_step=1)
test_sg_2.print_all_node_beautiful_format()

print("But we've already advanced task on Step 2!:", test_sg_2.test_task_completeness(task_stack_name="Test Stack 7", actor_name="Alex", abs_step=0))

# #Okay, but what if we want to advance a task stack that's already cleared

#Hey, I think this means attempt_advance_task_stack works as intended so we don't have to test it anymore. Wahehey!
test_sg_2.attempt_advance_task_stack(task_stack_name="Test Stack 7", actor_name="Alex", abs_step=3)
test_sg_2.print_all_node_beautiful_format()
test_sg_2.attempt_advance_task_stack(task_stack_name="Test Stack 7", actor_name="Alex", abs_step=5)
test_sg_2.add_story_part(part=snodey, character=alex, location=village)
test_sg_2.print_all_node_beautiful_format()

print("Whoops! Looks like this task stack is already completed:", test_sg_2.test_task_completeness(task_stack_name="Test Stack 7", actor_name="Alex", abs_step=3))