from components.UtilityEnums import TestType

class ConditionTest:
    def __init__(self, name, inverse=False):
        self.name = name
        self.inverse = inverse

class HeldItemTagTest(ConditionTest):
    def __init__(self, holder_to_test, tag_to_test, value_to_test, inverse = False):
        
        super().__init__("Held Item Test", inverse)

        self.holder_to_test = holder_to_test
        self.tag_to_test = tag_to_test
        self.value_to_test = value_to_test
        self.test_type = TestType.HELD_ITEM_TAG

    def __str__(self):
        return self.name + " (" + str(self.holder_to_test) + " {" + str(self.tag_to_test) + ":" + str(self.value_to_test) + "}, inverse = " + str(self.inverse) + ")"

class SameLocationTest(ConditionTest):
    def __init__(self, list_to_test, inverse = False):

        super().__init__("Same Location Test", inverse)

        self.list_to_test = list_to_test
        self.test_type = TestType.SAME_LOCATION

    def __str__(self):

        printlist = ""

        for item in self.list_to_test:
            printlist += str(item)
            printlist += ", "

        return self.name + " (" + printlist[:-2] + ", inverse = " + str(self.inverse) + ")"

class HasEdgeTest(ConditionTest):
    def __init__(self, object_from_test, edge_name_test, object_to_test, value_test = None, soft_equal = False, inverse = False):

        super().__init__("Has Edge Test", inverse)

        self.object_from_test = object_from_test
        self.edge_name_test = edge_name_test
        self.object_to_test = object_to_test
        self.value_test = value_test
        self.soft_equal = soft_equal
        self.test_type = TestType.HAS_EDGE

    def __str__(self):
        return self.name + " (" + str(self.object_from_test) + " " + str(self.edge_name_test) + " " + str(self.object_to_test) + ", " + "inverse = " + str(self.inverse) + ")"

class HasDoubleEdgeTest(ConditionTest):
    def __init__(self, object_from_test, edge_name_test, object_to_test, value_test = None, soft_equal = False, inverse = False):

        super().__init__("Has Edge Test", inverse)

        self.object_from_test = object_from_test
        self.edge_name_test = edge_name_test
        self.object_to_test = object_to_test
        self.value_test = value_test
        self.soft_equal = soft_equal
        self.test_type = TestType.HAS_DOUBLE_EDGE

    def __str__(self):
        return self.name + " (" + str(self.object_from_test) + " " + str(self.edge_name_test) + " " + str(self.object_to_test) + ", " + "inverse = " + str(self.inverse) + ")"

        
