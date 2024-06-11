from datetime import datetime
import sys
sys.path.insert(0,'')

from application.components.StoryObjects import *
from application.components.WorldState import *
from application.components.CharacterTask import *
from application.components.StoryGraphTwoWS import *
from application.components.StoryNode import *
from application.components.RelChange import *
from application.components.UtilityEnums import *
from application.components.RewriteRuleWithWorldState import *

from application.StoryGeneration_NewFlowchart_WithMetrics import generate_multiple_graphs, generate_story_from_starter_graph, make_base_graph_from_previous_graph
import os

# Do you feel Happy? Alice is Forever Happy
alice = CharacterNode(name="Alice", tags = {"Type":"Character", "Emotion":"Happy"}, internal_id=0)
bob = CharacterNode(name="Bob", internal_id=1)

somewhere = LocationNode(name="Somewhere", internal_id=2)

testws = WorldState(name="Test WS", objectnodes=[alice, bob, somewhere])
testws.connect(from_node=somewhere, edge_name=testws.DEFAULT_HOLD_EDGE_NAME, to_node=alice)
testws.connect(from_node=somewhere, edge_name=testws.DEFAULT_HOLD_EDGE_NAME, to_node=bob)

alice_is_happy_check = HasTagTest(object_to_test=alice, tag="Emotion", value="Happy")

testsg = StoryGraph(name="Test SG", character_objects=[alice, bob], starting_ws=testws, always_true_tests=[alice_is_happy_check])

become_sad = TagChange(name="Sadness.", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="Emotion", value="Sad", add_or_remove=ChangeAction.ADD)
sadness = StoryNode(name="Sadness.", effects_on_next_ws=[become_sad])

print(testsg.check_continuation_validity(actor=alice, abs_step_to_cont_from=0, cont_list=[sadness]))