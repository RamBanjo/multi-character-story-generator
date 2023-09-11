# Testing the Main Function. Here are the things we need to test:

# 1. Testing if replacement rules are recognized.
# Graph starts with A-B-C. We have rules that say B -> DE and C -> FG. If we make the graph continue generating until the shortest path length of 5 is reached we would get ADEFG.
# There are also invalid rules that the main character can't do. We want to make sure the program is able to ignore those as well. B -> Bad_1 and C -> Bad_2 are invalid because those nodes are invalid for the character.
#
# 2. Testing if task is recognized.
# Graph starts with A-B-C, where A contains a TaskChange Object.
# ...performing the task would potentially put you in a different location. What if B or C travels to another node? Would doing a chart break that? I don't like the sound of this.
# I mean, it *would* make the option invalid at least if we put the proper requirements in the traveling nodes...
#
# 3. Testing if joint rules are recognized.
# Graph starts with A-B-C for two characters. There is a rule where C -> Joint Node X, Joint Node X -> Joint Node Y, and Joint Node Y -> D or E. Both characters should have the same chart.
#
# 4. Testing if scores are recognized
# Graph is A-B-C. There are 10 rules, each trying to continue C with 10 different nodes. If the scores are properly recognized, we would be able to get Top 5 only.
#
# 5. Testing if task locations are recognized
# Graph is A-B-C. Player gets a Task Stack with only one task in Location X, but they are currently in Location Z. They must travel from Z to Y and then X to do that task.
#
# 6. Like a ReGEN
# Rules, characters, and objects are based of ReGEN. There are two main characters, Alice and Bob.
# All the rules specify that they can only be done by Main Characters, so other characters will do a lot of waiting.

from StoryGeneration_NewFlowchart import attempt_apply_rule, generate_story_from_starter_graph
from components.ConditionTest import HasTagTest
from components.RewriteRuleWithWorldState import RewriteRule
from components.StoryGraphTwoWS import StoryGraph
from components.StoryNode import StoryNode
from components.StoryObjects import CharacterNode, LocationNode
from components.UtilityEnums import GenericObjectNode
from components.WorldState import WorldState

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
bob = CharacterNode(name="Alice", tags={"Type":"Character", "Job":"Fighter"})
charlie = CharacterNode(name="Alice", tags={"Type":"Character", "Job":"Bard"})
town = LocationNode(name = "Town")

state_1 = WorldState(name="State 1", objectnodes=[alice, town])
state_1.connect(from_node=town, edge_name="holds", to_node=alice)

graph_1 = StoryGraph(name="Graph 1", character_objects=[alice], location_objects=[town], starting_ws = state_1)

graph_1.insert_multiple_parts(part_list=[node_a, node_b, node_c], character=alice, location_list=[town, town, town])

rule_b_to_de = RewriteRule(name="b->de",story_condition=[node_b], story_change=[node_d, node_e], remove_before_insert=True)
rule_c_to_fg = RewriteRule(name="c->fg",story_condition=[node_c], story_change=[node_f, node_g], remove_before_insert=True)
rule_b_to_bad1 = RewriteRule(name="b->bad1",story_condition=[node_b], story_change=[bad_1])
rule_c_to_bad2 = RewriteRule(name="c->bad2",story_condition=[node_c], story_change=[bad_2])

# graph_1.print_all_node_beautiful_format()
# graph_1.refresh_longest_path_length()
# print(graph_1.get_longest_path_length_by_character(character=alice))
# print(graph_1.get_latest_story_node_from_character(character=alice))

graph_1_modded = generate_story_from_starter_graph(init_storygraph=graph_1, list_of_rules=[rule_b_to_bad1, rule_b_to_de, rule_c_to_bad2, rule_c_to_fg], required_story_length=5, top_n=5, extra_attempts=-1, verbose=True)

print("We expect the story following Story Graph to contain the following nodes for Alice: A-D-E-F-G.")
graph_1_modded.print_all_node_beautiful_format()


#TODO (Important): I think there might be something wrong with the insert functions. They might not be properly adding the "next nodes" or "previous nodes".
# We gotta test Attempt Apply Rule because apparently that thing isn't working...
