import copy
import itertools
import math
import random
import sys
sys.path.insert(0,'')

from application.components.ConditionTest import HasEdgeTest, HasTagTest, HeldItemTagTest, InBiasRangeTest, SameLocationTest, IntersectObjectExistsTest, ObjectPassesAtLeastOneTestTest
from application.components.Edge import Edge
from application.components.RelChange import ConditionalChange, RelChange, RelativeBiasChange, RelativeTagChange, TagChange, TaskAdvance, TaskCancel, TaskChange
from application.components.StoryObjects import ObjectNode
from application.components.UtilityEnums import ChangeType, GenericObjectNode, TestType

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

def permute_actor_for_task_stack_requirements(actor_name_list, placeholder_fill_slots):
    all_permute = sorted(list(set(itertools.permutations(actor_name_list))))

    return_list = sorted(list(set([x[:placeholder_fill_slots] for x in all_permute])))

    return return_list

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
        list_of_appropriate_lengths = range_number_to_range_list([actors_wanted])[0]
    elif actors_wanted == -1:
        full_range = (len(list_of_base_node_structures), entire_character_count)
        list_of_appropriate_lengths = range_number_to_range_list([full_range])[0]
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

#Placeholder always comes first
def replace_multiple_placeholders_with_multiple_test_takers(test, placeholder_tester_pair_list):

    copiedtest = copy.deepcopy(test)

    for thing in placeholder_tester_pair_list:
        copiedtest = replace_placeholder_object_with_test_taker(test=copiedtest, test_taker=thing[1], placeholder_object=thing[0])

    return copiedtest

def replace_placeholder_object_with_test_taker(test, test_taker, placeholder_object):
        
        #Check what kind of test is going to be done here

        test_type = test.test_type

        match test_type:
            case TestType.HELD_ITEM_TAG:
                return replace_placeholder_object_with_test_taker_holds(test, test_taker, placeholder_object)
            case TestType.SAME_LOCATION:
                return replace_placeholder_object_with_test_taker_sameloc(test, test_taker, placeholder_object)
            case TestType.HAS_EDGE:
                return replace_placeholder_object_with_test_taker_hasedge(test, test_taker, placeholder_object)
            case TestType.TAG_VALUE_IN_RANGE:
                return replace_placeholder_object_with_test_taker_hasedge(test, test_taker, placeholder_object)
            case TestType.HAS_TAG:
                return replace_placeholder_object_with_test_taker_hastag(test, test_taker, placeholder_object)
            case TestType.IN_BIAS_RANGE:
                return replace_placeholder_object_with_test_taker_biasrange(test, test_taker, placeholder_object)
            case _:
                return None

def replace_placeholder_object_with_test_taker_hasedge(test, test_taker, placeholder_object):

    if test.object_from_test == placeholder_object:
        copiedtest = copy.deepcopy(test)
        copiedtest.object_from_test = test_taker
        return copiedtest
    
    if test.object_to_test == placeholder_object:
        copiedtest = copy.deepcopy(test)
        copiedtest.object_to_test = test_taker
        return copiedtest
        
    return test

def replace_placeholder_object_with_test_taker_valuerange(test, test_taker, placeholder_object):
    if test.object_to_test == placeholder_object:
        copiedtest = copy.deepcopy(test)
        copiedtest.object_to_test = test_taker
        return copiedtest
    
    return test
    

def replace_placeholder_object_with_test_taker_holds(test, test_taker, placeholder_object):

    if test.holder_to_test == placeholder_object:
        copiedtest = copy.deepcopy(test)
        copiedtest.holder_to_test = test_taker
        return copiedtest
    
    return test

def replace_placeholder_object_with_test_taker_sameloc(test, test_taker, placeholder_object):

    if placeholder_object in test.list_to_test:
        copiedtest = copy.deepcopy(test)
        copiedtest.list_to_test.remove(placeholder_object)
        copiedtest.list_to_test.append(test_taker)
        return copiedtest

    return test
    
