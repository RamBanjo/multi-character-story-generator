from cgitb import text
from copy import deepcopy
import random
from numpy import true_divide
from components.CharacterTask import CharacterTask

from components.Edge import Edge
from components.RelChange import *
from components.StoryNode import *
from components.StoryObjects import LocationNode, ObjectNode
from components.UtilFunctions import actor_count_sum, permute_all_possible_groups_with_ranges_and_freesize
from components.UtilityEnums import *

class WorldState:
    def __init__(self, name, objectnodes=[], DEFAULT_HOLD_EDGE_NAME = "holds", DEFAULT_ADJACENCY_EDGE_NAME = "connects"):

        '''
        Graph properties
        Name: Name of the graph
        objectnodes: The list of nodes!
        node_dict: The list of nodes, which can be looked up by name in the node dict
        '''
        self.name = name
        self.objectnodes = objectnodes
        self.edges = []
        self.node_dict = dict()
        self.make_node_dict()

        self.DEFAULT_HOLD_EDGE_NAME = DEFAULT_HOLD_EDGE_NAME
        self.DEFAULT_ADJACENCY_EDGE_NAME = DEFAULT_ADJACENCY_EDGE_NAME

    '''
    Node Attributes
    '''

    def set_node_name(self, node: ObjectNode, new_name):
        del self.node_dict[node.get_name]
        self.node_dict[new_name] = node
        node.set_name = new_name

    def add_node(self, node: ObjectNode):
        self.objectnodes.append(node)
        self.node_dict[node.get_name()] = node

    def add_nodes(self, nodes: list):
        for thing in nodes:
            self.add_node(thing)

    def remove_node(self, node: ObjectNode):

        for edge in node.get_outgoing_edge():
            edge.to_node.remove_incoming_edge(edge)

        for edge in node.get_incoming_edge():
            edge.from_node.remove_outgoing_edge(edge)

        del self.node_dict[node.get_name]
        self.objectnodes.remove(node)

    def set_node_attribute(self, node, attribute, tag):
        nodenum = self.objectnodes.index(node)
        self.objectnodes[nodenum].set_tag(attribute, tag)

    def make_node_dict(self):
        for node in self.objectnodes:	
            self.node_dict[node.get_name()] = node

    '''
    edge functions
    '''

    def check_connection(self, node_a: ObjectNode, node_b: ObjectNode, edge_name=None, edge_value=None, soft_equal=False):


        node_a_retrieved = self.node_dict.get(node_a.get_name(), None)
        node_b_retrieved = self.node_dict.get(node_b.get_name(), None)

        if node_a_retrieved is None or node_b_retrieved is None:
            return False

        check_name = True

        if edge_name is None:
            check_name = False

        for edge in self.edges:
            if not soft_equal and (edge.from_node == node_a_retrieved and edge.to_node == node_b_retrieved and edge.get_value() == edge_value) and (not check_name or edge.get_name() == edge_name):
                return True
            if soft_equal and (edge.from_node == node_a_retrieved and edge.to_node == node_b_retrieved) and (not check_name or edge.get_name() == edge_name):
                return True
        
        return False

    def check_double_connection(self, node_a: ObjectNode, node_b: ObjectNode, edge_name=None, edge_value=None, soft_equal = False):
        return self.check_connection(node_a, node_b, edge_name, edge_value, soft_equal) and self.check_connection(node_b, node_a, edge_name, edge_value, soft_equal)

    def list_location_adjacencies(self):
        print("Location Adjacencies:")

        locations_in_dict = [loco for loco in self.node_dict.values() if ('Type', 'Location') in loco.tags.items()]

        for location in locations_in_dict:
            adjacencies = self.node_dict[location.get_name()].get_adjacent_locations_list(self.DEFAULT_ADJACENCY_EDGE_NAME)

            texttoprint = location.get_name()
            texttoprint += " -> "

            for in_edge in adjacencies:
                texttoprint += in_edge.from_node.get_name()
                texttoprint += ", "
            if len(adjacencies) > 0:
                print(texttoprint[:-2])
            else:
                print(location.get_name(), "has no adjacencies!")

    def make_list_of_nodes_from_tag(self, tag, value):
        
        list_of_applicable_object_nodes = []

        for objectnode in self.node_dict.values():
            if objectnode.tags[tag] == value:
                list_of_applicable_object_nodes.append(objectnode)

        return list_of_applicable_object_nodes

    '''
    connect
    '''
    def connect(self, from_node: ObjectNode, edge_name, to_node: ObjectNode, value = None):

        #new edge
        new_edge = Edge(edge_name, from_node, to_node, value)

        #add stuff to the nodes
        from_node.add_outgoing_edge(new_edge)
        to_node.add_incoming_edge(new_edge)

        self.edges.append(new_edge)

    def doubleconnect(self, nodeA: ObjectNode, edge_name, nodeB: ObjectNode, value = None):

        self.connect(from_node = nodeA, edge_name = edge_name, to_node = nodeB, value = value)
        self.connect(from_node = nodeB, edge_name = edge_name, to_node = nodeA, value = value)

    def disconnect(self, from_node, edge_name, to_node, value = None, soft_equal = False):

        to_remove = Edge(edge_name, from_node, to_node, value)

        for my_edge in self.edges:
            if (not soft_equal and my_edge == to_remove) or (soft_equal and to_remove.soft_equal(my_edge)):
                my_edge.from_node.outgoing_edges.remove(to_remove)
                my_edge.to_node.incoming_edges.remove(to_remove)
                self.edges.remove(to_remove)


    def is_subgraph(self, other_world_state):
        #Okay, same deal with the other subgraph functions here:
        #If everything in self is contained in the other graph then it is a subgraph
        #To do this, we check every node and edge in this graph to see if it's contained within the other world state

        #TODO: Use HashTable/Dict to optimize speed if it turns out this is super inefficient later on

        result = True

        for node in self.objectnodes:
            result = result and node in other_world_state.objectnodes

        for edge in self.edges:
            result = result and edge in other_world_state.edges

        return result

    def apply_some_change(self, changeobject, reverse=False):
        if changeobject.changetype == ChangeType.RELCHANGE:
            self.apply_relationship_change(changeobject, reverse)
        if changeobject.changetype == ChangeType.TAGCHANGE:
            self.apply_tag_change(changeobject, reverse)

    # For each of the name found in list_of_test_object_names, find the corresponding object in this WorldState. Then, run tests given in the conditionalchange, replacing the placeholder token with the object.
    # If all the tests are passed, apply the change, by calling apply relationship change and apply tag change from this very same worldstate. Phew!

    # Note: We need to look at the state of the Previous World State, not this current world state. The changes should only be applied if and only if the previous world state passed those tests.
    def apply_conditional_change(self, condchange_object, previous_ws, reverse=False):

        for item_name in condchange_object.list_of_test_object_names:

            current_object = self.node_dict[item_name]

            pass_test = True

            for test in condchange_object.list_of_condition_tests:
                translated_test = replace_placeholder_object_with_test_taker(test, current_object)
                pass_test = pass_test and previous_ws.test_story_compatibility_with_conditiontest(translated_test)

            if pass_test:
                for change in condchange_object.list_of_changes:
                    translated_change = replace_placeholder_object_with_change_haver(change, current_object)
                    self.apply_some_change(translated_change, reverse=reverse)

    # Make it address for the case where the input is a list instead of a node. All of the members of the list would need to be addressed.
    # Not needed: We can simply loop through the entire list and run this function for each item in the list.
    #TODO: Sigh, we need to test this function again, what bs
    def apply_relationship_change(self, relchange_object, reverse=False):

        if (relchange_object.add_or_remove == ChangeAction.ADD and not reverse) or (relchange_object.add_or_remove == ChangeAction.REMOVE and reverse):
            #If the intention is to add, then we add a connection between the nodes
            #If either nodes don't exist already, then they must be added to the list of nodes.
            #Checks if either nodes already exists in the node dict
            #If it doesn't exist, add it to the node dict
            if relchange_object.node_a.get_name() not in self.node_dict:
                self.node_dict[relchange_object.node_a.get_name()] = relchange_object.node_a
            if relchange_object.node_b.get_name() not in self.node_dict:
                self.node_dict[relchange_object.node_b.get_name()] = relchange_object.node_b
            #After adding nodes that don't already exist, make the connections and add it to the list of edges

            if relchange_object.two_way:
                self.doubleconnect(from_node=self.node_dict[relchange_object.node_a.get_name()], edge_name = relchange_object.edge_name, to_node = self.node_dict[relchange_object.node_b.get_name()], value=relchange_object.value)
            else:
                self.connect(from_node=self.node_dict[relchange_object.node_a.get_name()], edge_name = relchange_object.edge_name, to_node = self.node_dict[relchange_object.node_b.get_name()], value=relchange_object.value)

        if (relchange_object.add_or_remove == ChangeAction.REMOVE and not reverse) or (relchange_object.add_or_remove == ChangeAction.ADD and reverse):
            #If the intention is to remove, then we remove this specific edge between the nodes (if it exists)
            #Don't delete the nodes, though
            #Check if this exact edge between these exact nodes exists

            node_a_retrieved = self.node_dict.get(relchange_object.node_a.get_name(), None)
            node_b_retrieved = self.node_dict.get(relchange_object.node_b.get_name(), None) #if self.check_connection(node_a=node_a_retrieved, node_b=node_b_retrieved, edge_name=relchange_object.edge_name, edge_value=relchange_object.value, soft_equal=relchange_object.soft_equal):
            
            
            self.disconnect(from_node=node_a_retrieved, edge_name=relchange_object.edge_name, to_node=node_b_retrieved, value=relchange_object.value, soft_equal=relchange_object.soft_equal)
            if relchange_object.two_way:
                self.disconnect(from_node=node_b_retrieved, edge_name=relchange_object.edge_name, to_node=node_a_retrieved, value=relchange_object.value, soft_equal=relchange_object.soft_equal)

            # check_edge = Edge(relchange_object.edge_name, relchange_object.node_a, relchange_object.node_b)

            # for my_edge in self.edges:
            #     if my_edge == check_edge:
            #         my_edge.from_node.outgoing_edges.remove(check_edge)
            #         my_edge.to_node.incoming_edges.remove(check_edge)
            #         self.edges.remove(check_edge)

    def apply_tag_change(self, tagchange_object, reverse=False):
        if (tagchange_object.add_or_remove == ChangeAction.ADD and not reverse) or (tagchange_object.add_or_remove == ChangeAction.REMOVE and reverse):
            self.node_dict[tagchange_object.object_node_name].set_tag(tagchange_object.tag, tagchange_object.value)
        if (tagchange_object.add_or_remove == ChangeAction.REMOVE and not reverse) or (tagchange_object.add_or_remove == ChangeAction.ADD and reverse):
            self.node_dict[tagchange_object.object_node_name].remove_tag(tagchange_object.tag)

    def print_all_nodes(self):
        print("=== List of Nodes in {} ===".format(self.name))
        for node in self.node_dict:
            print("- {}".format(node))
        print("======")

    def print_all_edges(self):
        print("=== List of Edges in {} ===".format(self.name))
        for edge in self.edges:
            print("- {}".format(edge))
        print("======")

    def test_story_compatibility_with_storynode(self, story_node):

        compatibility_result = True
        
        test_condition_list = story_node.condition_tests

        for condtest in test_condition_list:
            compatibility_result = compatibility_result and self.test_story_compatibility_with_conditiontest(condtest)

        return compatibility_result

    def test_story_compatibility_with_conditiontest(self, test):

        #Check what kind of test is going to be done here

        test_type = test.test_type
        test_result = False
        
        match test_type:
            case TestType.HELD_ITEM_TAG:
                test_result = self.held_item_tag_check(test.holder_to_test, test.tag_to_test, test.value_to_test)
            case TestType.SAME_LOCATION:
                test_result = self.same_location_check(test.list_to_test)
            case TestType.HAS_EDGE:
                test_result = self.check_connection(test.object_from_test, test.object_to_test, test.edge_name_test, test.value_test, test.soft_equal)
            case TestType.HAS_DOUBLE_EDGE:
                test_result = self.check_double_connection(test.object_from_test, test.object_to_test, test.edge_name_test, test.value_test, test.soft_equal)
            case _:
                test_result = False

        if test.inverse:
            test_result = not test_result
            
        return test_result

    #In order to ensure that all nodes called are from the worldstate directly, we will use the object name to invoke them
    def same_location_check(self, check_list):
        list_from_this_ws = []

        for item in check_list:
            list_from_this_ws.append(self.node_dict.get(item.get_name(), None))
            list_from_this_ws = list(filter(lambda a: a is not None, list_from_this_ws))
        
        return WorldState.check_items_in_same_location(list_from_this_ws)

    def held_item_tag_check(self, holder_test, value_test, tag_test=None):
        holder = self.node_dict.get(holder_test.get_name(), None)

        if holder is None:
            return False

        return holder.check_if_this_item_holds_item_with_tag(value_test, tag_test, self.DEFAULT_HOLD_EDGE_NAME)

    @staticmethod
    def check_items_in_same_location(item_checklist):
        #If there is one item or less in the list, return true
        if len(item_checklist) <= 1:
            return True
        else:
            #If it's not empty, first get the location of the first item in the list
            location_to_check = item_checklist[0].get_holder()
            list_of_things_at_checkloc = location_to_check.get_list_of_things_held_by_this_item()
            same_location = True

            for check_thing in item_checklist:
                same_location = same_location and check_thing in list_of_things_at_checkloc

            return same_location

    def make_split_joint_grouping_from_current_state(self, split_nodes, potential_actor_names):

        actor_count = len(potential_actor_names)

        grouping_info = []

        for node in split_nodes:
            grouping_info.append(actor_count_sum(node.charcount, node.target_count))

        possible_grouping_lists = permute_all_possible_groups_with_ranges_and_freesize(grouping_info, actor_count)

        print(possible_grouping_lists)

    def count_reachable_locations_from_location(self, starting_location):

        seen_locations = [starting_location]
        queue = [starting_location]
        
        while len(queue) > 0:
            current_loc = self.node_dict[queue.pop().get_name()]
            adjacent_locs = current_loc.get_adjacent_locations_list(adjacent_rel_name=self.DEFAULT_ADJACENCY_EDGE_NAME, return_as_objects=True)

            #Add to Queue if the locations weren't already seen
            queue_extend = [x for x in adjacent_locs if x not in seen_locations]
            queue.extend(queue_extend)

            #See the locations adjacent to current 
            
            unseen_adjacent_locs = [x for x in adjacent_locs if x not in seen_locations]
            seen_locations.extend(unseen_adjacent_locs)

        return len(seen_locations)
    #TODO: What this function should do: return one of the many possible paths to get to that location.
    # The path is formatted like [A, B, ..., C] where A is the current location and C is the destination location
    #If there's no possible path, then return None
    #I think this can be done using recursion?

    #Wait no frick, do we really have to do the shortest path? Maybe the shortest path could be more dangerous and it would be more practical to take the longer path in that case?
    #Or maybe the main character would take the shortest path, but they would also want to be smart about it and take a slight detour to do another task, then return on the main path to do the quest?
    
    #Okay, okay, I got an idea, and I'm writing this down even though this isn't normally my workday. I'm doing so so I don't forget about this later.
    # 1. Check for tasks in current location
    # 1.1 If there are tasks in current location, do those tasks
    # 1.2 If there aren't any tasks in current location, look for tasks in adjacent locations
    # 1.2.1 If there are tasks in adjacent locations, head to one of the locations with tasks to do randomly, weighted by number of tasks
    # 1.2.2 If there are not any tasks in adjacent locations, look for tasks in one of the adjacent-adjacent locations, excluding the places we have already looked, starting with one of the adjacent locations randomly, repeat until a task is found or all nodes are found without tasks
    # 2. The final output should be a tuple with the following information: (Task Location, Number of Tasks, Path towards that Location, Actions to Take At the Location)
    # 2.1 To get the task location, follow algorithm written in 
    # 2.2 To get the Number of Tasks, do 2.1 and grab the number of tasks there.
    # 2.3 To get the path towards location, each time 1.2.1 and 1.2.2 are called, add the current location to the path, so all locations have the path getting there from base location at all times.
    # 3. How to Manage Tasks?
    # 3.1 We can add a new property to CharacterNode called List of Tasks
    # 3.2 We can add a new ChangeObject called TaskChange that Adds or Removes tasks
    # 3.3 Task Management sounds a bit tough. 
    # (SG2WS) Write a function called Perform Task, where if the character is in the correct location, it will add the task's actions to the character's storyline and mark the task as complete.
    # def get_path_towards_target_location(self, current_location, target_location, current_path = []):

    #     current_path.append(current_location)
    #     if current_location == target_location:
    #         return current_path

    #If the current location has tasks, return the current location.
    #If the current location does not have tasks but at least one adjacent location has tasks, return an adjacent location.
    #If the current location does not have tasks and adjacent locations don't have tasks either, continue looking for tasks, recording the distance towards nearest task. When a task is found, attempt to pick a location with the lowest number..
    #If there are no tasks at all, return return one random reachable location, including the current location.
    #
    # (Note that some tasks don't have locations therefore cannot be located, and must be done based on )
    def get_optimal_location_towards_task(self, actor):        
        actor_task_stacks = actor.list_of_task_stacks
        current_location = self.node_dict[actor.get_incoming_edge("holds").from_node]
        
        names_of_locations_with_tasks = set()
        task_location_count_dict = dict()
        list_of_current_tasks = []

        #We're getting all the task locations from here
        for task_list in actor_task_stacks:
            if task_list.current_task != -1:
                list_of_current_tasks.append(task_list.get_current_task())

        for task in list_of_current_tasks:
            if task.location_name not in names_of_locations_with_tasks:
                names_of_locations_with_tasks.add(task.location_name)
                task_location_count_dict[task.location_name] = 1
            else:
                task_location_count_dict[task.location_name] += 1

        #If the current location has tasks, return the current location.
        if current_location.get_name() in names_of_locations_with_tasks:
            return current_location
        
        #If there aren't anywhere with tasks, return one random reachable location.
        if len(names_of_locations_with_tasks) == 0:
            valid_locations = current_location.get_adjacent_locations_list()
            valid_locations.append(current_location)
            return random.choice(valid_locations)
        
        #If there's no tasks in the current location, look for tasks that are in adjacent locations.
        if current_location.get_name() not in names_of_locations_with_tasks:
            adjacent_locations = current_location.get_adjacent_locations_list()

            list_of_checking_location_names = []
            for loc in adjacent_locations:
                list_of_checking_location_names.append(loc.get_name())

            for locname in list_of_checking_location_names:
                if locname not in names_of_locations_with_tasks:
                    list_of_checking_location_names.remove(locname)

            if len(list_of_checking_location_names) > 0:
                return self.node_dict[random.choice(list_of_checking_location_names)]
            
        #If all previous tests fail, then we need to find the closest path towards the next task, because there certainly is one that doesn't include our own.
        distance_from_closest_task_dict_for_each_adjnode = dict()
        adjacent_locations = current_location.get_adjacent_locations_list()

        minimum_distance = 999999999
        all_location_set = set(self.get_all_location_names())
        for loc in adjacent_locations:
            distance_from_closest_task_dict_for_each_adjnode[loc.get_name()] = "infinity"
            list_of_seen_locations = current_location.get_adjacent_locations_list()
            list_of_seen_locations.append(current_location)
            seen_location_names_set = set([x.get_name() for x in list_of_seen_locations])

            current_check_queue = [loc]
            
            distance_count = 1
            while len(seen_location_names_set.intersection(names_of_locations_with_tasks)) == 0:
                current_node_adjacents = current_check_queue[0].get_adjacent_locations_list()
                adj_node_name_set = set([x.get_name() for x in current_node_adjacents])

                for seenlocname in seen_location_names_set:
                    if seenlocname in adj_node_name_set:
                        adj_node_name_set.remove(seenlocname)

                found_task_node = False
                for adjloc in current_node_adjacents:
                    if adjloc.get_name() in names_of_locations_with_tasks:
                        found_task_node = True

                distance_from_closest_task_dict_for_each_adjnode[loc.get_name()]
                seen_location_names_set.add(current_check_queue[0].get_name())

                if found_task_node:
                    distance_from_closest_task_dict_for_each_adjnode[loc.get_name()] = distance_count

                if not found_task_node:
                    current_check_queue.extend(current_node_adjacents)
                    current_check_queue.pop(0)
                    distance_count += 1

                if len(seen_location_names_set) == len(all_location_set) and not found_task_node:
                    break

            if distance_count <= minimum_distance:
                minimum_distance = distance_count

        next_location_candidates = [x[0] for x in distance_from_closest_task_dict_for_each_adjnode.items() if x[1] == minimum_distance]
        return self.node_dict[random.choice(next_location_candidates)]


    def get_all_locations(self):
        return [x for x in self.node_dict.values() if type(x) == LocationNode]
    
    def get_all_location_names(self):
        return [x.get_name() for x in self.node_dict.values() if type(x) == LocationNode]

