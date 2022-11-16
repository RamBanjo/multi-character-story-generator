from components.StoryGraphTwoWS import StoryGraph
from components.StoryObjects import CharacterNode, ObjectNode, LocationNode
from components.StoryNode import StoryNode
from components.WorldState import WorldState

alice = CharacterNode("Alice")
sword = ObjectNode("Sword", {"Type": "Weapon"})
forest = LocationNode("Forest")
castle = LocationNode("Castle")

bob = CharacterNode("Bob")

#Alice goes to Forest, Alice picks up sword, Alice goes back home
#The pattern we want to look for is the going to the forest and the picking up of the sword

#Bob also goes to the forest, but he's not there to take the sword, he's there to do some fishing. So, his storyline will not return true if we ask about the pattern.

go_forest = StoryNode("Go to Forest", None, None, {"Type": "movement"}, 1)
take_sword = StoryNode("Take Sword", None, None, {"Type": "gain_item"}, 1)
go_fishing = StoryNode("Go Fishing", None, None, {"Type": "hobby"}, 1)
slay_monsters = StoryNode("Slay Monsters", None, None, {"Type": "quest"}, 1)
cook_fish = StoryNode("Cook Fish", None, None, {"Type": "cooking"}, 1)

ws = WorldState("Test WS", [alice, sword, forest, castle, bob])

ws.connect(forest, "holds", sword)
ws.connect(castle, "holds", alice)
ws.connect(castle, "holds", bob)
ws.doubleconnect(forest, "is_adjacent", castle)

testsg = StoryGraph("Test Graph", [alice, bob], [forest, castle], ws)

testsg.add_story_part(go_forest, alice)
testsg.add_story_part(go_forest, bob)
testsg.add_story_part(take_sword, alice)
testsg.add_story_part(go_fishing, bob)
testsg.add_story_part(slay_monsters, alice)
testsg.add_story_part(cook_fish, bob)

print("Test if Alice is fishing and cooking fish, expected False and an empty array:", testsg.check_for_pattern_in_storyline([go_fishing, cook_fish], alice))
print("Test if Bob is fishing and cooking fish, expected True and an array with 1 member:", testsg.check_for_pattern_in_storyline([go_fishing, cook_fish], bob))