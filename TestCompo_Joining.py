from components.RewriteRules import ContinuousJointRule, JoiningJointRule, RewriteRule, SplittingJointRule
from components.StoryGraph import StoryGraph
from components.StoryNode import StoryNode
from components.StoryObjects import CharacterNode, LocationNode

node_a = StoryNode("Action A", None, None, None, 1)
node_b = StoryNode("Action B", None, None, None, 1)
node_f = StoryNode("Joint Action F", None, None, None, 2)

dummy1 = CharacterNode("Dummy A")
dummy2 = CharacterNode("Dummy B")

#The rule:
#If character A is doing A, and Character B is doing B, then in the next step both of them can do F together.

#Slot A is restricted so that only Alice fits all three criteria. Slot B is unrestricted and can be filled with anyone.
rule = JoiningJointRule(2, [node_a, node_b], node_f, "Test Rule", [{"Job": "Swordmaster"}, None], [{"Wealth": "Rich"}, None], [{"lawbias": (-100, -30), "moralbias": (-100, -30)}, None])

#Follows all requirements
alice = CharacterNode("Alice", {"lawbias": -50, "moralbias": -50}, tags={"Type": "Character", "Job": "Swordmaster", "Wealth":"Poor"})

#Does not follow Biases
bob = CharacterNode("Bob", {"lawbias": 50, "moralbias": 50}, tags={"Type": "Character", "Job": "Swordmaster", "Wealth":"Poor"})

#Does not follow Unwanted Nodes
charlie = CharacterNode("Charlie", {"lawbias": -50, "moralbias": -50}, tags={"Type": "Character", "Job": "Swordmaster", "Wealth":"Rich"})

#Does not follow Required Nodes
david = CharacterNode("David", {"lawbias": -50, "moralbias": -50}, tags={"Type": "Character", "Job": "Chef", "Wealth":"Poor"})

#This should return true
print("Checking compatibilities with Alice in Slot A and Bob in Slot B:", rule.check_compatibilities([alice, bob]))

##########
#Now, we will make a story graph that will include the following, all within the same timestep of Timestep 0:
# Step 1: Alice does Action A
# Step 2: Alice does Action B
# Step 1: Bob does Action C
# Step 2: Bob does Action D
# Step 3: Alice performs E
# Step 3: Bob performs F
#
# We also include a rule that states that if one character performs C and another performs D in the same step, then the next node can be X.
# Therefore, the final state should be:
# abs_step | alice | bob |
#-------------------------
#    0     |   A   |  B
#    1     |   C   |  D
#    2     |   X   |  X
#    3     |   E   |  F

node_a = StoryNode("Action A", None, None, None, 1)
node_b = StoryNode("Action B", None, None, None, 1)
node_c = StoryNode("Action C", None, None, None, 1)
node_d = StoryNode("Action D", None, None, None, 1)
node_e = StoryNode("Action E", None, None, None, 1)
node_f = StoryNode("Action F", None, None, None, 1)
node_x = StoryNode("Joint Action X", None, None, None, 2)
node_y = StoryNode("Joint Action Y", None, None, None, 2)
node_g = StoryNode("Action G", None, None, None, 1)
node_h = StoryNode("Action H", None, None, None, 1)

town = LocationNode("Town")

other_rule = JoiningJointRule(2, [node_c, node_d], node_x, "If CD Then X")
other_rule_2 = ContinuousJointRule(2, node_x, node_y, "If X then Y")
other_rule_3 = SplittingJointRule(2, node_y, [node_g, node_h], "If Y then GH")

test_graph = StoryGraph("Test Joint Rule Graph", [alice, bob], [town])
test_graph.add_story_part(node_a, alice, town, 0)
test_graph.add_story_part(node_b, bob, town, 0)
test_graph.add_story_part(node_c, alice, town, 0)
test_graph.add_story_part(node_d, bob, town, 0)
test_graph.add_story_part(node_e, alice, town, 0)
test_graph.add_story_part(node_f, bob, town, 0)

test_graph.apply_joint_rule(other_rule, [alice, bob], [town], applyonce=True)
test_graph.apply_joint_rule(other_rule_2, [alice, bob], [town], applyonce=True)
test_graph.apply_joint_rule(other_rule_3, [alice, bob], [town, town], applyonce=True)

#Now, let's see if it works!
print("Alice's Actions, from steps 0 to 5:")
print(test_graph.story_parts[('Alice', 0)].get_name())
print(test_graph.story_parts[('Alice', 1)].get_name())
print(test_graph.story_parts[('Alice', 2)].get_name())
print(test_graph.story_parts[('Alice', 3)].get_name())
print(test_graph.story_parts[('Alice', 4)].get_name())
print(test_graph.story_parts[('Alice', 5)].get_name())

print("Bob's Actions, from steps 0 to 5:")
print(test_graph.story_parts[('Bob', 0)].get_name())
print(test_graph.story_parts[('Bob', 1)].get_name())
print(test_graph.story_parts[('Bob', 2)].get_name())
print(test_graph.story_parts[('Bob', 3)].get_name())
print(test_graph.story_parts[('Bob', 4)].get_name())
print(test_graph.story_parts[('Bob', 5)].get_name())
