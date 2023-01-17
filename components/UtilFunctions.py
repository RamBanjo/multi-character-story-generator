import math
from components import Edge
from components import StoryObjects
from components import StoryNode

#Function: Initialize Object
#Inputs: Object, Location
#Action: Define that object is at location, and add relationship edges to signify such
def init_object(thing_to_init, loca):
    holds = Edge.Edge("holds", loca, thing_to_init)
    thing_to_init.incoming_edges.add(holds)
    loca.outgoing_edges.add(holds)

#Function: Remove Relationship
#Inputs: Object, Edge, Target
#Action: Removes edge from object and target (Remove incoming from object, remove outgoing target)
def remove_relationship(obj, tar, edge):
    obj.outgoing_edges.remove(edge)
    tar.incoming_edges.remove(edge)

#Function: Add Relationship
#Inputs: Object, Edge, Target
#Action: Adds a new relationship from object to target with edge.
def add_relationship(obj, tar, edge):
    obj.outgoing_edges.add(edge)
    tar.incoming_edges.add(edge)
    
#Relationship Change Definition
#For use in Take Action function to change relationship type
#add or remove can either be add or remove, the relationship will add or remove depending on that
#fromtype can either be actor or target
#totype can either be actor or target
#from actor to actor: all actors will change their relationship towards each of the other actors
#from actor to target: all actors will change their relationship towards each of the targets
#from target to target: all targets will change their relationship towards each of the other targets
#from target to actor: all targets will change their relationship towards each of the actors

class RelationshipChange:
    def __init__(self, edge, add_or_remove, fromtype, totype):
        self.edge = edge
        self.add_or_remove = add_or_remove

#Function: Take Action
#Inputs: Actor, StoryNode, Target, Relationship
#Action: Actor will act on Target with StoryNode, and call Add Relationship or Remove Relationship
#Relcha is the list of relationships!
#StoryNode is the node that they will do
#obj is object
#tar is target
#there is a lot to process here
        
#OH NO I FORGOT THAT AN ACTION MAY HAVE MULTIPLE OBJECTS OR OBJ AND TARGET
#Sob.

def take_action(obj, tar, relchalst, storynode, prevnode = None):
    
    storynode.actor.add(obj)
    storynode.target.add(tar)
    
    if prevnode is not None:
        storynode.previous_node[obj.unique_id] = prevnode
        prevnode.next_node[obj.unique_id] = storynode
    
    #Here's the problem child
    #yanno what, here's what i'll do
    #Every time the location needs to be changed, the two relationship changes are:
    #Character is no longer in Old Location
    #Character is in New Location
    #Because each thing can be in one location at a time
    #this makes sense!!!
    for relcha in relchalst:
        if(relcha.add_or_remove == "add"):
            
            obj.outgoing_edge.add(relcha.edge)
            tar.incoming_edge.add(relcha.edge)
            
            relcha.edge.from_node = obj
            relcha.edge.to_node = tar
            
        if(relcha.add_or_remove == "remove"):
            
            obj.outgoing_edge.remove(relcha.edge)
            tar.incoming_edge.remove(relcha.edge)
            
            relcha.edge.from_node = None
            relcha.edge.to_node = None
            
            
def print_all_incoming(list_of_nodes):
    
    incoming_edge_list = []
    
    for objnode in list_of_nodes:
        incoming_edge_list += [edgy for edgy in objnode.incoming_edges]
        
    for edge in incoming_edge_list:
        print(edge)
        
        
def print_all_outgoing(list_of_nodes):
    
    outgoing_edge_list = []
    
    for objnode in list_of_nodes:
        outgoing_edge_list += [edgy for edgy in objnode.outgoing_edges]
        
    for edge in outgoing_edge_list:
        print(edge)

def get_max_possible_grouping_count(group_size_list):
    max_pos_groupcount = math.factorial(sum(group_size_list))
    
    for groupsize in group_size_list:
        max_pos_groupcount = max_pos_groupcount / math.factorial(groupsize)

    return max_pos_groupcount

def get_max_possible_actor_target_count(actor_count, target_count, total_char_count):

    if actor_count != -1 and target_count != -1:
        return math.comb(total_char_count, actor_count)

    if actor_count == -1 and target_count != -1:
        return math.comb(total_char_count, target_count)

    if actor_count != -1 and target_count == -1:
        return math.comb(total_char_count, actor_count)

    if actor_count == -1 and target_count == -1:
        return math.pow(total_char_count, 2) - 2

    return 0
            
