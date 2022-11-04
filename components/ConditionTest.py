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

class SameLocationTest(ConditionTest):
    def __init__(self, list_to_test, inverse = False):

        super().__init__("Same Location Test", inverse)

        self.list_to_test = list_to_test
        self.test_type = TestType.SAME_LOCATION

class HasEdgeTest(ConditionTest):
    def __init__(self, object_from_test, edge_name_test, object_to_test, inverse = False):

        super().__init__("Has Edge Test", inverse)

        self.object_from_test = object_from_test
        self.edge_name_test = edge_name_test
        self.object_to_test = object_to_test
        self.test_type = TestType.HAS_EDGE

class HasDoubleEdgeTest(ConditionTest):
    def __init__(self, object_from_test, edge_name_test, object_to_test, inverse = False):

        super().__init__("Has Edge Test", inverse)

        self.object_from_test = object_from_test
        self.edge_name_test = edge_name_test
        self.object_to_test = object_to_test
        self.test_type = TestType.HAS_DOUBLE_EDGE
        
