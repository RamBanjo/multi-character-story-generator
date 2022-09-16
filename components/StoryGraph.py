from operator import truediv
import random
from time import time
from numpy import empty
from components.StoryNode import *
from components.StoryObjects import *
from copy import deepcopy

'''
Storygraph!

The story graph contains the following things:

In this version we will attempt to cut out the middleman and directly put the list of worldstates and list of nodes into the StoryGraph directly!

For StoryNodes, they will be kept in a dict. The key will be a tuple that consists of the character's name and the timestep number.
For example:
("Alice", 0) -> Alice finds a sword
("Bob", 0) -> Bob eats a sandwich
("Alice", 1) -> Alice goes to the bar
("Bob", 1) -> Bob goes to the bar
("Alice", 2) -> Alice talks with Bob
("Bob", 2) - > Alice talks with Bob

When a replacement is made for a character, it will check for all the entries with that character's name.
If a match is found, then a replacement can be made.

This replacement will be done by changing what each tuples point to.

("Alice", 0) -> a
("Alice", 1) -> b
("Alice", 2) -> c

If we use a rule that replaces b with d, e on Alice's storyline the entries will be changed like this:

("Alice", 0) -> a
("Alice", 1) -> d
("Alice", 2) -> e
("Alice", 3) -> c

For WorldStates, they will be kept in a list. Replacing the worldstate would be as easy as duplicating the worldstates from the rule and
replacing it in the list. (Since we don't have to care about connections between world states here, this should be possible!)

TODO: Rewrite this class entirely (all the functions) so that they can handle multiple events in one timestep
'''
class StoryGraph:
    def __init__(self, name, character_objects, location_objects):
        self.name = name
        self.world_states = []
        self.character_objects = character_objects
        self.location_objects = location_objects
        self.story_parts = dict()
        self.longest_path_length = 0

    #Copy=False would be used in the case of joint.

    #TODO: Add an option that allows the user to start at another point other than 0.
    #Possible: Create blank nodes in order to keep all the nodes equal?
    def add_story_part(self, part, character, location, timestep, copy=True, targets=[]):

        char_name = None

        if character is not None:
            char_name = character.get_name()
        
        #first we need to get the last entry in this character's story
        character_path_length = self.get_longest_path_length_by_character(character)

        new_part = self.add_story_part_at_step(part, character, location, character_path_length, timestep, copy, targets)

        for target in targets:
            new_part.add_target(target)

        if character_path_length > 0:
            self.story_parts[(char_name, character_path_length-1)].add_next_node(new_part, character)

        return new_part

    def add_story_part_at_step(self, part, character, location, absolute_step, timestep, copy=True, targets=[]):

        char_name = None

        if character is not None:
            char_name = character.get_name()

        if copy:
            new_part = deepcopy(part)
        else:
            new_part = part

        self.story_parts[(char_name, absolute_step)] = new_part

        #print(character.name, "added to", part.name)
        new_part.add_actor(character)
        new_part.timestep = timestep
        new_part.abs_step = absolute_step

        if location is not None:
            new_part.set_location(location)

        for target in targets:
            new_part.add_target(target)

        return new_part

    def remove_story_part(self, character, absolute_step):

        char_name = None

        if character is not None:
            char_name = character.get_name()

        removed = self.story_parts.pop((char_name, absolute_step), None)

        if removed is not None:

            current_longest = self.get_longest_path_length_by_character(character)

            prevnode = None
            nextnode = None

            #if there is a previous node, remove references to this node
            if absolute_step-1 >= 0:
                prevnode = self.story_parts[(char_name, absolute_step-1)]
                prevnode.remove_next_node(character)
            
            #if the removed thing is not the last thing, then we need to move stuff down
            if absolute_step < current_longest:

                nextnode = self.story_parts[(char_name, absolute_step+1)]

                for i in range(absolute_step+1, current_longest+1):
                
                    move_down = self.story_parts.pop((char_name, i))
                    self.story_parts[(char_name, i-1)] = move_down

            #finally, if both conditions are met, then those two must be connected
            if prevnode is not None and nextnode is not None:
                prevnode.add_next_node(nextnode, character)

    def insert_story_part(self, part, character, location, absolute_step, copy=True, targets=[]):
        #check if this would be the last storypart in the list, if it is, then call add story part like normal
        #TODO: Also need to check whether this story part 
        char_name = None

        if character is not None:
            char_name = character.get_name()

        if self.story_parts.get((char_name, absolute_step-1), None) is None:
            timestep = 0
        else:
            timestep = self.story_parts[(char_name, absolute_step-1)].timestep

        character_path_length = self.get_longest_path_length_by_character(character)

        if absolute_step >= character_path_length:
            self.add_story_part(part, character, location, timestep, copy)
        else:
            #first, we need to move everything that comes after this part up by one
            for i in range(character_path_length-1, absolute_step-1, -1):
                move_up = self.story_parts.pop((char_name, i))
                self.story_parts[(char_name, i+1)] = move_up

            #then, we add a new story part at the spot
            new_part = self.add_story_part_at_step(part, character, location, absolute_step, timestep, copy)

            #we also add the targets here
            for target in targets:
                new_part.add_target(target)

            #finally, connect this to other nodes
            #the node that comes after,
            new_part.add_next_node(self.story_parts[(char_name, absolute_step+1)], character)

            #and the node that comes before if it's not inserted as first node

            if absolute_step-1 >= 0:
                prevnode =  self.story_parts[(char_name, absolute_step-1)]
                prevnode.remove_next_node(character)
                prevnode.add_next_node(new_part, character)

    def replace_story_parts(self, character, start_time_abs, end_time_abs, list_of_storynode_and_location_and_target_tuples):

        #First, record the start time. That is where the nodes will be inserted

        #Then, remove everything from start time to end time. That's a lot
        for remove_index in range(start_time_abs, end_time_abs+1):
            self.remove_story_part(character, start_time_abs)


        insert_index = start_time_abs
        #Finally, insert everything at start time (increment each by 1), with the character's name attached. Neat!  
        #Also, if doing this causes the entire story graph to be empty, then there is no need to call insert story part, just call add story part lol

        if self.get_longest_path_length_by_character(character) <= 0:
            for story_loc_tuple in list_of_storynode_and_location_and_target_tuples:
                if(len(story_loc_tuple[2]) > 0):
                    self.add_story_part(story_loc_tuple[0], character, story_loc_tuple[1], insert_index, copy=True, targets=story_loc_tuple[2])
                else:
                    self.add_story_part(story_loc_tuple[0], character, story_loc_tuple[1], insert_index, copy=True)
                insert_index += 1
        else:
            for story_loc_tuple in list_of_storynode_and_location_and_target_tuples:
                if(len(story_loc_tuple[2]) > 0):
                    self.insert_story_part(story_loc_tuple[0], character, story_loc_tuple[1], insert_index, targets=story_loc_tuple[2])
                else:
                    self.insert_story_part(story_loc_tuple[0], character, story_loc_tuple[1], insert_index)
                insert_index += 1

        

    def refresh_longest_path_length(self):
        longest = 0

        for character in self.character_objects:
            character_path_length = self.get_longest_path_length_by_character(character)
            if character_path_length > longest:
                longest = character_path_length

        self.longest_path_length = longest
    
    def get_longest_path_length_by_character(self, character):
        
        name = None
        
        if character is not None:
            name = character.get_name()

        i = 0

        for node in self.story_parts:
            if node[0] is name:
                i += 1

        return i

        '''current_part = self.story_parts.get((name, i), False)

        if current_part:
            while(current_part):
                i += 1
                current_part = self.story_parts.get((name, i), False)
            return i
        else:
            return 0'''

    def add_world_state(self, new_state):
        self.world_states.append(new_state)

    def remove_world_state(self, index):
        self.world_states.pop(index)

    def insert_world_state(self, new_state, index):
        self.world_states.insert(index, new_state)

    def replace_world_states(self, start_index, end_index, list_of_world_states):
        list_start = self.world_states[:start_index]
        list_end = self.world_states[end_index+1:]
        new_world_state_list = list_start + list_of_world_states + list_end
        self.world_states = new_world_state_list

    def clone_world_state(self, index):
        new_ws = deepcopy(self.world_states[index])
        self.insert_world_state(new_ws, index+1)
        return new_ws
    

    def apply_rewrite_rule(self, rule, character, location_list, targets_requirement_list=[], target_replacement_list=[], applyonce=False, banned_subgraph_locs=[]):
        #Check for that specific character's storyline
        #Check if Rule applies (by checking if the rule is a subgraph of this graph)

        is_subgraph, subgraph_locs = StoryGraph.is_subgraph(rule.story_condition, self, rule.dummychar, character, targets_requirement_list)

        for banned_loc in banned_subgraph_locs:
            subgraph_locs.remove(banned_loc)

        if is_subgraph:
            #If yes to both, do a replacement
            #Get all instances and replace all of them if ApplyOnce is false
            #If ApplyOnce is true, then replace only one random instance
            print("Rule is subgraph of Self, replacing storyline")

            if not applyonce:
                print("applyonce is false, replacing all instances of this rule")
            else:
                print("applyonce is true, one random instance will be replaced")
                subgraph_locs = [random.choice(subgraph_locs)]

            rule_length = rule.story_change.get_longest_path_length_by_character(rule.dummychar)

            part_and_loc_tuple_list = []

            for i in range(0, rule_length):
                new_part = deepcopy(rule.story_change.story_parts[(rule.dummychar.get_name(), i)])
                new_part.remove_actor(rule.dummychar)

                #TODO: Add the target into this tuple
                new_part_and_loc_and_tar_tuple = (new_part, location_list[i], target_replacement_list[i])
                part_and_loc_tuple_list.append(new_part_and_loc_and_tar_tuple)
            
            for start_index in subgraph_locs:
                end_index = start_index + rule_length - 1
                #self.replace_world_states(start_index, end_index, rule.story_change.world_states)
                self.replace_story_parts(character, start_index, end_index, part_and_loc_tuple_list)
                
        else:
            print("Nothing is replaced: Rule is not subgraph of Self")

    def apply_joint_node (self, joint_node, character_list, location, absolute_step):
        new_joint = deepcopy(joint_node)
        new_joint.remove_all_actors()

        self.insert_story_part(new_joint, character_list[0], location, absolute_step, copy=False)

        for other_char_index in range(1, len(character_list)):
            self.insert_story_part(new_joint, character_list[other_char_index], location, absolute_step, copy=False)

        return new_joint


    '''
    This function is for making the character's next node some node that already exists in another character's path.

    It probably should also check for time paradoxes (to be defined)

    Alright, to prevent time paradoxes, we will not allow joining into any nodes where the timestep numbers are different.

    Lol as it turns out this retains the same wording but now has a different meaning, thanks to the new way to handle timesteps (lol)

    There should be three of these, one for each type of Joint Rule.
    '''

    def apply_joint_rule(self, joint_rule, characters, location_list, applyonce=False, target_require=[], target_replace=[], character_grouping=[]):

        if joint_rule.joint_type == "joining":
            self.apply_joining_joint_rule(joint_rule, characters, location_list, applyonce, target_require=target_require, target_replace=target_replace)
        if joint_rule.joint_type == "continuous":
            self.apply_continuous_joint_rule(joint_rule, characters, location_list, applyonce, target_require=target_require, target_replace=target_replace)
        if joint_rule.joint_type == "splitting":
            self.apply_splitting_joint_rule(joint_rule, characters, location_list, character_grouping=character_grouping, applyonce=applyonce)
    
    #If you figure out one, you figure out all three
    def apply_joining_joint_rule(self, join_rule, characters, location, applyonce=False, target_require=[], target_replace=[]):

        eligible_insertion_list = []

        for i in range(0, self.get_longest_path_length_by_character(characters[0])):

            current_index_eligible = False

            #First, check for the length of the first character's path
            #Check if any nodes that character perform is the same as the first node in the join rule's requirement
            current_first_char_node = self.story_parts.get((characters[0].name, i), None)
            if current_first_char_node.get_name() == join_rule.base_actions[0].get_name():

                current_index_eligible = True

                if len(target_require) > 0:
                    for target in target_require[0]:
                        current_index_eligible = current_index_eligible and target in current_first_char_node.target

                #If it is, check nodes performed by the 2nd character (and beyond) within the same absolute step to see if it's the same as
                #the required node
                for other_char_index in range(1, len(characters)):
                    current_chars_node = self.story_parts.get((characters[other_char_index].name, other_char_index), None)
                    current_index_eligible = current_index_eligible and current_chars_node.get_name() == join_rule.base_actions[other_char_index].get_name()
                    if len(target_require) > 0:
                        for target in target_require[other_char_index]:
                            current_index_eligible = current_index_eligible and target in current_chars_node.target
                
                #Add to list if true
                if current_index_eligible:
                    eligible_insertion_list.append(i+1)

        #After all the nodes are checked, check if The List is empty. If it is, nothing happens.
        #If there is something in The List, then apply the rule and append the Joint Story Node.
        if len(eligible_insertion_list) > 0:
            
            #If Apply Once is False, then all the instances in The List gets applied.
            #Otherwise, a random instance is applied to.
            if applyonce:
                eligible_insertion_list = [random.choice(eligible_insertion_list)]

        #Applying here is inserting the next node to be the Joint Node for the first character, then having the second character and so on Join in.
        #This is where the copy=false in the add node function comes in handy.
        for insert_loc in eligible_insertion_list:
            new_joint = self.apply_joint_node(join_rule.joint_node, characters, location, insert_loc)

            if len(target_replace) > 0:
                for target in target_replace:
                    new_joint.add_target(target)

    def apply_continuous_joint_rule(self, cont_rule, characters, location, applyonce=False, target_require=[], target_replace=[]):
        eligible_insertion_list = []

        for i in range(0, self.get_longest_path_length_by_character(characters[0])):

            current_index_eligible = False

            #First, check for the length of the first character's path
            #Check if any nodes that character perform is the same as the first node in the join rule's requirement
            current_first_char_node = self.story_parts.get((characters[0].name, i), None)
            if current_first_char_node.get_name() == cont_rule.base_joint.get_name():
                current_index_eligible = True

                if len(target_require) > 0:
                    for target in target_require:
                        current_index_eligible = current_index_eligible and target in current_first_char_node.target

                #If it is, check nodes performed by the 2nd character (and beyond) within the same absolute step to see if they are in the joint node
                for other_char_index in range(1, len(characters)):

                    current_index_eligible = current_index_eligible and characters[other_char_index] in current_first_char_node.actor
                
                #Add to list if true
                if current_index_eligible:
                    eligible_insertion_list.append(i+1)

        #After all the nodes are checked, check if The List is empty. If it is, nothing happens.
        #If there is something in The List, then apply the rule and append the Joint Story Node.
        if len(eligible_insertion_list) > 0:
            
            #If Apply Once is False, then all the instances in The List gets applied.
            #Otherwise, a random instance is applied to.
            if applyonce:
                eligible_insertion_list = [random.choice(eligible_insertion_list)]

        #Applying here is inserting the next node to be the Joint Node for the first character, then having the second character and so on Join in.
        #This is where the copy=false in the add node function comes in handy.
        for insert_loc in eligible_insertion_list:
            new_joint = self.apply_joint_node(cont_rule.joint_node, characters, location, insert_loc)

            if len(target_replace) > 0:
                for target in target_replace:
                    new_joint.add_target(target)


    def apply_splitting_joint_rule(self, split_rule, characters, location_list, character_grouping=[], applyonce=False, target_require=[], target_replace=[]):
        eligible_insertion_list = []

        for i in range(0, self.get_longest_path_length_by_character(characters[0])):

            current_index_eligible = False

            #First, check for the length of the first character's path
            #Check if any nodes that character perform is the same as the first node in the join rule's requirement
            current_first_char_node = self.story_parts.get((characters[0].name, i), None)
            if current_first_char_node.get_name() == split_rule.base_joint.get_name():
                current_index_eligible = True

                if len(target_require) > 0:
                    for target in target_require:
                        current_index_eligible = current_index_eligible and target in current_first_char_node.target

                #If it is, check nodes performed by the 2nd character (and beyond) within the same absolute step to see if they are in the joint node
                for other_char_index in range(1, len(characters)):
                    current_index_eligible = current_index_eligible and characters[other_char_index] in current_first_char_node.actor
                
                #Add to list if true
                if current_index_eligible:
                    eligible_insertion_list.append(i+1)

        #After all the nodes are checked, check if The List is empty. If it is, nothing happens.
        #If there is something in The List, then apply the rule and append the Joint Story Node.
        if len(eligible_insertion_list) > 0:
            
            #If Apply Once is False, then all the instances in The List gets applied.
            #Otherwise, a random instance is applied to.
            if applyonce:
                eligible_insertion_list = [random.choice(eligible_insertion_list)]

        #Applying here is inserting the next nodes for each character in the node, splitting the characters apart. If working with more than 2 characters,
        #It might be possible to split

        if len(character_grouping) > 0:
            for insert_loc in eligible_insertion_list:
                for i in range(0, len(character_grouping)):
                    new_joint = deepcopy(split_rule.split_list[i])
                    new_joint.remove_all_actors()
                    added_joint = self.apply_joint_node(new_joint, character_grouping[i], location_list[i], insert_loc)

                    if len(target_replace) > 0:
                        for target in target_replace[i]:
                            added_joint.add_target(target)
        else:
            for insert_loc in eligible_insertion_list:
                for i in range(0, len(characters)):
                    new_joint = deepcopy(split_rule.split_list[i])
                    new_joint.remove_all_actors()
                    added_joint = self.insert_story_part(new_joint, characters[i], location_list[i], insert_loc)   

                    if len(target_replace) > 0:
                        for target in target_replace[i]:
                            added_joint.add_target(target)


    def print_all_nodes(self):
        for node in self.story_parts:
            print(node)

    def print_all_node_values(self):
        for node in self.story_parts.values():
            print(node)

    def print_all_node_beautiful_format(self):
        print("LIST OF NODES")
        for node in self.story_parts:
            print(node)
            print("Node Name:", self.story_parts[node].get_name())
            print("Timestep", self.story_parts[node].timestep)
            print("Actors:", self.story_parts[node].get_actor_names())
            print("Targets:", self.story_parts[node].get_target_names())
            print("----------")
        
    '''
    A story graph is considered to be a subgraph of another storygraph when:
    1) There exists a sequence of timesteps that contains similar nodes
    2) Each of the node mentioned must be performed by the same character

    Oh also. I want this function to return the starting points of each subgraph

    ToDo: Fix this Subgraph Function

    def is_subgraph(self, other_graph, character):

        list_of_subgraph_locs = []

        #First of all, this graph can't be the other graph's subgraph if it has more timesteps than the other graph
        if self.get_longest_path_length_by_character(character) > other_graph.get_longest_path_length_by_character(character):
            return False, list_of_subgraph_locs

        #Second of all, check each timestep to see if the timestep is in fact a sub timestep of the othergraph's timestep
        #If there are less timesteps remaining in the other graph than there are timesteps in this graph then it can't be subset 
        for x in range(0, other_graph.get_longest_path_length_by_character(character) - self.get_longest_path_length_by_character(character) + 1):

            result = True

            #Check all the timesteps of this graph to see if it's contained within the other timestep
            for y in range(0, self.get_longest_path_length_by_character(character)):

                #For each of the timestep in this graph, we check if the steps the character (this one in specific) take are the same.
                result = result and self.story_parts[(character.get_name(), x+y)] == other_graph.story_parts[(character.get_name(), y)]

                #We also check if the world state is a subset.
                result = result and self.world_states[x+y].is_subgraph(other_graph.world_states[y])

                if result:
                    list_of_subgraph_locs.append(x)


        #If list is empty then it's false. If list is not empty then it's true. Then also return that list.
        return len(list_of_subgraph_locs) > 0, list_of_subgraph_locs

    '''
    
    '''def is_subgraph(self, other_graph, character, self_none = False):

        list_of_subgraph_locs = []

        self_char = None
        self_charname = None

        if not self_none:
            self_char = character
            self_charname = character.get_name()

        #First of all, this graph can't be the other graph's subgraph if it has more timesteps than the other graph
        if self.get_longest_path_length_by_character(self_char) > other_graph.get_longest_path_length_by_character(character):
            return False, list_of_subgraph_locs

        #Second of all, check each timestep to see if the timestep is in fact a sub timestep of the othergraph's timestep
        #If there are less timesteps remaining in the other graph than there are timesteps in this graph then it can't be subset 
        for x in range(0, other_graph.get_longest_path_length_by_character(character) - self.get_longest_path_length_by_character(self_char) + 1):

            result = True

            #Check all the timesteps of this graph to see if it's contained within the other timestep
            for y in range(0, self.get_longest_path_length_by_character(self_char)):
                print(y)
                #For each of the timestep in this graph, we check if the steps the character (this one in specific) take are the same.

                this_part_here = self.story_parts[(self_charname, y)].get_name()
                other_part_here = other_graph.story_parts[(character.get_name(), x+y)].get_name()

                print(this_part_here)
                print(other_part_here)

                result = result and this_part_here == other_part_here

                #We also check if the world state is a subset.
                result = result and self.world_states[y].is_subgraph(other_graph.world_states[x+y])

            if result:
                list_of_subgraph_locs.append(x)

        #If list is empty then it's false. If list is not empty then it's true. Then also return that list.
        return len(list_of_subgraph_locs) > 0, list_of_subgraph_locs'''

    '''
    TODO: List of Subgraph Locs should exclude parts of subgraph that overlaps two different timesteps
    '''
    def is_subgraph(subgraph, supergraph, subgraph_char, supergraph_char, targets_list=[]):

        #Since we only care if a certain character's storyline is a subgraph of another character's storyline
        #We will do this
        subdict = deepcopy(subgraph.story_parts)
        superdict = deepcopy(supergraph.story_parts)

        subset = dict()
        superset = dict()
        supertimestepdict = dict()
        supertargetsdict = dict()

        for key in subdict:
            if key[0] == subgraph_char.get_name():
                subset[key[1]] = subdict[key].get_name()
        for key in superdict:
            if key[0] == supergraph_char.get_name():
                superset[key[1]] = superdict[key].get_name()
                supertimestepdict[key[1]] = superdict[key].timestep
                supertargetsdict[key[1]] = tuple(sorted(superdict[key].target))

        list_of_subgraph_locs = []

        #First of all, this graph can't be the other graph's subgraph if it has more timesteps than the other graph
        if len(subset) > len(superset):
            return False, list_of_subgraph_locs

        for super_i in range(0, len(superset) - len(subset) + 1):

            result = True

            timesteps_of_superset = []

            for sub_i in range(0, len(subset)):
                
                #For each of the node in this graph, we check if the steps the character (this one in specific) take are the same.
                result = result and subset[sub_i] == superset[super_i + sub_i]

                #Additionally, if targets_list isn't empty, then we also need to check the superset's targets to see if they line up with the list of targets.
                if len(targets_list) > 0:
                    result = result and supertargetsdict[super_i + sub_i] == tuple(sorted(targets_list[sub_i]))
                
                #NEED ANOTHER WAY TO CHECK WORLDSTATES

                #WORLDSTATE Will no longer be tied to StoryGraph's subgraph

                #Instead, new timesteps will be generated by taking into account all the events that happened in the previous timesteps.

                #Therefore, we're going to need the following rules in the story nodes:
                #Change in Next Timestep:
                #If this node is included in this timestep, how will it change the next timestep?

                #We also check if the world state is a subset.
                #result = result and subgraph.world_states[sub_i].is_subgraph(supergraph.world_states[super_i + sub_i])

                #Add the timestep to the list of superset timesteps
                timesteps_of_superset.append(supertimestepdict[super_i+sub_i])
            
            
            #The subgraph loc will only be added if the supergraph steps are in the same timesteps
            if result and all(ele == timesteps_of_superset[0] for ele in timesteps_of_superset):
                list_of_subgraph_locs.append(super_i)

        return len(list_of_subgraph_locs) > 0, list_of_subgraph_locs

    


    