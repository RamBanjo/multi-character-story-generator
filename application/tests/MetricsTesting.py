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
daniel = CharacterNode(name="Daniel", internal_id=3)

somewhere = LocationNode(name="Somewhere", internal_id=3)

test_ws = WorldState(name="Test WS", objectnodes=[alice, bob, charlie, somewhere])
test_ws.connect(from_node=somewhere, edge_name="holds", to_node=alice)
test_ws.connect(from_node=somewhere, edge_name="holds", to_node=bob)
test_ws.connect(from_node=somewhere, edge_name="holds", to_node=charlie)

test_ws2 = WorldState(name="I made you specifically to test Jointability", objectnodes=[alice, bob, charlie, daniel, somewhere])
test_ws2.connect(from_node=somewhere, edge_name="holds", to_node=alice)
test_ws2.connect(from_node=somewhere, edge_name="holds", to_node=bob)
test_ws2.connect(from_node=somewhere, edge_name="holds", to_node=charlie)
test_ws2.connect(from_node=somewhere, edge_name="holds", to_node=daniel)

action_a = StoryNode(name="Action A")
costly_action_b = StoryNode(name="Action B", tags={"Type":"Placeholder","costly":True})
important_action_c = StoryNode(name="Action C", tags={"Type":"Placeholder","important_action":True})
action_d = StoryNode(name="Action D")
action_e = StoryNode(name="Action E")
action_f = StoryNode(name="Action F")
joint_node_g = StoryNode(name="Joint Node G", charcount=1, target_count=1)

test_sg_cost = StoryGraph(name="Test Costly SG", character_objects=[alice, bob, charlie], starting_ws=test_ws)
test_sg_unique = StoryGraph(name="Test Unique SG", character_objects=[alice, bob,charlie], starting_ws=test_ws)
test_sg_jointy = StoryGraph(name="Test Jointy SG", character_objects=[alice, bob, charlie, daniel], starting_ws=test_ws2)
test_sg_prefer = StoryGraph(name="Test Prefer SG", character_objects=[alice, bob, charlie], starting_ws=test_ws)

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

# Alice currently has 20 score because 1/5 nodes are costly nodes
# Appending 1 non-cost makes it 1/6, changing the score to 16.667...
# Appending 1 cost node makes it 2/6, changing the score to 33.333...

# Keep Lower:
# - Returns false if adding a node would increase metrics while the metric value is higher than the Metric Goal
alice_cost_lower_10 = StoryMetric(metric_type=MetricType.COST, value=10, metric_mode=MetricMode.LOWER, character_object=alice)

test_result = test_sg_cost.test_if_given_node_list_will_follow_metric_rule(metric=alice_cost_lower_10, node_list=[costly_action_b], step=5)
print("Alice has Lower than 10 Cost Metric, Attempting to append a Costly node should return False: ", test_result)

# - Returns true no matter what if the value is already lower, or if the value decreases while value is higher.
alice_cost_lower_40 = StoryMetric(metric_type=MetricType.COST, value=40, metric_mode=MetricMode.LOWER, character_object=alice)

test_result = test_sg_cost.test_if_given_node_list_will_follow_metric_rule(metric=alice_cost_lower_10, node_list=[action_a], step=5)
print("Alice has Lower than 10 Cost Metric, Attempting to append a non-Costly node should return True: ", test_result)

test_result = test_sg_cost.test_if_given_node_list_will_follow_metric_rule(metric=alice_cost_lower_40, node_list=[costly_action_b], step=5)
print("Alice has Lower than 40 Cost Metric, Attempting to append a Costly node should return True: ", test_result)

test_result = test_sg_cost.test_if_given_node_list_will_follow_metric_rule(metric=alice_cost_lower_40, node_list=[action_a], step=5)
print("Alice has Lower than 40 Cost Metric, Attempting to append a non-Costly node should return True: ", test_result)

# Keep Higher:
# - Returns false if adding a node would decrease metrics while the metric value is lower than the Metric Goal
alice_cost_higher_30 = StoryMetric(metric_type=MetricType.COST, value=30, metric_mode=MetricMode.HIGHER, character_object=alice)

