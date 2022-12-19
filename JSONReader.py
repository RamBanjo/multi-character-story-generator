from components.RelChange import *
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

def read_held_item_test_from_extracted_dict(data, world_state):
    return HeldItemTagTest(holder_to_test=world_state.node_dict[data["holder"]], tag_to_test=data["tag_to_test"], value_to_test=data["value_to_test"], inverse=data["inverse"])

def read_has_edge_test_from_extracted_dict(data, world_state):
    return HasEdgeTest(object_from_test=world_state.node_dict[data["from"]], object_to_test=world_state.node_dict[data["to"]], edge_name_test=data["edge_name"], soft_equal=data["soft_equal"], inverse=data["inverse"])

def read_has_double_edge_test_from_extracted_dict(data, world_state):
    return HasDoubleEdgeTest(object_from_test=world_state.node_dict[data["from"]], object_to_test=world_state.node_dict[data["to"]], edge_name_test=data["edge_name"], soft_equal=data["soft_equal"], inverse=data["inverse"])

def read_same_location_test_from_extracted_dict(data, world_state):

    list_to_test = []

    for char_name in data["char_name_list"]:
        list_to_test.append(world_state.node_dict[char_name])

    return SameLocationTest(list_to_test=list_to_test, inverse=data["inverse"])

#Story Node will require some conversions from the test functions above
def read_story_node_from_json(json_file_name, world_state):
    data = read_from_json(json_file_name)

    test_list = read_list_of_tests_from_json(data["condition_test_list"], world_state)

    return StoryNode(name = data["name"], biasweight=data["biasweight"], tags=data["tags"], charcount=data["charcount"], required_tags_list=data["required_tags"], unwanted_tags_list=data["unwanted_tags"], bias_range = data["bias_range"], required_tags_list_target=data["required_tags"], unwanted_tags_list_target=data["unwanted_tags"], bias_range_target=data["bias_range"],condition_tests=test_list)

def read_list_of_tests_from_json(data, world_state):

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

def make_connection_from_json(json_file_name, world_state):

    data = read_from_json(json_file_name)
    for connection in data:
        world_state.connect(from_node = world_state.node_dict[connection["from_node"]], edge_name = connection["edge_name"], to_node = world_state.node_dict[connection["to_node"]])

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
def make_story_graph_from_json(json_file_name, world_state):

    data = read_from_json(json_file_name)
    
    pass

thing_list = read_list_of_objects_from_json("json/TestObjectList.json", verbose=True)