

#Alice and Bob will mutually stop hating each other and start liking each other.

from components.RelChange import RelChange
from components.StoryObjects import CharacterNode
from components.UtilityEnums import ChangeAction, ChangeType
from components.WorldState import WorldState


alice = CharacterNode(name = "Alice")
bob = CharacterNode(name = "Bob")
charlie = CharacterNode(name = "Charlie")
test_ws = WorldState(name="TestWS", objectnodes=[alice, bob])

test_ws.doubleconnect(nodeA=alice, edge_name="hates", nodeB=bob)
test_ws.doubleconnect(nodeA=bob, edge_name="hates", nodeB=charlie)

#First, we test if a RelChange that says both characters stop hating each other works.
stop_hate = RelChange(name="Stop Hating Each Other", node_a=alice, edge_name="hates", node_b=bob, value=None, add_or_remove=ChangeAction.REMOVE, soft_equal=True, two_way=True)

test_ws.apply_relationship_change(stop_hate)

print("Printing outgoing edges with the name hates, expect empty list:", alice.get_outgoing_edge("hates"))
print("Printing outgoing edges with the name hates, expect Bob hating Charlie:", bob.get_outgoing_edge("hates"))
print("Checking that edge:", bob.get_outgoing_edge("hates")[0])

#Then, we test if a RelChange that says both characters start being friends with each other also works.
mutual_friends = RelChange(name="Start Befriend Each Other", node_a=alice, edge_name="friend_of", node_b=bob, value=None, two_way=True, add_or_remove=ChangeAction.ADD)

test_ws.apply_relationship_change(mutual_friends)

print("Printing outgoing edges with the name friend_of, expect Alice friends with Bob:", alice.get_outgoing_edge("friend_of")[0])
print("Printing outgoing edges with the name friend_of, expect Bob friends with Alice:", bob.get_outgoing_edge("friend_of")[0])