test_result = test_sg_cost.test_if_given_node_list_will_follow_metric_rule(metric=alice_cost_higher_30, node_list=[action_a], step=5)
print("Alice has Higher than 30 Cost Metric, Attempting to append a non-Costly node should return False: ", test_result)

# - Returns true no matter what if the value is already higher, or if the value increases while value is lower.
alice_cost_higher_10 = StoryMetric(metric_type=MetricType.COST, value=10, metric_mode=MetricMode.HIGHER, character_object=alice)

test_result = test_sg_cost.test_if_given_node_list_will_follow_metric_rule(metric=alice_cost_higher_30, node_list=[costly_action_b], step=5)
print("Alice has Higher than 30 Cost Metric, Attempting to append a Costly node should return True: ", test_result)

test_result = test_sg_cost.test_if_given_node_list_will_follow_metric_rule(metric=alice_cost_higher_10, node_list=[action_a], step=5)
print("Alice has Higher than 10 Cost Metric, Attempting to append a non-Costly node should return True: ", test_result)

test_result = test_sg_cost.test_if_given_node_list_will_follow_metric_rule(metric=alice_cost_higher_10, node_list=[costly_action_b], step=5)
print("Alice has Higher than 10 Cost Metric, Attempting to append a Costly node should return True: ", test_result)

# Keep Stable:
# - Returns false if adding a node would increase metrics while the metric value is too much higher than the Metric Goal
# - Returns false if adding a node would decrease metrics while the metric value is too much lower than the Metric Goal
# - "Too Much" is currently defined as being more than 5 points away from the given goal value in the test_if_given_node_list_will_follow_metric_rule function.

alice_cost_stable_10 = StoryMetric(metric_type=MetricType.COST, value=10, metric_mode=MetricMode.STABLE, character_object=alice)
alice_cost_stable_70 = StoryMetric(metric_type=MetricType.COST, value=70, metric_mode=MetricMode.STABLE, character_object=alice)
alice_cost_stable_20 = StoryMetric(metric_type=MetricType.COST, value=20, metric_mode=MetricMode.STABLE, character_object=alice)

print()
test_result = test_sg_cost.test_if_given_node_list_will_follow_metric_rule(metric=alice_cost_stable_10, node_list=[action_a], step=5)
print("Alice has Stable 10 Cost Metric, Attempting to append a non-Costly node should return True: ", test_result)

test_result = test_sg_cost.test_if_given_node_list_will_follow_metric_rule(metric=alice_cost_stable_10, node_list=[costly_action_b], step=5)
print("Alice has Stable 10 Cost Metric, Attempting to append a Costly node should return False: ", test_result)

test_result = test_sg_cost.test_if_given_node_list_will_follow_metric_rule(metric=alice_cost_stable_70, node_list=[action_a], step=5)
print("Alice has Stable 70 Cost Metric, Attempting to append a non-Costly node should return False: ", test_result)

test_result = test_sg_cost.test_if_given_node_list_will_follow_metric_rule(metric=alice_cost_stable_70, node_list=[costly_action_b], step=5)
print("Alice has Stable 70 Cost Metric, Attempting to append a Costly node should return True: ", test_result)

#This one returns true because even after decreasing the value, 16.67... is still within plus/minus of 20 so It Works.
test_result = test_sg_cost.test_if_given_node_list_will_follow_metric_rule(metric=alice_cost_stable_20, node_list=[action_a], step=5)
print("Alice has Stable 20 Cost Metric, Attempting to append a non-Costly node should return True: ", test_result)

#However, 33.33... is not within plus/minus of 20 and will return False.
test_result = test_sg_cost.test_if_given_node_list_will_follow_metric_rule(metric=alice_cost_stable_20, node_list=[costly_action_b], step=5)
print("Alice has Stable 20 Cost Metric, Attempting to append a Costly node should return False: ", test_result)

#Okay, so we figured out that test_if_given_node_list_will_follow_metric_rule works as intended. Therefore, now we only need to test if these other metrics can be properly measured.
#If they can be properly measured, then the score calculations should also be right.

