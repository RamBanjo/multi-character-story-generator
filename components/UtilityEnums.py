# Overlap of Location-based Actions?
# Define clearly how Location should be handled if it's also a Target, and vice versa.
from enum import Enum

class GenericObjectNode(Enum):
    GENERIC_ACTOR = 0
    GENERIC_LOCATION = 1
    GENERIC_TARGET = 2
    ALL_ACTORS = 3
    CONDITION_TESTOBJECT_PLACEHOLDER = 4
    TASK_GIVER = 5
    TASK_OWNER = 6

class ChangeAction(Enum):
    REMOVE = 0
    ADD = 1

class ChangeType(Enum):
    RELCHANGE = 0
    TAGCHANGE = 1
    CONDCHANGE = 2
    TASKCHANGE = 3
    TASKADVANCECHANGE = 4

class TestType(Enum):
    HELD_ITEM_TAG = 0
    SAME_LOCATION = 1
    HAS_EDGE = 2
    HAS_DOUBLE_EDGE = 3

class JointType(Enum):
    JOIN = 0
    CONT = 1
    SPLIT = 2