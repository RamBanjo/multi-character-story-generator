#Today we are going to make a ConditionTest
#Basically that thing where if you kill someone everyone who witnesses it hates you or something
import sys
sys.path.insert(0,'')

from copy import deepcopy
from application.components.StoryObjects import *
from application.components.WorldState import *
from application.components.RelChange import *
from application.components.ConditionTest import *
from application.components.UtilityEnums import *

alice = CharacterNode(name = "Alice")
bob = CharacterNode(name = "Bob")
charlie = CharacterNode(name = "Charlie")
dave = CharacterNode(name = "Dave")
eliane = CharacterNode(name = "Eliane")
frank = CharacterNode(name = "Frank")

castle = LocationNode(name = "Castle")
town = LocationNode(name = "Town")

#The scenario: Alice kills Bob. Charlie likes Bob and is in the same location when it happened. Dave likes bob, but is in a different location. Eliane does not know Bob, and is in the same location. Frank does not know Bob, and is in a different location.
#Only Bob should start hating Alice if there is a conditional node for this.

test_ws = WorldState("Test WorldState", objectnodes=[alice, bob, charlie, dave, eliane, frank, castle, town])
test_ws.connect(from_node=alice, edge_name="hates", to_node=bob, value="murder_lover")
test_ws.connect(from_node=charlie, edge_name="friends", to_node=bob, value="profession")
test_ws.connect(from_node=dave, edge_name="friends", to_node=bob, value="profession")
test_ws.connect(from_node=eliane, edge_name="dislikes", to_node=bob, value="arrogant")
test_ws.connect(from_node=frank, edge_name="dislikes", to_node=bob, value="arrogant")

test_ws.connect(from_node=castle, edge_name="holds", to_node=alice)
test_ws.connect(from_node=castle, edge_name="holds", to_node=bob)
test_ws.connect(from_node=castle, edge_name="holds", to_node=charlie)
test_ws.connect(from_node=castle, edge_name="holds", to_node=eliane)
test_ws.connect(from_node=town, edge_name="holds", to_node=dave)
test_ws.connect(from_node=town, edge_name="holds", to_node=frank)

placeholder_friends_with_target = HasEdgeTest(object_from_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name_test="friends", object_to_test=bob, soft_equal=True)
placeholder_share_location_with_target_and_actor = SameLocationTest(list_to_test=[GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, bob])

#For now we won't be able to stack Conditional Changes, but imagine if we need to do that *shudders*
placeholder_hates_actor = RelChange(name="hate_alice", node_a=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name="hates", node_b=alice, add_or_remove=ChangeAction.ADD, value="murder_of_friend")
if_share_location_and_friends_hate_murderer = ConditionalChange(name="if share location and friends hate murderer", list_of_condition_tests=[placeholder_friends_with_target, placeholder_share_location_with_target_and_actor], list_of_changes=[placeholder_hates_actor])

# changereplaced = replace_placeholder_object_with_change_haver(placeholder_hates_actor, charlie)
# print(changereplaced.node_a)
# print(changereplaced.edge_name)
# print(changereplaced.node_b)
# print(changereplaced.value)

advanced_ws = deepcopy(test_ws)
advanced_ws.apply_conditional_change(if_share_location_and_friends_hate_murderer, test_ws)

advanced_ws.print_all_edges()