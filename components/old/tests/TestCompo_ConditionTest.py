#Things that exist in the testws and can be tested:
from components.ConditionTest import HasDoubleEdgeTest, HasEdgeTest, HeldItemTagTest, SameLocationTest
from components.StoryObjects import CharacterNode, LocationNode, ObjectNode
from components.WorldState import WorldState


alice = CharacterNode("Alice")
bob = CharacterNode("Bob")
alicehouse = LocationNode("Alice's House")
bobhouse = LocationNode("Bob's House")
door = ObjectNode("Door", {"Type": "Door", "UnlockBy": "AliceHouse", "LockState": "Locked"})
doorkey = ObjectNode("Door Key", {"Type": "Key", "UnlockGroup": "AliceHouse"})

#Things that don't exist in the testws and can't be tested, therefore it will return false:

charlie = CharacterNode("Charlie")
sword = ObjectNode("Sword", {"Type": "Weapon"})
library = LocationNode("Library")

testws = WorldState("Test WS", [alice, bob, alicehouse, bobhouse, door, doorkey])

testws.doubleconnect(alicehouse, "adjacent_to", bobhouse)
testws.connect(bob, "likes", alice)
testws.connect(alice, "loves", bob)
testws.connect(alice, "holds", doorkey)
testws.connect(alicehouse, "holds", alice)
testws.connect(alicehouse, "holds", door)
testws.connect(bobhouse, "holds", bob)

#Same loc tests that should be true:
test_alice_and_door_same_loc = SameLocationTest([alice, door])
test_alice_and_charlie_same_loc = SameLocationTest([alice, charlie])

#Same loc tests that should be false:
test_alice_and_bob_same_loc = SameLocationTest([alice, bob])

#Held item tag tests that should be true:
test_alice_carries_key = HeldItemTagTest(alice, "UnlockGroup", "AliceHouse")

#Held item tag tests that should be false:
test_bob_carries_key = HeldItemTagTest(bob, "UnlockGroup", "AliceHouse")
test_charlie_carries_key = HeldItemTagTest(charlie, "UnlockGroup", "AliceHouse")
test_alice_carries_weapon = HeldItemTagTest(alice, "Type", "Weapon")

#Has Edge Tests that should be true:
test_bob_likes_alice = HasEdgeTest(bob, "likes", alice)

#Has Edge Tests that should be false:
test_bob_likes_door = HasEdgeTest(bob, "likes", door)
test_alice_likes_bob = HasEdgeTest(alice, "likes", bob)
test_bob_likes_charlie = HasEdgeTest(bob, "likes", charlie)
test_charlie_likes_bob = HasEdgeTest(charlie, "likes", bob)
test_library_holds_charlie = HasEdgeTest(library, "holds", charlie)

#Has Double Edge Tests that should be true:
test_houses_doubleconnected = HasDoubleEdgeTest(alicehouse, "adjacent_to", bobhouse)

#Has Double Edge Tests that should be false:
test_alibob_doubleconnected = HasDoubleEdgeTest(alice, "loves", bob)
test_alicharlie_doubleconnected = HasDoubleEdgeTest(alice, "loves", charlie)
test_charliebob_doubleconnected = HasDoubleEdgeTest(charlie, "loves", bob)
test_charliesword_doubleconnected = HasDoubleEdgeTest(charlie, "loves", sword)

print("Same Location Tests:")
print("Testing if Alice and Door is in the same location, expected True:", testws.test_story_compatibility_with_conditiontest(test_alice_and_door_same_loc))
print("Testing if Alice and Charlie is in the same location, expected True:", testws.test_story_compatibility_with_conditiontest(test_alice_and_charlie_same_loc))
print("Testing if Alice and Bob is in the same location, expected False:", testws.test_story_compatibility_with_conditiontest(test_alice_and_bob_same_loc))
print()
print("Carry Object with Tag Tests:")
print("Testing if Alice carries UnlockGroup: AliceHouse, expected True:", testws.test_story_compatibility_with_conditiontest(test_alice_carries_key))
print("Testing if Bob carries UnlockGroup: AliceHouse, expected False:", testws.test_story_compatibility_with_conditiontest(test_bob_carries_key))
print("Testing if Charlie carries UnlockGroup: AliceHouse, expected False:", testws.test_story_compatibility_with_conditiontest(test_charlie_carries_key))
print("Testing if Alice carries Type: Weapon, expected False:", testws.test_story_compatibility_with_conditiontest(test_alice_carries_weapon))
print()
print("Has Edge Tests:")
print("Testing if Bob likes Alice, Expecting True:", testws.test_story_compatibility_with_conditiontest(test_bob_likes_alice))
print("Testing if Bob likes Door, Expecting False:", testws.test_story_compatibility_with_conditiontest(test_bob_likes_door))
print("Testing if Alice likes Bob, Expecting False:", testws.test_story_compatibility_with_conditiontest(test_alice_likes_bob))
print("Testing if Bob likes Charlie, Expecting True:", testws.test_story_compatibility_with_conditiontest(test_bob_likes_charlie))
print("Testing if Charlie likes Bob, Expecting True:", testws.test_story_compatibility_with_conditiontest(test_charlie_likes_bob))
print("Testing if Library holds Charlie, Expecting True:", testws.test_story_compatibility_with_conditiontest(test_library_holds_charlie))
print()
print("Has Double Edge Tests:")
print("Testing if the houses are double adjacent, Expecting True:", testws.test_story_compatibility_with_conditiontest(test_houses_doubleconnected))
print("Testing if the alice and bob are double love, Expecting True:", testws.test_story_compatibility_with_conditiontest(test_alibob_doubleconnected))
print("Testing if the alice and charlie are double love, Expecting True:", testws.test_story_compatibility_with_conditiontest(test_alicharlie_doubleconnected))
print("Testing if the charlie and bob are double love, Expecting True:", testws.test_story_compatibility_with_conditiontest(test_charliebob_doubleconnected))
print("Testing if the charlie and sword are double love, Expecting True:", testws.test_story_compatibility_with_conditiontest(test_charliesword_doubleconnected))