def replace_placeholder_object_with_test_taker_hastag(test, test_taker, placeholder_object):

    if test.object_to_test == placeholder_object:
        copiedtest = copy.deepcopy(test)
        copiedtest.object_to_test = test_taker
        return copiedtest
    
    return test
    
def replace_placeholder_object_with_test_taker_biasrange(test, test_taker, placeholder_object):

    if test.object_to_test == placeholder_object:
        copiedtest = copy.deepcopy(test)
        copiedtest.object_to_test = test_taker
        return copiedtest
    
    return test

def replace_multiple_placeholders_with_multiple_change_havers(change, placeholder_tester_pair_list):
    copiedchange = copy.deepcopy(change)

    for thing in placeholder_tester_pair_list:
        copiedchange = replace_placeholder_object_with_change_haver(changeobject=copiedchange, change_haver=thing[1], placeholder_object=thing[0])

    return copiedchange

def replace_placeholder_object_with_change_haver(changeobject, change_haver, placeholder_object):

    if changeobject.changetype == ChangeType.RELCHANGE:
        return replace_placeholder_object_with_change_haver_rel(changeobject, change_haver, placeholder_object)
    if changeobject.changetype == ChangeType.TAGCHANGE:
        return replace_placeholder_object_with_change_haver_tag(changeobject, change_haver, placeholder_object)
        
    return changeobject

def replace_placeholder_object_with_change_haver_rel(changeobject, change_haver, placeholder_object):

    if changeobject.node_a == placeholder_object:
        copiedchange = copy.deepcopy(changeobject)
        copiedchange.node_a = change_haver
        return copiedchange

    if changeobject.node_b == placeholder_object:
        copiedchange = copy.deepcopy(changeobject)
        copiedchange.node_b = change_haver
        return copiedchange
        
    return changeobject

def replace_placeholder_object_with_change_haver_tag(changeobject, change_haver, placeholder_object):

    if changeobject.object_node_name == placeholder_object:
        copiedchange = copy.deepcopy(changeobject)
        copiedchange.object_node_name = change_haver.get_name()
        return copiedchange
    
    return changeobject

# Put in a generalized relchange with "actor"

#This method should return a list of relationshp changes
#If there's only one actor and target, then the list should only be 1 element long
#Otherwise, we need to pair all the actors to all the targets and return a list of all pairs
#Even if there is no change in relationship, return the relationship as a 1 element list anyways

def translate_generic_change(change, populated_story_node):

    equivalent_changelist = []

    match change.changetype:
        case ChangeType.RELCHANGE:
            equivalent_changelist = translate_generic_relchange(change, populated_story_node)
        case ChangeType.TAGCHANGE:
            equivalent_changelist = translate_generic_tagchange(change, populated_story_node)
        case ChangeType.RELATIVETAGCHANGE:
            equivalent_changelist = translate_generic_relative_tagchange(change, populated_story_node)
        case ChangeType.RELATIVEBIASCHANGE:
            equivalent_changelist = translate_generic_relative_biaschange(change, populated_story_node)
        case ChangeType.CONDCHANGE:
            equivalent_changelist = translate_generic_condchange(change, populated_story_node)
        case ChangeType.TASKCHANGE:
            equivalent_changelist = translate_generic_taskchange(change, populated_story_node)
        case ChangeType.TASKADVANCECHANGE:
            equivalent_changelist = translate_generic_taskadvance(change, populated_story_node)
        case ChangeType.TASKCANCELCHANGE:
            equivalent_changelist = translate_generic_taskcancel(change, populated_story_node)
        case _:
            equivalent_changelist = [change]

    return equivalent_changelist

