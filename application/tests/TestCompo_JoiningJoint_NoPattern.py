import sys

sys.path.insert(0,'')

from application.components.StoryObjects import CharacterNode, LocationNode, ObjectNode
from application.components.WorldState import WorldState
from application.components.StoryGraphTwoWS import StoryGraph
from application.components.StoryNode import StoryNode
from application.components.RewriteRuleWithWorldState import JoiningJointRule
from application.StoryGeneration_NewFlowchart import attempt_apply_rule

alice = CharacterNode(name="Alice", internal_id=0)
bob = CharacterNode(name="Bob", internal_id=1)
someplace = LocationNode(name="Somewhere", internal_id=2)

node_a =  StoryNode(name="Node A", biasweight=0, tags= {"Type":"Placeholder"}, charcount=1)
node_b =  StoryNode(name="Node B", biasweight=0, tags= {"Type":"Placeholder"}, charcount=1)
node_c =  StoryNode(name="Node C", biasweight=0, tags= {"Type":"Placeholder"}, charcount=1)
node_d =  StoryNode(name="Node D", biasweight=0, tags= {"Type":"Placeholder"}, charcount=1)
node_e =  StoryNode(name="Node E", biasweight=0, tags= {"Type":"Placeholder"}, charcount=1)
node_f =  StoryNode(name="Node F", biasweight=0, tags= {"Type":"Placeholder"}, charcount=1)
joint_x = StoryNode(name="Joint X", biasweight=30, tags= {"Type":"Placeholder"}, charcount=1, target_count=1)

jointrule = JoiningJointRule(base_actions=[], joint_node=joint_x, rule_name="Can a Patternless Boy and a Joint Node X fall in Love...")

world_state = WorldState(name="Test WS", objectnodes=[alice, bob, someplace])

world_state.connect(from_node=someplace, edge_name="holds", to_node=alice)
world_state.connect(from_node=someplace, edge_name="holds", to_node=bob)

testgraph = StoryGraph(name="Test Graph", character_objects=[alice, bob], location_objects=[someplace], starting_ws=world_state)

testgraph.insert_multiple_parts(part_list=[node_a, node_b, node_c], character=alice, location_list=[someplace, someplace, someplace])
testgraph.insert_multiple_parts(part_list=[node_d, node_e, node_f], character=bob, location_list=[someplace, someplace, someplace])

grouping = [{'actor_group':[alice], 'target_group':[bob]}]

# testgraph.check_joint_continuity_validity(joint_rule=jointrule, main_character=alice, grouping_split=grouping, insert_index=0, verbose=True)

print(attempt_apply_rule(rule_object=jointrule, perform_index=0, target_story_graph=testgraph, character_object=alice, shortest_path_charname_list=["Alice", "Bob"]))
testgraph.fill_in_locations_on_self()

testgraph.print_all_node_beautiful_format()