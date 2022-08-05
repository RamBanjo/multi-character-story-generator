from components.RewriteRules import JoiningJointRule, RewriteRule
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
rule = JoiningJointRule(2, [node_a, node_b], node_f, [dummy1, dummy2], "Test Rule", [{"Job": "Swordmaster"}, None], [{"Wealth": "Rich"}, None], [{"lawbias": (-100, -30), "moralbias": (-100, -30)}, None])

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

#Next up: Writing a function in the StoryGraph that accepts the Joint Rule in order to make changes to the story.