def translate_generic_relchange(relchange, populated_story_node):
    lhs_list = check_keyword_and_return_objectnodelist(populated_story_node, relchange.node_a)
    rhs_list = check_keyword_and_return_objectnodelist(populated_story_node, relchange.node_b)

    list_of_equivalent_relchanges = []

    for lhs_item in lhs_list:
        for rhs_item in rhs_list:
            newchange = RelChange(name = relchange.name, node_a=lhs_item, edge_name=relchange.edge_name, node_b=rhs_item, value=relchange.value, add_or_remove=relchange.add_or_remove, soft_equal=relchange.soft_equal)
            list_of_equivalent_relchanges.append(newchange)

    return list_of_equivalent_relchanges

def translate_generic_tagchange(tagchange, populated_story_node):
    list_of_equivalent_tagchanges = []

    objectlist = check_keyword_and_return_objectnodelist(populated_story_node, tagchange.object_node_name)

    for item in objectlist:
        if issubclass(type(item), ObjectNode):
            list_of_equivalent_tagchanges.append(TagChange(name=tagchange.name, object_node_name=item.name, tag=tagchange.tag, value=tagchange.value, add_or_remove=tagchange.add_or_remove))
        else:
            list_of_equivalent_tagchanges.append(TagChange(name=tagchange.name, object_node_name=item, tag=tagchange.tag, value=tagchange.value, add_or_remove=tagchange.add_or_remove))

    return list_of_equivalent_tagchanges

def translate_generic_relative_tagchange(tagchange, populated_story_node):
    list_of_equivalent_tagchanges = []

    objectlist = check_keyword_and_return_objectnodelist(populated_story_node, tagchange.object_node_name)

    for item in objectlist:
        if issubclass(type(item), ObjectNode):
            list_of_equivalent_tagchanges.append(RelativeTagChange(name=tagchange.name, object_node_name=item.name, tag=tagchange.tag, value_delta=tagchange.value_delta))
        else:
            list_of_equivalent_tagchanges.append(RelativeTagChange(name=tagchange.name, object_node_name=item, tag=tagchange.tag, value_delta=tagchange.value_delta))

    return list_of_equivalent_tagchanges

def translate_generic_relative_biaschange(biaschange, populated_story_node):
    list_of_equivalent_biaschange = []

    objectlist = check_keyword_and_return_objectnodelist(populated_story_node, biaschange.object_node_name)

    for item in objectlist:
        if issubclass(type(item), ObjectNode):
            list_of_equivalent_biaschange.append(RelativeBiasChange(name=biaschange.name, object_node_name=item.name, bias=biaschange.bias, biasvalue_delta=biaschange.biasvalue_delta))
        else:
            list_of_equivalent_biaschange.append(RelativeBiasChange(name=biaschange.name, object_node_name=item, bias=biaschange.bias, biasvalue_delta=biaschange.biasvalue_delta))

    return list_of_equivalent_biaschange


def translate_generic_condchange(change, populated_story_node):
    equivalent_tests = []
    equivalent_changes = []

    for test in change.list_of_condition_tests:
        equivalent_tests.extend(translate_generic_test(test, populated_story_node))

    for subchange in change.list_of_changes:
        equivalent_changes.extend(translate_generic_change(subchange, populated_story_node))

    return ConditionalChange(name=change.name, list_of_condition_tests=equivalent_tests, list_of_changes=equivalent_changes)

def translate_generic_taskchange(change, populated_story_node):

    equivalent_givers = check_keyword_and_return_objectnodelist(storynode=populated_story_node, objnode_to_check=change.task_giver_name)
    equivalent_owners = check_keyword_and_return_objectnodelist(storynode=populated_story_node, objnode_to_check=change.task_owner_name)

    equivalent_changes = []
    for giver_name in equivalent_givers:
        for owner_name in equivalent_owners:

            giver_name_adjusted = giver_name
            owner_name_adjusted = owner_name

            if issubclass(type(giver_name_adjusted), ObjectNode):
                giver_name_adjusted = giver_name.get_name()

            if issubclass(type(owner_name_adjusted), ObjectNode):
                owner_name_adjusted = owner_name.get_name()

            equivalent_changes.append(TaskChange(name=change.name, task_giver_name=giver_name_adjusted, task_owner_name=owner_name_adjusted, task_stack=change.task_stack))

    return equivalent_changes

