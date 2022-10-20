# Overlap of Location-based Actions?
# Define clearly how Location should be handled if it's also a Target, and vice versa.
from enum import Enum

class GenericObjectNode(Enum):
    GENERIC_ACTOR = 0
    GENERIC_LOCATION = 1
    GENERIC_TARGET = 2
    ALL_ACTORS = 3

class ChangeAction(Enum):
    REMOVE = 0
    ADD = 1

class ChangeType(Enum):
    RELCHANGE = 0
    TAGCHANGE = 1

class TestType(Enum):
    HELD_ITEM_TAG = 0
    SAME_LOCATION = 1
    OUTGOING_LINK = 2
    INCOMING_LINK = 3