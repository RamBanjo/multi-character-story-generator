#The Situation:
#The story is the same story from SG2WS_FillLocationSelf
#However, we would like to fill in a step where Bob goes to another place, talks to Charlie, before heading to Alice's house.

from typing import Generic
from components.ConditionTest import HasDoubleEdgeTest, HasEdgeTest, SameLocationTest, HeldItemTagTest
from components.RelChange import RelChange
from components.StoryGraphTwoWS import StoryGraph
from components.StoryNode import StoryNode
from components.StoryObjects import CharacterNode, LocationNode, ObjectNode
from components.WorldState import WorldState
from components.UtilityEnums import *

bob = CharacterNode("Bob")
bobhouse = LocationNode("Bob's House")
shop = LocationNode("Shop")
birthdaypresent = ObjectNode("Birthday Present", {"Type":"Present"})
alicehouse = LocationNode("Alice's House")

init_ws = WorldState("First World State", [bob, bobhouse, shop, birthdaypresent, alicehouse])

init_ws.connect(shop, "holds", birthdaypresent)
init_ws.connect(bobhouse, "holds", bob)
init_ws.doubleconnect(bobhouse, "adjacent_to", alicehouse)
init_ws.doubleconnect(bobhouse, "adjacent_to", shop)
init_ws.doubleconnect(alicehouse, "adjacent_to", shop)

move_to_shop = RelChange("move_towards_shop", shop, "holds", GenericObjectNode.GENERIC_ACTOR, ChangeAction.ADD)
move_away = RelChange("move_away_from_cur_loc", GenericObjectNode.GENERIC_LOCATION, "holds", GenericObjectNode.GENERIC_ACTOR, ChangeAction.REMOVE)
double_edge_shop = HasDoubleEdgeTest(GenericObjectNode.GENERIC_LOCATION, "adjacent_to", shop)

go_shop = StoryNode("Go to Shop", None, None, {"Type": "movement"}, 1, effects_on_next_ws=[move_away, move_to_shop], condition_tests=[double_edge_shop])

present_pickup_add = RelChange("present_pickup_add", GenericObjectNode.GENERIC_ACTOR, "holds", birthdaypresent, ChangeAction.ADD)
present_pickup_rem = RelChange("present_pickup_rem", GenericObjectNode.GENERIC_LOCATION, "holds", birthdaypresent, ChangeAction.REMOVE)
actor_in_same_room_as_present = SameLocationTest([GenericObjectNode.GENERIC_ACTOR, birthdaypresent])

get_present = StoryNode("Get Present", None, None, {"Type" "item_pickup"}, 1, effects_on_next_ws=[present_pickup_add, present_pickup_rem], condition_tests=[actor_in_same_room_as_present])

move_to_alicehouse = RelChange("move_towards_ahouse", alicehouse, "holds", GenericObjectNode.GENERIC_ACTOR, ChangeAction.ADD)
double_edge_alicehouse = HasDoubleEdgeTest(GenericObjectNode.GENERIC_LOCATION, "adjacent_to", alicehouse)

go_to_alicehouse = StoryNode("Go to Alicehouse", None, None, {"Type": "movement"}, 1, effects_on_next_ws=[move_to_alicehouse, move_away], condition_tests=[double_edge_alicehouse])

mystory = StoryGraph("Bob Gets Birthday Present for Alice", [bob], [bobhouse, shop, alicehouse], init_ws)

mystory.add_story_part(go_shop, bob, 0, targets=[shop])
mystory.add_story_part(get_present, bob, 0, targets=[birthdaypresent])
mystory.add_story_part(go_to_alicehouse, bob, 0, targets=[alicehouse])

#The following must be true:
#   
#   On the step where Bob leaves the Shopgoes to the park:
#       - The Park (Charlie's Location) must be adjacent to the Shop (HasDoubleEdge)
#   On the step where Bob Talks to Charlie about the present:
#       - Bob must not hate Charlie (Reverse of HasEdge)
#       - Bob must have the birthday present (HeldItem: Present)
#       - Bob and Charlie must be in the same location (The Park) (SameLocation)
#   (Note that the node where Bob goes to Alice's house takes the Generic Location as the current location,
#   it can be called from the park as long as park is adjacent to Alice's House.)   
#
#   Additionally, at Alice's House, we would like Bob to give the present to Alice, this continues from the step where Bob goes to the house.
#   On the step where Bob gives the present to Alice:
#       - Bob must have the birthday present (HasEdge)
#       - Bob must like Alice (like)
#       - Bob and Alice must be in the same location (SameLocation)

alice = CharacterNode("Alice")
charlie = CharacterNode("Charlie")
park = LocationNode("Park")

move_to_park = RelChange("move_towards_shop", shop, "holds", GenericObjectNode.GENERIC_ACTOR, ChangeAction.ADD)
double_edge_park = HasDoubleEdgeTest(GenericObjectNode.GENERIC_LOCATION, "adjacent_to", park)

go_park = StoryNode("Go to Park", None, None, {"Type": "movement"}, 1, effects_on_next_ws=[move_away, move_to_park], condition_tests=[double_edge_park])

bob_not_hate_charlie = HasEdgeTest(GenericObjectNode.GENERIC_ACTOR, "hates", charlie, inverse=True)
bob_has_present = HeldItemTagTest(GenericObjectNode.GENERIC_ACTOR, "Type", "Present")
#There is no change in world state doing this action

talk_charlie = StoryNode("Talk to Charlie about Present", None, None, {"Type": "conversation"}, 2, condition_tests=[bob_not_hate_charlie, bob_has_present])

present_give_to_alice_add = RelChange("present_give_to_alice_add", alice, "holds", birthdaypresent, ChangeAction.ADD)
present_give_to_alice_rem = RelChange("present_give_to_alice_rem", GenericObjectNode.GENERIC_ACTOR, "holds", birthdaypresent, ChangeAction.REMOVE)
bob_holds_present = HasEdgeTest(GenericObjectNode.GENERIC_ACTOR, "holds", birthdaypresent)
bob_likes_alice = HasEdgeTest(GenericObjectNode.GENERIC_ACTOR, "likes", alice)
bob_same_room_alice = SameLocationTest([GenericObjectNode.GENERIC_ACTOR, alice])

give_present_to_alice = StoryNode("Give Present to Alice", None, None, {"Type": "give_item"}, 2, effects_on_next_ws=[], condition_tests=[bob_holds_present, bob_likes_alice, bob_same_room_alice])

mystory.fill_in_locations_on_self()

mystory.update_list_of_changes()

#Obviously, if we attempt to check validity before any conditions are added to the graph, then the result should be false because the requirements don't exist yet, nor do the nodes we mentioned.

insert_at_step_2 = [go_park, talk_charlie]
insert_after_last_step = [give_present_to_alice]

print("Continuation Validity before literally adding anyting to graph, expected False:", mystory.check_continuation_validity(bob, 2, insert_at_step_2))

#Now, we will add the proper conditions that will allow the graph to be acceptable. We will set up the initial worldstate in a way that enables the conditions in the nodes used.

init_ws.add_nodes([charlie, park])
init_ws.doubleconnect(park, "adjacent_to", alicehouse)
init_ws.doubleconnect(park, "adjacent_to", shop)

print("Continuation Validity after adding Charlie and Park, along with expected relations, expected True:", mystory.check_continuation_validity(bob, 2, insert_at_step_2))