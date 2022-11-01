#In this scenario, we will test the scenario where only two world states are kept and check if we can find the state of a middle timestep with this.

# Step 1: Alice takes House Keys
# Step 2: Alice goes to Cafe

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
from typing import final
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

init_state.connect(home, "holds", house_keys)
init_state.connect(home, "holds", alice)
init_state.connect(cafe, "holds", coffee)

final_state = deepcopy(init_state)
final_state.name = "Latest State"

print("========== State #1 ==========")
final_state.print_all_nodes()
final_state.print_all_edges()

list_of_state_changes = []

#Perform Step 2, add stuff to list of state changes, update final state, print to see it's proper
first_state_change = []
alice_has_key = Edge("holds", alice, house_keys)
home_has_key = Edge("holds", home, house_keys)
add_alice_has_key = RelChange("add_alice_has_key", alice, alice_has_key, house_keys, "add")
rem_home_has_key = RelChange("rem_home_has_key", home, home_has_key, house_keys, "remove")
first_state_change.append(add_alice_has_key)
first_state_change.append(rem_home_has_key)
list_of_state_changes.append(first_state_change)

for sc in first_state_change:
    final_state.apply_relationship_change(sc)

print("========== State #2 ==========")
final_state.print_all_nodes()
final_state.print_all_edges()

#Perform Step 3, add stuff to list of state changes, update final state, print to see it's proper
second_state_change = []
cafe_has_alice = Edge("holds", cafe, alice)
home_has_alice = Edge("holds", home, alice)
add_cafe_has_alice = RelChange("add_cafe_has_alice", cafe, cafe_has_alice, alice, "add")
rem_home_has_alice = RelChange("rem_home_has_alice", home, home_has_alice, alice, "remove")
second_state_change.append(add_cafe_has_alice)
second_state_change.append(rem_home_has_alice)
list_of_state_changes.append(second_state_change)

for sc in second_state_change:
    final_state.apply_relationship_change(sc)

print("========== State #3 ==========")
final_state.print_all_nodes()
final_state.print_all_edges()

#Check what the world state in Step 2 looks like, print to see that it's the same as when State 2 was introduced
stopping_step = 1 #the 2nd step is at index 1
traveling_state = deepcopy(init_state)

for index in range(0, stopping_step):
    for change in list_of_state_changes[index]:
        traveling_state.apply_relationship_change(change)

print("========== State #2 (built from list of relchanges) ==========")
traveling_state.print_all_nodes()
traveling_state.print_all_edges()

#Add Wallet to the Initial World State, and then insert a list with RelChange that would make Alice pick up Wallet in Step 2,
#pushing the original 2 and 3 away to be 3 and 4.

print("We will add 2 steps here.")
print("After Alice grabs Keys, she will also grab Wallet. Also, Wallet will be added to the initial state.")
print("We will also add the final state where Alice picks up the coffee.")

after_keys_state_change = []

wallet = ObjectNode("Wallet")

init_state.add_node(wallet)
init_state.connect(home, "holds", wallet)

alice_has_wallet = Edge("holds", alice, wallet)
home_has_wallet = Edge("holds", home, wallet)

add_alice_has_wallet = RelChange("add_alice_has_wallet", alice, alice_has_wallet, wallet, "add")
rem_home_has_wallet = RelChange("rem_home_has_wallet", home, home_has_wallet, wallet, "remove")

after_keys_state_change.append(add_alice_has_wallet)
after_keys_state_change.append(rem_home_has_wallet)

list_of_state_changes.insert(1, after_keys_state_change)

after_arrive_cafe_state_change = []

#Add a 5th step where Alice takes the coffee too.

alice_has_coffee = Edge("holds", alice, coffee)
cafe_has_coffee = Edge("holds", cafe, coffee)

add_alice_has_coffee = RelChange("alice_has_coffee", alice, alice_has_coffee, coffee, "add")
rem_cafe_has_coffee = RelChange("rem_cafe_has_coffee", cafe, cafe_has_coffee, coffee, "remove")

after_arrive_cafe_state_change.append(add_alice_has_coffee)
after_arrive_cafe_state_change.append(rem_cafe_has_coffee)

list_of_state_changes.append(after_arrive_cafe_state_change)

#Check the state of each steps using partial update techniques to see if the WS comes out right.

final_state_2 = deepcopy(init_state)
final_state_2.name = "Latest State"

print("========== State #", index, "After Adding Wallet and Coffee Actions ==========")
final_state_2.print_all_nodes()
final_state_2.print_all_edges()

for index in range(0, len(list_of_state_changes)):
    for change in list_of_state_changes[index]:
        final_state_2.apply_relationship_change(change)
    print("========== State #", index, "After Adding Wallet and Coffee Actions ==========")
    final_state_2.print_all_nodes()
    final_state_2.print_all_edges()