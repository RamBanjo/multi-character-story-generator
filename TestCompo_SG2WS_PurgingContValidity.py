from components.StoryGraphTwoWS import StoryGraph
from components.StoryNode import StoryNode
from components.StoryObjects import *
from components.WorldState import WorldState

bob = CharacterNode("Bob")
home = LocationNode("Home")

node_a = StoryNode("Node A", None, None, {"Type":"placeholder"}, 1)
node_b = StoryNode("Node B", None, None, {"Type":"placeholder"}, 1)
node_c = StoryNode("Node C", None, None, {"Type":"placeholder"}, 1)
node_d = StoryNode("Node D", None, None, {"Type":"placeholder"}, 1)
node_e = StoryNode("Node E", None, None, {"Type":"placeholder"}, 1)

node_x = StoryNode("Node X", None, None, {"Type":"placeholder"}, 1)
node_y = StoryNode("Node Y", None, None, {"Type":"placeholder"}, 1)
node_z = StoryNode("Node Z", None, None, {"Type":"placeholder"}, 1)

insert_list = [node_x, node_y, node_z]

testws = WorldState("Test WS", [bob, home])

testws.connect(home, "holds", bob)

testgraph = StoryGraph("test graph", [bob], [home], testws)

testgraph.add_story_part(node_a, bob, home)
testgraph.add_story_part(node_b, bob, home)
testgraph.add_story_part(node_c, bob, home)
testgraph.add_story_part(node_d, bob, home)
testgraph.add_story_part(node_e, bob, home)

# testgraph.remove_parts_by_count(1, 1, bob)
# testgraph.insert_multiple_parts(insert_list, bob, absolute_step=1)

# #Expercting a, x, y, z, c, d, e
# for storypart in testgraph.story_parts:
#     print(storypart, testgraph.story_parts[storypart])

testgraph.check_continuation_validity(bob, 1, insert_list, purge_count=1)