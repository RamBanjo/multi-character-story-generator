import sys
sys.path.insert(0,'')

from application.components.ConditionTest import InBiasRangeTest
from application.components.StoryGraphTwoWS import StoryGraph
from application.components.StoryNode import StoryNode
from application.components.StoryObjects import CharacterNode, LocationNode
from application.components.UtilityEnums import GenericObjectNode
from application.components.WorldState import WorldState


alice = CharacterNode("Alice", biases={"moralbias": 0, "lawbias": 50})
bob = CharacterNode("Bob", biases={"moralbias": 0, "lawbias": -40})
charlie = CharacterNode("Charlie", biases={"moralbias": 50, "lawbias": 0})
somewhere = LocationNode("Somewhere")

basews = WorldState("BaseWS", [alice, bob, charlie])

basesg = StoryGraph("Base Story Graph", [alice, bob, charlie], [somewhere], basews)


lawful_test = InBiasRangeTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, bias_axis="lawbias", min_accept=0, max_accept=100)
cont_a = StoryNode(name="Cont A", biasweight=0, tags={"Type":"Placeholder"}, charcount=1, target_count=1, required_test_list=[lawful_test])

#The function to test. We want to make sure all the proper splits can be generated.
#Let's say the continuation node has a condition where the Law Bias cannot be negative for the Actor, and there's 1 Actor Slot and 1 Target Slot.
#Then, the limitation would be Bob can't be the Actor, but any other combination is fine. (DONE!)

# all_groupings = basesg.generate_all_valid_actor_and_target_splits(node=cont_a, abs_step=0, character_list=[alice, bob, charlie])

# for entry in all_groupings:
#     print("===NEW GROUP===")
#     for actor in entry['actor_group']:
#         print("Actor", actor)
#     for target in entry['target_group']:
#         print("Target", target)

#Alright now we are adding more conts. Let's see...if we limit Cont B to 
cont_b = StoryNode(name="Cont B", biasweight=0, tags={"Type":"Placeholder"}, charcount=1, required_test_list=[])

valid_groupings = basesg.generate_all_valid_character_grouping_for_splitting(continuations=[cont_a, cont_b], abs_step=0, character_list=[alice, bob, charlie])

print(valid_groupings)