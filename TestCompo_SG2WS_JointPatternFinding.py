#This will test the check abs step if it has a pattern that can be used for joint pattern.
#There are five storylines from five characters.
# A: X, Y, X, Z
# B: Y, Z, Z, Z
# C: Z, Z, Z, Z
# D: Z, Z, X, Z
# E: Z, X, Y, Z
#
# The pattern we want is [X, Y]. The expected results for each timestep is:
# 0: True, [[A, B]]
# 1: True, [[A, E]]
# 2: True, [[A, E], [D, E]]
# 3: False, []

from components.StoryGraphTwoWS import StoryGraph
from components.StoryObjects import LocationNode, CharacterNode
from components.StoryNode import StoryNode
from components.WorldState import WorldState

alice = CharacterNode("Alice")
bob = CharacterNode("Bob")
charlie = CharacterNode("Charlie")
david = CharacterNode("David")
elise = CharacterNode("Elise")

somewhere = LocationNode("Somewhere")

node_x = StoryNode("Snode X", biasweight=0, tags={"Type":"Placeholder"}, charcount=1)
node_y = StoryNode("Snode Y", biasweight=0, tags={"Type":"Placeholder"}, charcount=1)
node_z = StoryNode("Snode Z", biasweight=0, tags={"Type":"Placeholder"}, charcount=1)

base_ws = WorldState("Base WS", [alice, bob, charlie, david, elise, somewhere])
base_sg = StoryGraph("Base SG", [alice, bob, charlie, david, elise], [somewhere], base_ws)

base_sg.insert_multiple_parts(character=alice, part_list=[node_x, node_y, node_x, node_x])
base_sg.insert_multiple_parts(character=bob, part_list=[node_y, node_z, node_z, node_z])
base_sg.insert_multiple_parts(character=charlie, part_list=[node_z, node_z, node_z, node_z])
base_sg.insert_multiple_parts(character=david, part_list=[node_z, node_z, node_x, node_z])
base_sg.insert_multiple_parts(character=elise, part_list=[node_z, node_x, node_y, node_z])

print(base_sg.check_if_abs_step_has_joint_pattern(required_story_nodes_list=[node_x, node_y], character_name_list=["Alice","Bob","Charlie","David","Elise"], absolute_step_to_search=0))
print(base_sg.check_if_abs_step_has_joint_pattern(required_story_nodes_list=[node_x, node_y], character_name_list=["Alice","Bob","Charlie","David","Elise"], absolute_step_to_search=1))
print(base_sg.check_if_abs_step_has_joint_pattern(required_story_nodes_list=[node_x, node_y], character_name_list=["Alice","Bob","Charlie","David","Elise"], absolute_step_to_search=2))
print(base_sg.check_if_abs_step_has_joint_pattern(required_story_nodes_list=[node_x, node_y], character_name_list=["Alice","Bob","Charlie","David","Elise"], absolute_step_to_search=3))