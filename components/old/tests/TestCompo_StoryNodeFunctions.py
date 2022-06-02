from components.StoryNode import *
from components.StoryObjects import *
from components.WorldState import *
from components.Edge import *

'''
We're gonna test all the functions for story node here.
'''

alice = CharacterNode("Alice", {"lawbias": 0, "moralbias": 0})

print(alice)

nodeA = StoryNode("Kill Some People", {"moralbias": -50}, {"moralbias": -10}, ["fighting"], 1)

print(nodeA)

nodeA.add_actor(alice)

print(nodeA)

#nodeA.remove_actor(alice)

#print(nodeA)

nodeB = StoryNode("Collect Sword", None, None, ["get_item"], 1)

nodeA.add_next_node(nodeB, alice)


print(nodeA.next_nodes[alice.get_name()])