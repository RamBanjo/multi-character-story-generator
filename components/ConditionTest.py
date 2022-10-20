from components.UtilityEnums import TestType

class ConditionTest:
    def __init__(self, name):
        self.name = name

class HeldItemTagTest(ConditionTest):
    def __init__(self, holder_to_test, tag_to_test, value_to_test):
        
        super().__init__("Held Item Test")

        self.holder_to_test = holder_to_test
        self.tag_to_test = tag_to_test
        self.value_to_test = value_to_test
        self.test_type = TestType.HELD_ITEM_TAG

class SameLocationTest(ConditionTest):
    def __init__(self, list_to_test):

        super().__init__("Same Location Test")

        self.list_to_test = list_to_test
        self.test_type = TestType.SAME_LOCATION

class HasOutgoingEdgeTest(ConditionTest):
    def __init__(self, edge_name_test, object_to_test):

        super().__init__("Has Outgoing Edge Test")

        self.edge_name_test = edge_name_test
        self.object_to_test = object_to_test
        self.test_type = TestType.OUTGOING_LINK

class HasIncomingEdgeTest(ConditionTest):
    def __init__(self, edge_name_test, object_to_test):

        super().__init__("Has Incoming Edge Test")

        self.edge_name_test = edge_name_test
        self.object_to_test = object_to_test
        self.test_type = TestType.INCOMING_LINK
