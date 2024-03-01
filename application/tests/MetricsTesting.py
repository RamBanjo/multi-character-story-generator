import sys

sys.path.insert(0,'')

from components.StoryMetrics import *
from components.StoryObjects import *
from components.WorldState import *
from components.StoryGraphTwoWS import *

alice = CharacterNode(name="Alice", biases={"lawbias":50, "moralbias":50})
bob = CharacterNode(name="Bob", biases={"lawbias":0, "moralbias":-50})
charlie = CharacterNode(name="Charlie")

somewhere = LocationNode(name="Somewhere")

test_ws = WorldState(name="Test WS", objectnodes=[alice, bob, somewhere])
test_ws.connect(from_node=somewhere, edge_name="holds", to_node=alice)
test_ws.connect(from_node=somewhere, edge_name="holds", to_node=bob)

action_a = StoryNode(name="Action A")
costly_action_b = StoryNode(name="Action B", tags={"Type":"Placeholder","costly":True})
important_action_c = StoryNode(name="Action C", tags={"Type":"Placeholder","important_actiion":True})
action_d = StoryNode(name="Action D")
action_e = StoryNode(name="Action E")
action_f = StoryNode(name="Action F")

test_sg_cost = StoryGraph(name="Test Costly SG", character_objects=[alice, bob], starting_ws=test_ws)
test_sg_unique = StoryGraph(name="Test Unique SG", character_objects=[alice, bob], starting_ws=test_ws)
test_sg_jointy = StoryGraph(name="Test Jointy SG", character_objects=[alice, bob], starting_ws=test_ws)
test_sg_prefer = StoryGraph(name="Test Prefer SG", character_objects=[alice, bob], starting_ws=test_ws)

#Alice's storyline has 2 costly actions and is 5 nodes long. The score should be 20.
test_sg_cost.insert_multiple_parts(part_list=[costly_action_b, costly_action_b, action_a, important_action_c, action_d], character=alice, location_list=[somewhere, somewhere, somewhere, somewhere, somewhere])

#Bob's storyline has no costly actions and is 5 nodes long. The score should be 0.

#Charlie's storyline has only costly actions. The score should be 100.

#Here is how we will want to test our Metrics Functions:

# Testing measuring costs
# Scenario 1: Test Cost of a Story: See if it can count Costly Nodes properly
# Scenario 2: Test Uniqueness of a Story: See if it can count unique nodes properly
# Scenario 3: Test Jointability of a Story: See if it can count Joint Nodes properly
# Scenario 4: Test Preference of a Story: See if it can count Important Nodes properly

# Testing score calculations
# Scenario 1: Test Cost Score Calculation: See if it can get the score of Cost properly
# Scenario 2: Test Uniqueness Score Calculation: See if it can get the score of Uniqueness properly
# Scenario 3: Test Jointability Score Calculation: See if it can get the score of Jointability properly
# Scenario 4: Test Preference Score Calculation: See if it can get the score of Preference properly

# Testing "Follows Metric Rules" functions
# Scenario 1: Test Cost Metric Rule Follow (True and False)
# Scenario 2: Test Uniqueness Metric Rule Follow (True and False)
# Scenario 3: Test Jointability Metric Rule Follow (True and False)
# Scenario 4: Test Preference Metric Rule Follow (True and False)

#TODO: Literal shower thoughts, but these metrics can only read and calculate what's in the current graph. We will need to make a solution for when there are multiple graphs at play...
# - Input previous metrics?
# Pros: Most accurate metrics
# Cons: Will need an additional function to read metrics from multiple graphs, also I probably need to finish writing the multi graph function

# - Ignore previous graph's metrics?
# Pros: No further action will be needed, just need to connect graphs normally
# Cons: Metrics get more inaccurate over time

# - Only calculate current graph and previous graph's metrics? (The older graphs should not count it's way in the past)
# Pros: 
# Cons: It requires new code --- I might as well as do the first option if we're doing this option

# - Weighted metrics that favors the present: The closer the graph is to the present the more it will affect the present
# Pros: This would mean that metric
# Cons: Requires user to input how much characters care about the present than the previous graph (some decay value multiplied?)

# Yep we're going with the prof's suggestion with the weighted metrics. Gotta figure out how to do the decay functions...

# Yeah it looks like the best choice is the first option