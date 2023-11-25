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
from application.components.StoryObjects import *

class SomeChange:
    def __init__(self, name, changetype, internal_id:int = 0):
        self.name = name
        self.changetype = changetype
        self.internal_id = internal_id

    def export_object_as_dict(self) -> dict:

        return_dict = dict()

        return_dict["name"] = self.name
        return_dict["changetype"] = self.changetype
        return_dict["internal_id"] = self.internal_id

        return return_dict

class RelChange(SomeChange):
    def __init__(self, name, node_a, edge_name, node_b, add_or_remove: ChangeAction, value=None, soft_equal = False, two_way = False, **kwargs):
        
        super().__init__(name=name, changetype=ChangeType.RELCHANGE)

        self.node_a = node_a
        self.edge_name = edge_name
        self.node_b = node_b
        self.value = value
        self.add_or_remove = add_or_remove
        self.soft_equal = soft_equal
        self.two_way = two_way

    def export_object_as_dict(self) -> dict:
        return_dict = super().export_object_as_dict()

        node_a_name = self.node_a
        if issubclass(type(node_a_name), ObjectNode):
            node_a_name = self.node_a.get_name()

        node_b_name = self.node_b
        if issubclass(type(node_b_name), ObjectNode):
            node_b_name = self.node_b.get_name()

        return_dict["node_a_name"] = node_a_name
        return_dict["node_b_name"] = node_b_name
        return_dict["edge_name"] = self.edge_name
        return_dict["value"] = self.value
        return_dict["add_or_remove"] = self.add_or_remove
        return_dict["soft_equal"] = self.soft_equal
        return_dict["two_way"] = self.two_way
    
        return return_dict

    def __str__(self):
        return "RelChange: " + str(self.node_a) + " --(" + str(self.edge_name) + ")--> " + str(self.node_b) + " (Value: " + str(self.value) +", TwoWay: " + str(self.two_way) + ", SoftEqual: " + str(self.soft_equal) + ", ChangeAction: " + str(self.add_or_remove) + ")"

class TagChange(SomeChange):
    def __init__(self, name, object_node_name, tag, value, add_or_remove: ChangeAction, **kwargs):
        
        super().__init__(name=name, changetype=ChangeType.TAGCHANGE)
        
        self.object_node_name = object_node_name
        self.tag = tag
        self.value = value
        self.add_or_remove = add_or_remove

    def export_object_as_dict(self) -> dict:
        return_dict = super().export_object_as_dict()

        return_dict["object_node_name"] = str(self.object_node_name)
        return_dict["tag"] = self.tag
        return_dict["value"] = self.value
        return_dict["add_or_remove"] = int(self.add_or_remove)
    
        return return_dict

    def __str__(self):
        return "TagChange: " + str(self.object_node_name) + " " + str(self.add_or_remove) + " (" + self.tag + ": " + str(self.value) + ")"

class RelativeTagChange(SomeChange):

    def __init__(self, name, object_node_name, tag, value_delta, **kwargs):

        super().__init__(name=name, changetype=ChangeType.RELATIVETAGCHANGE)

        self.object_node_name = object_node_name
        self.tag = tag
        self.value_delta = value_delta

    def export_object_as_dict(self) -> dict:
        return_dict = super().export_object_as_dict()

        return_dict["object_node_name"] = self.object_node_name
        return_dict["tag"] = self.tag
        return_dict["value_delta"] = self.value_delta

        return return_dict
        
    def __str__(self):
        return "RelativeTagChange: " + str(self.object_node_name) + " " + str(self.tag) + " " + str(self.value_delta)

class RelativeBiasChange(SomeChange):
    
    def __init__(self, name, object_node_name, bias, biasvalue_delta, **kwargs):

        super().__init__(name=name, changetype=ChangeType.RELATIVEBIASCHANGE)

        self.object_node_name = object_node_name
        self.bias = bias
        self.biasvalue_delta = biasvalue_delta

    def export_object_as_dict(self) -> dict:
        return_dict = super().export_object_as_dict()

        return_dict["object_node_name"] = self.object_node_name
        return_dict["tag"] = self.bias
        return_dict["biasvalue_delta"] = self.biasvalue_delta

        return return_dict

class ConditionalChange(SomeChange):
    def __init__(self, name, list_of_condition_tests, list_of_changes, **kwargs):

        super().__init__(name=name, changetype=ChangeType.CONDCHANGE)

        self.list_of_condition_tests = list_of_condition_tests
        self.list_of_changes = list_of_changes

    def export_object_as_dict(self) -> dict:
        return_dict = super().export_object_as_dict()

        return_dict["list_of_condition_test_ids"] = []
        return_dict["list_of_change_ids"] = []

        for test in self.list_of_condition_tests:
            return_dict["list_of_condition_test_ids"].append(test.internal_id)
        for change in self.list_of_changes:
            return_dict["list_of_change_ids"].append(change.internal_id)

        return return_dict

class TaskChange(SomeChange):
    def __init__(self, name, task_giver_name, task_owner_name, task_stack):

        super().__init__(name=name, changetype=ChangeType.TASKCHANGE)

        self.task_giver_name = task_giver_name
        self.task_owner_name = task_owner_name
        self.task_stack = task_stack
        self.add_or_remove = ChangeAction.ADD
        self.placeholder_dict = dict()

    def export_object_as_dict(self) -> dict:
        return_dict = super().export_object_as_dict()

        return_dict["task_giver_name"] = self.task_giver_name
        return_dict["task_owner_name"] = self.task_owner_name
        return_dict["task_stack_id"] = self.task_stack.internal_id
    
        return return_dict    

    def __str__(self) -> str:
        return "TaskChange: " +self.name + " given from " + str(self.task_giver_name) + " to " + str(self.task_owner_name)
        
class TaskAdvance(SomeChange):
    def __init__(self, name, actor_name, task_stack_name):

        super().__init__(name=name, changetype=ChangeType.TASKADVANCECHANGE)

        self.actor_name = actor_name
        self.task_stack_name = task_stack_name

    def export_object_as_dict(self) -> dict:
        return_dict = super().export_object_as_dict()

        return_dict["actor_name"] = self.actor_name
        return_dict["task_stack_name"] = self.task_stack_name
    
        return return_dict    

    def __eq__(self, rhs):

        if type(rhs) != TaskAdvance:
            return False
        
        return self.name == rhs.name, self.actor_name == rhs.actor_name, self.task_stack_name == rhs.task_stack_name

class TaskCancel(SomeChange):
    def __init__(self, name, actor_name, task_stack_name):

        super().__init__(name=name, changetype=ChangeType.TASKCANCELCHANGE)

        self.actor_name = actor_name
        self.task_stack_name = task_stack_name

    def export_object_as_dict(self) -> dict:
        return_dict = super().export_object_as_dict()

        return_dict["actor_name"] = self.actor_name
        return_dict["task_stack_name"] = self.task_stack_name
    
        return return_dict    