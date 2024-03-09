import sys
sys.path.insert(0,'')

from application.components.StoryObjects import *
from application.components.WorldState import *
from application.components.CharacterTask import *
from application.components.StoryGraphTwoWS import *
from application.components.StoryNode import *
from application.components.RelChange import *
from application.components.UtilityEnums import *

from application.StoryGeneration_NewFlowchart_WithMetrics import make_base_graph_from_previous_graph

busman = CharacterNode(name="Busman")

bus_stop_1 = LocationNode(name="Bus Stop 1")
bus_stop_2 = LocationNode(name="Bus Stop 2")
bus_stop_3 = LocationNode(name="Bus Stop 3")
bus_stop_4 = LocationNode(name="Bus Stop 4")
bus_stop_5 = LocationNode(name="Bus Stop 5")