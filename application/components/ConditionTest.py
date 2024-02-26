import sys
sys.path.insert(0,'')

from application.components.StoryObjects import ObjectNode
from application.components.UtilityEnums import TestType

class ConditionTest:
    def __init__(self, name, test_type, inverse=False, score=1, internal_id:int = 0):
        self.name = name
        self.inverse = inverse
        self.score = score
        self.test_type = test_type
        self.internal_id = internal_id

    def export_object_as_dict(self) -> dict:

        return_dict = dict()

        return_dict["name"] = self.name
        return_dict["inverse"] = self.inverse
        return_dict["score"] = self.score
        return_dict["test_type"] = self.test_type
        return_dict["internal_id"] = self.internal_id

        return return_dict
        
class HeldItemTagTest(ConditionTest):
    def __init__(self, holder_to_test, tag_to_test, value_to_test, soft_equal = True, inverse = False, score=1):
        
        super().__init__(name="Held Item Test", test_type= TestType.HELD_ITEM_TAG, inverse=inverse, score=score)

        self.holder_to_test = holder_to_test
        self.tag_to_test = tag_to_test
        self.value_to_test = value_to_test
        self.soft_equal = soft_equal

    def __str__(self):
        return self.name + " (" + str(self.holder_to_test) + " {" + str(self.tag_to_test) + ":" + str(self.value_to_test) + "}, inverse = " + str(self.inverse) + ")"
    
    def export_object_as_dict(self) -> dict:
        return_dict = super().export_object_as_dict()

        holder_name = self.holder_to_test
        if issubclass(type(holder_name), ObjectNode):
            holder_name = holder_name.get_name()

        return_dict["holder_name"] = holder_name
        return_dict["tag_to_test"] = self.tag_to_test
        return_dict["value_to_test"] = self.value_to_test
        return_dict["soft_equal"] = self.soft_equal

        return return_dict
# HOW THIS WORKS
# (Not allowed to stack with each other)
# Gets a list of tests with placeholders
# Each test will replace the placeholder with each object in the world state
# A list of objects passing the test will be given
# Intersect all lists, and if the list at the end has at least one object then this test will pass
# If successful, this might even replace HeldItemTagTest as a more generic thing.
class SomethingPassesAllGivenTestsTest(ConditionTest):
    def __init__(self, list_of_tests_with_placeholder, inverse=False, score=1):

        super().__init__(name="Intersect Object Exists Test", test_type=TestType.SOMETHING_PASSES_ALL, inverse=inverse, score=score)

        self.list_of_tests_with_placeholder = list_of_tests_with_placeholder

    def export_object_as_dict(self) -> dict:
        return_dict = super().export_object_as_dict()

        return_dict["list_of_condition_test_ids"] = []
        for test in self.list_of_tests_with_placeholder:
            return_dict["list_of_condition_test_ids"].append(test.internal_id)

        return return_dict
    
# HOW THIS WORKS
# (Not allowed to stack with each other)
# Gets a list of tests with placeholders, as well as an object to replace those placeholders
# This passes the test if at least one test returns true.

#TODO: Go and edit the things that interact with ConditionTest in WorldState and SG2WS to accept these two tests.
class ObjectPassesAtLeastOneTestTest(ConditionTest):
    def __init__(self, list_of_tests_with_placeholder, object_to_test, inverse=False, score=1):

        super().__init__(name="Object Passes At Least One", test_type=TestType.OBJECT_PASSES_ONE, inverse=inverse, score=score)

        self.object_to_test = object_to_test
        self.list_of_tests_with_placeholder = list_of_tests_with_placeholder

    def export_object_as_dict(self) -> dict:
        return_dict = super().export_object_as_dict()

        object_name = self.object_to_test
        if issubclass(type(object_name), ObjectNode):
            object_name = object_name.get_name()

        return_dict["list_of_condition_test_ids"] = []
        for test in self.list_of_tests_with_placeholder:
            return_dict["list_of_condition_test_ids"].append(test.internal_id)

        return return_dict

class SameLocationTest(ConditionTest):
    def __init__(self, list_to_test, inverse = False, score=1):

        super().__init__(name="Same Location Test", test_type=TestType.SAME_LOCATION, inverse=inverse, score=score)

        self.list_to_test = list_to_test

    def __str__(self):

        printlist = ""

        for item in self.list_to_test:
            printlist += str(item)
            printlist += ", "

        return self.name + " (" + printlist[:-2] + ", inverse = " + str(self.inverse) + ")"
    
    def export_object_as_dict(self) -> dict:
        return_dict = super().export_object_as_dict()
        return_dict["object_name_list"] = []

        for item in self.list_to_test:
            object_name = item
            if issubclass(type(object_name), ObjectNode):
                object_name = item.get_name()
            return_dict["object_name_list"].append(object_name)

        return return_dict

