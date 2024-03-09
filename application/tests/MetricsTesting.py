import sys

sys.path.insert(0,'')

from application.components.StoryMetrics import *
from application.components.StoryObjects import *
from application.components.WorldState import *
from application.components.StoryGraphTwoWS import *
from application.components.StoryNode import *
from application.components.StoryMetrics import *

alice = CharacterNode(name="Alice", biases={"lawbias":50, "moralbias":50}, internal_id=0)
bob = CharacterNode(name="Bob", biases={"lawbias":0, "moralbias":-50}, internal_id=1)
charlie = CharacterNode(name="Charlie", internal_id=2)

somewhere = LocationNode(name="Somewhere", internal_id=3)

test_ws = WorldState(name="Test WS", objectnodes=[alice, bob, charlie, somewhere])
test_ws.connect(from_node=somewhere, edge_name="holds", to_node=alice)
test_ws.connect(from_node=somewhere, edge_name="holds", to_node=bob)
test_ws.connect(from_node=somewhere, edge_name="holds", to_node=charlie)

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

#Here is how we will want to test our Metrics Functions:

# Testing measuring Costly Nodes

test_sg_cost.insert_multiple_parts(part_list=[action_a, costly_action_b, important_action_c, action_e, action_d], character=alice, location_list=[somewhere, somewhere, somewhere, somewhere, somewhere])
test_sg_cost.insert_multiple_parts(part_list=[action_a, important_action_c, action_e, action_a, action_d], character=bob, location_list=[somewhere, somewhere, somewhere, somewhere, somewhere])
test_sg_cost.insert_multiple_parts(part_list=[costly_action_b, costly_action_b, costly_action_b, costly_action_b, costly_action_b], character=charlie, location_list=[somewhere, somewhere, somewhere, somewhere, somewhere])

#Alice's storyline has 2 costly actions and is 5 nodes long. The score should be 40.
#Bob's storyline has no costly actions and is 5 nodes long. The score should be 0.
#Charlie's storyline has only costly actions. The score should be 100.

# Scenario 1: Test Cost of a Story: See if it can count Costly Nodes properly
# Scenario 2: Test Cost Score Calculation: See if it can get the score of Cost properly

alice_cost_metric = test_sg_cost.get_metric_score(metric_type=MetricType.COST, character=alice)
bob_cost_metric = test_sg_cost.get_metric_score(metric_type=MetricType.COST, character=bob)
charlie_cost_metric = test_sg_cost.get_metric_score(metric_type=MetricType.COST, character=charlie)

print("Alice Cost Metric (Expected 20):", alice_cost_metric)
print("Bob Cost Metric (Expected 0):", bob_cost_metric)
print("Charlie Cost Metric (Expected 100):", charlie_cost_metric)

# Scenario 3: Test Cost Metric Rule Follow (True and False)

# Keep Lower:
# - Returns false if adding a node would increase metrics while the metric value is higher than the Metric Goal

# Keep Higher:
# - Returns false if adding a node would decrease metrics while the metric value is lower than the Metric Goal

# Keep Stable:
# - Returns false if adding a node would increase metrics while the metric value is too much higher than the Metric Goal
# - Returns false if adding a node would decrease metrics while the metric value is too much lower than the Metric Goal

# Testing Measuring Uniqueness
# Scenario 1: Test Uniqueness of a Story: See if it can count unique nodes properly
# Scenario 2: Test Uniqueness Score Calculation: See if it can get the score of Uniqueness properly
# Scenario 3: Test Uniqueness Metric Rule Follow (True and False)

# Testing Jointability
# Scenario 1: Test Jointability of a Story: See if it can count Joint Nodes properly
# Scenario 2: Test Jointability Score Calculation: See if it can get the score of Jointability properly
# Scenario 3: Test Jointability Metric Rule Follow (True and False)

# Testing Maincharacterness
# Scenario 1: Test Preference of a Story: See if it can count Important Nodes properly
# Scenario 2: Test Preference Score Calculation: See if it can get the score of Preference properly
# Scenario 3: Test Preference Metric Rule Follow (True and False)

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