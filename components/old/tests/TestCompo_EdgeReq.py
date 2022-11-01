# Testing Edge Requirements, and testing node conditions

from components.StoryObjects import *
from components.WorldState import WorldState

bob = CharacterNode("Bob")
key = ObjectNode("Key", tags={"Type": "Object", "Unlocks":"BobHomeDoor"})
home = LocationNode("Home")
door = ObjectNode("Door", tags={"Type": "Object", "UnlockGroup":"BobHomeDoor", "LockState":"Locked"})

# Init Worldstate
bws = WorldState("Base Worldstate", [bob, key, home, door])
bws.connect(home, "holds", key)
bws.connect(home, "holds", bob)
bws.connect(home, "holds", door)