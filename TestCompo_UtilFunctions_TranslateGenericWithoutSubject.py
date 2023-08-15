#Testing the functions where we try to call translate generic changes while slots are empty

from components.ConditionTest import HasEdgeTest, InBiasRangeTest
from components.StoryNode import StoryNode
from components.StoryObjects import CharacterNode
from components.UtilFunctions import translate_generic_test
from components.UtilityEnums import GenericObjectNode
from components.WorldState import WorldState


alice = CharacterNode("Alice", biases={"lawbias":50, "moralbias":50}, tags={"Job":"Swordmaster", "Wealth":"Average"})
bob = CharacterNode("Bob", biases={"lawbias":50, "moralbias":-50}, tags={"Job":"Ranger"})
charlie = CharacterNode("Charlie", biases={"lawbias":-50, "moralbias":50}, tags={"Job":"Wizard"})
daniel = CharacterNode("Daniel", biases={"lawbias":-50, "moralbias":-50}, tags={"Job":"Rouge"})

test_ws = WorldState("Test WS", objectnodes=[alice, bob, charlie, daniel])

test_neg_law = InBiasRangeTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, bias_axis="lawbias", min_accept=-100, max_accept=-1)
test_actor_hate_target = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="hates", object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True)

commit_murder = StoryNode("Kill Hated Person", biasweight=1, tags={"Type":"Murder"}, charcount=1, target_count=1, required_test_list=[test_neg_law, test_actor_hate_target])

test_ws.connect(from_node= charlie, edge_name="hates", to_node=daniel)

commit_murder.actor = [charlie]

list_of_tests = translate_generic_test(condtest=test_neg_law, populated_story_node=commit_murder)

print(list_of_tests)