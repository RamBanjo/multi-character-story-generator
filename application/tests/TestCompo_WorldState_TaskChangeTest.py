#Testing Task Changes...with a dict!
#
# Scenario: Alice gets a quest from Bob. Bob wants Alice to deliver an item to one of his friends. However, someone that hates Bob wants to steal that item to cause trouble for bob.
#
# Task: Deliver Item to Target
# Steps: Fight Thief, Deliver Item
#
# Dict:
# Task Owner -> Alice
# Task Giver -> Bob
# Gift Receiver -> Charlie
# Gift Thief -> Daniel
#
# Task Stack Require
# "thief" hates the Task Giver
# "present_receiver" is a friend of Task Giver

# Things that should change after this task is applied:
# Charlie has the gift
# Alice gets the gift when she starts the quest, but loses it when she gives it to Charlie
# Charlie likes Alice for doing quest
# Bob likes Alice for doing quest
# Daniel hates Alice for doing quest
# Daniel becomes Injured
# (Wait NVM these will be tested in the World State. Oops!)
import sys
sys.path.insert(0,'')

from application.components.CharacterTask import CharacterTask, TaskStack
from application.components.ConditionTest import HasEdgeTest
from application.components.RelChange import RelChange, TagChange, TaskChange
from application.components.StoryNode import StoryNode
from application.components.StoryObjects import CharacterNode, LocationNode, ObjectNode
from application.components.UtilityEnums import ChangeAction, GenericObjectNode
from application.components.WorldState import WorldState

alice = CharacterNode(name="Alice")
bob = CharacterNode(name="Bob")
charlie = CharacterNode(name="Charlie")
daniel = CharacterNode(name="Daniel")
eve = CharacterNode(name="Eve")

town = LocationNode(name="TownSquare")

present = ObjectNode(name="Present", tags={"Type":"Present"})

test_ws = WorldState(name="Test State", objectnodes=[alice, bob, charlie, daniel, eve, town, present])

test_ws.connect(from_node=bob, edge_name="holds", to_node=present)
test_ws.doubleconnect(nodeA=bob, edge_name="friend_of", nodeB=charlie)
test_ws.doubleconnect(nodeA=bob, edge_name="hates", nodeB=daniel)

test_ws.connect(from_node=town, edge_name="holds", to_node=alice)
test_ws.connect(from_node=town, edge_name="holds", to_node=bob)
test_ws.connect(from_node=town, edge_name="holds", to_node=charlie)
test_ws.connect(from_node=town, edge_name="holds", to_node=daniel)
test_ws.connect(from_node=town, edge_name="holds", to_node=eve)

placeholder_for_present_task = {GenericObjectNode.TASK_GIVER: "Bob", GenericObjectNode.TASK_OWNER: "Alice", "thief":"Daniel", "present_receiver":"Charlie"}

#Eve can't be present receiver or thief because she does not have the right relations to Bob.
placeholder_for_present_task_bad = {GenericObjectNode.TASK_GIVER: "Bob", GenericObjectNode.TASK_OWNER: "Alice", "thief":"Daniel", "present_receiver":"Eve"}
placeholder_for_present_task_bad2 = {GenericObjectNode.TASK_GIVER: "Bob", GenericObjectNode.TASK_OWNER: "Alice", "thief":"Eve", "present_receiver":"Charlie"}

target_hates_actor = RelChange(name = "Target Hate Actor", node_a=GenericObjectNode.GENERIC_TARGET, edge_name="hates", node_b=GenericObjectNode.GENERIC_ACTOR, value="defeat_for_steal_present_attempt", add_or_remove=ChangeAction.ADD)
target_becomes_injured = TagChange(name = "Target Becomes Injured", object_node_name=GenericObjectNode.GENERIC_TARGET, tag="Injured", value="minor", add_or_remove=ChangeAction.ADD)

target_likes_actor = RelChange(name = "Target Like Actor", node_a=GenericObjectNode.GENERIC_TARGET, edge_name="likes", node_b=GenericObjectNode.GENERIC_ACTOR, value="successful_item_delivery", add_or_remove=ChangeAction.ADD)
task_giver_likes_task_owner = RelChange(name = "Owner Like Giver", node_a=GenericObjectNode.TASK_OWNER, edge_name="likes", node_b=GenericObjectNode.TASK_GIVER, value="successful_item_delivery", add_or_remove=ChangeAction.ADD)
actor_loses_present = RelChange(name = "Actor Loses Present",  node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="holds", value = None, node_b=present, soft_equal=True, add_or_remove=ChangeAction.REMOVE)
target_gains_present = RelChange(name = "Target Gains Present", node_a=GenericObjectNode.GENERIC_TARGET, edge_name="holds", value = None, node_b=present, add_or_remove=ChangeAction.ADD)

thief_hates_task_giver = HasEdgeTest(object_from_test="thief", edge_name_test="hates", object_to_test=GenericObjectNode.TASK_GIVER, soft_equal=True)
receiver_friends_task_giver = HasEdgeTest(object_from_test="present_receiver", edge_name_test="friend_of", object_to_test= GenericObjectNode.TASK_GIVER, soft_equal=True, two_way=True)
tstack_req = [thief_hates_task_giver, receiver_friends_task_giver]

list_of_change_actor_give_target_present = [actor_loses_present, target_gains_present]

task_giver_gives_present = StoryNode(name="Get Present from Quest Giver", biasweight=0, tags={"give_item"}, charcount=1, target_count=1, actor=[GenericObjectNode.TASK_GIVER], target=[GenericObjectNode.TASK_OWNER])
thief_intercept_present = StoryNode(name="Intercepted by Thief", biasweight=0, tags={"Type":"make_fight_reason"}, charcount=1, target_count=1, actor=["thief"], target=[GenericObjectNode.TASK_OWNER])
defeat_thief = StoryNode(name="Defeat Thief", biasweight=0, tags={"Type":"fight"}, charcount=1, target_count=1, actor=[GenericObjectNode.TASK_OWNER], target=["thief"])
give_present_to_receiver = StoryNode(name="Give Present to Recipient", biasweight=0, tags={"Type":"give_item"}, charcount=1, target_count=1, actor=[GenericObjectNode.TASK_OWNER], target=["present_receiver"])

give_present_thief_intercept_task = CharacterTask(task_name="Give Present Interception Task", task_actions=[thief_intercept_present, defeat_thief, give_present_to_receiver], task_location_name="TownSquare", actor_placeholder_string_list=["thief", "present_receiver"])
give_present_thief_intercept_stack = TaskStack(stack_name="Give Persent Interception Stack", task_stack=[give_present_thief_intercept_task], stack_giver_name="Bob", stack_owner_name="Alice", task_stack_requirement=tstack_req)
give_present_thief_intercept_stack.placeholder_info_dict = placeholder_for_present_task

add_gpti_stack = TaskChange(name="Give GPTI Stack Task", task_giver_name="Bob", task_owner_name="Alice", task_stack=give_present_thief_intercept_stack)

tstack = test_ws.make_list_of_possible_task_stack_character_replacements(give_present_thief_intercept_stack)
test_ws.apply_task_change(add_gpti_stack, verbose=True)