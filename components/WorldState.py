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
        self.objectnodes.add(node)
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

    def add_to_worldstate(self, new_graph):
        #TODO: Maybe check everything in the new_graph, and: for each node in the new graph, add it to the self (if it isn't in)
        #And add relationships too
        pass

    def apply_relationship_change(self, relchange_object):
        if relchange_object.add_or_remove == "add":
            #If the intention is to add, then we add a connection between the nodes
            #If either nodes don't exist already, then they must be added to the list of nodes.

            #Checks if either nodes already exists in the node dict
            #If it doesn't exist, add it to the node dict
            if not self.node_dict.has_key(relchange_object.node_a.get_name()):
                self.node_dict[relchange_object.node_a.get_name()] = relchange_object.node_a
            if not self.node_dict.has_key(relchange_object.node_b.get_name()):
                self.node_dict[relchange_object.node_b.get_name()] = relchange_object.node_b
            #After adding nodes that don't already exist, make the connections and add it to the list of edges
                self.connect(self.node_dict[relchange_object.node_a.get_name()], relchange_object.edge, self.node_dict[relchange_object.node_b.get_name()])

        if relchange_object.add_or_remove == "remove":
            #If the intention is to remove, then we remove this specific edge between the nodes (if it exists)
            #Don't delete the nodes, though
            #Check if this exact edge between these exact nodes exists
            if relchange_object.edge in self.edges:
                #If it exists, remove it
                self.edges.remove(relchange_object.edge)


