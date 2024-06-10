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

alice = CharacterNode(name="Alice", internal_id=0)
bob = CharacterNode(name="Bob", internal_id=1)
charlie = CharacterNode(name="Charlie", internal_id=2)

somewhere = LocationNode(name="Somewhere", internal_id=3)

test_ws = WorldState(name="Test WS", objectnodes=[alice, bob, charlie, somewhere])

test_ws.connect(from_node=somewhere, edge_name=test_ws.DEFAULT_HOLD_EDGE_NAME, to_node=alice)
test_ws.connect(from_node=somewhere, edge_name=test_ws.DEFAULT_HOLD_EDGE_NAME, to_node=bob)
test_ws.connect(from_node=somewhere, edge_name=test_ws.DEFAULT_HOLD_EDGE_NAME, to_node=charlie)


test_ws.connect(from_node=alice, edge_name="likes", to_node=bob)
test_ws.connect(from_node=alice, edge_name="likes", to_node=charlie)
test_ws.connect(from_node=charlie, edge_name="hates", to_node=bob)

#Alice is the only one who likes Bob: Set charlie to hates

unique_like_incoming = HasEdgeTest(object_from_test=None, edge_name_test="likes", object_to_test=bob, soft_equal=True, unique_incoming_test=True, only_test_uniqueness=True)
unique_like_outgoing = HasEdgeTest(object_from_test=alice, edge_name_test="likes", object_to_test=None, soft_equal=True, unique_outgoing_test=True, only_test_uniqueness=True)

print(test_ws.test_story_compatibility_with_conditiontest(test=unique_like_outgoing))
