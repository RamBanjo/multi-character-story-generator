#Alright here's the thing
#Alice wants to ask Bob to do a task, to kill someone she hates
#The requirements are:
# - Task Giver must hate the "kill_target"
# - Task Giver must not hate the Task Owner
# - Task Owner must not like the "kill_target"
# - Task Owner must not love the "kill_target"

from components.CharacterTask import CharacterTask, TaskStack
from components.ConditionTest import HasEdgeTest
from components.RelChange import TagChange
from components.StoryNode import StoryNode
from components.StoryObjects import CharacterNode, LocationNode
from components.UtilityEnums import ChangeAction, GenericObjectNode
from components.WorldState import WorldState


alice = CharacterNode("Alice")
bob = CharacterNode("Bob")
charlie = CharacterNode("Charlie")
daniel = CharacterNode("Daniel")
eve = CharacterNode("Eve")
frank = CharacterNode("Frank")

town_square = LocationNode("Town Square")
castle = LocationNode("Castle")

test_ws = WorldState("TestWS", objectnodes=[alice, bob, charlie, daniel, eve, frank, town_square, castle])

test_ws.connect(from_node=bob, edge_name="hates", to_node=charlie, value="political_rival")
test_ws.connect(from_node=bob, edge_name="hates", to_node=daniel, value="political_rival")
test_ws.connect(from_node=bob, edge_name="hates", to_node=frank, value="political_rival")
test_ws.doubleconnect(nodeA=alice, edge_name="loves", nodeB=daniel, value="married")

test_ws.connect(from_node=town_square, edge_name="holds", to_node=alice)
test_ws.connect(from_node=town_square, edge_name="holds", to_node=bob)
test_ws.connect(from_node=castle, edge_name="holds", to_node=charlie)
test_ws.connect(from_node=castle, edge_name="holds", to_node=daniel)
test_ws.connect(from_node=castle, edge_name="holds", to_node=eve)
test_ws.connect(from_node=castle, edge_name="holds", to_node=frank)

task_giver_hates_target = HasEdgeTest(object_from_test=GenericObjectNode.TASK_GIVER, edge_name_test="hates", object_to_test="kill_target", soft_equal=True)
task_giver_not_hate_task_owner = HasEdgeTest(object_from_test=GenericObjectNode.TASK_GIVER, edge_name_test="hates", object_to_test=GenericObjectNode.TASK_OWNER, soft_equal=True, inverse=True)
task_owner_not_like_target = HasEdgeTest(object_from_test=GenericObjectNode.TASK_OWNER, edge_name_test="friends", object_to_test="kill_target", soft_equal=True, inverse=True)
task_owner_not_love_target = HasEdgeTest(object_from_test=GenericObjectNode.TASK_OWNER, edge_name_test="loves", object_to_test="kill_target", soft_equal=True, inverse=True)

murder_target_dies = TagChange("Murder Target Dies", object_node_name="kill_target", tag="Alive", value=False, add_or_remove=ChangeAction.ADD)
kill_murder_target_node = StoryNode(name="Kill Target", charcount=1, target_count=1, biasweight=0, tags={"Type":"Murder"}, effects_on_next_ws=[murder_target_dies], actor=[GenericObjectNode.TASK_OWNER], target=["kill_target"])

kill_murder_target_task = CharacterTask(task_name="Kill Murder Target", task_actions=[kill_murder_target_node], task_location_name="Castle", actor_placeholder_string_list=["kill_target"])

#TaskStack objects might have to be created on demand if it requires the names of the task giver and task owner
kill_hated_character_task = TaskStack(stack_name="Kill Hated Character", task_stack=[kill_murder_target_task], task_stack_requirement=[task_giver_hates_target, task_giver_not_hate_task_owner, task_owner_not_like_target, task_owner_not_love_target], stack_owner_name="Alice", stack_giver_name="Bob")

#Bob hates Charlie Daniel and Frank.
#Alice loves Daniel.
#Eve is unrelated.
#There should be two kill targets: Frank or Charlie

