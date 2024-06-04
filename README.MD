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

```py
some_action = StoryNode(name = "Do Something")
```
