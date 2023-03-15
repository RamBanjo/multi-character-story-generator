import copy
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

def permute_all_possible_freesize_groups(actor_count, group_count):

    return_list = []

    for grouping in partitionfunc(actor_count, group_count):
        for tup_part in list(itertools.permutations(grouping)):
            return_list.append(tup_part)

    return list(set(return_list))

def all_possible_actor_groupings(grouping_info, charcter_list):
    '''Please note that this function does not accept -1 or tuples as grouping info input. For that functionality, please use all_possible_actor_groupings_with_ranges_and_freesizes() instead.'''

    permutations_of_character_list = itertools.permutations(charcter_list)
    all_possible_grouping_list = []

    for line in permutations_of_character_list:

        current_line = []
        actor_count = 0

        for grouping in grouping_info:

            this_group = []
            for iteration in range(0, grouping):
                this_group.append((line[actor_count]))
                actor_count += 1

            this_group = sorted(list(set(this_group)))
            current_line.append(tuple(this_group))

        all_possible_grouping_list.append(tuple(current_line))

    return sorted(list(set(all_possible_grouping_list)))

def all_possible_actor_groupings_with_ranges_and_freesizes(grouping_info, character_list):

    complete_list = []

    list_of_possible_groupings = permute_all_possible_groups_with_ranges_and_freesize(grouping_info, len(character_list))
    
    for grouping in list_of_possible_groupings:
        complete_list += all_possible_actor_groupings(grouping, character_list)

    return complete_list

def permute_all_possible_groups_with_ranges_and_freesize(size_list, required_sum, verbose = False):
    '''size_list is a list that contains the number of characters required for each of the split.
    Putting a tuple with size 2 in the size list will allow that slot to contain any characters between that range (inclusive),
    and putting a -1 in the size list will mark that slot as freesize and allow any positive integer in it.
    
    required_sum is the goal sum to add up to.'''
    #Given a sum, some ranges, and some amount of -1, list all possible ways to reach that sum.
    #Integer Partition will be useful for this
    #TDivide the list into three parts, integers, ranges, and -1s
    #First, deduct the integers from the required sum. Those are already taken care of.
    #Next, w

    #This dict will record all the items by type.
    remaining_sum = required_sum

    dict_of_items = {"integers":[], "ranges":[], "freesizes":[]}
    for item in size_list:
        if type(item) == tuple:
            dict_of_items["ranges"].append(item)
        elif item != -1:
            dict_of_items["integers"].append(item)
            remaining_sum -= item
        elif item == -1:
            dict_of_items["freesizes"].append(item)

    range_count = len(dict_of_items["ranges"])
    free_count = len(dict_of_items["freesizes"])

    if range_count == 0 and free_count == 0:
        return [size_list]

    if remaining_sum - (range_count+free_count) < 0:
        if(verbose):
            print("There's just not enough numbers left to make this combination possible.")
        return None

    all_possible_ranges = []
    if range_count != 0:
        for range_combi in permute_full_range_list(range_number_to_range_list(dict_of_items["ranges"])):
            all_possible_ranges.append(range_combi)

    all_possible_freesizes = []
    if free_count != 0:
        for count in range(1, remaining_sum+1):
            all_possible_freesizes += permute_all_possible_freesize_groups(count, free_count)

    combinations_with_good_sum = []
    if range_count == 0:
        combinations_with_good_sum = [free_combi for free_combi in all_possible_freesizes if sum(free_combi) == remaining_sum]

    elif free_count == 0:
        combinations_with_good_sum = [range_combi for range_combi in all_possible_ranges if sum(range_combi) == remaining_sum]
    else:
        for free_combi in all_possible_freesizes:
            for range_combi in all_possible_ranges:
                if sum(free_combi) + sum(range_combi) == remaining_sum:
                    combinations_with_good_sum.append({"freesizes":free_combi, "ranges":range_combi})

    final_list = []
    for good_combi in combinations_with_good_sum:

        current_size_list=[]
        current_range = 0
        current_free = 0

        for item in size_list:
            if type(item) == tuple:
                if free_count == 0:
                    current_size_list.append(good_combi[current_range])
                else:
                    current_size_list.append(good_combi["ranges"][current_range])
                current_range += 1

            elif item != -1:
                current_size_list.append(item)

            elif item == -1:
                if range_count == 0:
                    current_size_list.append(good_combi[current_free])
                else:
                    current_size_list.append(good_combi["freesizes"][current_free])
                current_free += 1

        final_list.append(current_size_list)

    return final_list

    # list_of_completed_ranges_and_frees = []

    # for range_combi in permute_full_range_list(range_number_to_range_list(dict_of_items["ranges"])):
    #     current_sum = remaining_sum - sum(range_combi)
    #     possible_freesizes_for_current_sum = permute_all_possible_groups(current_sum, len(dict_of_items["freesizes"]))

    #     if len(possible_freesizes_for_current_sum) > 0 or free_count == 0:
    #         list_of_completed_ranges_and_frees.append({"range":range_combi, "freesize":possible_freesizes_for_current_sum})


    # final_return_list = []

    # for pair in list_of_completed_ranges_and_frees:

        
    #     for freesize_no in range(0, len(pair["freesize"])):

    #         current_size_list = []
    #         current_range = 0
    #         current_free = 0

    #         for item in size_list:
    #             if type(item) == tuple:
    #                 current_size_list.append(pair["range"][current_range])
    #                 current_range += 1
    #             elif item != -1:
    #                 current_size_list.append(item)
    #             elif item == -1:
    #                 current_size_list.append(pair["freesize"][freesize_no][current_free])

    #     final_return_list.append(current_size_list)

    # return final_return_list                

        

