# Testing the Main Function. Here are the things we need to test:

# 1. Testing if replacement rules are recognized.
# Graph starts with A-B-C. We have rules that say B -> DE and C -> FG. If we make the graph continue generating until the shortest path length is reached we would get ADEFG.
# There are also invalid rules that the main character can't do. We want to make sure the program is able to ignore those as well. B -> Bad_1 and C -> Bad_2 are invalid because H and I are invalid for the character.
#
# 2. Testing if task is recognized.
# Graph starts with A-B-C, where A contains a TaskChange Object.
# ...performing the task would potentially put you in a different location. What if B or C travels to another node? Would doing a chart break that? I don't like the sound of this.
# I mean, it *would* make the option invalid at least if we put the proper requirements in the traveling nodes...
#
# 3. Testing if joint rules are recognized.
# Graph starts with A-B-C for two characters. There is a rule where C -> Joint Node X, Joint Node X -> Joint Node Y, and Joint Node Y -> D or E. Both characters should have the same chart.
#
# 4. Testing if scores are recognized
# Graph is A-B-C. There are 10 rules, each trying to continue C with 10 different nodes. If the scores are properly recognized, we would be able to get Top 5 only.
#
# 5. Testing if task locations are recognized
# Graph is A-B-C. Player gets a Task Stack with only one task in Location X, but they are currently in Location Z. They must travel from Z to Y and then X to do that task.
#
# 6. Like a ReGEN
# Rules, characters, and objects are based of ReGEN. There are two main characters, Alice and Bob.
# All the rules specify that they can only be done by Main Characters, so other characters will do a lot of waiting.

from components.StoryNode import StoryNode
from components.StoryObjects import CharacterNode


node_a = StoryNode(name="Node A")
node_b = StoryNode(name="Node B")
node_c = StoryNode(name="Node C")
node_d = StoryNode(name="Node D")
node_e = StoryNode(name="Node E")
node_f = StoryNode(name="Node F")
node_g = StoryNode(name="Node G")
bad_1 = StoryNode(name="Bad_1")
bad_2 = StoryNode(name="Bad_2")

alice = CharacterNode(name="Alice", tags={"Type":"Character", "Job":"Swordmaster"})