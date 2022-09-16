#In this scenario, we will test the scenario where only two world states are kept and check if we can find the state of a middle timestep with this.

# Step 1: Alice takes House Keys
# Step 2: Alice goes to Cafe
# Step 3: Alice takes Coffee

# WS1: Home holds Alice, Home holds HouseKeys, Cafe holds Coffee
# WS2: Alice holds HouseKeys, Home holds Alice, Cafe holds Coffee
# WS3: Cafe holds Alice, Alice holds HouseKeys, Cafe holds Coffee

# We will add a step where Alice picks up Wallet between Step 1 and 2, which will cause the timeline to change like this
# Step 1: Alice takes House Keys
# Step 2: Alice takes Wallet
# Step 3: Alice goes to Cafe
# Step 4: Alice takes Coffee
#
# WS1: Home holds Alice, Home holds HouseKeys, Cafe holds Coffee, Home holds Wallet
# WS2: Alice holds HouseKeys, Home holds Alice, Cafe holds Coffee, Home holds Wallet
# WS3: Alice holds HouseKeys, Home holds Alice, Cafe holds Coffee, Alice holds Wallet
# WS4: Cafe holds Alice, Alice holds HouseKeys, Cafe holds Coffee, Alice holds Wallet
#
# This is to ensure that we can change the past and use the inital step to update all nodes up up to the latest state.

# We need functions that change tags/states (characters becoming rich, poor, alive, dead, etc.)

from copy import deepcopy
from components.WorldState import WorldState
from components.StoryObjects import ObjectNode
from components.StoryObjects import CharacterNode
from components.StoryObjects import LocationNode
from components.Edge import Edge
from components.RelChange import RelChange

alice = CharacterNode("Alice")
home = LocationNode("Home")
cafe = LocationNode("Cafe")
house_keys = ObjectNode("House Keys")
coffee = ObjectNode("Coffee")

init_state = WorldState("First State", [alice, home, cafe, house_keys, coffee])
final_state = deepcopy(init_state)
final_state.name = "Latest State"

list_of_state_changes = []

#Perform Step 2, add stuff to list of state changes, update final state, print to see it's proper

#Perform Step 3, add stuff to list of state changes, update final state, print to see it's proper

#Check what the world state in Step 2 looks like, print to see that it's the same as when State 2 was introduced

#Add Wallet to the Initial World State, and then insert a list with RelChange that would make Alice pick up Wallet in Step 2, pushing the original 2 and 3 away to be 3 and 4.

#Check the state of each steps using partial update techniques to see if the WS comes out right.

#Check WS2

#Check WS3

#Check WS4