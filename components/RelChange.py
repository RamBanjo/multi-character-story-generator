# Possible string values for generic nodes:
# "actor": Take from the character performing the node. This assumes only one actor.
# "all_actors": Take from the list of characters performing the node together. This assumes all actors.
# "location": Take from the location where the node happened.
# "target": Take from the target of the node. This assumes all the targets
# For relationship changes where one of the sides are specific, use the actual node.

from enum import Enum
from operator import lshift

from components.Edge import Edge
from components.UtilityEnums import ChangeAction, ChangeType

class SomeChange:
    def __init__(self, name):
        self.name = name

class RelChange(SomeChange):
    def __init__(self, name, node_a, edge_name, node_b, value, add_or_remove: ChangeAction, **kwargs):
        
        super().__init__(name)

        self.node_a = node_a
        self.edge_name = edge_name
        self.node_b = node_b
        self.value = value
        self.add_or_remove = add_or_remove
        self.changetype = ChangeType.RELCHANGE

class TagChange(SomeChange):
    def __init__(self, name, object_node_name, tag, value, add_or_remove: ChangeAction, **kwargs):
        
        super().__init__(name)
        
        self.object_node_name = object_node_name
        self.tag = tag
        self.value = value
        self.add_or_remove = add_or_remove
        self.changetype = ChangeType.TAGCHANGE