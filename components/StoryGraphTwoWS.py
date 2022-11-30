from operator import truediv
import random
from time import time
from numpy import empty
from components.ConditionTest import HasDoubleEdgeTest, HasEdgeTest, HeldItemTagTest, SameLocationTest
from components.RelChange import *
from components.StoryNode import *
from components.StoryObjects import *
from copy import deepcopy
from components.UtilityEnums import GenericObjectNode, TestType
from components.WorldState import WorldState

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

Only two world states will be kept: The starting world state and the worldstate of the latest world state.
'''
class StoryGraph:
    def __init__(self, name, character_objects, location_objects, starting_ws):
        self.name = name
        self.character_objects = character_objects
        self.location_objects = location_objects
        self.story_parts = dict()
        self.longest_path_length = 0
        self.starting_ws = starting_ws
        
        self.list_of_changes = []
        self.latest_ws = self.make_latest_state()

    def add_to_story_part_dict(self, character_name, abs_step, story_part):
        self.story_parts[(character_name, abs_step)] = story_part

    #Copy=False would be used in the case of joint.
    def add_story_part(self, part, character, location=None, timestep=0, copy=True, targets=[]):

        char_name = None

        if character is not None:
            char_name = character.get_name()
        
        #first we need to get the last entry in this character's story
        character_path_length = self.get_longest_path_length_by_character(character)

        new_part = self.add_story_part_at_step(part, character, location, character_path_length, timestep, copy, targets)

        if character_path_length > 0:
            self.story_parts[(char_name, character_path_length-1)].add_next_node(new_part, character)

        self.refresh_longest_path_length()

        return new_part

    def add_story_part_at_step(self, part, character, location=None, absolute_step=0, timestep=0, copy=True, targets=[]):

        char_name = None

        if character is not None:
            char_name = character.get_name()

        if copy:
            new_part = deepcopy(part)
        else:
            new_part = part

        self.add_to_story_part_dict(character_name=char_name, abs_step=absolute_step, story_part=new_part)

        #print(character.name, "added to", part.name)
        new_part.add_actor(character)
        new_part.timestep = timestep
        new_part.abs_step = absolute_step

        if location is not None:
            new_part.set_location(location)

        for target in targets:
            new_part.add_target(target)

        self.refresh_longest_path_length()

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

                    self.add_to_story_part_dict(character_name=char_name, abs_step=i-1, story_part=move_down)

            #finally, if both conditions are met, then those two must be connected
            if prevnode is not None and nextnode is not None:
                prevnode.add_next_node(nextnode, character)
        
        self.refresh_longest_path_length()

    def insert_story_part(self, part, character, location=None, absolute_step=0, copy=True, targets=[]):
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
                self.add_to_story_part_dict(character_name=char_name, abs_step=i+1, story_part=move_up)

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

        self.refresh_longest_path_length()

    def insert_multiple_parts(self, part_list, character, location_list=None, absolute_step=0, copy=True, targets=None):

        index = 0

        for item in part_list:

            cur_loc = None
            cur_tar = []

            if location_list != None:
                cur_loc = location_list[index]
            if targets != None:
                cur_tar = targets[index]

            self.insert_story_part(item, character, cur_loc, absolute_step+index, copy, cur_tar)

            index += 1

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

        self.refresh_longest_path_length()

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

    def make_latest_state(self, state_name = "Latest State"):
        #TODO: Take the initial world state and copy it.
        #TODO: Then, cycle through the list of changes, applying the changes from it.
        #TODO: returns the latest state

        return self.make_state_at_step(len(self.list_of_changes), state_name)

    def make_state_at_step(self, stopping_step, state_name = "Traveling State"):
        #TODO: Same as make_latest_state, but you can choose the step where to stop.
        #TODO: In fact, make_latest_state should call this function but set the stopping step as the last step.

        self.update_list_of_changes()

        traveling_state = deepcopy(self.starting_ws)
        traveling_state.name = state_name

        for index in range(0, stopping_step):
            for change in self.list_of_changes[index]:
                traveling_state.apply_some_change(change)
        
        return traveling_state

    def reverse_steps(self, number_of_reverse, state_name = "Reversed State"):
        #TODO: Returns a World State, reversing the changes for steps equal to number_of_reverse from the last state

        traveling_state = deepcopy(self.latest_ws)
        traveling_state.name = state_name

        for index in range(len(self.list_of_changes)-1, len(self.list_of_changes)-1-number_of_reverse, -1):
            for change in self.list_of_changes[index]:
                traveling_state.apply_some_change(change, reverse=True)


    #TODO: Redo this entire function. Since we no longer intend to include the Dummy Character
    #TODO: We also need to redo the is subgraph function in this case
    def apply_rewrite_rule(self, rule, character, location_list = None, applyonce=False, banned_subgraph_locs=[]):
        #Check for that specific character's storyline
        #Check if Rule applies (by checking if the rule is a subgraph of this graph)
        #Check if the rule that will be applied is a valid continuation in each of the subgraph loc

        is_subgraph, subgraph_locs = self.check_for_pattern_in_storyline(rule.story_condition, character)

        for banned_loc in banned_subgraph_locs:
            subgraph_locs.remove(banned_loc)

        #Here, we will check each loc in subgraph_locs to see if the continuation from that point on is valid.
        valid_insert_points = []
        for potential_insert_point in subgraph_locs:

            purge_count = 0

            if rule.remove_before_insert:
                purge_count = len(rule.story_condition)

            if self.check_continuation_validity(character, potential_insert_point, rule.story_change, rule.target_list, purge_count):
                valid_insert_points.append(potential_insert_point)

        if len(valid_insert_points) > 0:
            print("There is at least one valid insert point. Applying Rule.")
            subgraph_locs = if_applyonce_choose_one(subgraph_locs, applyonce)

            for change_location in subgraph_locs:
                if rule.remove_before_insert:

                    #Remove the parts
                    self.remove_parts_by_count(change_location, len(rule.story_condition), character)

                #add the right parts
                self.insert_multiple_parts(self.story_before_insert, character, location_list, change_location, copy=True, targets=rule.target_list)

        else:
            print("There are no valid insert points. Rule is not applied.")

        self.refresh_longest_path_length()

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

    #TODO: Redo all three of these, since we want to put all the target-related inputs in the story node itself
    #TODO: We should be able to add a special continuation validity that adds one joint node to multiple character's storylines
    #TODO: Remember, the joint continuity's location is based on the timesteps/abs step of the first character
    #TODO: Here's how the check should be done for each of the joint rule type, but basically the procedure is to try inserting into a copy of the graph without caring about restrictions and see if it still holds:
    #TODO: Apply Join Rule: insert the joint node after a select number of character's storylines (for example, if insert into A at 4, will also insert into B and C at 4)
    #TODO: Apply Cont Rule: just insert the joint node after a certain joint node, using it to continue the story of the characters there (ABC at 5 -> ABC at 6)
    #TODO: Apply Split Rule: insert the continuations for each of the character in a list, split them after joint node. (ABC at 6 -> A at 7, B at 7, C at 7)

    def check_joint_continuity_validity(self, joint_rule, actors_to_test, targets_to_test, insert_index):

        #First, we must check a few prerequisites. If any characters mentioned in actors_to_test don't exist in the storyline, then we definitely cannot continue the storyline.

        for testchar in actors_to_test:
            if testchar not in self.character_objects:
                return False
        
        validity = False
        
        if joint_rule.joint_type == "joining" or joint_rule.joint_type == "continuous":
            self.check_add_joint_validity(joint_rule.joint_node, actors_to_test, targets_to_test, insert_index)
        if joint_rule.joint_type == "splitting":
            self.check_add_split_validity(joint_rule.split_list, actors_to_test, targets_to_test, insert_index)
        
        return validity

    def check_add_joint_validity(self, joint_node, actors_to_test, targets_to_test, insert_index):

        graphcopy = deepcopy(self)
        graphcopy.joint_continuation([insert_index], True, joint_node, actors_to_test, None, targets_to_test)

        return graphcopy.check_worldstate_validity_on_own_graph(insert_index)
        
    def check_add_split_validity(self, split_list, actors_to_test, targets_to_test, insert_index, with_grouping = False):
        
        graphcopy = deepcopy(self)
        graphcopy.split_continuation(split_list, actors_to_test, insert_index, None, target_replace=targets_to_test, with_grouping=with_grouping)

        return graphcopy.check_worldstate_validity_on_own_graph(insert_index)

    def apply_joint_rule(self, joint_rule, characters, location_list, applyonce=False, target_require=[], target_replace=[], character_grouping=[]):

        if joint_rule.joint_type == "joining":
            self.apply_joining_joint_rule(joint_rule, characters, location_list, applyonce, target_require=target_require, target_replace=target_replace)
        if joint_rule.joint_type == "continuous":
            self.apply_continuous_joint_rule(joint_rule, characters, location_list, applyonce, target_require=target_require, target_replace=target_replace)
        if joint_rule.joint_type == "splitting":
            self.apply_splitting_joint_rule(joint_rule, characters, location_list, character_grouping=character_grouping, applyonce=applyonce)
        self.refresh_longest_path_length()
    

    def add_story_node_to_targets_storyline(self, pot_target, abs_step, story_part):
        if pot_target in self.character_objects:
            self.add_to_story_part_dict(character_name=pot_target.get_name(), abs_step=abs_step, story_part=story_part)

    def joint_continuation(self, loclist, applyonce, joint_node, actors, location, target_list):
        insert_list = if_applyonce_choose_one(loclist, applyonce)

        #Applying here is inserting the next node to be the Joint Node for the first character, then having the second character and so on Join in.
        #This is where the copy=false in the add node function comes in handy.
        for insert_loc in insert_list:
            new_joint = self.apply_joint_node(joint_node, actors, location, insert_loc)

            if len(target_list) > 0:
                self.add_targets_to_storynode(new_joint, insert_loc, target_list)

    def find_shared_base_joint_locations(self, character_list, rule, target_requirements):

        eligible_list = []

        for i in range(0, self.get_longest_path_length_by_character(character_list[0])):

            current_index_eligible = False

            #First, check for the length of the first character's path
            #Check if any nodes that character perform is the same as the first node in the join rule's requirement
            current_first_char_node = self.story_parts.get((character_list[0].name, i), None)
            if current_first_char_node.get_name() == rule.base_joint.get_name():
                current_index_eligible = True

                if len(target_requirements) > 0:
                    for target in target_requirements:
                        current_index_eligible = current_index_eligible and target in current_first_char_node.target

                #If it is, check nodes performed by the 2nd character (and beyond) within the same absolute step to see if they are also in the joint node
                for other_char_index in range(1, len(character_list)):

                    current_index_eligible = current_index_eligible and character_list[other_char_index] in current_first_char_node.actor
                
                #Add to list if true
                if current_index_eligible:
                    eligible_list.append(i+1)

        return eligible_list

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

        self.joint_continuation(eligible_insertion_list, applyonce, join_rule.joint_node, characters, location, target_replace)

    def apply_continuous_joint_rule(self, cont_rule, characters, location, applyonce=False, target_require=[], target_replace=[]):
        eligible_insertion_list = self.find_shared_base_joint_locations(characters, cont_rule, target_require)
        self.joint_continuation(eligible_insertion_list, applyonce, cont_rule.joint_node, characters, location, target_replace)

    #TODO: We don't have the character grouping YET. So we need a function to generate the grouping.

    def generate_valid_character_grouping(self, continuations, abs_step, character_list, grouping=[]):
        
        failed_groupings = []

        state_at_step = self.make_state_at_step(abs_step) #This is the state where we will check if the characters are compatible with each of their assigned nodes.

        found_valid_grouping = False

        while (not found_valid_grouping):

            unchosen_chars = []

            for charobj in character_list:
                unchosen_chars.append(state_at_step.node_dict[charobj.get_name()])

            current_grouping = []

            if len(grouping) > 0:
                #TODO: For the list of Grouping, we expect an array of the grouping. For example, [2,3] means that we want two groups, 2 members for the first group and 3 for the second group.

                for group_size in grouping:

                    new_group = random.sample(unchosen_chars, group_size)
                    current_grouping.append(new_group)

                    for remove_char in new_group:
                        unchosen_chars.remove(remove_char)

            else:
                #If grouping information is empty, then assume there are equal number of characters and nodes and randomly assign.
                for iteration in range(0, len(character_list)):
                
                    chosen_char = random.sample(unchosen_chars, 1)
                    current_grouping.append(chosen_char)

                    unchosen_chars.remove(chosen_char[0])
            this_one_is_valid = True

            if current_grouping not in failed_groupings: #Only check combinations that have not failed yet
                for story_index in range(0, len(continuations)):
                    this_one_is_valid = this_one_is_valid and continuations[story_index].check_character_compatibility_for_many_characters(current_grouping[story_index])
            else:
                this_one_is_valid = False #We will skip checking any combinations that we know have already failed

            if this_one_is_valid:
                found_valid_grouping = True
            else:
                failed_groupings.append(current_grouping)

        return current_grouping


    #TODO: Maybe decide upon the split grouping before calling split continuation
    def apply_splitting_joint_rule(self, split_rule, characters, location_list, character_grouping=[], applyonce=False, target_require=[], target_replace=[]):
        
        eligible_insertion_list = self.find_shared_base_joint_locations(characters, split_rule, target_require)
        eligible_insertion_list = if_applyonce_choose_one(eligible_insertion_list, applyonce)

        #Applying here is inserting the next nodes for each character in the node, splitting the characters apart. If working with more than 2 characters,
        #It might be possible to split

        if len(character_grouping) > 0:
            for insert_loc in eligible_insertion_list:
                 self.split_continuation(split_rule.split_list, character_grouping, insert_loc, location_list, target_replace, with_grouping=True)
        else:
            for insert_loc in eligible_insertion_list:
                self.split_continuation(split_rule.split_list, characters, insert_loc, location_list, target_replace, with_grouping=False)

    def split_continuation(self, split_list, chargroup_list, abs_step, location_list = None, target_replace = [], with_grouping = False):
        for i in range(0, len(chargroup_list)):
            new_joint = deepcopy(split_list)
            new_joint.remove_all_actors()

            if with_grouping and location_list != None:
                added_joint = self.apply_joint_node(new_joint, chargroup_list[i], location_list[i], abs_step)
            if with_grouping and location_list == None:
                added_joint = self.apply_joint_node(new_joint, chargroup_list[i], None, abs_step)
            if not with_grouping and location_list != None:
                added_joint = self.insert_story_part(new_joint, chargroup_list[i], location_list[i], abs_step)
            if not with_grouping and location_list == None:
                added_joint = self.insert_story_part(new_joint, chargroup_list[i], None, abs_step)

            if len(target_replace) > 0:
                self.add_targets_to_storynode(added_joint, abs_step, target_replace[i])

    def add_targets_to_storynode(self, node, abs_step, target_list):
        for target in target_list:
            node.add_target(target)
            #TODO: Check if any of the targets exist in self.characters. If there is one, then make sure to add this node to that character's StoryGraph in the same step.
            self.add_story_node_to_targets_storyline(target, abs_step, node)

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

    #TODO: Need to replace this function with a better, clearer one.
    #TODO: For example, instead of the following parameters, we need to use self instead
    #TODO: Maybe add new function to return a normal list of story parts or a dict of story parts given a character name
    #TODO: And then we translate the input from the rewrite rule (that will be a list) into a dict

    def check_for_pattern_in_storyline(self, pattern_to_test, character_to_extract):

        #preliminary check: check if the character exists inside of the storyline, return false if it does not
        if character_to_extract not in self.character_objects:
            return [], False
        
        #This will return the length of subgraph locs and the list of subgraph locs, just like the function above it.
        #The only difference is that we will require way, way less inputs.
        character_storyline = self.make_story_part_list_of_one_character(character_to_extract)

        list_of_subgraph_locs = []

        #The pattern can't exist in the storyline if it's longer than the storyline.
        if len(pattern_to_test) > len(character_storyline):
            return False, list_of_subgraph_locs

        #We will now cycle through the character's storyline.
        for super_index in range(0, len(character_storyline) - len(pattern_to_test) + 1):
            
            result = True

            timesteps_of_storyline = []

            for pattern_index in range(0, len(pattern_to_test)):

                #For each node in the graph, we check if the steps are the same.
                result = result and (pattern_to_test[pattern_index].get_name() == character_storyline[super_index + pattern_index].get_name())

                #We will no longer check the Target List, that is the responsibility of the Condition Test.

                #However, checking that the entire list shares the same timestep is still our responsibility.
                timesteps_of_storyline.append(character_storyline[super_index + pattern_index].timestep)

            #So we still need to check if all the elements have the same timestep.
            if result and all(ele == timesteps_of_storyline[0] for ele in timesteps_of_storyline):
                list_of_subgraph_locs.append(super_index)

        return len(list_of_subgraph_locs) >0, list_of_subgraph_locs
        
    def make_story_part_list_of_one_character(self, character_to_extract):
        
        #This function accepts an input of character and extracts parts involving that character along with the index into a dict
        #For use with the new subgraph function

        list_of_char_parts = []

        keys_for_this_char = [selfkey for selfkey in self.story_parts.keys() if selfkey[0] == character_to_extract.get_name()]

        for cur_index in range(0, len(keys_for_this_char)):
            list_of_char_parts.append(self.story_parts[keys_for_this_char[cur_index]])

        return list_of_char_parts
        
    def remove_parts_by_count(self, start_step, count, actor):
        end_index = start_step + count - 1

        for remove_index in range(start_step, end_index+1):
            self.remove_story_part(actor, start_step)

    def check_continuation_validity(self, actor, abs_step_to_cont_from, cont_list, target_list = None, purge_count = 0):
        #TODO: We did the main function, but now we also need to check if the character is being a target, and pull up the requirement for being a target instead if that's the case.

        #Preliminary: Check if the actor is found in the list, if not then it's false
        if actor not in self.character_objects:
            return False

        graphcopy = deepcopy(self)

        # We need a "Make Location List" function in here
        # It detects all the "RelChanges" that changes locations of a character and then applies the location to the Story Graph
        # I forgot if we ever made that a thing but for now, we will use None as the 
        # Wait we cannot get away with using None. There are some Generic Locations we would use in 

        if purge_count > 0:
            graphcopy.remove_parts_by_count(abs_step_to_cont_from, purge_count, actor)

        graphcopy.insert_multiple_parts(cont_list, actor, None, abs_step_to_cont_from, targets=target_list)
        graphcopy.fill_in_locations_on_self()
        graphcopy.update_list_of_changes()

        #TODO: A loop that goes through each of the steps, checking the story for each char and checks the Req/Unwanted Tag Lists, Bias Range
        #TODO: and Condition Tests and check whether it's valid.
        #TODO: If any is found out to be false then continuation_is_valid should be turned to False.

        # for node in graphcopy.story_parts:
        #     print(node)
        #     print(graphcopy.story_parts[node])

        graphcopy.refresh_longest_path_length()

        return graphcopy.check_worldstate_validity_on_own_graph(abs_step_to_cont_from)

    def check_worldstate_validity_on_own_graph(self, start_step):
        self.refresh_longest_path_length()

        for check_index in range(start_step, self.longest_path_length):

            #Make the world state
            current_ws = self.make_state_at_step(check_index)

            for current_char in self.character_objects:
                current_step = self.story_parts.get((current_char.get_name(), check_index))
                current_char_at_current_step = current_ws.node_dict[current_char.get_name()]

                if current_step is not None:

                    if (current_char_at_current_step not in current_step.actor) and (current_char_at_current_step not in current_step.target):
                        return False

                    if current_char_at_current_step in current_step.actor:
                        if not current_step.check_character_compatibility(current_char_at_current_step):
                            return False

                    if current_char_at_current_step in current_step.target:
                        if not current_step.check_target_compatibility(current_char_at_current_step):
                            return False

                    for current_test_to_convert in current_step.condition_tests:

                        equivalent_tests = translate_generic_test(current_test_to_convert, current_step)

                        for current_test_to_check in equivalent_tests:

                            if not current_ws.test_story_compatibility_with_conditiontest(current_test_to_check):

                                #print(current_test_to_check)
                                return False
        return True

    def make_list_of_nodes_at_step(self, abs_step):
        list_of_nodes_at_step = []

        for character in self.character_objects:
            if self.story_parts[(character.get_name(), abs_step)] is not None:
                list_of_nodes_at_step.append(self.story_parts[(character.get_name(), abs_step)])

        return list_of_nodes_at_step

    def make_list_of_changes_at_step(self, abs_step):
        return make_list_of_changes_from_list_of_story_nodes(self.make_list_of_nodes_at_step(abs_step))

    def update_list_of_changes(self):
        max_length = self.longest_path_length
        self.list_of_changes = []

        for index in range(0, max_length):
            self.list_of_changes.append(self.make_list_of_changes_at_step(index))

    def fill_in_locations_on_self(self):
        #TODO: Make a function that checks through the storyline of each character.
        #TODO: Assume that the first location is given.
        #TODO: Give that Location to each of the absolute step. Until a new RelationshipChange comes up, the location would be the same
        #TODO: When the character owning the storyline changes their location, then the location of the story changes.
        #TODO: Repeat this for all characters.

        #TODO: We will cycle through all the timesteps. Since we know that each node comes with a relChange anyways, we can pull the location information from
        #the current worldstate.

        self.refresh_longest_path_length()

        for index in range(0, self.longest_path_length):
            self.update_list_of_changes()
            cur_state = self.make_state_at_step(index)

            for story_char in self.character_objects:

                current_step = self.story_parts.get((story_char.get_name(), index), None)

                if current_step is not None:

                    #Pull the location information from cur_state
                    char_in_ws = cur_state.node_dict[story_char.get_name()]
                    location_holding_char = char_in_ws.get_holder()
                    current_step.set_location(location_holding_char)


def make_list_of_changes_from_list_of_story_nodes(story_node_list):
    changeslist = []
        
    for snode in story_node_list:
        for change in snode.effects_on_next_ws:
            changes_from_snode = translate_generic_change(change, snode)
            changeslist.extend(changes_from_snode)

    return changeslist

def if_applyonce_choose_one(loclist, applyonce):
    #After all the nodes are checked, check if The List is empty. If it is, nothing happens.
    #If there is something in The List, then apply the rule and append the Joint Story Node.
    if len(loclist) > 0:
            
        #If Apply Once is False, then all the instances in The List gets applied.
        #Otherwise, a random instance is applied to.
        if applyonce:
            loclist = [random.choice(loclist)]
        
    return loclist

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
        case _:
            equivalent_changelist = [change]

    return equivalent_changelist

def translate_generic_relchange(relchange, populated_story_node):
    lhs_list = check_keyword_and_return_objectnodelist(populated_story_node, relchange.node_a)
    rhs_list = check_keyword_and_return_objectnodelist(populated_story_node, relchange.node_b)

    list_of_equivalent_relchanges = []

    for lhs_item in lhs_list:
        for rhs_item in rhs_list:
            newchange = RelChange(relchange.name, lhs_item, relchange.edge_name, rhs_item, relchange.value, relchange.add_or_remove)
            list_of_equivalent_relchanges.append(newchange)

    return list_of_equivalent_relchanges

def translate_generic_tagchange(tagchange, populated_story_node):
    list_of_equivalent_tagchanges = []

    objectlist = check_keyword_and_return_objectnodelist(populated_story_node, tagchange.object_node_name)

    for item in objectlist:
        list_of_equivalent_tagchanges.append(TagChange(tagchange.name, item.name, tagchange.tag, tagchange.value, tagchange.add_or_remove))

    return list_of_equivalent_tagchanges

def check_keyword_and_return_objectnodelist(storynode, objnode_to_check):
    return_list = []

    match objnode_to_check:
        case GenericObjectNode.GENERIC_ACTOR:
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
def translate_generic_test(condtest, populated_story_node):

    list_of_equivalent_condtests = []

    match condtest.test_type:
        case TestType.HELD_ITEM_TAG:
            list_of_equivalent_condtests = translate_generic_held_item_test(condtest, populated_story_node)
        case TestType.SAME_LOCATION:
            list_of_equivalent_condtests = translate_generic_same_location_test(condtest, populated_story_node)
        case TestType.HAS_EDGE:
            list_of_equivalent_condtests = translate_generic_has_edge_test(condtest, populated_story_node)
        case TestType.HAS_DOUBLE_EDGE:
            list_of_equivalent_condtests = translate_generic_has_doubleedge_test(condtest, populated_story_node)
        case _:
            list_of_equivalent_condtests = [condtest]
        
    return list_of_equivalent_condtests

def translate_generic_held_item_test(test, node):

    list_of_equivalent_tests = []

    objectlist = check_keyword_and_return_objectnodelist(node, test.holder_to_test)

    for item in objectlist:
        list_of_equivalent_tests.append(HeldItemTagTest(item, test.tag_to_test, test.value_to_test, inverse=test.inverse))

    return list_of_equivalent_tests

def translate_generic_same_location_test(test, node):

    objectlist = []

    for item in test.list_to_test:
        objectlist.extend(check_keyword_and_return_objectnodelist(node, item))

    return [SameLocationTest(objectlist, inverse=test.inverse)]

def translate_generic_has_edge_test(test, node):

    list_of_equivalent_tests = []

    from_node = check_keyword_and_return_objectnodelist(node, test.object_from_test)
    to_node = check_keyword_and_return_objectnodelist(node, test.object_to_test)

    for lhs_item in from_node:
        for rhs_item in to_node:
            list_of_equivalent_tests.append(HasEdgeTest(lhs_item, test.edge_name_test, rhs_item, value_test=test.value_test, soft_equal=test.soft_equal, inverse=test.inverse))    

    return list_of_equivalent_tests

def translate_generic_has_doubleedge_test(test, node):
    
    list_of_equivalent_tests = []

    from_node = check_keyword_and_return_objectnodelist(node, test.object_from_test)
    to_node = check_keyword_and_return_objectnodelist(node, test.object_to_test)

    for lhs_item in from_node:
        for rhs_item in to_node:
            list_of_equivalent_tests.append(HasDoubleEdgeTest(lhs_item, test.edge_name_test, rhs_item, value_test=test.value_test, soft_equal=test.soft_equal, inverse=test.inverse))    

    return list_of_equivalent_tests