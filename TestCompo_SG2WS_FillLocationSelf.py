from components.RelChange import RelChange
from components.StoryGraphTwoWS import StoryGraph
from components.StoryNode import StoryNode
from components.StoryObjects import CharacterNode, LocationNode, ObjectNode
from components.WorldState import WorldState
from components.UtilityEnums import *

# Consider this scenario: Bob moves from his home to the shop, buys something there, and then moves to Alice's house.
# In step 0, Bob is at home and will move to the Shop.
# In step 1, Bob is at the shop, and will buy things.
# In step 2, Bob is at the shop, and will move to Alice's home.
# In step 3, Bob is at Alice's home.

bob = CharacterNode("Bob")
bobhouse = LocationNode("Bob's House")
shop = LocationNode("Shop")
birthdaypresent = ObjectNode("Birthday Present")
alicehouse = LocationNode("Alice's House")

init_ws = WorldState("First World State", [bob, bobhouse, shop, birthdaypresent, alicehouse])

init_ws.connect(shop, "holds", birthdaypresent)
init_ws.connect(bobhouse, "holds", bob)
init_ws.doubleconnect(bobhouse, "adjacent_to", alicehouse)
init_ws.doubleconnect(bobhouse, "adjacent_to", shop)
init_ws.doubleconnect(alicehouse, "adjacent_to", shop)

go_shop = StoryNode("Go to Shop", None, None, {"Type": "Movement"}, 1, effects_on_next_ws=[RelChange("move_away_from_cur_loc", GenericObjectNode.GENERIC_LOCATION, )])