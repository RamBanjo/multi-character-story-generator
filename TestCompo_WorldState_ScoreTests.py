from components.ConditionTest import HasTagTest, InBiasRangeTest
from components.StoryGraphTwoWS import StoryGraph
from components.StoryNode import StoryNode
from components.StoryObjects import CharacterNode, LocationNode
from components.UtilityEnums import GenericObjectNode
from components.WorldState import WorldState


alice = CharacterNode("Alice", biases={"lawbias":50, "moralbias":50}, tags={"Job":"Swordmaster", "Wealth":"Average"})
bob = CharacterNode("Bob", biases={"lawbias":-50, "moralbias":-50}, tags={"Job":"Swordmaster", "Wealth":"Wealthy"})
charlie = CharacterNode("Charlie", biases={"lawbias":50, "moralbias":50}, tags={"Job":"Wizard", "Wealth":"Wealthy"})
daniel = CharacterNode("Daniel", biases={"lawbias":-50, "moralbias":-50}, tags={"Job":"Rouge","Wealth":"Poor"})

#So in order to perform the following node... We favor Swordmasters with a positive law bias

test_pos_law = InBiasRangeTest(object_to_test=alice, bias_axis="lawbias", min_accept=1, max_accept=100, score=1)
test_job_swordmaster = HasTagTest(object_to_test=alice, tag="Job", value="Swordmaster", score=2)

test_ws = WorldState("Test WS", objectnodes=[alice, bob, charlie, daniel])

#Alice expects 3 (Pass both)
#Bob expects 2 (Only pass Job)
#Charlie expects 1 (Only pass pos law)
#Daniel expects 0 (Pass none)

print("Alice Score Test (Expect 3)", test_ws.get_score_from_list_of_test([test_pos_law, test_job_swordmaster]))

test_pos_law.object_to_test = bob
test_job_swordmaster.object_to_test = bob

print("Bob Score Test (Expect 2)", test_ws.get_score_from_list_of_test([test_pos_law, test_job_swordmaster]))

test_pos_law.object_to_test = charlie
test_job_swordmaster.object_to_test = charlie

print("Charlie Score Test (Expect 1)", test_ws.get_score_from_list_of_test([test_pos_law, test_job_swordmaster]))

test_pos_law.object_to_test = daniel
test_job_swordmaster.object_to_test = daniel

print("Daniel Score Test (Expect 0)", test_ws.get_score_from_list_of_test([test_pos_law, test_job_swordmaster]))

test_pos_law.object_to_test = GenericObjectNode.GENERIC_ACTOR
test_job_swordmaster.object_to_test = GenericObjectNode.GENERIC_ACTOR

go_on_patrol = StoryNode(name="Go on Patrol for Criminals", biasweight=1, tags={"Type":"Look_For_Trouble"}, charcount=1, suggested_test_list=[test_pos_law, test_job_swordmaster])
go_on_patrol.actor = [alice]
print("Alice Score Test with Node (Expect 3)", test_ws.get_score_from_story_node(go_on_patrol))

go_on_patrol.actor = [bob]
print("Bob Score Test with Node (Expect 2)", test_ws.get_score_from_story_node(go_on_patrol))

go_on_patrol.actor = [charlie]
print("Charlie Score Test with Node (Expect 1)", test_ws.get_score_from_story_node(go_on_patrol))

go_on_patrol.actor = [daniel]
print("Daniel Score Test with Node (Expect 0)", test_ws.get_score_from_story_node(go_on_patrol))

#Next, we want to test calculate_score_from_char_and_cont here.
#First we want to add ABCD to Alice's storyline.
#Then, we want to add XYZ to Alice's storyline at the point after B, but we want to calculate the score first
#Finally, we want to test if the program can detect a bad node by including an invalid node in the sequence

node_a = StoryNode(name = "Node A", biasweight=1, tags={"Type":"Placeholder"}, charcount=1, required_test_list=[], suggested_test_list=[])
node_b = StoryNode(name = "Node B", biasweight=1, tags={"Type":"Placeholder"}, charcount=1, required_test_list=[], suggested_test_list=[])
node_c = StoryNode(name = "Node C", biasweight=1, tags={"Type":"Placeholder"}, charcount=1, required_test_list=[], suggested_test_list=[])
node_d = StoryNode(name = "Node D", biasweight=1, tags={"Type":"Placeholder"}, charcount=1, required_test_list=[], suggested_test_list=[])

#XYZ should return a value of 3.
#X gives a value of 1 from the node itself, and 2 from the Swordmaster Test
#Y gives a value of 2 from the node itself, and 1 from the Positive Lawbias Test
#Z gives a value of 3 from itself.
#The max and average of any of these nodes are 3.

node_x = StoryNode(name = "Node X", biasweight=1, tags={"Type":"Placeholder"}, charcount=1, required_test_list=[], suggested_test_list=[test_job_swordmaster])
node_y = StoryNode(name = "Node Y", biasweight=2, tags={"Type":"Placeholder"}, charcount=1, required_test_list=[], suggested_test_list=[test_pos_law])
node_z = StoryNode(name = "Node Z", biasweight=3, tags={"Type":"Placeholder"}, charcount=1, required_test_list=[], suggested_test_list=[])

test_job_druid = HasTagTest(object_to_test=alice, tag="Job", value="Druid", score=2)

node_invalid = StoryNode(name = "Invalid Node", biasweight=1, tags={"Type":"Placeholder"}, charcount=1, required_test_list=[test_job_druid], suggested_test_list=[])

good_sequence = [node_x, node_y, node_z]
bad_sequence = [node_x, node_invalid, node_z]

town = LocationNode(name="Town")
test_ws.add_node(town)
test_ws.connect(from_node=town, edge_name="holds", to_node=alice)
test_ws.connect(from_node=town, edge_name="holds", to_node=bob)
test_ws.connect(from_node=town, edge_name="holds", to_node=charlie)
test_ws.connect(from_node=town, edge_name="holds", to_node=daniel)

test_sg = StoryGraph(name="Test SG", character_objects=[alice, bob, charlie, daniel], location_objects=[town], starting_ws=test_ws)
test_sg.insert_multiple_parts(part_list=[node_a, node_b, node_c, node_d], character=alice)
test_sg.fill_in_locations_on_self()

print("Score from Alice Story (expect 3)", test_sg.calculate_score_from_char_and_cont(actor=alice, insert_index=2, contlist=good_sequence))
print("Score from Alice Story with Bad Node (expect -999)", test_sg.calculate_score_from_char_and_cont(actor=alice, insert_index=2, contlist=bad_sequence))