#TODO (Extra Features): Hey, DoubleEdge test is very similar to normal Edge. What if we remove DoubleEdgeTest and add two-sided to DoubleEdgeTest instead.
class HasEdgeTest(ConditionTest):
    def __init__(self, object_from_test, edge_name_test, object_to_test, value_test = None, soft_equal = False, two_way = False, inverse = False, score=1):

        super().__init__("Has Edge Test", test_type=TestType.HAS_EDGE, inverse=inverse, score=score)

        self.object_from_test = object_from_test
        self.edge_name_test = edge_name_test
        self.object_to_test = object_to_test
        self.value_test = value_test
        self.soft_equal = soft_equal
        self.two_way = two_way

    def __str__(self):
        return self.name + " (" + str(self.object_from_test) + " " + str(self.edge_name_test) + " " + str(self.object_to_test) + ", " + "inverse = " + str(self.inverse) + ")"
    
    def export_object_as_dict(self) -> dict:
        return_dict = super().export_object_as_dict()

        from_name = self.object_from_test
        if issubclass(type(from_name), ObjectNode):
            from_name = from_name.get_name()

        to_name = self.object_to_test
        if issubclass(type(to_name), ObjectNode):
            to_name = to_name.get_name()

        return_dict["from_name"] = from_name
        return_dict["to_name"] = to_name
        return_dict["edge_name_test"] = self.edge_name_test
        return_dict["value_test"] = self.value_test
        return_dict["soft_equal"] = self.soft_equal
        return_dict["two_way"] = self.two_way 

        return return_dict
    
class HasTagTest(ConditionTest):
    def __init__(self, object_to_test, tag, value, soft_equal = False, inverse=False, score=1):
        super().__init__(name="Has Tag Test", test_type = TestType.HAS_TAG, inverse=inverse, score=score)

        self.object_to_test = object_to_test
        self.tag = tag
        self.value = value
        self.soft_equal = soft_equal

    def __str__(self):
        return self.name + " (" + str(self.object_to_test) + " " + str(self.tag) + " " + str(self.value) + ", " + "inverse = " + str(self.inverse) + ")"
    
    def export_object_as_dict(self) -> dict:
        return_dict = super().export_object_as_dict()

        to_name = self.object_to_test
        if issubclass(type(to_name), ObjectNode):
            to_name = to_name.get_name()

        return_dict["to_name"] = to_name
        return_dict["tag"] = self.tag
        return_dict["value"] = self.value
        return_dict["soft_equal"] = self.soft_equal

        return return_dict
    
class TagValueInRangeTest(ConditionTest):
    def __init__(self, object_to_test, tag, value_min, value_max, inverse=False, score=1):

        super().__init__(name="Tag Value in Range Test", test_type = TestType.TAG_VALUE_IN_RANGE, inverse=inverse, score=score)

        self.object_to_test = object_to_test
        self.tag = tag
        self.value_min = value_min
        self.value_max = value_max

    def __str__(self) -> str:
        return self.name + " (" + str(self.object_to_test) + " " + str(self.tag) + " " + str(self.value_min) + " to " + str(self.value_max) + ", " + "inverse = " + str(self.inverse) + ")"

    def export_object_as_dict(self) -> dict:
        return_dict = super().export_object_as_dict()

        to_name = self.object_to_test
        if issubclass(type(to_name), ObjectNode):
            to_name = to_name.get_name()

        return_dict["to_name"] = to_name
        return_dict["tag"] = self.tag
        return_dict["value_min"] = self.value_min
        return_dict["value_max"] = self.value_max

        return return_dict
    
class InBiasRangeTest(ConditionTest):
    def __init__(self, object_to_test, bias_axis, min_accept=-100, max_accept=100, inverse=False, score=1):
        super().__init__(name="In Bias Range Test", test_type = TestType.IN_BIAS_RANGE, inverse=inverse, score=score)

        self.object_to_test = object_to_test
        self.bias_axis = bias_axis
        self.min_accept = min_accept
        self.max_accept = max_accept

    def export_object_as_dict(self) -> dict:
        return_dict = super().export_object_as_dict()

        to_name = self.object_to_test
        if issubclass(type(to_name), ObjectNode):
            to_name = to_name.get_name()

        return_dict["to_name"] = to_name
        return_dict["bias_axis"] = self.bias_axis
        return_dict["min_accept"] = self.min_accept
        return_dict["max_accept"] = self.max_accept

class ObjectEqualityTest(ConditionTest):
    def __init__(self, object_list, inverse=False, score=1):
        super().__init__(name="Object Equality Test", test_type=TestType.OBJECT_EQUALITY, inverse=inverse, score=score)

        self.object_list = object_list

    def __str__(self):

        printlist = ""

        for item in self.object_list:
            printlist += str(item)
            printlist += ", "

        return self.name + " (" + printlist[:-2] + ", inverse = " + str(self.inverse) + ")"
    
    def export_object_as_dict(self) -> dict:
        return_dict = super().export_object_as_dict()
        return_dict["object_name_list"] = []

        for item in self.object_list:
            object_name = item
            if issubclass(type(object_name), ObjectNode):
                object_name = item.get_name()
            return_dict["object_name_list"].append(object_name)

        return return_dict



# class HasDoubleEdgeTest(ConditionTest):
#     def __init__(self, object_from_test, edge_name_test, object_to_test, value_test = None, soft_equal = False, inverse = False):

#         super().__init__("Has Edge Test", inverse)

#         self.object_from_test = object_from_test
#         self.edge_name_test = edge_name_test
#         self.object_to_test = object_to_test
#         self.value_test = value_test
#         self.soft_equal = soft_equal
#         self.test_type = TestType.HAS_DOUBLE_EDGE

#     def __str__(self):
#         return self.name + " (" + str(self.object_from_test) + " " + str(self.edge_name_test) + " " + str(self.object_to_test) + ", " + "inverse = " + str(self.inverse) + ")"

        
