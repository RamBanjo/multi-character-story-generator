from JSONReader import *

thing_list = read_list_of_objects_from_json("json/TestObjectList.json", verbose=True)

print()
print("Printing list of objects made with the read list function:")
for item in thing_list:
    print(item)

print()
print("Now, we will attempt to make a world state out of this list")

test_ws = make_world_state_from_extracted_list_of_objects("Test WS", thing_list)

print("We made the World State! Now we will print all the nodes")
test_ws.print_all_nodes()

print()
print("We will now attempt to connect nodes!")
print()
make_connection_from_json("json/TestConnections.json", test_ws, verbose=True)
print()
print("We finished making connections! Printing all edges...")
test_ws.print_all_edges()
print()

test_sg = make_initial_graph_from_world_state("Test SG", test_ws)

print()
print("We finished making the Story Graph, now we will print the things we put in")
print("Location Objects in Story Graph")
for loc in test_sg.location_objects:
    print(loc)

print()
print("Character Objects in Story Graph")
for chara in test_sg.character_objects:
    print(chara)

print()
print("Attempting to create a list of Condition Tests")

test_condlist = read_condition_test_list_from_json("json/TestCondTests.json", test_ws)

for item in test_condlist:
    print(item)

print()
print("Attempting to do a Story Node.")

test_sn = read_story_node_from_json("json/TestStoryNode.json", test_ws)
print("We created a story node, now we're adding Alice to it!")
test_sn.add_actor(test_ws.node_dict["Alice"])
print(test_sn)

print("Can we read a list of Story Nodes? Let's see if we can!")
test_snode_list = read_list_of_story_nodes_from_json("json/RewriteRuleTesting/RRTNodeList.json", test_ws)

snode_dict = make_node_dict(test_snode_list)
print(snode_dict.items())

print("Let's make a rule next")
test_rule = read_rewriterule_from_json("json/RewriteRuleTesting/TestRewriteRule.json", snode_dict)
print(test_rule, type(test_rule))

print("We have a list of changes, can we read it?")

changedata_test = [{"name":"Actor Dies","changetype":"tags","object_node_name_text":"generic_actor","tag":"Alive","value":False,"add_or_remove_text":"add"},{"name":"Remove Alice Wanted for Murder","changetype":"tags","object_node_name_text":"Alice","tag":"Wanted","value":"Murder","add_or_remove_text":"remove"},{"name":"Alice and Bob Become Friends","changetype":"rel","node_a_name":"Alice","node_b_name":"Bob","edge_name":"friends","value":"Profession","add_or_remove_text":"add"},{"name":"Location No Longer Holds Actor","changetype":"rel","node_a_name":"generic_location","node_b_name":"generic_actor","edge_name":"holds","value":"Profession","add_or_remove_text":"add"}]

changelist = read_list_of_changes_from_extracted_list(data=changedata_test, world_state=test_ws)

for thing in changelist:
    print(thing.name)