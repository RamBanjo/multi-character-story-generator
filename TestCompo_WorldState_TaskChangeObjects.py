#Test the Task Change Objects

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

town_square = LocationNode("Town Square")
castle = LocationNode("Castle")

test_ws = WorldState("TestWS", objectnodes=[alice, bob, charlie, daniel, eve, town_square, castle])

#The test: Bob hates Charlie and Daniel. The Task involves the actor doing the task traveling towards the location of the character hated by the task giver and killing them.

task_giver_hates_target = HasEdgeTest(object_from_test=GenericObjectNode.TASK_GIVER, edge_name_test="hates", object_to_test="murder_target", soft_equal=True)
task_giver_not_hate_task_owner = HasEdgeTest(object_from_test=GenericObjectNode.TASK_GIVER, edge_name_test="hates", object_to_test=GenericObjectNode.TASK_OWNER, soft_equal=True, inverse=True)
task_owner_not_like_target = HasEdgeTest(object_from_test=GenericObjectNode.TASK_OWNER, edge_name_test="friends", object_to_test="murder_target", soft_equal=True, inverse=True)
task_owner_not_love_target = HasEdgeTest(object_from_test=GenericObjectNode.TASK_OWNER, edge_name_test="loves", object_to_test="murder_target", soft_equal=True, inverse=True)

murder_target_dies = TagChange("Murder Target Dies", object_node_name="murder_target", tag="Alive", value=False, add_or_remove=ChangeAction.ADD)
kill_murder_target_node = StoryNode(name="Kill Target", charcount=1, target_count=1)

kill_murder_target_task = CharacterTask(task_name="Kill Murder Target", task_actions=[kill_murder_target_node], task_location_name="Castle")

#TaskStack objects might have to be created on demand if it requires the names of the task giver and task owner
kill_hated_character_task = TaskStack(stack_name="Kill Hated Character", task_stack=[kill_murder_target_task], task_stack_requirement=[task_giver_hates_target, task_giver_not_hate_task_owner, task_owner_not_like_target, task_owner_not_love_target], stack_owner_name="Alice", stack_giver_name="Bob")