def translate_generic_taskadvance(change, populated_story_node):

    equivalent_actors = check_keyword_and_return_objectnodelist(storynode=populated_story_node, objnode_to_check=change.actor_name)

    equivalent_changes = []
    for item_name in equivalent_actors:

        item_name_adjusted = item_name
        if issubclass(type(item_name_adjusted), ObjectNode):
            item_name_adjusted = item_name.get_name()

        equivalent_changes.append(TaskAdvance(name=change.name, actor_name=item_name_adjusted, task_stack_name=change.task_stack_name))

    return equivalent_changes

def translate_generic_taskcancel(change, populated_story_node):

    equivalent_actors = check_keyword_and_return_objectnodelist(storynode=populated_story_node, objnode_to_check=change.actor_name)

    equivalent_changes = []
    for item_name in equivalent_actors:

        item_name_adjusted = item_name
        if issubclass(type(item_name_adjusted), ObjectNode):
            item_name_adjusted = item_name.get_name()

        equivalent_changes.append(TaskCancel(name=change.name, actor_name=item_name_adjusted, task_stack_name=change.task_stack_name))

    return equivalent_changes

def check_keyword_and_return_objectnodelist(storynode, objnode_to_check):
    return_list = []

    match objnode_to_check:
        case GenericObjectNode.GENERIC_ACTOR:
            if storynode.actor is not None:
                if len(storynode.actor) > 0:
                    return_list.append(storynode.actor[0])
        case GenericObjectNode.GENERIC_LOCATION:
            return_list.append(storynode.location)
        case GenericObjectNode.GENERIC_TARGET:
            return_list.extend(storynode.target)
        case GenericObjectNode.ALL_ACTORS:
            return_list.extend(storynode.actor)
        case _:
            return_list.append(objnode_to_check)

    return return_list

#We'll use this to translate tests with generic tags instead of node here
#Since it cycles between all of the valid objects, whenever a slot is unassigned the tests don't show up. We can use this to our advantage.
def translate_generic_test(condtest, populated_story_node):

    list_of_equivalent_condtests = []

    match condtest.test_type:
        case TestType.HELD_ITEM_TAG:
            list_of_equivalent_condtests = translate_generic_held_item_test(test=condtest, node=populated_story_node)
        case TestType.SAME_LOCATION:
            list_of_equivalent_condtests = translate_generic_same_location_test(test=condtest, node=populated_story_node)
        case TestType.HAS_EDGE:
            list_of_equivalent_condtests = translate_generic_has_edge_test(test=condtest, node=populated_story_node)
        case TestType.HAS_TAG:
            list_of_equivalent_condtests = translate_has_tag_test(test=condtest, node=populated_story_node)
        case TestType.IN_BIAS_RANGE:
            list_of_equivalent_condtests = translate_in_bias_range_test(test=condtest, node=populated_story_node)
        case TestType.INTERSECTED_OBJECT_EXISTS:
            list_of_equivalent_condtests = translate_intersect_object_test(test=condtest, node=populated_story_node)
        # case TestType.HAS_DOUBLE_EDGE:
        #     list_of_equivalent_condtests = translate_generic_has_doubleedge_test(condtest, populated_story_node)
        case _:
            list_of_equivalent_condtests = [condtest]
        
    return list_of_equivalent_condtests

def translate_generic_held_item_test(test, node):

    list_of_equivalent_tests = []

    objectlist = check_keyword_and_return_objectnodelist(node, test.holder_to_test)

    for item in objectlist:
        list_of_equivalent_tests.append(HeldItemTagTest(item, test.tag_to_test, test.value_to_test, inverse=test.inverse, soft_equal=test.soft_equal, score=test.score))

    return list_of_equivalent_tests

