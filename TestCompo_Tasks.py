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
scenario_4_task = CharacterTask(task_name=None, task_location_name="Colton", task_giver_name="Bob", task_actions=[wait])
scenario_5_task = CharacterTask(task_name="Funhouse", task_location_name="Colton", task_giver_name="Bob", task_actions=[wait])

scenario_1_stack = TaskStack(stack_name="Scenario 1 TaskStack")