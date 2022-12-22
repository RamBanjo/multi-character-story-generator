from components.RelChange import *
from components.StoryGraphTwoWS import StoryGraph
from components.StoryObjects import *
from components.ConditionTest import *
from components.StoryNode import *
from components.UtilityEnums import *

import json

from components.WorldState import WorldState

def read_from_json(json_file_name):
    f = open(json_file_name)
    data = json.load(f)
    f.close()

    return data

def read_character_node_from_extracted_dict(data):
    return CharacterNode(name = data["name"], biases = data["biases"], tags = data["tags"])

def read_object_node_from_extracted_dict(data):
    return ObjectNode(name = data["name"], tags = data["tags"])

def read_location_node_from_extracted_dict(data):
    return LocationNode(name = data["name"], tags = data["tags"])

def read_list_of_objects_from_json(json_file_name, verbose = False):
    data = read_from_json(json_file_name)

    obj_list_returns = []

    for sub_data in data:
        detected_type = sub_data.get("type", "[Cannot Find Object Type]")
        match detected_type:
            case "story_object":
                if verbose:
                    print("Adding Story Object:", sub_data["name"])
                obj_list_returns.append(read_object_node_from_extracted_dict(sub_data))
            case "character_object":
                if verbose:
                    print("Adding Character Object:", sub_data["name"])                
                obj_list_returns.append(read_character_node_from_extracted_dict(sub_data))
            case "location_object":
                if verbose:
                    print("Adding Location Object:", sub_data["name"])                
                obj_list_returns.append(read_location_node_from_extracted_dict(sub_data))
            case _:
                if verbose:
                    print("Invalid object type, nothing added. Detected type:", detected_type)

    if verbose:
        print("Object list is complete! List size:", str(len(obj_list_returns)))
    return obj_list_returns

#Switch Case?
#There are so many types of Condition Tests so it might be better to break this into multiple functions

def read_condition_test_from_json(json_file_name, world_state):
    data = read_from_json(json_file_name)
    return read_condition_test_from_extracted_dict(data, world_state)


def read_condition_test_from_extracted_dict(data, world_state):
    match data["test_type"]:
        case "held_item_tag_test":
            return read_held_item_test_from_extracted_dict(data, world_state)
        case "has_edge_test":
            return read_has_edge_test_from_extracted_dict(data, world_state)
        case "has_double_edge_test":
            return read_has_double_edge_test_from_extracted_dict(data, world_state)
        case "same_location_test": 
            read_same_location_test_from_extracted_dict(data, world_state)
        case _:
            return     

def read_condition_test_list_from_json(json_file_name, world_state):
    data = read_from_json(json_file_name)

    test_list = []
    for test in data:
        test_to_append = read_condition_test_from_extracted_dict(test, world_state)
        if test_to_append is not None:
            test_list.append(test)

    return data

def read_held_item_test_from_extracted_dict(data, world_state):

    designated_holder = world_state.node_dict.get(data.get("holder", None), None)
    designated_tag = world_state.node_dict.get(data.get("tag_to_test", None), None)
    designated_value = world_state.node_dict.get(data.get("value_to_test", None), None)
    designated_inverse = data.get("inverse", False)

    if designated_holder is None or designated_tag is None:
        return None

    return HeldItemTagTest(holder_to_test=designated_holder, tag_to_test=designated_tag, value_to_test=designated_value, inverse=designated_inverse)

def read_has_edge_test_from_extracted_dict(data, world_state):

    designated_from_node = world_state.node_dict.get(data.get("from", None), None)
    designated_to_node = world_state.node_dict.get(data.get("to", None), None)
    designated_edge_name = data.get("edge_name", None)
    designated_value = data.get("value", None)
    desginated_soft_equal = data.get("soft_equal", False)
    designated_inverse = data.get("inverse", False)

    if designated_from_node is None or designated_to_node is None:
        return None

    return HasEdgeTest(object_from_test=designated_from_node, object_to_test=designated_to_node, edge_name_test=designated_edge_name, value_test=designated_value,soft_equal=desginated_soft_equal, inverse=designated_inverse)

def read_has_double_edge_test_from_extracted_dict(data, world_state):

    designated_from_node = world_state.node_dict.get(data.get("from", None), None)
    designated_to_node = world_state.node_dict.get(data.get("to", None), None)
    designated_edge_name = data.get("edge_name", None)
    designated_value = data.get("value", None)
    desginated_soft_equal = data.get("soft_equal", False)
    designated_inverse = data.get("inverse", False)

    if designated_from_node is None or designated_to_node is None:
        return None
    
    return HasDoubleEdgeTest(object_from_test=designated_from_node, object_to_test=designated_to_node, edge_name_test=designated_edge_name, value_test=designated_value,soft_equal=desginated_soft_equal, inverse=designated_inverse)

