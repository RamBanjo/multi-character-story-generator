#Testing Requirement for Rewrite Rules

from components.RewriteRules_old_2 import RewriteRule
from components.StoryGraph_old_2 import StoryGraph
from components.StoryObjects import CharacterNode, LocationNode

placeholder_location = LocationNode("Place")

#Follows all requirements
alice = CharacterNode("Alice", {"lawbias": -50, "moralbias": -50}, tags={"Type": "Character", "Job": "Swordmaster", "Wealth":"Poor"})

#Does not follow Biases
bob = CharacterNode("Bob", {"lawbias": 50, "moralbias": 50}, tags={"Type": "Character", "Job": "Swordmaster", "Wealth":"Poor"})

#Does not follow Unwanted Nodes
charlie = CharacterNode("Charlie", {"lawbias": -50, "moralbias": -50}, tags={"Type": "Character", "Job": "Swordmaster", "Wealth":"Rich"})

#Does not follow Required Nodes
david = CharacterNode("David", {"lawbias": -50, "moralbias": -50}, tags={"Type": "Character", "Job": "Chef", "Wealth":"Poor"})

dummy = CharacterNode("Placeholder Char", None, {"Type":"Character", "Placeholder":"Placeholder"})

dummygraph_a = StoryGraph("graph a", [dummy], [placeholder_location])
dummygraph_b = StoryGraph("graph b", [dummy], [placeholder_location])
my_rules = RewriteRule(dummygraph_a, dummygraph_b, dummy, "test char compat", {"Job": "Swordmaster"}, {"Wealth": "Rich"}, {"lawbias": (-100, -30), "moralbias": (-100, -30)})

print("Alice compatible should be True:", my_rules.check_character_compatibility(alice))
print("Bob compatible should be False:", my_rules.check_character_compatibility(bob))
print("Charlie compatible should be False:", my_rules.check_character_compatibility(charlie))
print("David compatible should be False:", my_rules.check_character_compatibility(david))