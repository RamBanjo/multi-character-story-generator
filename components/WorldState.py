from cgitb import text
from numpy import true_divide

from components.Edge import Edge
from components.RelChange import *
from components.StoryNode import *
from components.StoryObjects import ObjectNode
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

        self.DEFAULT_HOLD_EDGE_NAME = "holds"
        self.DEFAULT_ADJACENCY_EDGE_NAME = "connects"

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

    def doubleconnect(self, nodeA: ObjectNode, edge_name, nodeB: ObjectNode):

        self.connect(nodeA, edge_name, nodeB)
        self.connect(nodeB, edge_name, nodeA)

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

    # TODO: Make it address for the case where the input is a list instead of a node. All of the members of the list would need to be addressed.
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
            self.connect(self.node_dict[relchange_object.node_a.get_name()], relchange_object.edge_name, self.node_dict[relchange_object.node_b.get_name()])

        if (relchange_object.add_or_remove == ChangeAction.REMOVE and not reverse) or (relchange_object.add_or_remove == ChangeAction.ADD and reverse):
            #If the intention is to remove, then we remove this specific edge between the nodes (if it exists)
            #Don't delete the nodes, though
            #Check if this exact edge between these exact nodes exists
            
            check_edge = Edge(relchange_object.edge_name, relchange_object.node_a, relchange_object.node_b)

            for my_edge in self.edges:
                if my_edge == check_edge:
                    my_edge.from_node.outgoing_edges.remove(check_edge)
                    my_edge.to_node.incoming_edges.remove(check_edge)
                    self.edges.remove(check_edge)

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

        #TODO: Make a function to check the condition for each separate case
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
        
    # TODO:
    # - We should create a function when, given a story node split list and a list of character names, returns True and a character grouping that splits the characters properly according to the following rules. If no good grouping is found, then return False, then an empty list:
    #     - Make a list of all possible groupings from the list of node. Each tuple in the list represents a node grouping.
    #         - There should be something in Utilfunctions that can help with this. If there isn't something like this yet, write a new one.
    #         - For example, if it's a non-joint node without targets, then we would expect a tuple of size one.
    #         - If it's a joint node, the tuple is size two. Index 0 are actors. Index 1 are targets.
    #         - If the number of actors and the number of total slots from the split list are inequal, return False, and an empty list.
    #     - Assign characters to the nodes.
    #     - Test for story graph and world state validity.
    #         - If the test fails: remove this grouping from the list of all groupings.
    #         - If the test passes: return True, and this grouping.
    #     - Finally, check if there are any groupings left in the possible list.
    #         - If there are, loop to beginning.
    #         - If there are not, return False, and an empty list.

    def make_split_joint_grouping_from_current_state(self, split_nodes, potential_actor_names):

        actor_count = len(potential_actor_names)

        grouping_info = []

        for node in split_nodes:
            grouping_info.append(actor_count_sum(node.charcount, node.target_count))

        possible_grouping_lists = permute_all_possible_groups_with_ranges_and_freesize(grouping_info, actor_count)

        print(possible_grouping_lists)




            
            