test_sg_unique.insert_multiple_parts(part_list=[action_a, costly_action_b, important_action_c, action_d, action_e], character=alice, location_list=[somewhere, somewhere, somewhere, somewhere, somewhere])
test_sg_unique.insert_multiple_parts(part_list=[action_a, action_a, action_a, action_a, action_a], character=bob, location_list=[somewhere, somewhere, somewhere, somewhere, somewhere])
test_sg_unique.insert_multiple_parts(part_list=[action_a, costly_action_b, costly_action_b, action_a, action_a], character=charlie, location_list=[somewhere, somewhere, somewhere, somewhere, somewhere])

# Testing Measuring Uniqueness
# Scenario 1: Test Uniqueness of a Story: See if it can count unique nodes properly
# Scenario 2: Test Uniqueness Score Calculation: See if it can get the score of Uniqueness properly

alice_unique_metric = test_sg_unique.get_metric_score(metric_type=MetricType.UNIQUE, character=alice)
bob_unique_metric = test_sg_unique.get_metric_score(metric_type=MetricType.UNIQUE, character=bob)
charlie_unique_metric = test_sg_unique.get_metric_score(metric_type=MetricType.UNIQUE, character=charlie)

print()
#All of Alice's nodes are Unique, it should be 100
print("Alice Unique Metric (Expected 100):", alice_unique_metric)

#Bob only has 1 Unique out of 5, it should be 20
print("Bob Unique Metric (Expected 20):", bob_unique_metric)

#Charlie has 2 uniques out of 5, it should be 40
print("Charlie Unique Metric (Expected 40):", charlie_unique_metric)

# Scenario 3: Test Uniqueness Metric Rule Follow (True and False)

# Testing Jointability
# Scenario 1: Test Jointability of a Story: See if it can count Joint Nodes properly
# Scenario 2: Test Jointability Score Calculation: See if it can get the score of Jointability properly

# There are 5 actions.
# Alice joints with Bob and Charlie all the time, so she will be at 100.
# Bob joints with Alice 2 times. His score should be 40.
# Charlie joints with Alice 3 times. His score should be 60.
# Daniel never joints with anyone so his score should be 0.

test_sg_jointy.insert_joint_node(joint_node=joint_node_g, main_actor=alice, other_actors=[bob], location=somewhere)
test_sg_jointy.insert_joint_node(joint_node=joint_node_g, main_actor=bob, other_actors=[alice], location=somewhere, absolute_step=1)
test_sg_jointy.insert_multiple_parts(part_list=[action_a, action_a, action_a], character=bob, location_list=[somewhere, somewhere, somewhere], absolute_step=2)

test_sg_jointy.insert_multiple_parts(part_list=[action_a, action_a], character=charlie, location_list=[somewhere, somewhere, somewhere, somewhere, somewhere])
test_sg_jointy.insert_joint_node(joint_node=joint_node_g, main_actor=alice, other_actors=[charlie], location=somewhere, absolute_step=2)
test_sg_jointy.insert_joint_node(joint_node=joint_node_g, main_actor=charlie, other_actors=[alice], location=somewhere, absolute_step=3)
test_sg_jointy.insert_joint_node(joint_node=joint_node_g, main_actor=alice, other_actors=[charlie], location=somewhere, absolute_step=4)

test_sg_jointy.insert_multiple_parts(part_list=[action_a, costly_action_b, costly_action_b, action_a, action_a], character=daniel, location_list=[somewhere, somewhere, somewhere, somewhere, somewhere])

alice_joint_metric = test_sg_jointy.get_metric_score(metric_type=MetricType.JOINTS, character=alice)
bob_joint_metric = test_sg_jointy.get_metric_score(metric_type=MetricType.JOINTS, character=bob)
charlie_joint_metric = test_sg_jointy.get_metric_score(metric_type=MetricType.JOINTS, character=charlie)
daniel_joint_metric = test_sg_jointy.get_metric_score(metric_type=MetricType.JOINTS, character=daniel)

print()
print("Alice Jointable Metric (Expected 100):", alice_joint_metric)
print("Bob Jointable Metric (Expected 40):", bob_joint_metric)
print("Charlie Jointable Metric (Expected 60):", charlie_joint_metric)
print("Daniel Jointable Metric (Expected 0):", daniel_joint_metric)

