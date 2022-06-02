from copy import deepcopy
from turtle import st
from components.RewriteRules import RewriteRule
from components.StoryObjects import *
from components.Timestep import TimeStep
from components.WorldState import *
from components.StoryGraph import *

sword = ObjectNode("sword")
sword.set_tag("Price", "Expensive")
sword.set_tag("Category", "Weapon")

sword2 = ObjectNode("sword")
sword2.set_tag("Price", "Inexpensive")
sword2.set_tag("Category", "Weapon")

beyblade = ObjectNode("beyblade")
beyblade.set_tag("Price", "Inexpensive")
beyblade.set_tag("Category", "Toy")

#Testing equality on objectnodes
print("Test ObjectNode Equality expected true:", sword == sword2)
print("Test ObjectNode Equality expected true:", sword2 == sword)
print("Test ObjectNode Equality expected false:", sword == beyblade)
print("Test ObjectNode Equality expected false:", sword2 == beyblade)

alice = CharacterNode("Alice")
bob = CharacterNode("Bob")
charlie = CharacterNode("Charlie")

sg1 = WorldState("w1", [alice, bob, sword])
sg1.connect(alice, "likes", bob)
sg1.connect(bob, "dislikes", alice)
sg1.connect(alice, "holds", sword)

sg2 = WorldState("w2", [alice, bob, charlie, sword, beyblade])
sg2.connect(alice, "likes", bob)
sg2.connect(bob, "dislikes", alice)
sg2.connect(alice, "holds", sword)
sg2.doubleconnect(bob, "likes", charlie)
sg2.connect(charlie, "holds", beyblade)

print("Test WorldState Subgraph expected true:", sg1.is_subgraph(sg2))

#Testing replacement Rule
#Simple stuff:
#Alice gains Sword -> (Alice Finds Merchant, Alice Buys Sword From Merchant)

storynode1 = StoryNode("gain", None, None, {"gain_item"}, 1)
storynode2 = StoryNode("visit_merchant", None, None, {"gain_item", "purchase"}, 1)
storynode3 = StoryNode("buy_from_merchant", None, None, {"gain_item", "purchase"}, 1)
storynode4 = StoryNode("eat_sandwich", None, None, {"consume_item"}, 1)

base_ws = WorldState("base_ws", [alice, sword, bob])

base_sg = StoryGraph("base_sg", [alice, bob], None)
base_t1 = TimeStep("base_t1", base_ws)
base_t1.story_parts.append(deepcopy(storynode1))
base_t1.story_parts.append(deepcopy(storynode4))
base_t1.story_parts[0].add_actor(alice)
base_t1.story_parts[1].add_actor(bob)
base_sg.timesteps.append(base_t1)

lhs_ws = WorldState("lhs_ws", [alice, sword])
rhs_ws1 = WorldState("rhs_ws1", [alice, sword])
rhs_ws2 = WorldState("rhs_ws2", [alice, sword])

lhs_rule = StoryGraph("lhs_rule", [alice], None)
lhs_t1 = TimeStep("lhs_t1", lhs_ws)
lhs_t1.story_parts.append(deepcopy(storynode1))
lhs_t1.story_parts[0].add_actor(alice)
lhs_rule.timesteps.append(lhs_t1)

rhs_rule = StoryGraph("hs_rule", [alice], None)
rhs_t1 = TimeStep("rhs_t1", rhs_ws1)
rhs_t2 = TimeStep("rhs_t2", rhs_ws2)

rhs_t1.story_parts.append(storynode2)
storynode2.add_next_node(storynode3, alice)
rhs_t2.story_parts.append(storynode3)

rhs_t2.current_world_state.connect(alice, "holds", sword)

testrule = RewriteRule(lhs_rule, rhs_rule, "test_rule")

rhs_graph = StoryGraph("base_graph_rhs", [alice], None)



'''st_a = deepcopy(storynode1)
st_a.add_actor(alice)
st_b = deepcopy(storynode1)
st_b.add_actor(alice)

print(st_a.get_name())
print(st_b.get_name())

print (st_a == st_b)'''


print("Test LHS_WS is subraph of Base WS expected True:", lhs_ws.is_subgraph(base_ws))
print("Test LHS_Timestep1 is subgraph of Base_Timestep1 expected True:", lhs_t1.is_subgraph(base_t1))

subgraph_result, subgraph_loc = lhs_rule.is_subgraph(base_sg)

print("Test StoryGraph Subgraph Expected True:", subgraph_result, "Locs:", subgraph_loc)
print(base_sg.apply_rewrite_rule(testrule, alice, False))