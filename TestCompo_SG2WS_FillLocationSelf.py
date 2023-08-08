from typing import Generic
from components.ConditionTest import HasEdgeTest, SameLocationTest
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

move_to_shop = RelChange("move_towards_shop", shop, "holds", GenericObjectNode.GENERIC_ACTOR, ChangeAction.ADD)
move_away = RelChange("move_away_from_cur_loc", GenericObjectNode.GENERIC_LOCATION, "holds", GenericObjectNode.GENERIC_ACTOR, ChangeAction.REMOVE)
double_edge_shop = HasEdgeTest(GenericObjectNode.GENERIC_LOCATION, "adjacent_to", shop, two_way=True)

go_shop = StoryNode("Go to Shop", None, {"Type": "movement"}, 1, effects_on_next_ws=[move_away, move_to_shop], required_test_list=[double_edge_shop])

present_pickup_add = RelChange("present_pickup_add", GenericObjectNode.GENERIC_ACTOR, "holds", birthdaypresent, ChangeAction.ADD)
present_pickup_rem = RelChange("present_pickup_rem", GenericObjectNode.GENERIC_LOCATION, "holds", birthdaypresent, ChangeAction.REMOVE)
actor_in_same_room_as_present = SameLocationTest([GenericObjectNode.GENERIC_ACTOR, birthdaypresent])

get_present = StoryNode("Get Present", None, {"Type" "item_pickup"}, 1, effects_on_next_ws=[present_pickup_add, present_pickup_rem], required_test_list=[actor_in_same_room_as_present])

move_to_alicehouse = RelChange("move_towards_ahouse", alicehouse, "holds", GenericObjectNode.GENERIC_ACTOR, ChangeAction.ADD)
double_edge_alicehouse = HasEdgeTest(GenericObjectNode.GENERIC_LOCATION, "adjacent_to", alicehouse, two_way=True)

go_to_alicehouse = StoryNode("go_to_alicehouse", None, {"Type": "movement"}, 1, effects_on_next_ws=[move_to_alicehouse, move_away], required_test_list=[double_edge_alicehouse])

mystory = StoryGraph("Bob Gets Birthday Present for Alice", [bob], [bobhouse, shop, alicehouse], init_ws)

mystory.add_story_part(go_shop, bob, 0, targets=[shop])
mystory.add_story_part(get_present, bob, 0, targets=[birthdaypresent])
mystory.add_story_part(go_to_alicehouse, bob, 0, targets=[alicehouse])

mystory.refresh_longest_path_length()

print("Longest Path Length:",mystory.longest_path_length)

mystory.fill_in_locations_on_self()

mystory.update_list_of_changes()

# index = 0

# for change_at_step in mystory.list_of_changes:
#     for change in change_at_step:
#         print("Step", index, change.name)

#     index += 1

# ws1 = mystory.make_state_at_step(1)
# ws2 = mystory.make_state_at_step(2)
# ws3 = mystory.make_state_at_step(3)
#mystory.fill_in_locations_on_self()

print("First Location Name:", mystory.story_parts[("Bob", 0)].get_location())
print("Second Location Name:",mystory.story_parts[("Bob", 1)].get_location())
print("Third Location Name:",mystory.story_parts[("Bob", 2)].get_location())
