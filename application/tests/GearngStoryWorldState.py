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

all_characters = []
all_locations = []
other_objects = []

all_objects = all_characters + all_locations + other_objects

world_state = WorldState(name="World of Gearngs Story", objectnodes=all_objects)

#Now, we need to make connections