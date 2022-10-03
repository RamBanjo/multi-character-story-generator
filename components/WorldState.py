from cgitb import text
from numpy import true_divide

from components.Edge import Edge
from components.StoryNode import *
from components.StoryObjects import ObjectNode

class WorldState:
    def __init__(self, name, objectnodes=[], node_dict = dict()):

        '''
        Graph properties
        Name: Name of the graph
        objectnodes: The list of nodes!
        node_dict: The list of nodes, which can be looked up by name in the node dict
        '''
        self.name = name
        self.objectnodes = objectnodes
        self.edges = []
        self.node_dict = node_dict
        self.make_node_dict()

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
    def check_adjacency(self, node_a: ObjectNode, node_b: ObjectNode):
        for edge in self.edges:
            if (edge.from_node == node_a and edge.to_node == node_b) or (edge.from_node == node_b and edge.to_node == node_a):
                return True
            else:
                return False

    def list_location_adjacencies(self):
        print("Location Adjacencies:")

        locations_in_dict = [loco for loco in self.node_dict.values() if ('Type', 'Location') in loco.tags.items()]

        for location in locations_in_dict:
            adjacencies = self.node_dict[location.get_name()].get_adjacent_locations_list()

            texttoprint = location.get_name()
            texttoprint += " -> "

            for in_edge in adjacencies:
                texttoprint += in_edge.from_node.get_name()
                texttoprint += ", "
            if len(adjacencies) > 0:
                print(texttoprint[:-2])
            else:
                print(location.get_name(), "has no adjacencies!")


    '''
    connect
    '''
    def connect(self, from_node: ObjectNode, edge_name, to_node: ObjectNode):

        #new edge
        new_edge = Edge(edge_name, from_node, to_node)

        #add stuff to the nodes
        from_node.add_outgoing_edge(new_edge)
        to_node.add_incoming_edge(new_edge)

        self.edges.append(new_edge)

    def doubleconnect(self, nodeA: ObjectNode, edge_name, nodeB: ObjectNode):

        self.connect(nodeA, edge_name, nodeB)
        self.connect(nodeB, edge_name, nodeA)

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
        if changeobject.changetype == "relationship":
            self.apply_relationship_change(changeobject, reverse)
        if changeobject.changetype == "tag":
            self.apply_tag_change(changeobject, reverse)

    # TODO: Change how this entire function works.
    # Instead of directly calling the obj
    def apply_relationship_change(self, relchange_object, reverse=False):
        if (relchange_object.add_or_remove == "add" and not reverse) or (relchange_object.add_or_remove == "remove" and reverse):
            #If the intention is to add, then we add a connection between the nodes
            #If either nodes don't exist already, then they must be added to the list of nodes.
            #Checks if either nodes already exists in the node dict
            #If it doesn't exist, add it to the node dict
            if relchange_object.node_a.get_name() not in self.node_dict:
                self.node_dict[relchange_object.node_a.get_name()] = relchange_object.node_a
            if relchange_object.node_b.get_name() not in self.node_dict:
                self.node_dict[relchange_object.node_b.get_name()] = relchange_object.node_b
            #After adding nodes that don't already exist, make the connections and add it to the list of edges
            self.connect(self.node_dict[relchange_object.node_a.get_name()], relchange_object.edge.name, self.node_dict[relchange_object.node_b.get_name()])

        if (relchange_object.add_or_remove == "remove" and not reverse) or (relchange_object.add_or_remove == "add" and reverse):
            #If the intention is to remove, then we remove this specific edge between the nodes (if it exists)
            #Don't delete the nodes, though
            #Check if this exact edge between these exact nodes exists

            if relchange_object.edge in self.edges:
                #If it exists, remove it
                self.edges.remove(relchange_object.edge)

    def apply_tag_change(self, tagchange_object, reverse=False):
        if (tagchange_object.add_or_remove == "add" and not reverse) or (tagchange_object.add_or_remove == "remove" and reverse):
            self.node_dict[tagchange_object.object_node_name].set_tag(tagchange_object.tag, tagchange_object.value)
        if (tagchange_object.add_or_remove == "remove" and not reverse) or (tagchange_object.add_or_remove == "add" and reverse):
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