list_of_pos_replacements = test_ws.make_list_of_possible_task_stack_character_replacements(kill_hated_character_task)

print("Kill Target Dicts")
for x in list_of_pos_replacements:
    print(x)
print("=====")

#The second part of this will test tasks with more than one step, now that we know tasks with more than one right answer works properly.

# The task:
# Bob wants to relay some information to one of his friends, but that information has to threatened out of one of his enemies.
# 
# Alice: Task owner
# Bob: Task giver
# Charlie, Frank: Enemy of Bob
# Gary, Hailey, Irma: Friend of Bob
#
# We can expect 6 different dicts from this.

gary = CharacterNode("Gary")
hailey = CharacterNode("Hailey")
irma = CharacterNode("Irma")

pub = LocationNode("Pub")

test_ws.add_nodes([gary, hailey, irma, pub])

test_ws.doubleconnect(nodeA=bob, edge_name="enemies", nodeB=charlie)
test_ws.doubleconnect(nodeA=bob, edge_name="enemies", nodeB=frank)
test_ws.doubleconnect(nodeA=bob, edge_name="friend_of", nodeB=gary)
test_ws.doubleconnect(nodeA=bob, edge_name="friend_of", nodeB=hailey)
test_ws.doubleconnect(nodeA=bob, edge_name="friend_of", nodeB=irma)

test_ws.connect(from_node=pub, edge_name="holds", to_node=gary)
test_ws.connect(from_node=pub, edge_name="holds", to_node=hailey)
test_ws.connect(from_node=pub, edge_name="holds", to_node=irma)

task_giver_friend_with_information_getter = HasEdgeTest(object_from_test=GenericObjectNode.TASK_GIVER, edge_name_test="friend_of", object_to_test="information_getter", soft_equal=True)
task_giver_enemies_with_information_extract_target = HasEdgeTest(object_from_test=GenericObjectNode.TASK_GIVER, edge_name_test="enemies", object_to_test="information_extract_target", soft_equal=True)

#in order to test whether or not the simulation performs these steps, I will have the nodes do the following;
#First Step: Once performed, will give the task's generic actor a new tag called "know_info_on_task" which will be set to True.
#Second Step: This part will require the tag "know_info_on_task" to be "True".
know_information_by_actor = TagChange(name="Actor Learns Info", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="known_info_on_Get Info and Report_task", value=True, add_or_remove=ChangeAction.ADD)
know_information_by_target = TagChange(name="Target Learns Info", object_node_name=GenericObjectNode.GENERIC_TARGET, tag="known_info_on_Get Info and Report_task", value=True, add_or_remove=ChangeAction.ADD)

extract_info_from_enemy = StoryNode(name="Extract Info", charcount=1, target_count=1, biasweight=0, tags={"Type":"Investigate"}, effects_on_next_ws=[know_information_by_actor], actor=[GenericObjectNode.TASK_OWNER], target=["information_extract_target"])
give_info_to_ally = StoryNode(name="Give Info", charcount=1, target_count=1, biasweight=0, tags={"Type":"Conversation"}, effects_on_next_ws=[know_information_by_target], actor=[GenericObjectNode.TASK_OWNER], target=["information_getter"])

extract_info_task = CharacterTask(task_name="Extract Info Task", task_actions=[extract_info_from_enemy], task_location_name="Castle", task_requirement=[], actor_placeholder_string_list=["information_extract_target"])
give_info_task = CharacterTask(task_name="Give Info Task", task_actions=[give_info_to_ally], task_location_name="Pub", task_requirement=[], actor_placeholder_string_list=["information_getter"])
get_info_and_report_taskstack = TaskStack(stack_name="Get Info and Report", stack_owner_name="Alice", stack_giver_name="Bob", task_stack=[extract_info_task, give_info_task], task_stack_requirement=[task_giver_friend_with_information_getter, task_giver_enemies_with_information_extract_target])

list_of_pos_replacements = test_ws.make_list_of_possible_task_stack_character_replacements(get_info_and_report_taskstack)

print("Info Gathering Dict")
for x in list_of_pos_replacements:
    print(x)
print("=====")