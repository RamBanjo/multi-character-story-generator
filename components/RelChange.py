# Possible string values for generic nodes:
# "actor": Take from the character performing the node. This assumes only one actor.
# "all_actors": Take from the list of characters performing the node together. This assumes all actors.
# "location": Take from the location where the node happened.
# "target": Take from the target of the node. This assumes all the targets
# For relationship changes where one of the sides are specific, use the actual node.

from enum import Enum
from operator import lshift

from components.Edge import Edge

# Overlap of Location-based Actions?
# Define clearly how Location should be handled if it's also a Target, and vice versa.
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

class RelChange:
    def __init__(self, name, node_a, edge, node_b, add_or_remove: ChangeAction):
        self.name = name
        self.node_a = node_a
        self.edge = edge
        self.node_b = node_b
        self.add_or_remove = add_or_remove
        self.changetype = ChangeType.RELCHANGE

class TagChange:
    def __init__(self, name, object_node_name, tag, value, add_or_remove: ChangeAction):
        self.name = name
        self.object_node_name = object_node_name
        self.tag = tag
        self.value = value
        self.add_or_remove = add_or_remove
        self.changetype = ChangeType.TAGCHANGE