import sys
sys.path.insert(0,'')

from application.components.ConditionTest import TagValueInRangeTest
from application.components.RelChange import RelativeTagChange, RelativeBiasChange
from application.components.StoryObjects import CharacterNode, LocationNode
from application.components.WorldState import WorldState

alice = CharacterNode(name="Alice", tags={"Type":"Character", "FunnyNumber":69})
someplace = LocationNode(name="Hell")

test_ws = WorldState(name="Test WS", objectnodes=[alice, someplace])

test_ws.connect(from_node=someplace, edge_name="holds", to_node=alice)

alice_from_ws = test_ws.node_dict["Alice"]
print("Alice Funny Number Value:", alice_from_ws.tags["FunnyNumber"])

print("We make the funny number a bit less funny by adding 1 to it.")

change_tag_value_plus_1 = RelativeTagChange(name="Unfunny Number", object_node_name="Alice", tag="FunnyNumber", value_delta=+1)
test_ws.apply_some_change(change_tag_value_plus_1)

print("Alice Funny Number Value:", alice_from_ws.tags["FunnyNumber"])

print("We make the number funny again, minus 1")
change_tag_value_minus_1 = RelativeTagChange(name="Funny Number", object_node_name="Alice", tag="FunnyNumber", value_delta=-1)
test_ws.apply_some_change(change_tag_value_minus_1)

print("Alice Funny Number Value:", alice_from_ws.tags["FunnyNumber"])

print("Alice Bias Values:", alice_from_ws.biases)
print("Let's make Alice Lawful Evil")

lawfulbonus = RelativeBiasChange(name="Lawful Alice", object_node_name="Alice", bias="lawbias", biasvalue_delta=+50)
evilbonus = RelativeBiasChange(name="Evil Alice", object_node_name="Alice", bias="moralbias", biasvalue_delta=-50)

test_ws.apply_some_change(lawfulbonus)
test_ws.apply_some_change(evilbonus)

print("Alice Bias Values:", alice_from_ws.biases)

print("Time to test if the Funny Number is really Funny")

#This test is true
test1 = TagValueInRangeTest(object_to_test=alice, tag="FunnyNumber", value_min=50, value_max=70)
test2 = TagValueInRangeTest(object_to_test=alice, tag="FunnyNumber", value_min=69, value_max=69)

#These two are false
test3 = TagValueInRangeTest(object_to_test=alice, tag="FunnyNumber", value_min=50, value_max=60)
test4 = TagValueInRangeTest(object_to_test=alice, tag="FunnyNumber", value_min=70, value_max=80)

print("Expect True:", test_ws.test_story_compatibility_with_conditiontest(test1))
print("Expect True:", test_ws.test_story_compatibility_with_conditiontest(test2))
print("Expect False:", test_ws.test_story_compatibility_with_conditiontest(test3))
print("Expect False:", test_ws.test_story_compatibility_with_conditiontest(test4))