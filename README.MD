# Affinity-Based Multi Character Story Generator Using Rewrite Rules

Hello! This is the guide on how to use the Multi Character Story Generator's source code to generate your stories from an input of object nodes.

## 1. Creating a new file.

First, create a python (.py) file in the tests folder. Then, at the top of the file, make the following imports:

```py
#Imports below this line are required
import sys
sys.path.insert(0,'')

from application.components.StoryObjects import *
from application.components.WorldState import *
from application.components.CharacterTask import *
from application.components.StoryGraphTwoWS import *
from application.components.StoryNode import *
from application.components.RelChange import *
from application.components.UtilityEnums import *
from application.components.RewriteRuleWithWorldState import *
from application.StoryGeneration_NewFlowchart_WithMetrics import generate_multiple_graphs, generate_story_from_starter_graph, make_base_graph_from_previous_graph

#This import is optional, if you want to print the results to a folder instead of printing it in console.
import os

#This report is optional, if you want to print the time spent generating the graph.
from datetime import datetime
```

## 2. Define the characters.

Now, you can begin defining the characters of your story. I recommend only defining characters with a significant amount of actions in the story as CharacterNodes, the rest can be defined as ObjectNodes if you feel they do not do too many actions within the story.

Here is an example of characters being defined.

```py
#Example from LittleRedWorldState.py
red = CharacterNode(name="Red", tags={"Type":"Character", "Age":"Child", "Alive":True}, internal_id=0)
wolf = CharacterNode(name="Wolf", biases={"moralbias":-50, "lawbias":-50}, tags={"Type":"Character", "Age":"Adult", "EatsChildren":True, "EatsNonChildren":True, "Alive":True, "CanKill":"Fangs"}, internal_id=1)
brick_pig = CharacterNode(name="Brick", tags={"Type":"Character", "Age":"Adult", "Pacifist":True, "Alive":True, "LikesTreasure":True, "OwnsForestHome":True}, internal_id=2)
grandma = CharacterNode(name="Grandma", biases={"moralbias":-50, "lawbias":0}, tags={"Type":"Character", "Age":"Adult", "Alive":True, "LikesKnowledge":True, "CanKill":"Knife"}, internal_id=3)

#Example from ColumboStoryWorldState.py
columbo = CharacterNode(name="Columbo", biases={"lawbias":0, "moralbias":0}, tags={"Type":"Character","Job":"Explorer","Species":"Human", "Goal":"Explore New World","Alive":True, "PlotArmor":True, "Stranded":True}, internal_id=0)
iris = CharacterNode(name="Iris", biases={"lawbias":0, "moralbias":0}, tags={"Type":"Character","Job":"Destroyer","Species":"Robot", "Goal":"Eradicate Living Beings", "Version":"Old", "Alive":True}, internal_id=1)
amil = CharacterNode(name="Amil", biases={"lawbias":0, "moralbias":0}, tags={"Type":"Character","Job":"Military","Species":"Human", "Goal":"Rescue Mission","PlotArmor":True,"Alive":True}, internal_id=2)

```

## 3. Define other objects and locations.

Next, define the important objects in your world state, as well as locations. Characters that do not contribute much to the story can also be defined as ObjectNodes.

```py
#Example from ColumboStoryWorldState.py
tatain = LocationNode(name="Tatain", tags={"Type":"Location", "Climate":"Sandy", "AlienGodsWill":"Destroy"}, internal_id=7)
outer_space = LocationNode(name="Outer Space", tags={"Type":"Location", "Climate":"Space", "AlienGodsWill":"Unknown"}, internal_id=10)

#Example from LittleRedWorldState.py
mom = ObjectNode(name="Red's Mom", tags={"Type":"NoStoryCharacter", "Age":"Adult", "Alive":True}, internal_id=5)
wood_pig = ObjectNode(name="Wood Pig", tags={"Type":"NoStoryCharacter", "Age":"Child", "Alive":True}, internal_id=6)

protection_pillar = ObjectNode(name="Protection Pillar", tags={"Type":"Object", "ProtectsHomes":True, "Active":False}, internal_id=12)
columbo_diary = ObjectNode(name="Columbo's Diary", tags={"Type":"Object", "KnowledgeObject":True}, internal_id=13)
golden_goose = ObjectNode(name="Golden Goose", tags={"Type":"Object", "Valuable":True}, internal_id=14)
singing_harp = ObjectNode(name="Singing Harp", tags={"Type":"Object", "Valuable":True}, internal_id=15)
```

