import copy
from components.RelChange import *
from components.StoryGraphTwoWS import StoryGraph
from components.StoryObjects import *
from components.ConditionTest import *
from components.StoryNode import *
from components.UtilityEnums import *
from components.RewriteRuleWithWorldState import *

import json

from components.WorldState import WorldState

def read_from_json(json_file_name):
    f = open(json_file_name)
    data = json.load(f)
    f.close()

    return data

def read_character_node_from_extracted_dict(data):
    return CharacterNode(**data)

def read_object_node_from_extracted_dict(data):
    return ObjectNode(**data)

def read_location_node_from_extracted_dict(data):
    return LocationNode(**data)

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

#Because almost all of these require inputs of object such as a list of story nodes, and we don't want to repeat ourselves every single time, then the way reading rewrite rules should work is that we call the nodes' name from the list instead:

def read_rewriterule_from_json(file_name, node_dict):

    data = read_from_json(file_name)

    return read_rewriterule_from_extracted_dict(data, node_dict)

def make_node_dict(node_list):
    
    node_dict = dict()

    for node in node_list:
        node_dict[node.get_name()] = node

    return node_dict

def read_rewriterule_from_extracted_dict(data, node_dict):

    designated_condition = []
    designated_rewrite = []

    for condition_node_name in data.get("story_condition_list", []):
        designated_condition.append(node_dict.get(condition_node_name, None))

    for rewrite_node_name in data.get("story_change_list", []):
        designated_rewrite.append(node_dict.get(rewrite_node_name, None))

    if None in designated_condition or None in designated_rewrite:
        return None

    if len(condition_node_name) <= 0 or len(rewrite_node_name) <= 0:
        return None

    return RewriteRule(story_condition=designated_condition, story_change=designated_rewrite ,**data)

# def read_list_of_jointrules_from_json(json_file_name, verbose=False):
#     data = read_from_json(json_file_name)

#     obj_list_returns = []

#     for sub_data in data:
#         detected_type = sub_data.get("type", "[Cannot Find Joint Rule Type]")
#         match detected_type:
#             case "joining_joint":
#                 if verbose:
#                     print("Adding Joining Joint Rule:", sub_data["name"])
#                 obj_list_returns.append(read_joining_joint_rule(sub_data))
#             case "cont_joint":
#                 if verbose:
#                     print("Adding Continuous Joint Rule:", sub_data["name"])                
#                 obj_list_returns.append(read_cont_joint_rule(sub_data))
#             case "splitting_joint":
#                 if verbose:
#                     print("Adding Splitting Joint Rule:", sub_data["name"])                
#                 obj_list_returns.append(read_split_joint_rule(sub_data))
#             case _:
#                 if verbose:
#                     print("Invalid object type, nothing added. Detected type:", detected_type)

#     if verbose:
#         print("Object list is complete! List size:", str(len(obj_list_returns)))
#     return obj_list_returns

# def read_joining_joint_rule(data, story_node_list):
#     return JoiningJointRule(**data)

# def read_cont_joint_rule(data):
#     return ContinuousJointRule(**data)

# def read_split_joint_rule(data):
#     return SplittingJointRule(**data)

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

def make_object_node_dict_from_worldstate(world_state):

    return_ws = copy.deepcopy(world_state.node_dict)
    #Check if these four already exist.
    
    reserved_keys  = ["generic_actor","generic_location","generic_target","all_actors"]

    #If it already exists, return None to show that this World State isn't valid.
    for testkey in reserved_keys:
        if testkey in return_ws.keys():
            return None

    #If this is what we're doing, we need to prevent these names from being used to name Nodes
    return_ws["generic_actor"] = GenericObjectNode.GENERIC_ACTOR
    return_ws["generic_location"] = GenericObjectNode.GENERIC_LOCATION
    return_ws["generic_target"] = GenericObjectNode.GENERIC_TARGET
    return_ws["all_actors"] = GenericObjectNode.ALL_ACTORS

    return return_ws

def read_held_item_test_from_extracted_dict(data, world_state):

    ws_dict = make_object_node_dict_from_worldstate(world_state)

    designated_holder = ws_dict.get(data.get("holder", None), None)
    designated_tag = ws_dict.get(data.get("tag_to_test", None), None)
    designated_value = ws_dict.get(data.get("value_to_test", None), None)
    designated_inverse = data.get("inverse", False)

    if designated_holder is None or designated_tag is None:
        return None

    kwargs = {"holder_to_test":designated_holder, "tag_to_test":designated_tag, "value_to_test":designated_value, "inverse":designated_inverse}

    return HeldItemTagTest(**kwargs)

