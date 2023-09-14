#Here, we are going to test whether the new stuffs we got work properly.

#InBiasRange will be tested to see if they can really see the bias ranges of different characters.
import sys
sys.path.insert(0,'')

from application.components.ConditionTest import HasTagTest, InBiasRangeTest
from application.components.StoryNode import StoryNode
from application.components.StoryObjects import CharacterNode
from application.components.UtilityEnums import GenericObjectNode
from application.components.WorldState import WorldState

#Do we need soft equality for tags... No. No we don't need Soft Equality for Tags but we're keeping it anyways Just In Case
alice = CharacterNode("Alice", biases={"lawbias":50, "moralbias":50}, tags={"Job":"Swordmaster", "Wealth":"Average"})
bob = CharacterNode("Bob", biases={"lawbias":50, "moralbias":-50}, tags={"Job":"Ranger"})
charlie = CharacterNode("Charlie", biases={"lawbias":-50, "moralbias":50}, tags={"Job":"Wizard"})
daniel = CharacterNode("Daniel", biases={"lawbias":-50, "moralbias":-50}, tags={"Job":"Rouge", "Dead":"Murdered"})

test_ws = WorldState("Test WS", objectnodes=[alice, bob, charlie, daniel])

test_neg_law = InBiasRangeTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, bias_axis="lawbias", min_accept=-100, max_accept=-1)
test_pos_law = InBiasRangeTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, bias_axis="lawbias", min_accept=1, max_accept=100)
test_neg_mor = InBiasRangeTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, bias_axis="moralbias", min_accept=-100, max_accept=-1)
test_pos_mor = InBiasRangeTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, bias_axis="moralbias", min_accept=1, max_accept=100)

node_good = StoryNode(name="Be Good", biasweight=1, tags={"Type":"Placeholder"}, charcount=1, required_test_list=[test_pos_mor])
node_lawful = StoryNode(name="Be Lawful", biasweight=1, tags={"Type":"Placeholder"}, charcount=1, required_test_list=[test_pos_law])
node_evil = StoryNode(name="Be Evil", biasweight=1, tags={"Type":"Placeholder"}, charcount=1, required_test_list=[test_neg_mor])
node_chaotic = StoryNode(name="Be Chaoric", biasweight=1, tags={"Type":"Placeholder"}, charcount=1, required_test_list=[test_neg_law])

test_neg_law.object_to_test = alice
print("Neg Law with Alice (Expect False)", test_ws.test_story_compatibility_with_conditiontest(test_neg_law))
test_neg_law.object_to_test = bob
print("Neg Law with Bob (Expect False)", test_ws.test_story_compatibility_with_conditiontest(test_neg_law))
test_neg_law.object_to_test = charlie
print("Neg Law with Charlie (Expect True)", test_ws.test_story_compatibility_with_conditiontest(test_neg_law))
test_neg_law.object_to_test = daniel
print("Neg Law with Daniel (Expect True)", test_ws.test_story_compatibility_with_conditiontest(test_neg_law))

test_neg_mor.object_to_test = alice
print("Neg Moral with Alice (Expect False)", test_ws.test_story_compatibility_with_conditiontest(test_neg_mor))
test_neg_mor.object_to_test = bob
print("Neg Moral with Bob (Expect True)", test_ws.test_story_compatibility_with_conditiontest(test_neg_mor))
test_neg_mor.object_to_test = charlie
print("Neg Moral with Charlie (Expect False)", test_ws.test_story_compatibility_with_conditiontest(test_neg_mor))
test_neg_mor.object_to_test = daniel
print("Neg Moral with Daniel (Expect True)", test_ws.test_story_compatibility_with_conditiontest(test_neg_mor))

#Okay cool. Let's try from the Story Node as well.

node_good.actor = [alice]
print("Being Good Node with Alice (Expect True)", test_ws.test_story_compatibility_with_storynode(node_good))
node_good.actor = [bob]
print("Being Good Node with Bob (Expect False)", test_ws.test_story_compatibility_with_storynode(node_good))
node_good.actor = [charlie]
print("Being Good Node with Charlie (Expect True)", test_ws.test_story_compatibility_with_storynode(node_good))
node_good.actor = [daniel]
print("Being Good Node with Daniel (Expect False)", test_ws.test_story_compatibility_with_storynode(node_good))

#Now that we know these stuff work, we should also try the brand new Tag Test.
test_job_swordmaster = HasTagTest(object_to_test=alice, tag="Job", value="Swordmaster")
test_wealth_poor_not_exist = HasTagTest(object_to_test=alice, tag="Wealth", value="Poor", inverse=True)

print("Alice has Job: Swordmaster (Expect True)", test_ws.test_story_compatibility_with_conditiontest(test_job_swordmaster))
print("Alice not have Wealth: Poor (Expect True)", test_ws.test_story_compatibility_with_conditiontest(test_wealth_poor_not_exist))

test_job_knight = HasTagTest(object_to_test=daniel, tag="Job", value="Knight")
test_dead_not_exist = HasTagTest(object_to_test=daniel, tag="Dead", value=None, soft_equal=True, inverse=True)

print("Daniel has Job: Knight (Expect False)", test_ws.test_story_compatibility_with_conditiontest(test_job_knight))
print("Daniel not have Dead (Expect False)", test_ws.test_story_compatibility_with_conditiontest(test_dead_not_exist))