## 4. Add all the defined objects to a list, then use it to define your initial WorldState.

```py
all_objects = [thing_1, thing_2, thing_3, thing_4, ... , thing_n]

world_state = WorldState(name="Test WS", objectnodes=all_objects)
```

## 5. Define connections between objects in your initial WorldState.

Remember that you can use world_state.DEFAULT_HOLD_EDGE_NAME and world_state.DEFAULT_ADJACENCY_EDGE_NAME to keep things consistent (assuming the WorldState's name is world_state)! The DEFAULT_HOLD_EDGE_NAME is used to define a relationship where an object holds another object (including characters having items and locations holding characters or objects), and the DEFAULT_ADJACENCY_EDGE_NAME is used to define a relationship where a character is able to travel to another location.

There are two ways to connect two nodes in a WorldState. Calling WorldState.connect connects the nodes in only one direction, and calling WorldState.doubleconnect connects the nodes in both directions, allowing you to create one-way relationships.

```py

world_state.connect(from_node=bear_house, edge_name=world_state.DEFAULT_HOLD_EDGE_NAME, to_node=papabear)
world_state.connect(from_node=papa_bear, edge_name=world_state.DEFAULT_HOLD_EDGE_NAME, to_node=honey_pot)

world_state.doubleconnect(from_node=plains_village, edge_name=world_state.DEFAULT_ADJACENCY_EDGE_NAME, to_node=forest_path)

#You can also define your own relationships.
world_state.doubleconnect(from_node=papabear, edge_name="romantic_love", to_node=mamabear)
world_state.connect(from_node=papabear, edge_name="hates", to_node=wolf)
world_state.connect(from_node=wolf, edge_name="likes", to_node=papabear)
```

## 6. Define the story nodes, along with the requirements and the changes it will cause on the world state once performed. (See ToolTip in StoryNode for more information)

Actions are defined as StoryNodes. If the action can be done by multiple characters, you can change the allowed number of characters by changing the charcount (for the number of actors) or target_count (for the number of targets). There is more information within the tooltip for the StoryNode.

Additionally, you can use GenericObjectNodes as pointers towards actor, the target, or the location of the StoryNode.

```py
some_action = StoryNode(name = "Do Something")

actor_dislikes_target = HasEdgeTest(object_from_test = GenericObjectNode.GENERIC_ACTOR, edge_name_test = "dislikes", object_to_test = GenericObjectNode.GENERIC_TARGET, soft_equal = True)
target_becomes_injured = TagChange(name = "Target Becomes Injured", object_node_name = GenericObjectNode.GENERIC_TARGET, tag="Injured", value=True, add_or_remove=ChangeAction.ADD)
attack_another_character = StoryNode(name = "Attack Another Character", charcount=1, target_count=1, effects_on_next_ws=[target_becomes_injured], required_test_list=[actor_dislikes_target])

#Tests can also be optional. When tests are listed in suggested_test_list instead of required_test_list they do not have to be fulfilled to have the node be valid, but they grant extra points during the generation process. The more points an action has, the more likely it will be performed by characters.
actor_likes_target_for_bonus_points = HasEdgeTest(object_from_test = GenericObjectNode.GENERIC_ACTOR, edge_name_test = "likes", object_to_test = GenericObjectNode.GENERIC_TARGET, soft_equal = True, score = 10)

give_candy = StoryNode(name = "Give Candy", charcount=1, target_count=1, effects_on_next_ws=[], required_test_list=[actor_likes_target_for_bonus_points])
```

## 7. Define rules that the StoryGenerator can use to change the story.

There are four types of rules that can be written. The RewriteRule is used for rules that only apply to one character's story line. If the pattern listed in story_condition exists in the story line, then the actions listed in story_change can be applied to that story line.

```py

some_action = StoryNode(name = "Do Something")
another_action = StoryNode(name = "Do Another Thing")
example_rule = RewriteRule(rule_name = "If Doing Something then Do Another Thing", story_condition = [some_action], story_change = [another_action])

#You can also write patternless rules. This rule can be applied anywhere in the story, as long as the conditions to perform the additional node is there.
sudden_action = StoryNode(name = "Sudden Action")
example_rule_2 = RewriteRule(rule_name = "Patternless Sudden Action", story_condition = [], story_change = [sudden_action])
```

The JoiningJointRule, the ContinuousJointRule, and the SplittingJointRule are for multiple characters and require joint nodes to be used in certain places.

```py

do_something_alone_a = StoryNode(name = "Do Something Alone A")
do_something_alone_b = StoryNode(name = "Do Something Alone B")
do_something_together = StoryNode(name = "Do Something Together", charcount = 2)
do_another_together = StoryNode(name = "Do Another Thing Together", charcount = 2)

joining_rule_1 = JoiningJointRule(rule_name = "Something Alone AB into Do Together", base_actions = [do_something_alone_a, do_something_alone_b], joint_node = do_something_together)

#JoiningJointRule can be patternless.
joining_rule_2 = JoiningJointRule(rule_name = "Patternless Joining Joint Rule", base_actions = [], joint_node = do_another_together)

continue_together = StoryNode (name = "Continue Something Together", charcount = 2)
cont_rule = ContinuousJointRule(rule_name = "Continuous Joint Rule", base_joint = do_something_together, joint_node = continue_together)

split_a = StoryNode (name = "Split A")
split_b = StoryNode (name = "Split B")

split_rule = SplittingJointRule(rule_name = "Splitting Rule", base_joint = continue_together, split_list = [split_a, split_b])
```

## 8. Define task actions and the tasks that the character can get / will start with.

Tasks are for actions with a specific location. A TaskStack is a list of CharacterTask and a CharacterTask consists of multiple StoryNodes to be done at a certain location. For nodes that are actions in tasks, you must fill in the actor and target (if there is any) with either an ObjectNode, a GenericObjectNode, or a placeholder string.

GenericObjectNode.TASK_OWNER is the character who owns the task, i.e. they are the one performing it.
GenericObjectNode.TASK_GIVER is the character who assigned the task. If there is not assigner, the Task Owner can also be the Task Giver.

Placeholder strings will be substituted with a CharacterObject that fulfills the ConditionTests listed in the CharacterTask and TaskStack.

Once the TaskStack is created, you can assign it to characters with a TaskChange object by adding the TaskChange object to a StoryNode. You may want to use conditionals to limit the task from being assigned to a character more than once if you intend to use this StoryNode as a part of a rule and not as an initial StoryGraph state.
```py

somewhere = LocationNode(name = "Somewhere")
another_place = LocationNode(name = "Another Place")

task_owner_likes_the_placeholder = HasEdgeTest(object_from_test = GenericObjectNode.TASK_OWNER, edge_name_test = "likes", object_to_test = "liked_character", soft_equal = True)

node_a1 = StoryNode(name = "Story Node A1", actor = [GenericObjectNode.TASK_OWNER])
node_a2 = StoryNode(name = "Story Node A2", actor = [GenericObjectNode.TASK_OWNER], target = ["liked_character"]) 

task_a = CharacterTask(task_name = "Task A", task_actions = [node_a1, node_a2], task_location_name = "Somewhere", task_requirement = [task_owner_likes_the_placeholder], actor_placeholder_string_list = ["liked_character"])

magic_key = ObjectNode(name = "Magic Key", tags = tags={"Type":"Key", "UnlocksMagicTemple":True}, internal_id = 10)

node_b1 = StoryNode(name = "Story Node B1", actor = [GenericObjectNode.TASK_OWNER])
node_b2 = StoryNode(name = "Story Node B2", actor = [GenericObjectNode.TASK_OWNER], target = [magic_key])

task_b = CharacterTask(task_name = "Task B", task_actions = [node_b1, node_b2], task_location_name = "Another Place")

example_stack = TaskStack(stack_name = "Stack Name", task_stack = [task_a, task_b])
example_stack_change = TaskChange(name = "Example TaskChange", task_stack = example_stack, task_giver_name = GenericObjectNode.GENERIC_ACTOR, task_owner_name = GenericObjectNode.GENERIC_ACTOR)

assign_task_action = StoryNode(name = "Assign Task Action", effects_on_next_ws = [example_stack_change])
```

## 9. Set up the initial StoryGraph.

This will be the state of the StoryGraph at the beginning of generation. Make sure to add the WorldState you created earlier as well as initial actions for the characters in the story.

```py
example_graph = StoryGraph(name = "Example Graph", character_objects = [alice, bob, charlie, daniel], starting_ws = example_world_state)

example_graph.insert_story_part(part = action_a, character = alice, location = somewhere)
example_graph.insert_joint_node(joint_node = joint_x, main_actor = bob, other_actors = [daniel], location = somewhere, targets = [charlie])
```

## 10. Set up the generation function.

Decide how many graphs you want to generate. If you want to generate only one graph, you can use generate_story_from_starter_graph to generate your graph.

```py

finish_gen_time = datetime.now()

generated_graph = generate_story_from_starter_graph(init_storygraph=initial_graph, list_of_rules = list_of_rules, required_story_length = 10)

finish_gen_time = datetime.now()
print("xxx")
print("Generation Time:", str(finish_gen_time-start_gen_time))
```

Multigraph generation is recommended for longer stories. The generation time increases with length exponentially, so splitting the story into multiple small graphs is recommended for longer stories.

```py

finish_gen_time = datetime.now()

generated_graph_list = generate_multiple_graphs(initial_graph=initial_graph, list_of_rules = list_of_rules, required_story_length=30, max_storynodes_per_graph=5)

finish_gen_time = datetime.now()
print("xxx")
print("Generation Time:", str(finish_gen_time-start_gen_time))
```

## 11. Display output, or record to text file.

Decide on how you want to see your results. The StoryGraph has a function that can print all of the nodes within it.

```py

# Usage on single graph
generated_graph.print_all_node_beautiful_format()

# Usage on list of graphs
for subgraph in generated_graph_list:
    subgraph.print_all_node_beautiful_format()
```

For larger stories that may be difficult to read in the console, we recommend writing to a text file.

```py
base_directory = "application/tests/test_output/"

# Usage on Single Graph
base_folder_name = "single_graph"
single_graph_directory = base_directory + base_folder_name + "/"
generated_graph.print_graph_nodes_to_text_file(directory=single_graph_directory, verbose=True)

# Usage on Multiple Graphs (this will also print the final world state of each subgraph)
graphcounter = 1
base_folder_name = "multi_graph"

for subgraph in generated_graph_list:
    print("Cycle Number:", str(graphcounter))
    fullpath = base_directory + base_folder_name + "/" + str(graphcounter) + "/"
    if not os.path.exists(fullpath):
        os.makedirs(fullpath)

    subgraph.print_graph_nodes_to_text_file(directory=fullpath, verbose=True)
    latest_ws = subgraph.make_latest_state()
    latest_ws.print_wsedges_to_text_file(directory=fullpath, verbose=True)

    graphcounter += 1
```

## IMPORTANT NOTICE
After some post-mortem testing, it has been discovered that the StoryMetrics were not as effective as they should have been. For those who would like to use StoryMetrics in the story's generation, please keep this notice in mind.