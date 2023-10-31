import sys
sys.path.insert(0,'')

from application.components.Edge import Edge
from application.components.RelChange import *
from application.components.StoryNode import *
from application.components.StoryObjects import CharacterNode, LocationNode, ObjectNode
from application.components.UtilFunctions import *
from application.components.UtilityEnums import *
from application.components.WorldState import *

alice = CharacterNode(name="Alice")
bob = CharacterNode(name="Bob")
charlie = CharacterNode(name="Charlie")

home = LocationNode(name="Home")
plaza = LocationNode(name="Plaza")

big_iron = ObjectNode(name="Big Iron")


world_state = WorldState(name="Test WS", objectnodes=[alice, bob, charlie, home, plaza, big_iron])