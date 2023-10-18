import sys

sys.path.insert(0,'')

from application.components.StoryObjects import CharacterNode, LocationNode
from application.components.WorldState import WorldState
from application.components.StoryNode import StoryNode
from application.components.RewriteRuleWithWorldState import RewriteRule
from application.components.UtilityEnums import GenericObjectNode, ChangeAction
from application.components.RelChange import TagChange
from application.components.ConditionTest import HasTagTest
from application.components.StoryGraphTwoWS import StoryGraph

alice = CharacterNode(name="Alice")
somewhere = LocationNode(name="Somewhere")

node_a = StoryNode(name="Node A")

alice_becomes_wanted = TagChange(name="Become Wanted",object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="Wanted", value="Criminal", add_or_remove=ChangeAction.ADD)
node_b = StoryNode(name="Node B", effects_on_next_ws=[alice_becomes_wanted])

node_c = StoryNode(name="Node C")

alice_is_wanted = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Wanted", value="Criminal")
node_d = StoryNode(name="Node D", required_test_list=[alice_is_wanted])

test_rule = RewriteRule(story_condition=[], story_change=[node_d])

test_ws = WorldState(name="TestWS", objectnodes=[alice, somewhere])
test_ws.connect(from_node=somewhere, edge_name="holds", to_node=alice)

test_sg = StoryGraph(name="TestSG", character_objects=[alice], location_objects=[somewhere], starting_ws=test_ws)
test_sg.insert_multiple_parts(part_list=[node_a, node_b, node_c], character=alice, location_list=[somewhere, somewhere, somewhere])

print(test_sg.check_for_pattern_in_storyline(pattern_to_test=[], character_to_extract=alice))
print("Reminder that B is where Alice starts becoming wanted")
print("Insert at Position 0 (Before Node A)",test_sg.calculate_score_from_rule_char_and_cont(actor=alice, insert_index=0, rule=test_rule))
print("Insert at Position 1 (Before Node B, After Node A)",test_sg.calculate_score_from_rule_char_and_cont(actor=alice, insert_index=1, rule=test_rule))
print("Insert at Position 2 (Before Node C, After Node B)",test_sg.calculate_score_from_rule_char_and_cont(actor=alice, insert_index=2, rule=test_rule))
print("Insert at Position 3 (After Node C)",test_sg.calculate_score_from_rule_char_and_cont(actor=alice, insert_index=3, rule=test_rule))