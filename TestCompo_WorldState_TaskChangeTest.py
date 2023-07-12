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

from components.ConditionTest import HasEdgeTest
from components.RelChange import RelChange, TagChange
from components.StoryNode import StoryNode
from components.StoryObjects import CharacterNode, LocationNode, ObjectNode
from components.UtilityEnums import ChangeAction, GenericObjectNode
from components.WorldState import WorldState

alice = CharacterNode(name="Alice")
bob = CharacterNode(name="Bob")
charlie = CharacterNode(name="Charlie")
daniel = CharacterNode(name="Daniel")

town = LocationNode(name="TownSquare")

present = ObjectNode(name="Present")

test_ws = WorldState(name="Test State", objectnodes=[alice, bob, charlie, daniel, town, present])

test_ws.connect(from_node=alice, edge_name="holds", to_node="present")
test_ws.doubleconnect(nodeA=bob, edge_name="friend_of", nodeB=charlie)
test_ws.doubleconnect(nodeA=bob, edge_name="hates", nodeB=charlie)

test_ws.connect(from_node=town, edge_name="holds", to_node=alice)
test_ws.connect(from_node=town, edge_name="holds", to_node=bob)
test_ws.connect(from_node=town, edge_name="holds", to_node=charlie)
test_ws.connect(from_node=town, edge_name="holds", to_node=daniel)

placeholder_for_present_task = {GenericObjectNode.TASK_GIVER: "Bob", GenericObjectNode.TASK_OWNER: "Alice", "thief":"Daniel", "present_receiver":"Charlies"}

target_hates_actor = RelChange(name = "Target Hate Actor", node_a=GenericObjectNode.GENERIC_TARGET, edge_name="hates", node_b=GenericObjectNode.GENERIC_ACTOR, value="defeat_for_steal_present_attempt", add_or_remove=ChangeAction.ADD)
target_becomes_injured = TagChange(name = "Target Becomes Injured", object_node_name=GenericObjectNode.GENERIC_TARGET, tag="Injured", value="minor", add_or_remove=ChangeAction.ADD)

target_likes_actor = RelChange(name = "Target Like Actor", node_a=GenericObjectNode.GENERIC_TARGET, edge_name="likes", node_b=GenericObjectNode.GENERIC_ACTOR, value="successful_item_delivery", add_or_remove=ChangeAction.ADD)
task_giver_likes_task_owner = RelChange(name = "Owner Like Giver", node_a=GenericObjectNode.TASK_OWNER, edge_name="likes", node_b=GenericObjectNode.TASK_GIVER, value="successful_item_delivery", add_or_remove=ChangeAction.ADD)
actor_loses_present = RelChange(name = "Actor Loses Present",  node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="holds", node_b=present, soft_equal=True, add_or_remove=ChangeAction.REMOVE)
target_gains_present = RelChange(name = "Target Gains Present", node_a=GenericObjectNode.GENERIC_TARGET, edge_name="holds", node_b=present, add_or_remove=ChangeAction.ADD)

thief_hates_task_giver = HasEdgeTest()
receiver_friends_task_giver = HasEdgeTest()

thief_intercept_present = StoryNode(name="Intercepted by Thief", bias_range=0, tags={"Type":"make_fight_reason"}, charcount=1, target_count=1, actor=["thief"], target=[GenericObjectNode.TASK_OWNER])
defeat_thief = StoryNode(name="Defeat Thief", bias_range=0, tags={"Type":"fight"}, charcount=1, target_count=1, actor=[GenericObjectNode.TASK_OWNER], target=["thief"])
give_present_to_receiver = StoryNode(name="Give Present to Recipient", bias_range=0, tags={"Type":"give_item"}, charcount=1, target_count=1, actor=[GenericObjectNode.TASK_OWNER], target=["present_receiver"])
