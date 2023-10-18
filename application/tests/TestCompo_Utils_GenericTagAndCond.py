import sys
sys.path.insert(0,'')

from application.components.ConditionTest import HasEdgeTest
from application.components.RelChange import ConditionalChange, RelChange, TagChange
from application.components.StoryNode import StoryNode
from application.components.StoryObjects import CharacterNode, ObjectNode
from application.components.UtilFunctions import translate_generic_condchange, translate_generic_tagchange
from application.components.UtilityEnums import ChangeAction, GenericObjectNode
from application.components.WorldState import WorldState

#Test these two.

test_ws = WorldState(name="TestWS")
alice = CharacterNode(name="Alice")
bob = CharacterNode(name="Bob")
charlie = CharacterNode(name="Charlie")
daniel = CharacterNode(name="Daniel")
eve = CharacterNode(name="Eve")
frank = CharacterNode(name="Frank")

get_injured_change = TagChange(name = "Actor Gets Hurt", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="injured", value="broken_leg", add_or_remove=ChangeAction.ADD)
get_injured_node = StoryNode(name="Get Injured", biasweight=0, tags={"Type":"Injury"}, charcount=1, target_count=0, actor=[alice], effects_on_next_ws=[get_injured_change])


gentagchange = translate_generic_tagchange(tagchange=get_injured_change, populated_story_node=get_injured_node)

for thing in gentagchange:
    print(thing)
    
test_relchange_str = RelChange(name="Alice Hates Bob", node_a=alice, edge_name="hates", node_b=bob, value="political_rival", add_or_remove=ChangeAction.ADD)
print(test_relchange_str)

test_ws.connect(from_node=charlie, edge_name="hates", to_node=bob, value="affair_with_wife")
test_ws.connect(from_node=daniel, edge_name="hates", to_node=bob, value="blackmailer")

placeholder_hate_test = HasEdgeTest(object_from_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name_test="hates", object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True)
placeholder_like_killer = RelChange(name="Liking the Killer", node_a=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name="likes", node_b=GenericObjectNode.GENERIC_ACTOR, value="killer_of_hated_person", add_or_remove=ChangeAction.ADD)

like_killer_for_killing_hated = ConditionalChange(name="Like Killer For Killing Hated Character", list_of_condition_tests=[placeholder_hate_test], list_of_changes=[placeholder_like_killer])
kill_node = StoryNode(name="Kill Victim", biasweight=0, tags={"Type":"Murder"}, charcount=1, target_count=1, actor=[alice], target=[bob])

getncondchange = translate_generic_condchange(like_killer_for_killing_hated, kill_node)

print(getncondchange.list_of_condition_tests[0])
print(getncondchange.list_of_changes[0])