def read_has_edge_test_from_extracted_dict(data, world_state):

    ws_dict = make_object_node_dict_from_worldstate(world_state)

    designated_from_node = ws_dict.get(data.get("from", None), None)
    designated_to_node = ws_dict.get(data.get("to", None), None)
    designated_edge_name = data.get("edge_name", None)
    designated_value = data.get("value", None)
    desginated_soft_equal = data.get("soft_equal", False)
    designated_inverse = data.get("inverse", False)

    if designated_from_node is None or designated_to_node is None:
        return None

    kwargs = {"object_from_test":designated_from_node, "object_to_test":designated_to_node, "edge_name_test":designated_edge_name, "value_test":designated_value, "soft_equal":desginated_soft_equal, "inverse":designated_inverse}

    return HasEdgeTest(**kwargs)

def read_has_double_edge_test_from_extracted_dict(data, world_state):

    ws_dict = make_object_node_dict_from_worldstate(world_state)

    designated_from_node = ws_dict.get(data.get("from", None), None)
    designated_to_node = ws_dict.get(data.get("to", None), None)
    designated_edge_name = data.get("edge_name", None)
    designated_value = data.get("value", None)
    desginated_soft_equal = data.get("soft_equal", False)
    designated_inverse = data.get("inverse", False)

    if designated_from_node is None or designated_to_node is None:
        return None

    kwargs = {"object_from_test":designated_from_node, "object_to_test":designated_to_node, "edge_name_test":designated_edge_name, "value_test":designated_value, "soft_equal":desginated_soft_equal, "inverse":designated_inverse}
    
    return HasDoubleEdgeTest(**kwargs)

def read_same_location_test_from_extracted_dict(data, world_state):
    
    ws_dict = make_object_node_dict_from_worldstate(world_state)

    list_to_test = []

    for char_name in data["char_name_list"]:

        if ws_dict.get(char_name, None) is not None:
            list_to_test.append(ws_dict[char_name])

    kwargs = {"list_to_test":list_to_test, "inverse":data["inverse"]}

    return SameLocationTest(**kwargs)

#Story Node will require some conversions from the test functions above

def read_story_node_from_extracted_dict(data, world_state):
    test_list = read_list_of_tests_from_data(data.get("condition_test_list", []), world_state)

    #Read tagchange object and relchange object
    change_list = read_list_of_changes_from_extracted_list(data.get("changes_list", []), world_state)
    
    return StoryNode(condition_tests=test_list, effects_on_next_ws=change_list, **data)

def read_story_node_from_json(json_file_name, world_state):
    data = read_from_json(json_file_name)
    return read_story_node_from_extracted_dict(data, world_state)

def read_list_of_story_nodes_from_json(json_file_name, world_state):
    data = read_from_json(json_file_name)
    list_of_story_nodes = []
    for story_node_data in data:
        list_of_story_nodes.append(read_story_node_from_extracted_dict(story_node_data, world_state))
    return list_of_story_nodes

# def read_list_of_tests_from_json(json_file_name, world_state):
#     data = read_list_of_tests_from_data(json_file_name, world_state)
#     return data
    

def read_list_of_tests_from_data(data, world_state):
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

    ws_dict = make_object_node_dict_from_worldstate(world_state)
    object_node_name = ws_dict[data["object_node_name_text"]]
    
    if type(object_node_name) == ObjectNode:
        object_node_name = object_node_name.get_name()

    add_or_remove = text_to_changeaction(data["add_or_remove_text"])

    if add_or_remove == "invalid":
        return

    return TagChange(add_or_remove=add_or_remove, object_node_name=object_node_name, **data)

def make_rel_change_object_from_extracted_list(data, world_state):

    ws_dict = make_object_node_dict_from_worldstate(world_state)

    add_or_remove = text_to_changeaction(data["add_or_remove_text"])

    if add_or_remove == "invalid":
        return

    node_a = ws_dict[data["node_a_name"]]
    node_b = ws_dict[data["node_b_name"]]
    
    return RelChange(node_a = node_a, node_b = node_b, add_or_remove=add_or_remove, **data)

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

            kwargs = {"from_node":designated_from_node, "to_node":designated_to_node, "edge_name":designated_edge_name, "value":designated_value}
            world_state.connect(**kwargs)
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

    kwargs = {"name":name, "character_objects":character_object_list, "location_objects":location_object_list, "starting_ws":world_state}

    return StoryGraph(**kwargs)