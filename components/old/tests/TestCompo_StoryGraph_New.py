from copy import deepcopy
from turtle import st

from numpy import place
from components.RewriteRules import RewriteRule
from components.StoryObjects import *
from components.WorldState import *
from components.StoryGraph import *

'''
Starting Point: A->B->C

Rules:

B into D->E

Therefore, replacement rule should change it to:

A->D->E->C

Good luck, Ram!
'''

#Node Templates, should not be directly used in storylines but they should be copied
node_a = StoryNode("Action A", None, None, None, 1)
node_b = StoryNode("Action B", None, None, None, 1)
node_c = StoryNode("Action C", None, None, None, 1)
node_d = StoryNode("Action D", None, None, None, 1)
node_e = StoryNode("Action E", None, None, None, 1)
node_f = StoryNode("Joint Action F", None, None, None, 2)

placeholder_location = LocationNode("Place")

alice = CharacterNode("Alice")
bob = CharacterNode("Bob")
charlie = CharacterNode("Charlie")

my_graph = StoryGraph("Test Graph", [alice, bob, charlie], [placeholder_location])

my_graph.add_story_part(node_a, alice, placeholder_location, 0)
my_graph.add_story_part(node_b, alice, placeholder_location, 0)
my_graph.add_story_part(node_c, alice, placeholder_location, 0)
my_graph.add_story_part(node_f, alice, placeholder_location, 0)
my_graph.add_story_part(node_a, bob, placeholder_location, 0)
my_graph.add_story_part(node_d, bob, placeholder_location, 0)
my_graph.add_story_part(node_e, bob, placeholder_location, 0)

#Since we want Bob to join in on the same part as Alice's 3rd step, we do this:
#Set copy as false so we don't create a copy of Alice's node and instead use the already existing Node
alicepart = my_graph.story_parts[("Alice", 3)]
my_graph.add_story_part(alicepart, bob, placeholder_location, False)

my_graph.print_all_nodes()
print(my_graph.story_parts)

#Okay cool, now let's see if we can find and replace stuff

'''
Removing has been tested: it works!

print("removing Step where Alice does Node B")

my_graph.remove_story_part(alice, 1)
my_graph.print_all_nodes()
print(my_graph.story_parts["Alice", 0].get_name())
print(my_graph.story_parts["Alice", 1].get_name())
print(my_graph.story_parts["Alice", 2].get_name())'''

'''
Removing edge case 1 has been tested: it works!

print("removing Step where Alice does Node A")

my_graph.remove_story_part(alice, 0)
my_graph.print_all_nodes()
print(my_graph.story_parts["Alice", 0].get_name())
print(my_graph.story_parts["Alice", 1].get_name())
print(my_graph.story_parts["Alice", 2].get_name())
'''

'''
Removing edge case 2 has been tested: it works!

print("removing Step where Alice does Node F")

my_graph.remove_story_part(alice, 3)
my_graph.print_all_nodes()
print(my_graph.story_parts["Alice", 0].get_name())
print(my_graph.story_parts["Alice", 1].get_name())
print(my_graph.story_parts["Alice", 2].get_name())
'''

'''
Inserting has been tested: it works!
print("inserting Part E at position 2, it should then be: A-B-E-C-F")

my_graph.insert_story_part(node_e, alice, placeholder_location, 2)
my_graph.print_all_nodes()

print(my_graph.story_parts["Alice", 0].get_name())
print(my_graph.story_parts["Alice", 1].get_name())
print(my_graph.story_parts["Alice", 2].get_name())
print(my_graph.story_parts["Alice", 3].get_name())
print(my_graph.story_parts["Alice", 4].get_name())'''

'''
Inserting Edge Case 1 has been tested: it works!

print("inserting Part E at position 4, it should then be: A-B-C-F-E")

my_graph.insert_story_part(node_e, alice, placeholder_location, 4)
my_graph.print_all_nodes()

print(my_graph.story_parts["Alice", 0].get_name())
print(my_graph.story_parts["Alice", 1].get_name())
print(my_graph.story_parts["Alice", 2].get_name())
print(my_graph.story_parts["Alice", 3].get_name())
print(my_graph.story_parts["Alice", 4].get_name())
'''