def replace_placeholder_object_with_test_taker(test, test_taker):
        
        #Check what kind of test is going to be done here

        test_type = test.test_type

        match test_type:
            case TestType.HELD_ITEM_TAG:
                return replace_placeholder_object_with_test_taker_holds(test, test_taker)
            case TestType.SAME_LOCATION:
                return replace_placeholder_object_with_test_taker_sameloc(test, test_taker)
            case TestType.HAS_EDGE:
                return replace_placeholder_object_with_test_taker_hasedge(test, test_taker)
            case TestType.HAS_DOUBLE_EDGE:
                return replace_placeholder_object_with_test_taker_hasedge(test, test_taker)
            case _:
                return None

def replace_placeholder_object_with_test_taker_hasedge(test, test_taker):

    if test.object_from_test is GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER:
        copiedtest = deepcopy(test)
        copiedtest.object_from_test = test_taker
        return copiedtest

    if test.object_to_test is GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER:
        copiedtest = deepcopy(test)
        copiedtest.object_to_test = test_taker
        return copiedtest
        
    return test

def replace_placeholder_object_with_test_taker_holds(test, test_taker):

    if test.holder_to_test is GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER:
        copiedtest = deepcopy(test)
        copiedtest.holder_to_test = test_taker
        return copiedtest
    
    return test

