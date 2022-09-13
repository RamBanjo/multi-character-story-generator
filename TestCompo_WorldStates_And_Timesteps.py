#Testing WorldStates and Timesteps
#This needs to be done in order to ensure a way to handle creating new world states

#We will test two things here
#  1) How will making a deepcopy the world state affect the world state object
#  2) If it does carry over the copy, how will we handle RelChange

# Scenario:
# Initially, there will be one state with three objects.
# Sir, Home, Sword
# In order for WS1 to become WS2, Home must drop the sword and give it to Sir.
# WS1: Home ---holds---> Sword, Home ---holds---> Sir
# WS2: Sir ---holds---> Sword, Home ---holds---> Sir
# We will test if we can do that by copying WS1 and then applying Relationship Change objects to the copy.

from copy import deepcopy
from components.Edge import Edge
from components.WorldState import WorldState
from components.StoryObjects import ObjectNode, CharacterNode, LocationNode
from components.RelChange import RelChange

sir = CharacterNode("Sir")
sword = ObjectNode("Sword", {"description":"weapon"})
home = LocationNode("Home")

ws1 = WorldState("WS1", [sir, sword, home])

ws1.connect(home, "holds", sword)
ws1.connect(home, "holds", sir)

ws1.print_all_nodes()
ws1.print_all_edges()

ws2 = deepcopy(ws1)

holds = Edge("holds")
holds2 = Edge("holds", home, sword)

home_drops_sword = RelChange("home_drops_sword", home, holds2, sword, "remove")
sir_gets_sword = RelChange("sir_gains_sword", sir, holds, sword, "add")

ws2.apply_relationship_change(home_drops_sword)
ws2.apply_relationship_change(sir_gets_sword)

ws2.name = "WS2"
ws2.print_all_nodes()
ws2.print_all_edges()

ws1.print_all_nodes()
ws1.print_all_edges()

#Testing finished: deepcopy will allow us to modify the new world state without affecting old world states.