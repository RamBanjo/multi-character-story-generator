from application.components.ConditionTest import HasTagTest, ObjectEqualityTest, SameLocationTest
from application.components.RelChange import ConditionalChange, RelChange, TagChange, TaskChange
from application.components.UtilityEnums import ChangeAction, GenericObjectNode
from application.components.StoryGraphTwoWS import StoryGraph
from application.components.WorldState import WorldState
from application.components.CharacterTask import CharacterTask, TaskStack
from application.components.StoryNode import StoryNode
from application.components.StoryObjects import CharacterNode, LocationNode

# Testing Conditions

# hey = [1,2,3,4,5]

# #expect:
# #First Step 0
# last_task_step = -1
# print(hey[last_task_step:])

# fruit = "abcde"
# print(fruit[:-1])

alice = CharacterNode("Alice")
bob = CharacterNode("Bob")
charlie = CharacterNode("Charlie", tags={"Type":"Character", "Job":"Police"})
daniel = CharacterNode("Daniel")

town = LocationNode("Town")

world_state = WorldState(name="World State", objectnodes=[alice, bob, charlie, daniel])

world_state.connect(from_node=town, edge_name="holds", to_node=alice)
world_state.connect(from_node=town, edge_name="holds", to_node=bob)
world_state.connect(from_node=town, edge_name="holds", to_node=charlie)
world_state.connect(from_node=town, edge_name="holds", to_node=daniel)
world_state.connect(from_node=bob, edge_name="rivals", to_node=daniel)
world_state.connect(from_node=daniel, edge_name="rivals", to_node=bob)

# Bob gives a task to Alice. Bob wants to get Daniel in legal trouble.
# - Alice goes to Daniel and plants evidence on him.
# - Alice reports it to Charlie.
actor_shares_location_with_target = SameLocationTest(list_to_test=[GenericObjectNode.GENERIC_ACTOR, GenericObjectNode.GENERIC_TARGET])
target_becomes_suspicious = TagChange(name="Target Becomes Sus", object_node_name=GenericObjectNode.GENERIC_TARGET, tag="Sus", value=True, add_or_remove=ChangeAction.ADD)

plant_evidence = StoryNode(name="Plant Evidence On Person", actor=[GenericObjectNode.TASK_OWNER], target=["mark"],target_count=1, required_test_list=[actor_shares_location_with_target], effects_on_next_ws=[target_becomes_suspicious])

target_is_police = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Job", value="Police")
target_shares_location_with_something =SameLocationTest(list_to_test=[GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, GenericObjectNode.GENERIC_TARGET])
something_is_sus = HasTagTest(object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, tag="Sus", value=True)
mark_is_not_police = ObjectEqualityTest(object_list=["mark", "police"], inverse=True)

target_investigating_something = RelChange(name="Begin Investigating Something", edge_name="investigating", node_a=GenericObjectNode.GENERIC_TARGET, node_b=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, value="suspicious", add_or_remove=ChangeAction.ADD)
if_its_sus_then_investigate = ConditionalChange(name="Investigate Sus People", list_of_condition_tests=[target_shares_location_with_something, something_is_sus], list_of_changes=[target_investigating_something])

report_suspicious_person = StoryNode(name="Report Suspicious Person", charcount=1, target_count=1, actor=[GenericObjectNode.GENERIC_ACTOR], target=["police"], required_test_list=[actor_shares_location_with_target, target_is_police, mark_is_not_police], effects_on_next_ws=[if_its_sus_then_investigate])

plant_evidence_on_rival_task = CharacterTask(task_name="Plant Evidence Task", task_actions=[plant_evidence], task_location_name="Town", actor_placeholder_string_list=["mark"])
report_to_police_task = CharacterTask(task_name="Report Police Task", task_actions=[report_suspicious_person], task_location_name="Town", actor_placeholder_string_list=["police", "mark"])

frame_rival_stack = TaskStack(stack_name="Frame Rival Stack", task_stack=[plant_evidence_on_rival_task, report_to_police_task])
give_frame_rival_stack = TaskChange(name="Change in Frame Rival Task", task_giver_name=GenericObjectNode.GENERIC_TARGET, task_owner_name=GenericObjectNode.GENERIC_ACTOR, task_stack=frame_rival_stack)

print(frame_rival_stack)
for task in frame_rival_stack.task_stack:
    print(task)
# To test this we also probably need a way to represent task stacks quicky in text form.