import sys

sys.path.insert(0,'')

from application.components.StoryObjects import CharacterNode, LocationNode, ObjectNode
from application.components.WorldState import WorldState
from application.components.StoryGraphTwoWS import StoryGraph
from application.components.StoryNode import StoryNode

alice = CharacterNode("Alice")
bob = CharacterNode("Bob")
charlie = CharacterNode("Charlie")
daniel = CharacterNode("Daniel")

town = LocationNode("Town")

testws = WorldState("TestWS", objectnodes=[alice, bob, charlie, daniel, town])
testws.connect(from_node=town, edge_name="holds", to_node=alice)
testws.connect(from_node=town, edge_name="holds", to_node=bob)
testws.connect(from_node=town, edge_name="holds", to_node=charlie)
testws.connect(from_node=town, edge_name="holds", to_node=daniel)

node_a = StoryNode(name="Test Node A")
node_b = StoryNode(name="Test Node B")

story_graph = StoryGraph(name="Graph", character_objects=[alice, bob, charlie, daniel], location_objects=[town], starting_ws=testws)

story_graph.insert_multiple_parts(part_list=[node_a, node_b], character=alice, location_list=[town, town])

print(story_graph.test_if_anyone_in_list_has_adjacent_duped_node_with_given_name(actor_list=[alice], dupe_node_name="Test Node A"))
