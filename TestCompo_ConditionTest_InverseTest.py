from components.WorldState import WorldState
from components.StoryObjects import *
from components.ConditionTest import *

alice = CharacterNode("Alice")
bob = CharacterNode("Bob")
charlie = CharacterNode("Charlie")

sword = ObjectNode("Sword", {"Type": "Weapon"})
book = ObjectNode("Book", {"Type": "Knowledge"})

alice_house = LocationNode("Alice House")
bob_house = LocationNode("Bob House")
charlie_house = LocationNode("Charlie House")
town_square = LocationNode("Town Square")

test_ws = WorldState("Test WS", [alice, bob, charlie, sword, alice_house, bob_house, charlie_house, town_square])

test_ws.connect(alice, "dislikes", bob)
test_ws.connect(bob, "knows", alice)
test_ws.doubleconnect(bob, "likes", charlie)

test_ws.connect(charlie, "holds", sword)

test_ws.doubleconnect(alice_house, "adjacent_to", town_square)
test_ws.doubleconnect(bob_house, "adjacent_to", town_square)
test_ws.doubleconnect(charlie_house, "adjacent_to", town_square)

test_ws.connect(bob_house, "holds", bob)
test_ws.connect(bob_house, "holds", charlie)
test_ws.connect(bob_house, "holds", book)
test_ws.connect(alice_house, "holds", alice)

#Tests:
#Has Edge Inverse
#Test that Alice does not like Bob: True
#Test that Charlie does not like Bob: 
inverse_edge_a = HasEdgeTest(alice, "likes", bob, inverse=True)
inverse_edge_b = HasEdgeTest(charlie, "likes", bob, inverse=True)

print("Test that Alice does not like Bob (Expect True):", test_ws.test_story_compatibility_with_conditiontest(inverse_edge_a))
print("Test that Charlie does not like Bob (Expect False):", test_ws.test_story_compatibility_with_conditiontest(inverse_edge_b))

#Has Double Edge Inverse
#Test that Alice House is not Double adjacent_to Charlie House: True
#Test that Alice House is not Double adjacent_to Town Square: False
inverse_double_a = HasEdgeTest(alice_house, "adjacent_to", charlie_house, inverse=True, two_way=True)
inverse_double_b = HasEdgeTest(alice_house, "adjacent_to", town_square, inverse=True, two_way=True)

print("Test that Alice House is not Double adjacent_to Charlie House (Expect True):", test_ws.test_story_compatibility_with_conditiontest(inverse_double_a))
print("Test that Alice House is not Double adjacent_to Town Square (Expect False):", test_ws.test_story_compatibility_with_conditiontest(inverse_double_b))

#Carry Item Inverse
#Test that Alice is not carrying a weapon: True
#Test that Bob is not carrying a weapon: False
inverse_carry_a = HeldItemTagTest(alice, "Type", "Weapon", inverse=True)
inverse_carry_b = HeldItemTagTest(charlie, "Type", "Weapon", inverse=True)

print("Test that Alice is not carrying (Type: Weapon) (Expect True):", test_ws.test_story_compatibility_with_conditiontest(inverse_carry_a))
print("Test that Charlie is not carrying (Type: Weapon) (Expect False):", test_ws.test_story_compatibility_with_conditiontest(inverse_carry_b))

#Same Location 
#Test that Bob, Charlie, and Alice are not in the same location: True
#Test that Bob, Charlie, and Book are not in the same location: False
inverse_location_a = SameLocationTest([bob, charlie, alice], inverse=True)
inverse_location_b = SameLocationTest([bob, charlie, book], inverse=True)

print("Test that Bob, Charlie, and Alice are not in the same location (Expect True):", test_ws.test_story_compatibility_with_conditiontest(inverse_location_a))
print("Test that Bob, Charlie, and Book are not in the same location. (Expect False):", test_ws.test_story_compatibility_with_conditiontest(inverse_location_b))