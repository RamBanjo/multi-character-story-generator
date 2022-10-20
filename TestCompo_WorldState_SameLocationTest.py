from components.WorldState import WorldState
from components.StoryObjects import *

kitchen = LocationNode("Kitchen")
pot = ObjectNode("Pot")
kettle = ObjectNode("Kettle")

bedroom = LocationNode("Bedroom")
pillow = ObjectNode("Pillow")
blanket = ObjectNode("Blanket")

ws = WorldState("my WorldState", [kitchen, pot, kettle, bedroom, pillow, blanket])
ws.connect(kitchen, "holds", pot)
ws.connect(kitchen, "holds", kettle)
ws.connect(bedroom, "holds", pillow)
ws.connect(bedroom, "holds", blanket)

ws.doubleconnect(kitchen, "adjacent_to", bedroom)

list_of_locations = ws.make_list_of_nodes_from_tag("Type", "Location")

print("List of Locations:")
for node in list_of_locations:
    print(node)

print()

list_of_things_at_kitchen = kitchen.get_list_of_things_held_by_this_item()

print("List of Kitchen Stuff:")
for node in list_of_things_at_kitchen:
    print(node)

print()

print("Test same Location")
print("Pot and Kettle Same Loc (Expect True):", WorldState.check_items_in_same_location([pot, kettle]))
print("Kettle and Pot Same Loc (Expect True):", WorldState.check_items_in_same_location([kettle, pot]))
print("Pot and Pot Same Loc (Expect True):", WorldState.check_items_in_same_location([pot, pot]))
print("Pot and Blanket Same Loc (Expect False):", WorldState.check_items_in_same_location([pot, blanket]))
print("Pot and Pillow Same Loc (Expect False):", WorldState.check_items_in_same_location([pot, pillow]))

#Yes, same location can now be checked! Now we will need to handle checking if a character is holding something that has a certain tag.

alice = CharacterNode("Alice")
sword = ObjectNode("Sword", tags = {"Type": "Weapon"})

bob = CharacterNode("Bob")
donut = ObjectNode("Donut", tags = {"Type": "Food"})

ws.add_nodes([alice, sword, bob, donut])
ws.connect(alice, "holds", sword)
ws.connect(bob, "holds", donut)

print()
print("Test held item verification")
print("Test Alice holding Weapon (Expect True):", alice.check_if_this_item_holds_item_with_tag("Type", "Weapon"))
print("Test Bob holding Food (Expect True):", bob.check_if_this_item_holds_item_with_tag("Type", "Food"))
print("Test Alice holding Food (Expect False):", alice.check_if_this_item_holds_item_with_tag("Type", "Food"))
print("Test Bob holding Weapon (Expect False):", bob.check_if_this_item_holds_item_with_tag("Type", "Weapon"))

#Next goal on the list: Create object representation of these things so that we can run a checklist of these checks.
# For example:
# HeldItemTagTest(alice, "Type", "Weapon")
# SharedLocationTest([])

# A new class called Tests? And then we can make a list of Tests and stick them into the world state
# Tests should also be able to benefit from the Generic Object Types implemented in RelChange