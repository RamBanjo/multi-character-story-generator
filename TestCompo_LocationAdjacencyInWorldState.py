from components.StoryObjects import LocationNode
from components.WorldState import WorldState

#How to check for adjacency
#Assume we have a map of Australia, with the following information:
#   New South Wales -> Victoria, South Australia, Queensland
#   Victoria -> New South Wales, South Australia, Tasmania
#   Queensland -> Northern Territory, South Australia, New South Wales
#   Northern Territory -> Western Australia, Queensland, South Australia
#   Western Australia -> Northern Territory, South Australia
#   South Australia -> Everything except Tasmania
#   Tasmania -> Victoria

australia = WorldState("Australia Map State")

nsw = LocationNode("New South Wales")
vic = LocationNode("Victoria")
qld = LocationNode("Queensland")
nt = LocationNode("Northern Territory")
wa = LocationNode("Western Australia")
sa = LocationNode("South Australia")
tas = LocationNode("Tasmania")

australia.add_node(nsw)
australia.add_node(vic)
australia.add_node(qld)
australia.add_node(nt)
australia.add_node(wa)
australia.add_node(sa)
australia.add_node(tas)

australia.doubleconnect(nsw, "adjacent_to", vic)
australia.doubleconnect(nsw, "adjacent_to", sa)
australia.doubleconnect(nsw, "adjacent_to", qld)
australia.doubleconnect(qld, "adjacent_to", nt)
australia.doubleconnect(qld, "adjacent_to", sa)
australia.doubleconnect(vic, "adjacent_to", sa)
australia.doubleconnect(vic, "adjacent_to", tas)
australia.doubleconnect(nt, "adjacent_to", wa)
australia.doubleconnect(nt, "adjacent_to", sa)
australia.doubleconnect(wa, "adjacent_to", sa)

# Query: What is Queensland adjacent to?

print("Locations adjacent to Queensland:")

qld_adjacencies = australia.node_dict["Queensland"].get_incoming_edge("adjacent_to")

texttoprint = "Queensland -> "

for in_edge in qld_adjacencies:
    texttoprint += in_edge.from_node.get_name()
    texttoprint += ", "

print(texttoprint[:-2])

print("----------")

australia.list_location_adjacencies()