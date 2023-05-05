from components.WorldState import WorldState
from components.StoryObjects import LocationNode

test_ws = WorldState("Test")

#The Map
#
# Ambertown <-> Borough <-> Cold Village <-> Death Desert
# Cold Village <-> Easelton
# Death Desert <-> Easelton
#
# Funhouse is not connected to any of the other locations.

ambertown = LocationNode("Amberton")
borough = LocationNode("Borough")
colton = LocationNode("Colton")
deathstar = LocationNode("Deathstar")
easelton = LocationNode("Easelton")
funhouse = LocationNode("Funhouse")

test_ws = WorldState("test_ws", [ambertown, borough, colton, deathstar, easelton, funhouse])
test_ws.doubleconnect(nodeA = ambertown, edge_name=test_ws.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=borough)
test_ws.doubleconnect(nodeA = borough, edge_name=test_ws.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=colton)
test_ws.doubleconnect(nodeA = colton, edge_name=test_ws.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=easelton)
test_ws.doubleconnect(nodeA = colton, edge_name=test_ws.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=deathstar)
test_ws.doubleconnect(nodeA = deathstar, edge_name=test_ws.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=easelton)

print("Ambertown -> Borough (Expected 1):",test_ws.measure_distance_between_two_locations(ambertown, borough))
print("Ambertown -> Colton (Expected 2):",test_ws.measure_distance_between_two_locations(ambertown, colton))
print("Ambertown -> Deathstar (Expected 3):",test_ws.measure_distance_between_two_locations(ambertown, deathstar))
print("Ambertown -> Funhouse (Expected -1):",test_ws.measure_distance_between_two_locations(ambertown, funhouse))
print("Ambertown -> Ambertown (Expected 0):",test_ws.measure_distance_between_two_locations(ambertown, ambertown))
print("Colton -> Deathstar (Expected 1):",test_ws.measure_distance_between_two_locations(colton, deathstar))
print("Colton -> Easelton (Expected 1):",test_ws.measure_distance_between_two_locations(colton, easelton))