def range_number_to_range_list(range_list):

    full_range_list = []
    for item in range_list:
        full_range_list.append(list(range(item[0], item[1]+1)))

    return full_range_list

def permute_full_range_list(full_range_list):
    if len(full_range_list) == 1:
        for item in full_range_list[0]:
            yield [item]
    else:
        for item in full_range_list[0]:
            for generated_item in permute_full_range_list(full_range_list[1:]):
                yield [item] + generated_item

def actor_count_sum(lhs, rhs):

    if lhs == -1 or rhs == -1:

        if type(lhs) == tuple:
            return (lhs[0]+1, 999)
        if type(rhs) == tuple:
            return (rhs[0]+1, 999)

        return -1

    if type(lhs) == int and type(rhs) == int:
        return lhs + rhs

    if type(lhs) == tuple and type(rhs) == tuple:
        return tuple([lhs[x]+rhs[x] for x in range(len(lhs))])
    elif type(lhs) == tuple and type(rhs) == int:
        return (lhs[0]+rhs, lhs[1]+rhs)
    elif type(lhs) == int and type(rhs) == tuple:
        return (rhs[0]+lhs, rhs[1]+lhs)

    return -1

def permute_actor_list_for_joint_with_range_and_freesize(current_actor, other_actors, size):

    if type(size) == tuple:
        return permute_actor_list_for_joint_with_variable_length(current_actor, other_actors, min_size=size[0], max_size=size[1])
    
    if size == -1:
        return permute_actor_list_for_joint_with_variable_length(current_actor, other_actors, min_size=2, max_size=len(other_actors)+1)
    
    return permute_actor_list_for_joint(current_actor, other_actors, size)

def permute_actor_list_for_joint(current_actor, other_actors, size_including_current_actor):

    all_actors = copy.copy(other_actors)
    all_actors.append(current_actor)

    include_index_0 = all_possible_actor_groupings([size_including_current_actor, len(all_actors)-size_including_current_actor], all_actors)
    
    return [x[0] for x in include_index_0 if current_actor in x[0]]

def permute_actor_list_for_joint_with_variable_length(current_actor, other_actors, min_size, max_size):

    true_max = max_size

    if max_size > len(other_actors) + 1:
        true_max = len(other_actors) + 1

    full_list = []
    for i in range(min_size, true_max+1):
        full_list += permute_actor_list_for_joint(current_actor, other_actors, i)

    return full_list

def getfirst(e):
    return e[0]

def getsecond(e):
    return e[1]

#TODO: Test this function.
def list_all_good_combinations_from_joint_join_pattern(dict_of_base_nodes: dict, actors_wanted, current_actor_name=None):

    #Turn the dict we got into a list.    
    list_of_base_node_structures = sorted(list(dict_of_base_nodes.items()), key=getfirst)

    #Get all the character names, and the count of how many characters there are.
    all_character_names = []
    for x in list_of_base_node_structures:
        all_character_names += x[1]
    entire_character_count = len(all_character_names)
    
    #Make a list of the lengths we want to include.
    list_of_appropriate_lengths = []
    if type(actors_wanted) == tuple:
        list_of_appropriate_lengths = range_number_to_range_list(actors_wanted)
    elif actors_wanted == -1:
        list_of_appropriate_lengths = range_number_to_range_list(len(list_of_base_node_structures), entire_character_count)
    else:
        list_of_appropriate_lengths = [actors_wanted]

    #Generate the baseline combinations. This will only include lists with appropriate sizes.
    list_of_good_combi = []
    for length in list_of_appropriate_lengths:
        take_index_0 =  all_possible_actor_groupings([length, entire_character_count-length], all_character_names)

        for group in take_index_0:
            list_of_good_combi.append(group[0])

    #Time to exclude the bad combis, then return.
    #Exclude things whose lengths are not in the list of lengths.
    #Exclude things that don't include the actor's name.
    if current_actor_name is not None:
        return [combi for combi in list_of_good_combi if current_actor_name in combi and check_if_list_contains_at_least_one_from_each_node(combi, list_of_base_node_structures)]
    else:
        return [combi for combi in list_of_good_combi if check_if_list_contains_at_least_one_from_each_node(combi, list_of_base_node_structures)]

def check_if_list_contains_at_least_one_from_each_node(actor_name_list, list_of_base_node_structures):
    
    for node_info in list_of_base_node_structures:
        count_for_node = 0
        for actor_name in node_info[1]:
            if actor_name in actor_name_list:
                count_for_node += 1

        if count_for_node == 0:
            return False
        
    return True