import sys
sys.path.insert(0,'')

from application.components.StoryObjects import CharacterNode, LocationNode, ObjectNode
from application.components.WorldState import WorldState
from application.components.ConditionTest import ObjectPassesAtLeastOneTestTest, IntersectObjectExistsTest, HasEdgeTest, HasTagTest
from application.components.UtilityEnums import GenericObjectNode

alice = CharacterNode(name="Alice", tags={"Type":"Character", "Job":"Warrior", "Alive":True})
bob = CharacterNode(name="Bob", tags={"Type":"Character", "Job":"Fighter", "Alive":True})
charlie = CharacterNode(name="Charlie", tags={"Type":"Character", "Job":"Bard", "Alive":True})
david = CharacterNode(name="David", tags={"Type":"Character", "Job":"Berserker", "Alive":False, "CanRevive":True})
eddy = CharacterNode(name="Eddy", tags={"Type":"Character", "Job":"Berserker", "Alive":False, "CanRevive":False})

town_a = LocationNode("Town A")

excalibur = ObjectNode(name="Excalibur", tags={"Type":"Weapon", "Value":"Priceless"})

testws = WorldState(name="World State", objectnodes=[alice, bob, charlie, david, town_a, excalibur])

testws.connect(from_node=town_a, edge_name="holds", to_node=alice)
testws.connect(from_node=town_a, edge_name="holds", to_node=bob)
testws.connect(from_node=town_a, edge_name="holds", to_node=charlie)
testws.connect(from_node=town_a, edge_name="holds", to_node=david)

testws.connect(from_node=alice, edge_name="likes", to_node=bob)
testws.connect(from_node=bob, edge_name="likes", to_node=charlie)

testws.connect(from_node=alice, edge_name="holds", to_node=excalibur)

alice_likes_someone = HasEdgeTest(object_from_test=alice, edge_name_test="likes", object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER)
someone_likes_charlie = HasEdgeTest(object_from_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name_test="likes", object_to_test=charlie)
theres_someone_alice_likes_that_likes_charlie = IntersectObjectExistsTest(list_of_tests_with_placeholder=[alice_likes_someone, someone_likes_charlie])

alice_holds_something = HasEdgeTest(object_from_test=alice, edge_name_test="holds", object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER)
something_is_priceless = HasTagTest(object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, tag="Value", value="Priceless")
theres_something_alice_holds_thats_priceless = IntersectObjectExistsTest(list_of_tests_with_placeholder=[alice_holds_something, something_is_priceless])

#Both should return True
print(testws.test_story_compatibility_with_conditiontest(theres_someone_alice_likes_that_likes_charlie))
print(testws.test_story_compatibility_with_conditiontest(theres_something_alice_holds_thats_priceless))

someone_is_alive = HasTagTest(object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, tag="Alive", value=True)
someone_can_be_revived = HasTagTest(object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, tag="CanRevive", value=True)

alice_is_alive_or_can_be_revived = ObjectPassesAtLeastOneTestTest(list_of_tests_with_placeholder=[someone_is_alive, someone_can_be_revived], object_to_test=alice)
david_is_alive_or_can_be_revived = ObjectPassesAtLeastOneTestTest(list_of_tests_with_placeholder=[someone_is_alive, someone_can_be_revived], object_to_test=david)
eddy_is_alive_or_can_be_revived = ObjectPassesAtLeastOneTestTest(list_of_tests_with_placeholder=[someone_is_alive, someone_can_be_revived], object_to_test=eddy)

#True, True, False
print(testws.test_story_compatibility_with_conditiontest(alice_is_alive_or_can_be_revived))
print(testws.test_story_compatibility_with_conditiontest(david_is_alive_or_can_be_revived))
print(testws.test_story_compatibility_with_conditiontest(eddy_is_alive_or_can_be_revived))