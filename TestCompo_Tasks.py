#SCENARIO:

# There are three characters, Alice, Bob, Charlie
# Alice is the Player Character
# Bob is the Quest Giver who wants to give a present to a Friend.
# Charlie is Bob's Friend.
#
# The task: Give present to Charlie
# Scenario 1: The task is in the same location, so the return location should be the same.
# Secnario 2: The task is in an adjacent location, so the return location should be the adjacent location.
# Scenario 3: The task is in a distant location, so the return location should be an adjacent location which is closer to the task.
# Scenario 4: The task is nowhere to be found in the worldstate, so the return location should be the same, or adjacent.

from components.CharacterTask import *
from components.StoryObjects import *
from components.WorldState import *

alice = CharacterNode("Alice")
bob = CharacterNode("Bob")
charlie = CharacterNode("Charlie")

#The Map
#
# Ambertown <-> Borough <-> Cold Village <-> Death Desert
# Cold Village <-> Easelton
# Death Desert <-> Easelton
#
# Funhouse is not connected to any of the other locations.
#
# Scenario 1: Alice and Task are in Cold Village (Expected to stay in Cold Village)
# Scenario 2: Alice is in Cold Village, task is in Borough (Expected to move to Borough)
# Scenario 3: Alice is in Cold Village, task is in Ambertown (Expected to move to Borough)
# Scenario 4: Alice has no location specific tasks (Expected to randomly move between Borough, Colton, Deathstar, Easelton)
# Secnario 5: Alice's task is in Funhouse, which currently cannot be reached (Expected to randomly move between Borough, Colton, Deathstar, Easelton)

ambertown = LocationNode("Amberton")
borough = LocationNode("Borough")
colton = LocationNode("Colton")
deathstar = LocationNode("Deathstar")
easelton = LocationNode("Easelton")
funhouse = LocationNode("Funhouse")

test_ws = WorldState("test_ws", [alice, bob, charlie, ambertown, borough, colton, deathstar, easelton, funhouse])
test_ws.doubleconnect(nodeA = ambertown, edge_name=test_ws.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=borough)
test_ws.doubleconnect(nodeA = borough, edge_name=test_ws.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=colton)
test_ws.doubleconnect(nodeA = colton, edge_name=test_ws.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=easelton)
test_ws.doubleconnect(nodeA = colton, edge_name=test_ws.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=deathstar)
test_ws.doubleconnect(nodeA = deathstar, edge_name=test_ws.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=easelton)

test_ws.connect(from_node = colton, edge_name=test_ws.DEFAULT_HOLD_EDGE_NAME, to_node = alice)
test_ws.connect(from_node = colton, edge_name=test_ws.DEFAULT_HOLD_EDGE_NAME, to_node = bob)

wait = StoryNode(name="Wait", biasweight=0, tags= {"Type":"Placeholder"}, charcount=1)

scenario_1_task = CharacterTask(task_name="Colton Task", task_location_name="Colton", task_giver_name="Bob", task_actions=[wait])
scenario_2_task = CharacterTask(task_name="Borough Task", task_location_name="Borough", task_giver_name="Bob", task_actions=[wait])
scenario_3_task = CharacterTask(task_name="Amberton Task", task_location_name="Amberton", task_giver_name="Bob", task_actions=[wait])
scenario_4_task = CharacterTask(task_name="Nothingburger Task", task_location_name=None, task_giver_name="Bob", task_actions=[wait])
scenario_5_task = CharacterTask(task_name="Funhouse Task", task_location_name="Funhouse", task_giver_name="Bob", task_actions=[wait])

scenario_1_stack = TaskStack(stack_name="Scenario 1 TaskStack", task_stack=[scenario_1_task])
scenario_2_stack = TaskStack(stack_name="Scenario 2 TaskStack", task_stack=[scenario_2_task])
scenario_3_stack = TaskStack(stack_name="Scenario 3 TaskStack", task_stack=[scenario_3_task])
scenario_4_stack = TaskStack(stack_name="Scenario 4 TaskStack", task_stack=[scenario_4_task])
scenario_5_stack = TaskStack(stack_name="Scenario 5 TaskStack", task_stack=[scenario_5_task])

#In addition to stacks with only one task, we will test stacks with more than one task to ensure that the program understands what the current task is.
long_stack = TaskStack(stack_name="Scenario 1 TaskStack", task_stack=[scenario_1_task, scenario_2_task, scenario_3_task])

print("Testing Current Taskness")
print("1st Current Task (Expected Colton Task):", long_stack.get_current_task().task_name)
print("Advance Task")
long_stack.mark_current_task_as_complete()
print("2nd Current Task (Expected Borough Task):", long_stack.get_current_task().task_name)
print("Advance Task")
long_stack.mark_current_task_as_complete()
print("3rd Current Task (Expected Amberton Task):", long_stack.get_current_task().task_name)
print("Advance Task")
long_stack.mark_current_task_as_complete()
print("After marking all tasks as complete, the current task should be None:", long_stack.get_current_task())
print("-----")

#Next, we will give Alice different tasks and looking for where to go next.
print("Adding Scenario 1 Task to Alice")
alice.add_task_stack(scenario_1_stack)
print("Expected result when calling function to look for nearest task: Current Location (Colton)")
opt_loc = test_ws.get_optimal_location_towards_task(alice, verbose=True)
print("Optimal Location:", opt_loc.get_name())

print("-----")
print("Remove Scenario 1, Add Scenario 2")
alice.remove_task_stack(scenario_1_stack.stack_name)
alice.add_task_stack(scenario_2_stack)
print("Expected result when calling function to look for nearest task: Adj. Loc with Task (Borough)")
opt_loc = test_ws.get_optimal_location_towards_task(alice, verbose=True)
print("Optimal Location:", opt_loc.get_name())

print("-----")
print("Remove Scenario 2, Add Scenario 3")
alice.remove_task_stack(scenario_2_stack.stack_name)
alice.add_task_stack(scenario_3_stack)
print("Expected result when calling function to look for nearest task: Adj. Loc closest to Task (Borough)")
opt_loc = test_ws.get_optimal_location_towards_task(alice, verbose=True)
print("Optimal Location:", opt_loc.get_name())

print("-----")
print("Remove Scenario 3, Add Scenario 4")
alice.remove_task_stack(scenario_3_stack.stack_name)
alice.add_task_stack(scenario_4_stack)
print("Expected result when calling function to look for nearest task: Random Movement (Colton, Borough, Deathstar, Easelton)")
opt_loc = test_ws.get_optimal_location_towards_task(alice, verbose=True)
print("Optimal Location:", opt_loc.get_name())

print("-----")
print("Remove Scenario 4, Add Scenario 5")
alice.remove_task_stack(scenario_4_stack.stack_name)
alice.add_task_stack(scenario_5_stack)
print("Expected result when calling function to look for nearest task: Random Movement (Colton, Borough, Deathstar, Easelton)")
opt_loc = test_ws.get_optimal_location_towards_task(alice, verbose=True)
print("Optimal Location:", opt_loc.get_name())