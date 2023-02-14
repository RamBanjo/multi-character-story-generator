from components.StoryGraphTwoWS import StoryGraph
from components.StoryObjects import CharacterNode, LocationNode
from components.StoryNode import *
from components.UtilFunctions import generate_grouping_from_group_size_lists
from components.WorldState import WorldState

base_joint_node = StoryNode("Base Joint", None, {"Type": "Placeholder"}, -1)

#Only characters whose Law Bias is in the positive can do Cont A
cont_a = StoryNode("Continuation A", None, {"Type": "Placeholder"}, 1, bias_range={"lawbias": (0, 100)})
cont_b = StoryNode("Continuation B", None, {"Type": "Placeholder"}, 1)
cont_c = StoryNode("Continuation C", None, {"Type": "Placeholder"}, 1)

alice = CharacterNode("Alice", biases={"moralbias": 0, "lawbias": 50})
bob = CharacterNode("Bob", biases={"moralbias": 0, "lawbias": -40})
charlie = CharacterNode("Charlie", biases={"moralbias": 50, "lawbias": 0})
somewhere = LocationNode("Somewhere")

basews = WorldState("BaseWS", [alice, bob, charlie])

basesg = StoryGraph("Base Story Graph", [alice, bob, charlie], [somewhere], basews)

#The this function can be converted into one line some way
#DONE! We now have add_multiple_characters_to_part function in StoryGrpahTwoWS!
basesg.add_story_part(base_joint_node, alice, somewhere, copy=True)
basesg.add_story_part(basesg.story_parts[("Alice", 0)], bob, somewhere, copy=False)
basesg.add_story_part(basesg.story_parts[("Alice", 0)], charlie, somewhere, copy=False)

print(basesg.story_parts[("Alice", 0)])

#Only Alice and Charlie should be able to go into cont_a. Bob should not go into cont_a because of the out-of-range Lawbias.

# generated = basesg.generate_valid_character_grouping([cont_a, cont_b, cont_c], 1, [alice, bob, charlie])

# groupno = 0
# for chargroup in generated:
#     for chara in chargroup:
#         print("Group", groupno, chara)
#     groupno += 1

#A different scenario: If we divide two groups and make it so that only people who have non negative lawbias can perform node d with 2 slots, bob would only be able to do the node with no bias

# cont_d = StoryNode("Continuation D", None, {"Type": "Placeholder"}, 2, bias_range={"lawbias": (0, 100)})
# cont_e = StoryNode("Continuation E", None, {"Type": "Placeholder"}, 1)

# generated = basesg.generate_valid_character_grouping([cont_d, cont_e], 1, [alice, bob, charlie], [2, 1])

#Yet another different scenario: cont f and cont g have no limits on the characters, but cont g will not allow anyone with 50 moral bias or above. Charlie won't be able to go there.
#Therefore, the only allowed setups should be: [AC][B],[BC][A],[C][AB]

# cont_f = StoryNode("Continuation F", None, {"Type": "Placeholder"}, -1)
# cont_g = StoryNode("Continuation G", None, {"Type": "Placeholder"}, -1, bias_range={"moralbias": (-100, 49)})

# test_grouping = generate_grouping_from_group_size_lists([-1, -1], 3)
# generated = basesg.generate_valid_character_grouping([cont_f, cont_g], 1, [alice, bob, charlie], test_grouping)

#A scenario: cont h and cont i have no limits on the characters. cont i does not allow anyone with a law bias outside of the [-10, 10] range, meaning that only Charlie would be allowed.
#Therefore, the only allowed setup should be: [AB][C]

cont_h = StoryNode("Continuation H", None, {"Type": "Placeholder"}, -1)
cont_i = StoryNode("Continuation I", None, {"Type": "Placeholder"}, -1, bias_range={"lawbias": (-10, 10)})

test_grouping = generate_grouping_from_group_size_lists([-1, -1], 3)
generated = basesg.generate_valid_character_grouping([cont_h, cont_i], 1, [alice, bob, charlie], test_grouping)

groupno = 0
print(generated)
if(generated is not None):
    for chargroup in generated:
        for chara in chargroup:
            print("Group", groupno, chara)
        groupno += 1