#We're going to get Bob tested!

# Scenario 3: Test Jointability Metric Rule Follow (True and False)

# Testing Maincharacterness
# Scenario 1: Test Preference of a Story: See if it can count Important Nodes properly
# Scenario 2: Test Preference Score Calculation: See if it can get the score of Preference properly
# Scenario 3: Test Preference Metric Rule Follow (True and False)

test_sg_prefer.insert_multiple_parts(part_list=[action_a, action_a, important_action_c, action_a, important_action_c], character=alice, location_list=[somewhere, somewhere, somewhere, somewhere, somewhere])
test_sg_prefer.insert_multiple_parts(part_list=[action_a, action_a, action_a, action_a, action_a], character=bob, location_list=[somewhere, somewhere, somewhere, somewhere, somewhere])
test_sg_prefer.insert_multiple_parts(part_list=[important_action_c, important_action_c, important_action_c, important_action_c, important_action_c], character=charlie, location_list=[somewhere, somewhere, somewhere, somewhere, somewhere])

alice_prefer_metric = test_sg_prefer.get_metric_score(metric_type=MetricType.PREFER, character=alice)
bob_prefer_metric = test_sg_prefer.get_metric_score(metric_type=MetricType.PREFER, character=bob)
charlie_prefer_metric = test_sg_prefer.get_metric_score(metric_type=MetricType.PREFER, character=charlie)

print()
print("Alice Preference Metric (Expected 40):", alice_prefer_metric)
print("Bob Preference Metric (Expected 0):", bob_prefer_metric)
print("Charlie Preference Metric (Expected 100):", charlie_prefer_metric)

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

# Now that every metric has been tested, we need to test one more aspect of the metrics: multigraph metrics! (muahahaha)

test_ws_only_alice = WorldState(name="Just Alice. (OK)", objectnodes=[alice, somewhere])

multigraph_cost_part_a = StoryGraph(name="Multigraph Cost A", character_objects=[alice], starting_ws=test_ws_only_alice)
multigraph_cost_part_b = StoryGraph(name="Multigraph Cost B", character_objects=[alice], starting_ws=test_ws_only_alice)
multigraph_cost_part_c = StoryGraph(name="Multigraph Cost C", character_objects=[alice], starting_ws=test_ws_only_alice)

multigraph_cost_part_a.insert_multiple_parts(part_list=[action_a, action_a, action_a, action_a, action_a], character=alice, location_list=[somewhere, somewhere, somewhere, somewhere, somewhere])
multigraph_cost_part_b.insert_multiple_parts(part_list=[action_a, action_a, action_a, action_a, action_a], character=alice, location_list=[somewhere, somewhere, somewhere, somewhere, somewhere])
multigraph_cost_part_c.insert_multiple_parts(part_list=[costly_action_b, costly_action_b, costly_action_b, costly_action_b, costly_action_b], character=alice, location_list=[somewhere, somewhere, somewhere, somewhere, somewhere])

# Graph A cost is 20
# Graph B cost is 40
# Graph C cost is 60

print()
# print("Score if Retention is 1:", multigraph_cost_part_c.get_multigraph_metric_score(metric_type=MetricType.UNIQUE, character=alice, previous_graphs=[multigraph_cost_part_a, multigraph_cost_part_b], score_retention=1)) #shouldn't this be 2/15?
# print("Score if Retention is 0.5:", multigraph_cost_part_c.get_multigraph_metric_score(metric_type=MetricType.UNIQUE, character=alice, previous_graphs=[multigraph_cost_part_a, multigraph_cost_part_b], score_retention=0.5))

# list_of_graphs = [multigraph_cost_part_a, multigraph_cost_part_b, multigraph_cost_part_c]

multigraph_cost_part_c.print_metric_of_each_character_to_text_file(directory="application/tests/test_output/", previous_graphs=[multigraph_cost_part_a, multigraph_cost_part_b], verbose=True, retention=1, include_true_uniqueness=True)

# test_list = [1,2,3,4,5]
# print(test_list[:1])