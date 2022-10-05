from components.WorldState import WorldState
from components.Edge import Edge
from components.StoryNode import StoryNode
from components.RelChange import RelChange, ChangeAction
from components.StoryObjects import CharacterNode, ObjectNode

alice = CharacterNode("Alice")
bob = CharacterNode("Bob")
sword = ObjectNode("Sword", {"Type":"Weapon", "Value":"Inexpensive"})
my_state = WorldState("Test World State")

my_state.add_node(alice)
my_state.add_node(bob)
my_state.add_node(sword)
my_state.connect(bob, "holds", sword)

print("Initial Worldstate State")
my_state.print_all_nodes()
my_state.print_all_edges()

print()
print("Now, we will use a RelChange object to make Bob Like Alice")

likes = Edge("likes")
bob_like = RelChange("bob likes alice", bob, likes, alice, ChangeAction.ADD)
my_state.apply_relationship_change(bob_like)

print("Bob should now like Alice")
my_state.print_all_nodes()
my_state.print_all_edges()

print()
print("Now, we're going to have Bob stop having the sword.")

holds = Edge("holds", bob, sword)
bob_sword_drop = RelChange("bob drops sword", bob, holds, sword, ChangeAction.REMOVE)
my_state.apply_relationship_change(bob_sword_drop)

print("Bob should now not have Sword")
my_state.print_all_nodes()
my_state.print_all_edges()