def replace_placeholder_object_with_test_taker_sameloc(test, test_taker):

    if GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER in test.list_to_test:
        copiedtest = deepcopy(test)
        copiedtest.list_to_test.remove(GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER)
        copiedtest.list_to_test.append(test_taker)
        return copiedtest
    
def replace_placeholder_object_with_change_haver(changeobject, change_haver):

    if changeobject.changetype == ChangeType.RELCHANGE:
        return replace_placeholder_object_with_change_haver_rel(changeobject, change_haver)
    if changeobject.changetype == ChangeType.TAGCHANGE:
        return replace_placeholder_object_with_change_haver_tag(changeobject, change_haver)
        
    return changeobject

def replace_placeholder_object_with_change_haver_rel(changeobject, change_haver):

    if changeobject.node_a is GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER:
        copiedchange = deepcopy(changeobject)
        copiedchange.node_a = change_haver
        return copiedchange

    if changeobject.node_b is GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER:
        copiedchange = deepcopy(changeobject)
        copiedchange.node_b = change_haver
        return copiedchange
        
    return changeobject

def replace_placeholder_object_with_change_haver_tag(changeobject, change_haver):

    if changeobject.object_node_name is GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER:
        copiedchange = deepcopy(changeobject)
        copiedchange.object_node_name = change_haver.get_name()
        return copiedchange
    
    return changeobject



            
            