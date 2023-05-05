

#Let's test this
#
# A <-> B <-> C
# D (not connected to anything)
# E <-> F <-> G
# F <-> H <-> I
# I <-> E

from components.StoryObjects import LocationNode
from components.WorldState import WorldState

district_a = LocationNode("District A")
district_b = LocationNode("District B")
district_c = LocationNode("District C")
district_d = LocationNode("District D")
district_e = LocationNode("District E")
district_f = LocationNode("District F")
district_g = LocationNode("District G")
district_h = LocationNode("District H")
district_i = LocationNode("District I")
district_j = LocationNode("District J")
district_k = LocationNode("District K")

test_ws = WorldState("test_ws", [district_a, district_b, district_c, district_d, district_e, district_f, district_g, district_h, district_i, district_j, district_k])

test_ws.doubleconnect(district_a, test_ws.DEFAULT_ADJACENCY_EDGE_NAME, district_b)
test_ws.doubleconnect(district_b, test_ws.DEFAULT_ADJACENCY_EDGE_NAME, district_c)

test_ws.doubleconnect(district_e, test_ws.DEFAULT_ADJACENCY_EDGE_NAME, district_f)
test_ws.doubleconnect(district_f, test_ws.DEFAULT_ADJACENCY_EDGE_NAME, district_g)
test_ws.doubleconnect(district_f, test_ws.DEFAULT_ADJACENCY_EDGE_NAME, district_h)
test_ws.doubleconnect(district_h, test_ws.DEFAULT_ADJACENCY_EDGE_NAME, district_i)
test_ws.doubleconnect(district_i, test_ws.DEFAULT_ADJACENCY_EDGE_NAME, district_e)

test_ws.connect(district_j, test_ws.DEFAULT_ADJACENCY_EDGE_NAME, district_k)

print("Locations reachable from A (Expect 3):", test_ws.count_reachable_locations_from_location(district_a))
print("Locations reachable from B (Expect 3):", test_ws.count_reachable_locations_from_location(district_b))
print("Locations reachable from C (Expect 3):", test_ws.count_reachable_locations_from_location(district_c))
print("Locations reachable from D (Expect 1):", test_ws.count_reachable_locations_from_location(district_d))
print("Locations reachable from E (Expect 5):", test_ws.count_reachable_locations_from_location(district_e))
print("Locations reachable from F (Expect 5):", test_ws.count_reachable_locations_from_location(district_f))
print("Locations reachable from G (Expect 5):", test_ws.count_reachable_locations_from_location(district_g))
print("Locations reachable from H (Expect 5):", test_ws.count_reachable_locations_from_location(district_h))
print("Locations reachable from I (Expect 5):", test_ws.count_reachable_locations_from_location(district_i))
print("Locations reachable from J (Expect 2):", test_ws.count_reachable_locations_from_location(district_j))
print("Locations reachable from K (Expect 1):", test_ws.count_reachable_locations_from_location(district_k))

print("A can reach B (True):", test_ws.test_reachability(district_a, district_b))
print("A can reach D (False):", test_ws.test_reachability(district_a, district_d))
print("A can reach E (False):", test_ws.test_reachability(district_a, district_e))
print("A can reach J (False):", test_ws.test_reachability(district_a, district_j))
print("A can reach A (True):", test_ws.test_reachability(district_a, district_a))
print("J can reach K (True):", test_ws.test_reachability(district_j, district_k))
print("K can reach J (False):", test_ws.test_reachability(district_k, district_j))