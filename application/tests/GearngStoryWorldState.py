import sys

sys.path.insert(0,'')

from application.components.StoryObjects import CharacterNode, LocationNode, ObjectNode
from application.components.WorldState import WorldState

columbo = CharacterNode
iris = CharacterNode
amil = CharacterNode
alien_god = CharacterNode

earth = LocationNode
new_world_greenland = LocationNode
tatain = LocationNode
death_paradise = LocationNode
outer_space = LocationNode

tatain_people = ObjectNode
death_paradise_robots = ObjectNode
enemy_mercenary = ObjectNode
earth_army = ObjectNode

all_characters = []
all_locations = []
other_objects = []

all_objects = all_characters + all_locations + other_objects

world_state = WorldState(name="World of Gearngs Story", objectnodes=all_objects)

#Now, we need to make connections

world_state.connect(from_node=new_world_greenland, edge_name="holds", to_node=columbo)
world_state.connect(from_node=tatain, edge_name="holds", to_node=iris)
world_state.connect(from_node=earth, edge_name="holds", to_node=amil)

world_state.connect(from_node=tatain, edge_name="holds", to_node=tatain_people)
world_state.connect(from_node=death_paradise, edge_name="holds", to_node=death_paradise_robots)
world_state.connect(from_node=outer_space, edge_name="holds", to_node=enemy_mercenary)
world_state.connect(from_node=earth, edge_name="holds", to_node=earth_army)