def read_same_location_test_from_extracted_dict(data, world_state):

    list_to_test = []

    for char_name in data["char_name_list"]:

        if world_state.node_dict.get(char_name, None) is not None:
            list_to_test.append(world_state.node_dict[char_name])

    return SameLocationTest(list_to_test=list_to_test, inverse=data["inverse"])

#Story Node will require some conversions from the test functions above
def read_story_node_from_json(json_file_name, world_state):
    data = read_from_json(json_file_name)

    test_list = read_list_of_tests_from_json(data["condition_test_list"], world_state)

    return StoryNode(name = data["name"], biasweight=data["biasweight"], tags=data["tags"], charcount=data["charcount"], required_tags_list=data["required_tags"], unwanted_tags_list=data["unwanted_tags"], bias_range = data["bias_range"], required_tags_list_target=data["required_tags"], unwanted_tags_list_target=data["unwanted_tags"], bias_range_target=data["bias_range"],condition_tests=test_list)

def read_list_of_tests_from_json(json_file_name, world_state):

    data = read_from_json(json_file_name)

    test_list_returns = []

    for test in data:
        test_list_returns.append(read_condition_test_from_extracted_dict(test, world_state))

    return test_list_returns

def read_list_of_changes_from_extracted_list(data, world_state):

    change_list_returns = []

    for change in data:
        change_list_returns.append(make_change_object_from_extracted_list(change, world_state))

    return change_list_returns

def make_change_object_from_extracted_list(data, world_state):

    if data["changetype"] == "tags":
        return make_tag_change_object_from_extracted_list(data, world_state)
    elif data["changetype"] == "rel":
        return make_rel_change_object_from_extracted_list(data, world_state)

    return


def text_to_changeaction(text):
    
    add_or_remove = "invalid"

    if text == "add":
        add_or_remove = ChangeAction.ADD
    elif text == "remove":
        add_or_remove = ChangeAction.REMOVE

    return add_or_remove


def make_tag_change_object_from_extracted_list(data, world_state):

    add_or_remove = text_to_changeaction(data["add_or_remove"])

    if add_or_remove == "invalid":
        return

    return TagChange(name = data["name"], object_node_name = world_state.node_dict[data["node_name"]], tag=data["tag"], add_or_remove=add_or_remove)

def make_rel_change_object_from_extracted_list(data, world_state):

    add_or_remove = text_to_changeaction(data["add_or_remove"])

    if add_or_remove == "invalid":
        return
    
    return RelChange(name = data["name"], node_a=world_state.node_dict[data["node_a"]], edge_name=data["edge_name"], node_b = world_state.node_dict[data["node_b"]], value=data["value"], add_or_remove=add_or_remove)

def make_connection_from_json(json_file_name, world_state, verbose = False):

    data = read_from_json(json_file_name)
    connections_made = 0
    for connection in data:


        #First, we must check if both the from node and the two node are nodes that exist within the world state. Only make a connection if they exist.

        designated_from_node = world_state.node_dict.get(connection.get("from_node", None), None)
        designated_to_node = world_state.node_dict.get(connection.get("to_node", None), None)
        designated_value = connection.get("value", None)
        designated_edge_name = connection.get("edge_name", None)
       

        if designated_from_node is not None and designated_to_node is not None and designated_edge_name is not None:
            if verbose:
                print("Connecting from", str(designated_from_node), "to", str(designated_to_node), "with edge", designated_edge_name, "(Value:", designated_value,")")
            world_state.connect(from_node = designated_from_node, edge_name = designated_edge_name, to_node = designated_to_node, value = designated_value)
            connections_made += 1
        elif verbose:
            print("Skipping incompatible input...")

    if verbose:
        print("Finished making connections in world state! Connections made:", str(connections_made))

    
            

def make_world_state_from_json(json_file_name, object_dict: dict):

    data = read_from_json(json_file_name)

    object_in_ws = []
    for object_name in data["objects"]:
        if object_dict.get(object_name, None) is not None:
            object_in_ws.append(object_dict[object_name])

    return WorldState(name = data["name"], objectnodes=object_in_ws)

#Paper draft this to see how it would fare?
#Maybe figure out how the JSON File would look like?
#Decide on what inputs we need and where we're getting initial graph states from? The story nodes?
#Or can we just initialize an empty story graph with just the characters and names?
#Just checked the constructor, we don't need this, we just need a world state input

#Maybe we do not need any specific file for World State
#Tested, this works
def make_world_state_from_extracted_list_of_objects(name, object_list):
    return WorldState(name, object_list)

#Might probably need to make the connection in a text file

#UNTESTED
def make_initial_graph_from_world_state(name, world_state):

    character_object_list = [storychar for storychar in world_state.objectnodes if type(storychar) is CharacterNode]
    location_object_list = [storyloc for storyloc in world_state.objectnodes if type(storyloc) is LocationNode]

    return StoryGraph(name=name, character_objects=character_object_list, location_objects=location_object_list, starting_ws=world_state)

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