# Possible string values for generic nodes:
# "actor": Take from the character performing the node. This assumes only one actor.
# "all_actors": Take from the list of characters performing the node together. This assumes all actors.
# "location": Take from the location where the node happened.
# "target": Take from the target of the node. This assumes all the targets
# For relationship changes where one of the sides are specific, use the actual node.

from enum import Enum
from operator import lshift
import sys
sys.path.insert(0,'')

from application.components.Edge import Edge
from application.components.UtilityEnums import ChangeAction, ChangeType

class SomeChange:
    def __init__(self, name):
        self.name = name

class RelChange(SomeChange):
    def __init__(self, name, node_a, edge_name, node_b, value, add_or_remove: ChangeAction, soft_equal = False, two_way = False, **kwargs):
        
        super().__init__(name)

        self.node_a = node_a
        self.edge_name = edge_name
        self.node_b = node_b
        self.value = value
        self.add_or_remove = add_or_remove
        self.soft_equal = soft_equal
        self.two_way = two_way
        self.changetype = ChangeType.RELCHANGE

    def __str__(self):
        return "RelChange: " + str(self.node_a) + " --(" + str(self.edge_name) + ")--> " + str(self.node_b) + " (Value: " + str(self.value) +", TwoWay: " + str(self.two_way) + ", SoftEqual: " + str(self.soft_equal) + ", ChangeAction: " + str(self.add_or_remove) + ")"

class TagChange(SomeChange):
    def __init__(self, name, object_node_name, tag, value, add_or_remove: ChangeAction, **kwargs):
        
        super().__init__(name)
        
        self.object_node_name = object_node_name
        self.tag = tag
        self.value = value
        self.add_or_remove = add_or_remove
        self.changetype = ChangeType.TAGCHANGE

    def __str__(self):
        return "TagChange: " + self.object_node_name + " " + str(self.add_or_remove) + " (" + self.tag + ": " + self.value + ")"

class RelativeTagChange(SomeChange):
    pass

class ConditionalChange(SomeChange):
    def __init__(self, name, list_of_test_object_names, list_of_condition_tests, list_of_changes, **kwargs):

        super().__init__(name)

        self.list_of_test_object_names = list_of_test_object_names
        self.list_of_condition_tests = list_of_condition_tests
        self.list_of_changes = list_of_changes
        self.changetype = ChangeType.CONDCHANGE

class TaskChange(SomeChange):
    def __init__(self, name, task_giver_name, task_owner_name, task_stack):

        super().__init__(name)

        self.task_giver_name = task_giver_name
        self.task_owner_name = task_owner_name
        self.task_stack = task_stack
        self.add_or_remove = ChangeAction.ADD
        self.changetype = ChangeType.TASKCHANGE
        self.placeholder_dict = dict()
        
class TaskAdvance(SomeChange):
    def __init__(self, name, actor_name, task_stack_name):

        super().__init__(name)

        self.actor_name = actor_name
        self.task_stack_name = task_stack_name
        self.changetype = ChangeType.TASKADVANCECHANGE

class TaskCancel(SomeChange):
    def __init__(self, name, actor_name, task_stack_name):

        super().__init__(name)

        self.actor_name = actor_name
        self.task_stack_name = task_stack_name
        self.changetype = ChangeType.TASKCANCELCHANGE    