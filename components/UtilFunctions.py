import itertools
import math
import random
from components.Edge import Edge

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

    #This function's calculations are based on the Pascal Triangle's combinatorics.

    if actor_count != -1 and target_count != -1:
        return math.comb(total_char_count, actor_count)

    if actor_count == -1 and target_count != -1:
        return math.comb(total_char_count, target_count)

    if actor_count != -1 and target_count == -1:
        return math.comb(total_char_count, actor_count)

    if actor_count == -1 and target_count == -1:
        #Minus 2 because we don't want the case where there are no actors or the case where there are no targets
        return math.pow(total_char_count, 2) - 2

    return 0

def generate_grouping_from_group_size_lists(size_list, actor_count):

    return_size_list = []

    freesize_count = len([elem for elem in size_list if elem == -1])
    normalsum = sum([elem for elem in size_list if elem != -1])

    rand_freesize_list = generate_posint_list_that_adds_to_n(freesize_count, actor_count-normalsum)

    if rand_freesize_list == None:
        return None

    freesize_iterator = 0
    for size in size_list:
        if size != -1:
            return_size_list.append(size)
        else:
            return_size_list.append(rand_freesize_list[freesize_iterator])
            freesize_iterator += 1

    return return_size_list
            
def generate_posint_list_that_adds_to_n(list_size, required_sum):
    if list_size > required_sum:
        return None

    return_list = [1] * list_size

    while sum(return_list) != required_sum:
        return_list[random.randint(0, list_size-1)] += 1

    return return_list

#Code taken from StackOverflow (https://stackoverflow.com/questions/18503096/python-integer-partitioning-with-given-k-partitions)
def partitionfunc(n,k,l=1):
    '''n is the integer to partition, k is the length of partitions, l is the min partition element size'''
    if k < 1:
        return
    if k == 1:
        if n >= l:
            yield (n,)
        return
    for i in range(l,n+1):
        for result in partitionfunc(n-i,k-1,i):
            yield (i,)+result

def permute_all_possible_groups(actor_count, group_count):

    return_list = []

    for grouping in partitionfunc(actor_count, group_count):
        for tup_part in list(itertools.permutations(list(grouping))):
            return_list.append(tup_part)

    return list(set(return_list))

def all_possible_actor_groupings(grouping_info, charcter_list):

    permutations_of_character_list = itertools.permutations(charcter_list)
    all_possible_grouping_list = []

    for line in permutations_of_character_list:

        current_line = []
        actor_count = 0

        for grouping in grouping_info:

            this_group = []
            for iteration in range(0, grouping):
                this_group.append(line[actor_count])
                actor_count += 1

            current_line.append(this_group)

        all_possible_grouping_list.append(current_line)

    return all_possible_grouping_list

def permute_all_possible_groups_with_ranges_and_freesize(size_list, required_sum):
    #TODO: Given a sum, some ranges, and some amount of -1, list all possible ways to reach that sum.
    #TODO: Integer Partition will be useful for this
    #TODO: Divide the list into three parts, integers, ranges, and -1s
    #TODO: First, deduct the integers from the required sum. Those are already taken care of.
    #TODO: For the ranges, permute all possible combinations. For each permutation, deduct the sum of the ranges from (Required Sum - integers).
    #TODO: If the subtracted sum is less than the number of freesize spots that we have, remove it (for example, if there are 2 freesize spots left but the sum we want is 1, then that's just impossible)
    #TODO: We now have a list of all possible ranges. For each list of possible ranges, use Integer Partition after deducting the values from the ranges and integers.
    #TODO: After we have all groups of possible Ranges and Freesizes, we need to arrange them. Refer to the original List Size to arrange them.
    #TODO: Finally, return a list of all possible groups.
    #TODO: Of course, doing the way that we are doing, we'll end up eliminating all the impossible cases off the list automatically.
    pass