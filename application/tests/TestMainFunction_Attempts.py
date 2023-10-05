#attempt_apply_rule
import sys
sys.path.insert(0,'')

from application.StoryGeneration_NewFlowchart import attempt_apply_rule
from application.components.ConditionTest import HasTagTest
from application.components.RewriteRuleWithWorldState import RewriteRule
from application.components.StoryGraphTwoWS import StoryGraph
from application.components.StoryNode import StoryNode
from application.components.StoryObjects import CharacterNode, LocationNode
from application.components.UtilityEnums import GenericObjectNode
from application.components.WorldState import WorldState


node_a = StoryNode(name="Node A")
node_b = StoryNode(name="Node B")
node_c = StoryNode(name="Node C")
node_d = StoryNode(name="Node D")
node_e = StoryNode(name="Node E")
node_f = StoryNode(name="Node F")
node_g = StoryNode(name="Node G")

not_warrior_tag = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Job", value="Warrior", inverse=True)
bad_1 = StoryNode(name="Bad_1", required_test_list=[not_warrior_tag])
bad_2 = StoryNode(name="Bad_2", required_test_list=[not_warrior_tag])

alice = CharacterNode(name="Alice", tags={"Type":"Character", "Job":"Warrior"})
town = LocationNode(name = "Town")

state_1 = WorldState(name="State 1", objectnodes=[alice, town])
state_1.connect(from_node=town, edge_name="holds", to_node=alice)

graph_1 = StoryGraph(name="Graph 1", character_objects=[alice], location_objects=[town], starting_ws = state_1)

graph_1.insert_multiple_parts(part_list=[node_a, node_b, node_c], character=alice, location_list=[town, town, town])

rule_b_to_de = RewriteRule(story_condition=[node_b], story_change=[node_d, node_e], remove_before_insert=True)
rule_c_to_fg = RewriteRule(story_condition=[node_c], story_change=[node_f, node_g], remove_before_insert=True)
rule_b_to_bad1 = RewriteRule(story_condition=[node_b], story_change=[bad_1])
rule_c_to_bad2 = RewriteRule(story_condition=[node_c], story_change=[bad_2])

# rule_attempt = graph_1.check_continuation_validity(actor=alice, abs_step_to_cont_from=0, cont_list=[node_d, node_e], target_list=None, purge_count=2)
rule_attempt = attempt_apply_rule(rule_object=rule_b_to_de, perform_index=1, target_story_graph=graph_1, character_object=alice, shortest_path_charname_list=["alice"])
# rule_attempt = graph_1.apply_rewrite_rule(rule=rule_b_to_de, character=alice, abs_step=1, verbose=True)
print(rule_attempt)