'''
Inserting Edge Case 2 has been tested: it works!
print("inserting Part E at position 0, it should then be: E-A-B-C-F")

my_graph.insert_story_part(node_e, alice, placeholder_location, 0)
my_graph.print_all_nodes()

print(my_graph.story_parts["Alice", 0].get_name())
print(my_graph.story_parts["Alice", 1].get_name())
print(my_graph.story_parts["Alice", 2].get_name())
print(my_graph.story_parts["Alice", 3].get_name())
print(my_graph.story_parts["Alice", 4].get_name())'''

'''
All cases, including edge cases, work perfectly fine!

print("Tesitng Find and Replace, originally Alice goes A-B-C-F, but we want to replace B-C with D-E")

replist = [(node_d, placeholder_location), (node_e, placeholder_location)]

my_graph.print_all_nodes()

print(my_graph.story_parts["Alice", 0].get_name())
print(my_graph.story_parts["Alice", 1].get_name())
print(my_graph.story_parts["Alice", 2].get_name())
print(my_graph.story_parts["Alice", 3].get_name())
'''


'''print("Testing Subgraphs")

graph_a = StoryGraph("Graph A", [alice], [placeholder_location])
graph_b = StoryGraph("Graph B", [alice], [placeholder_location])

placeholder_ws = WorldState("WorldPlace", [alice, placeholder_location])

graph_a.add_story_part(node_b, alice, placeholder_location)
graph_a.add_story_part(node_c, alice, placeholder_location)
graph_a.add_story_part(node_d, alice, placeholder_location)
graph_a.add_world_state(placeholder_ws)
graph_a.add_world_state(placeholder_ws)
graph_a.add_world_state(placeholder_ws)

graph_b.add_story_part(node_a, alice, placeholder_location)
graph_b.add_story_part(node_b, alice, placeholder_location)
graph_b.add_story_part(node_c, alice, placeholder_location)
graph_b.add_story_part(node_d, alice, placeholder_location)
graph_b.add_story_part(node_b, alice, placeholder_location)
graph_b.add_story_part(node_c, alice, placeholder_location)
graph_b.add_story_part(node_d, alice, placeholder_location)
graph_b.add_world_state(placeholder_ws)
graph_b.add_world_state(placeholder_ws)
graph_b.add_world_state(placeholder_ws)
graph_b.add_world_state(placeholder_ws)
graph_b.add_world_state(placeholder_ws)
graph_b.add_world_state(placeholder_ws)
graph_b.add_world_state(placeholder_ws)

print("Graph A:")
graph_a.print_all_nodes()

print("---")
print("Graph B:")
graph_b.print_all_nodes()

print(StoryGraph.is_subgraph(graph_a, graph_b, alice, alice))

#Subgraph is now working properly...NOT!'''

dummy = CharacterNode("Placeholder Char", None, {"Character", "Placeholder"})

print("Testing Rewrite Rule, this rewrite rule should replace the B-C and change it into D-E")
loclist = [placeholder_location, placeholder_location]

placeholder_ws = WorldState("WorldPlace", [alice, placeholder_location])

cond_graph = StoryGraph("rule1", None, None)

my_graph.add_world_state(placeholder_ws)
my_graph.add_world_state(placeholder_ws)
my_graph.add_world_state(placeholder_ws)
my_graph.add_world_state(placeholder_ws)

cond_graph.add_story_part(node_b, dummy, None, 0)
cond_graph.add_story_part(node_c, dummy, None, 0)
cond_graph.add_world_state(placeholder_ws)
cond_graph.add_world_state(placeholder_ws)

repl_graph = StoryGraph("rule2", None, None)

repl_graph.add_story_part(node_d, dummy, None, 0)
repl_graph.add_story_part(node_e, dummy, None, 0)
cond_graph.add_world_state(placeholder_ws)
cond_graph.add_world_state(placeholder_ws)

new_rule = RewriteRule(cond_graph, repl_graph, dummy, "My Rule")

print("subgraph check :", StoryGraph.is_subgraph(cond_graph, my_graph, dummy, alice))

my_graph.apply_rewrite_rule(new_rule, alice, [placeholder_location, placeholder_location])

my_graph.print_all_nodes()
print("---")
my_graph.print_all_node_values()