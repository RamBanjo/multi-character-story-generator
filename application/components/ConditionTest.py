import sys
sys.path.insert(0,'')

from application.components.UtilityEnums import TestType

class ConditionTest:
    def __init__(self, name, test_type, inverse=False, score=1):
        self.name = name
        self.inverse = inverse
        self.score = score
        self.test_type = test_type

class HeldItemTagTest(ConditionTest):
    def __init__(self, holder_to_test, tag_to_test, value_to_test, soft_equal = True, inverse = False, score=1):
        
        super().__init__(name="Held Item Test", test_type= TestType.HELD_ITEM_TAG, inverse=inverse, score=score)

        self.holder_to_test = holder_to_test
        self.tag_to_test = tag_to_test
        self.value_to_test = value_to_test
        self.soft_equal = soft_equal

    def __str__(self):
        return self.name + " (" + str(self.holder_to_test) + " {" + str(self.tag_to_test) + ":" + str(self.value_to_test) + "}, inverse = " + str(self.inverse) + ")"

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

class HasTagTest(ConditionTest):
    def __init__(self, object_to_test, tag, value, soft_equal = False, inverse=False, score=1):
        super().__init__(name="Has Tag Test", test_type = TestType.HAS_TAG, inverse=inverse, score=score)

        self.object_to_test = object_to_test
        self.tag = tag
        self.value = value
        self.soft_equal = soft_equal

    def __str__(self):
        return self.name + " (" + str(self.object_to_test) + " " + str(self.tag) + " " + str(self.value) + ", " + "inverse = " + str(self.inverse) + ")"

class TagValueInRangeTest(ConditionTest):
    def __init__(self, object_to_test, tag, value_min, value_max, inverse=False, score=1):

        super().__init__(name="Tag Value in Range Test", test_type = TestType.TAG_VALUE_IN_RANGE, inverse=inverse, score=score)

        self.object_to_test = object_to_test
        self.tag = tag
        self.value_min = value_min
        self.value_max = value_max

    def __str__(self) -> str:
        return self.name + " (" + str(self.object_to_test) + " " + str(self.tag) + " " + str(self.value_min) + " to " + str(self.value_max) + ", " + "inverse = " + str(self.inverse) + ")"


class InBiasRangeTest(ConditionTest):
    def __init__(self, object_to_test, bias_axis, min_accept=-100, max_accept=100, inverse=False, score=1):
        super().__init__(name="In Bias Range Test", test_type = TestType.IN_BIAS_RANGE, inverse=inverse, score=score)

        self.object_to_test = object_to_test
        self.bias_axis = bias_axis
        self.min_accept = min_accept
        self.max_accept = max_accept


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

        
