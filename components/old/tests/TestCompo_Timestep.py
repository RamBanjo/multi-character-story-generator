from copy import deepcopy
from turtle import st
from xml.dom import NO_DATA_ALLOWED_ERR

from numpy import place
from components.RewriteRules_old_2 import RewriteRule
from components.StoryObjects import *
from components.WorldState import *
from components.StoryGraph_old_2 import *

'''
Starting Point: 

A->B->C

where A, B are in TS 1 and C is in TS 2

If we apply the rule that replaces A->B with A->D->B then it should work and D would be in TS 1

but if we apply the rule that replaces B->C with B->E->C it would not work because B and C are in different timesteps

Here we go, Good luck, Ram!
'''

alice = CharacterNode("Alice")

town = LocationNode("Town")

placeholder_ws = WorldState("WorldPlace", [alice, town])

node_a = StoryNode("Action A", None, None, None, 1)
node_b = StoryNode("Action B", None, None, None, 1)
node_c = StoryNode("Action C", None, None, None, 1)
node_d = StoryNode("Action D", None, None, None, 1)
node_e = StoryNode("Action E", None, None, None, 1)

my_graph = StoryGraph("Test Graph", [alice], [town])

my_graph.add_story_part(node_a, alice, town, 0)
my_graph.add_story_part(node_b, alice, town, 0)
my_graph.add_story_part(node_c, alice, town, 1)

my_graph.add_world_state(placeholder_ws)
my_graph.add_world_state(placeholder_ws)

dummy = CharacterNode("Placeholder Char", None, {"Character", "Placeholder"})
lhs_graph_working = StoryGraph("LHS_Working", [dummy], [town])
rhs_graph_working = StoryGraph("RHS_Working", [dummy], [town])
lhs_graph_broken = StoryGraph("LHS_Broken", [dummy], [town])
rhs_graph_broken = StoryGraph("RHS_Broken", [dummy], [town])

lhs_graph_broken.add_world_state(placeholder_ws)
lhs_graph_working.add_world_state(placeholder_ws)
rhs_graph_broken.add_world_state(placeholder_ws)
rhs_graph_working.add_world_state(placeholder_ws)

lhs_graph_working.add_story_part(node_a, dummy, town, 0)
lhs_graph_working.add_story_part(node_b, dummy, town, 0)
rhs_graph_working.add_story_part(node_a, dummy, town, 0)
rhs_graph_working.add_story_part(node_d, dummy, town, 0)
rhs_graph_working.add_story_part(node_b, dummy, town, 0)

lhs_graph_broken.add_story_part(node_b, dummy, town, 0)
lhs_graph_broken.add_story_part(node_c, dummy, town, 0)
rhs_graph_broken.add_story_part(node_b, dummy, town, 0)
rhs_graph_broken.add_story_part(node_e, dummy, town, 0)
rhs_graph_broken.add_story_part(node_c, dummy, town, 0)

working_rule = RewriteRule(lhs_graph_working, rhs_graph_working, dummy, "Working Rule")
broken_rule = RewriteRule(lhs_graph_broken, rhs_graph_broken, dummy, "Broken Rule")

print("Checking subgraph: the lhs broken should not be a subgraph, the lhs working should be a subgraph")

print("lhs broken is false:", StoryGraph.is_subgraph(lhs_graph_broken, my_graph, dummy, alice))
print("lhs workiing is true:", StoryGraph.is_subgraph(lhs_graph_working, my_graph, dummy, alice))

#This subgraphiness is now working properly. Next, we need to work on figuring out World States