def translate_generic_same_location_test(test, node):

    objectlist = []

    for item in test.list_to_test:
        objectlist.extend(check_keyword_and_return_objectnodelist(node, item))

    return [SameLocationTest(objectlist, inverse=test.inverse, score=test.score)]

def translate_generic_has_edge_test(test, node):

    list_of_equivalent_tests = []

    from_node = check_keyword_and_return_objectnodelist(node, test.object_from_test)
    to_node = check_keyword_and_return_objectnodelist(node, test.object_to_test)

    for lhs_item in from_node:
        for rhs_item in to_node:
            list_of_equivalent_tests.append(HasEdgeTest(lhs_item, test.edge_name_test, rhs_item, value_test=test.value_test, soft_equal=test.soft_equal, two_way=test.two_way, inverse=test.inverse, score=test.score))    

    return list_of_equivalent_tests

def translate_has_tag_test(test, node):

    list_of_equivalent_tests = []

    object_list = check_keyword_and_return_objectnodelist(storynode=node, objnode_to_check=test.object_to_test)

    for item in object_list:
        list_of_equivalent_tests.append(HasTagTest(object_to_test=item, tag=test.tag, value=test.value, soft_equal=test.soft_equal, inverse=test.inverse, score=test.score))

    return list_of_equivalent_tests

def translate_in_bias_range_test(test, node):

    list_of_equivalent_tests = []

    object_list = check_keyword_and_return_objectnodelist(storynode=node, objnode_to_check=test.object_to_test)

    for item in object_list:
        list_of_equivalent_tests.append(InBiasRangeTest(object_to_test=item, bias_axis=test.bias_axis, min_accept=test.min_accept, max_accept=test.max_accept, inverse=test.inverse, score=test.score))

    return list_of_equivalent_tests
def translate_intersect_object_test(test, node):

    equivalent_tests = []
    for test in test.list_of_tests_with_placeholder:
        equivalent_tests.extend(translate_generic_test(condtest=test, populated_story_node=node))

    return [IntersectObjectExistsTest(list_of_tests_with_placeholder=equivalent_tests, inverse=test.inverse, score=test.score)]

def translate_one_test_test(test, node):

    list_of_all_tests = []
    object_list = check_keyword_and_return_objectnodelist(storynode=node, objnode_to_check=test.object_to_test)

    for object_eq in object_list:

        equivalent_tests = []
        
        for test in test.list_of_tests_with_placeholder:
            equivalent_tests.extend(translate_generic_test(condtest=test, populated_story_node=node))

        list_of_all_tests.append(ObjectPassesAtLeastOneTestTest(list_of_tests_with_placeholder=equivalent_tests, object_to_test=object_eq))

    return list_of_all_tests

def get_actor_object_from_list_with_actor_name(actor_name:str, actor_list=[]):

    for actor in actor_list:
        if actor.get_name() == actor_name:
            return actor
        
    return None

def replace_pair_value_with_actual_actors(kv_pair_list=[], actor_list=[]):
    return_list = []

    for kv_pair in kv_pair_list:
        new_val = get_actor_object_from_list_with_actor_name(actor_name=kv_pair[1], actor_list=actor_list)
        if new_val != None:
            return_list.append((kv_pair[0], new_val))
        else:
            return_list.append(kv_pair)
    return return_list


# def translate_generic_has_doubleedge_test(test, node):
    
#     list_of_equivalent_tests = []

#     from_node = check_keyword_and_return_objectnodelist(node, test.object_from_test)
#     to_node = check_keyword_and_return_objectnodelist(node, test.object_to_test)

#     for lhs_item in from_node:
#         for rhs_item in to_node:
#             list_of_equivalent_tests.append(HasDoubleEdgeTest(lhs_item, test.edge_name_test, rhs_item, value_test=test.value_test, soft_equal=test.soft_equal, inverse=test.inverse))    

#     return list_of_equivalent_tests