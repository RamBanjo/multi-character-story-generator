import sys
sys.path.insert(0,'')

from application.components.StoryGraphTwoWS import StoryGraph
from application.components.StoryNode import StoryNode
from application.components.StoryObjects import CharacterNode, LocationNode
from application.components.WorldState import WorldState


alice = CharacterNode(name="Alice")
town = LocationNode(name="Town")

test_ws = WorldState(name="Test WS", objectnodes=[alice, town])

test_ws.connect(from_node=town, edge_name="holds", to_node=alice)

test_sg = StoryGraph(name = "Test SG", character_objects=[alice], location_objects=[town], starting_ws=test_ws)

snode1 = StoryNode(name="Action 1", biasweight=0, tags={"Type":"Placeholder"}, charcount=1)
snode2 = StoryNode(name="Action 2", biasweight=0, tags={"Type":"Placeholder"}, charcount=1)
snode3 = StoryNode(name="Action 3", biasweight=0, tags={"Type":"Placeholder"}, charcount=1)
snode4 = StoryNode(name="Action 4", biasweight=0, tags={"Type":"Placeholder"}, charcount=1)
snode5 = StoryNode(name="Action 5", biasweight=0, tags={"Type":"Placeholder"}, charcount=1)

test_sg.add_story_part(part=snode1, character=alice, location=town)
test_sg.add_story_part(part=snode2, character=alice, location=town)
test_sg.add_story_part(part=snode3, character=alice, location=town)
test_sg.add_story_part(part=snode4, character=alice, location=town)
test_sg.add_story_part(part=snode5, character=alice, location=town)

test_sg.print_all_nodes_from_characters_storyline(alice)

print()
print("Remove 2 nodes from Index 2")
test_sg.remove_parts_by_count(start_step=2, count=2, actor=alice)
test_sg.print_all_nodes_from_characters_storyline(alice)