import sys
sys.path.insert(0,'')

from application.components.StoryGraphTwoWS import StoryGraph
from application.components.StoryNode import StoryNode
from application.components.StoryObjects import CharacterNode, LocationNode
from application.components.WorldState import WorldState


node_a = StoryNode(name="Node A")
node_b = StoryNode(name="Node B")
node_c = StoryNode(name="Node C")
node_d = StoryNode(name="Node D")
node_e = StoryNode(name="Node E")
node_f = StoryNode(name="Node F")
node_g = StoryNode(name="Node G")

alice = CharacterNode(name="Alice", tags={"Type":"Character", "Job":"Warrior"})
town = LocationNode(name = "Town")

state_1 = WorldState(name="State 1", objectnodes=[alice, town])
state_1.connect(from_node=town, edge_name="holds", to_node=alice)

graph_1 = StoryGraph(name="Graph 1", character_objects=[alice], location_objects=[town], starting_ws = state_1)

print("Initial Graph")
graph_1.insert_multiple_parts(part_list=[node_a, node_b, node_c, node_d, node_e], character=alice, location_list=[town, town, town, town, town])

print("Modification of Initial Graph")
graph_1.insert_multiple_parts(part_list=[node_f, node_g], character=alice, location_list=[town, town], absolute_step=2)

print("-----")
print("Prev Next Listing")
for part in graph_1.story_parts.values():
    print(part.name)
    print("prev:")
    for prevparts in part.previous_nodes.items():
        print(prevparts[0], prevparts[1].name)
    print("next:")
    for nextparts in part.next_nodes.items():
        print(nextparts[0], nextparts[1].name)
    print("-----")

