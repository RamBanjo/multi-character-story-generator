import math
from operator import truediv
import random
import statistics
from time import time
from numpy import empty
from components.ConditionTest import HasDoubleEdgeTest, HasEdgeTest, HeldItemTagTest, SameLocationTest
from components.RelChange import *
from components.RewriteRuleWithWorldState import JointType
from components.StoryNode import *
from components.StoryObjects import *
from copy import deepcopy
from components.UtilFunctions import all_possible_actor_groupings_with_ranges_and_freesizes, generate_grouping_from_group_size_lists, get_max_possible_actor_target_count, get_max_possible_grouping_count, list_all_good_combinations_from_joint_join_pattern, permute_all_possible_groups_with_ranges_and_freesize
from components.UtilityEnums import GenericObjectNode, TestType

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

        relevant_ws = self.make_state_at_step(stopping_step=absolute_step)

        char_name = None

        if character is not None:
            char_name = character.get_name()

        if copy:
            new_part = deepcopy(part)
        else:
            new_part = part

        #print(character.name, "added to", part.name)

        character_from_ws = relevant_ws.node_dict[char_name]

        new_part.add_actor(character_from_ws)
        new_part.timestep = timestep
        new_part.abs_step = absolute_step

        if location is not None:
            new_part.set_location(location)

        for target in targets:

            target_from_ws = relevant_ws.node_dict[target.get_name()]
            new_part.add_target(target_from_ws)

        self.add_to_story_part_dict(character_name=char_name, abs_step=absolute_step, story_part=new_part)
        self.refresh_longest_path_length()

        return new_part
    
    #TODO: Test this function
    def add_multiple_characters_to_part(self, main_actor, other_actors, part, location=None, targets=[], abs_step=0, timestep=0, copy=True):

        new_part = self.add_story_part_at_step(part=part, character=main_actor, location=location, absolute_step=abs_step, timestep=timestep, targets=targets, copy=copy)

        for additional_actor in other_actors:
            self.add_story_part_at_step(part=new_part, character=additional_actor, location=location, absolute_step=abs_step, timestep=timestep, copy=False)

        for target in new_part.targets:
            self.add_story_node_to_targets_storyline(pot_target=target, abs_step=abs_step, story_part=new_part)

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
        char_name = None

        if character is not None:
            char_name = character.get_name()

        if self.story_parts.get((char_name, absolute_step-1), None) is None:
            timestep = 0
        else:
            timestep = self.story_parts[(char_name, absolute_step-1)].timestep

        character_path_length = self.get_longest_path_length_by_character(character)

        if absolute_step >= character_path_length:
            self.add_story_part(part, character, location, timestep, copy, targets)
        else:
            #first, we need to move everything that comes after this part up by one
            for i in range(character_path_length-1, absolute_step-1, -1):
                move_up = self.story_parts.pop((char_name, i))
                self.add_to_story_part_dict(character_name=char_name, abs_step=i+1, story_part=move_up)

            #then, we add a new story part at the spot
            new_part = self.add_story_part_at_step(part, character, location, absolute_step, timestep, copy, targets)

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

    def get_latest_story_node_from_character(self, character):
        return self.story_parts.get((character.get_name(), self.get_longest_path_length_by_character(character)), None)

    def get_all_path_length_with_charname(self):
        check_list = []
        for actor in self.character_objects:
            check_list.append((self.get_longest_path_length_by_character(actor), actor.get_name()))

        return check_list

    def get_shortest_path_length_from_all(self):

        check_list = self.get_all_path_length_with_charname()
        return(min(check_list)[0])
    
    def get_characters_with_shortest_path_length(self):
        shortest_path_length = self.get_shortest_path_length_from_all()
        return [x[1] for x in self.get_all_path_length_with_charname() if x[0] == shortest_path_length]


    # Input: the required character, the base node
    # Output: A list of tuples. Each tuple is has the absolute step in index 0 and the list of character names in that node in index 1.
    #TODO: Test this function.
    
    def get_joint_node_steps_from_character_storyline(self, actor, joint_node):
        '''
        actor: the character object of the actor whose storyline we want to check.
        joint_node: the joint node we want to find. usually, this is the base joint.
        eligible_actors: the list of names of actors that we want to find. usually, this is the list of actors whose storyline length is the shortest
        this function returns a list of tuples. each tuple has the absolute step of the locations where the given joint node is found in index 0, and the list of characters in that node from both actors and targets
        '''
        return_list = []

        actor_name = actor.get_name()

        for node_index in range(0, self.get_longest_path_length_by_character(actor_name)):
            
            current_part = self.story_parts.get((actor_name, node_index), None)
            if current_part is not None:
                if current_part.get_name() == joint_node.get_name():
                    
                    eligible_actor_names_found_in_actors = [x.get_name() for x in joint_node.actor]
                    eligible_actor_names_found_in_targets = [x.get_name() for x in joint_node.target]

                    all_eligible_names = [actor_name]
                    all_eligible_names += eligible_actor_names_found_in_actors
                    all_eligible_names += eligible_actor_names_found_in_targets

                    #Remove dupe names
                    all_eligible_names = sorted(list(set(all_eligible_names)))

                    tuple_to_add = (node_index, all_eligible_names)
                    return_list.append(tuple_to_add)

        return return_list

    def make_latest_state(self, state_name = "Latest State"):
        #Take the initial world state and copy it.
        #Then, cycle through the list of changes, applying the changes from it.
        #returns the latest state

        return self.make_state_at_step(len(self.list_of_changes), state_name)

    def make_state_at_step(self, stopping_step, state_name = "Traveling State"):
        #Same as make_latest_state, but you can choose the step where to stop.
        #In fact, make_latest_state should call this function but set the stopping step as the last step.

        self.update_list_of_changes()

        traveling_state = deepcopy(self.starting_ws)
        traveling_state.name = state_name

        for index in range(0, stopping_step):
            for change in self.list_of_changes[index]:
                traveling_state.apply_some_change(change)
        
        return traveling_state

    # Join Joint and Cont Joint: The score is the max between the actor slot and the target slot.
    # Split Joint: The score is the max among all the given splits.

    #TODO: Test this function with all types of rules.
    def calculate_score_from_rule_char_and_cont(self, actor, insert_index, rule, mode=0):

        #There is no need to test if the rule fits this spot, because by the point that this function is called, all the unsuitable rules should have been removed from the list.

        #If it's a normal type of rule then we can use the normal calculate score function do do this.
        if not rule.is_joint_rule:
            purge_count = len(rule.story_condition)
            return self.calculate_score_from_char_and_cont(actor=actor, insert_index=insert_index, contlist=rule.story_change, mode=mode, purge_count=purge_count)
        else:

            #Get character information from the relevant step.
            character_from_ws = self.make_state_at_step(insert_index).node_dict[actor.get_name()]

            if rule.join_type == JointType.SPLIT:
                #TODO: We need to figure out if it's a split joint. If it is, then check the max/avg among all splits depending on the mode.

                list_of_split_scores = [node.calculate_weight_score(character_from_ws, mode=1) for node in rule.split_list]

                if mode == 1:
                    return statistics.mean(list_of_split_scores)
                else:
                    return max(list_of_split_scores)

            else:
                #If not, then max between actor slot and target slot.
                return rule.joint_node.calculate_weight_score(character_from_ws, mode=1)

    def calculate_score_from_char_and_cont(self, actor, insert_index, contlist, mode=0, purge_count=0):
        '''Mode is an int, depending on what it is, this function will do different things:
        mode = 0: return max between all the cont list.
        mode = 1: return average between all the cont list.
        
        if the mode integer is not listed here it will default to mode 0'''
        score = []
        
        graphcopy = deepcopy(self)

        if purge_count > 0:
            graphcopy.remove_parts_by_count(start_step=insert_index, count=purge_count, actor=actor)
        
        graphcopy.insert_multiple_parts(part_list=contlist, character=actor, absolute_step=insert_index)

        for current_index in range(insert_index, len(contlist)+1):
            current_state = graphcopy.make_state_at_step(current_index)
            current_actor = current_state.node_dict[actor.get_name()]
            current_node = graphcopy.story_parts[(actor.get_name(), current_index)]
            score.append(current_node.calculate_bonus_weight_score(current_actor) + current_node.biasweight)
        
        del(graphcopy)

        if mode == 1:
            return statistics.mean(score)
        else:
            return max(score)

    #TODO: Test this function
    def reverse_steps(self, number_of_reverse, state_name = "Reversed State"):
        #Returns a World State, reversing the changes for steps equal to number_of_reverse from the last state

        traveling_state = deepcopy(self.latest_ws)
        traveling_state.name = state_name

        for index in range(len(self.list_of_changes)-1, len(self.list_of_changes)-1-number_of_reverse, -1):
            for change in self.list_of_changes[index]:
                traveling_state.apply_some_change(change, reverse=True)

        return traveling_state

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
                self.insert_multiple_parts(rule.story_change, character, location_list, change_location, copy=True, targets=rule.target_list)

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

    #To clarify: Targets to test are all actors.
    def check_joint_continuity_validity(self, joint_rule, actors_to_test, targets_to_test, insert_index):

        #First, we must check a few prerequisites. If any characters mentioned in actors_to_test don't exist in the storyline, then we definitely cannot continue the storyline.

        for testchar in actors_to_test:
            if testchar not in self.character_objects:
                return False
        
        validity = False

        #Before anything else, if we're trying to test for cont or split, we must make sure that the node at the insert index fulfill the following conditions:
        # All the actors mentioned share the same node at the given insert_index
        # (That's it that's the only condition)

        assumed_node = self.story_parts[(actors_to_test[0].get_name(), insert_index)]
        if joint_rule.joint_type == JointType.CONT or joint_rule.joint_type == JointType.SPLIT:
            #If the node at the insert index doesn't have the same characters as the given actors and targets: return False
            #We just need to take the first character from the actors to test, find out what node they're in, and check it for existence of other characters
            #(It does not matter whether they are actors or targets, as long as it's the same characters)
            
            for actor in actors_to_test:
                if not assumed_node.check_if_character_exists_in_node(actor):
                    return False
            for target in targets_to_test:
                if not assumed_node.check_if_character_exists_in_node(target):
                    return False

        # If we are doing the Split rule, we must validate that each of the character in actors to test and targets to test are performing nodes included in the base nodes.
        # Before this can be done, we must decide what style of Joint Split we should be doing.
        # We have decided. (See check if abs step has joint pattern)
        if joint_rule.joint_type == JointType.JOIN:

            # For each of the actors in actors_to_test and target_to_test, turn them into one list. Then, call the list_all_good_combinations_from_joint_join_pattern from UtilFunctions to get a list.
            # After we get the list of all possible combinations, we then look for whether or not our specific combination of actors and targets exist in that list. If not, then return False. Otherwise continue with the check.

            list_of_testing_actor_names = set()

            for actor in actors_to_test:
                list_of_testing_actor_names.add(actor.get_name())
            for target in targets_to_test:
                list_of_testing_actor_names.add(target.get_name())

            list_of_possible_combi = list_all_good_combinations_from_joint_join_pattern(dict_of_base_nodes=self.check_if_abs_step_has_joint_pattern(required_story_nodes_list=joint_rule.base_actions, character_name_list=list(list_of_testing_actor_names), absolute_step_to_search=insert_index))

            found_exact_set = False
            for combi in list_of_possible_combi:
                if list_of_possible_combi == set(combi):
                    found_exact_set = True

            if not found_exact_set:
                return False
    
        if joint_rule.joint_type == JointType.JOIN or joint_rule.joint_type == JointType.CONT:
            validity = self.check_add_joint_validity(joint_rule.joint_node, actors_to_test, targets_to_test, insert_index)
        if joint_rule.joint_type == JointType.SPLIT:
            validity = self.check_add_split_validity(joint_rule.split_list, actors_to_test, targets_to_test, insert_index)
        
        return validity
    
    #This function is for testing if an absolute step contains a pattern that is suitable for a join joint.
    def check_if_abs_step_has_joint_pattern(self, required_story_nodes_list, character_name_list, absolute_step_to_search):
        
        dict_of_chars_with_nodename_as_key = dict()

        #List of valid nodes are taken from the required node list. This is taken from 
        valid_nodename_list = [snode.get_name() for snode in required_story_nodes_list]

        for charname in character_name_list:
            found_node = self.story_parts.get((charname, absolute_step_to_search), None)
            if found_node is not None:
                nodename = found_node.get_name()
                if nodename in valid_nodename_list:
                    if dict_of_chars_with_nodename_as_key.get(nodename, None) == None:
                        dict_of_chars_with_nodename_as_key[nodename] = [charname]
                    else:
                        dict_of_chars_with_nodename_as_key[nodename].append(charname)

        found_node_names = dict_of_chars_with_nodename_as_key.keys()
        for req_node in required_story_nodes_list:
            req_node_name = req_node.get_name()

            if req_node_name not in found_node_names:
                return False, dict_of_chars_with_nodename_as_key
            
        return True, dict_of_chars_with_nodename_as_key

    def check_for_jointrule_location_in_storyline(self, actor, joint_rule):
        if joint_rule.joint_type == JointType.JOIN:

            #For each of the possible base action, at any point if this character is seen performing the base action then add it to the list.
            valid_locs = []
            for base_node in joint_rule.base_actions:

                valid_locs += self.check_for_pattern_in_storyline([base_node], actor)[1]
                return len(valid_locs) > 0, sorted(list(set(valid_locs)))

            return self.check_for_pattern_in_storyline()
        if joint_rule.joint_type == JointType.CONT or joint_rule.joint_type == JointType.SPLIT:
            return self.check_for_pattern_in_storyline([joint_rule.base_joint], actor)
        
        return False, []

    def check_add_joint_validity(self, joint_node, actors_to_test, targets_to_test, insert_index):

        graphcopy = deepcopy(self)
        graphcopy.joint_continuation([insert_index], True, joint_node, actors_to_test, None, targets_to_test)

        validity = graphcopy.check_worldstate_validity_on_own_graph(insert_index)
        del(graphcopy)

        return validity
        
    def check_add_split_validity(self, split_list, actors_to_test, targets_to_test, insert_index, with_grouping = False):
        
        graphcopy = deepcopy(self)
        graphcopy.split_continuation(split_list, actors_to_test, insert_index, None, target_replace=targets_to_test, with_grouping=with_grouping)

        validity = graphcopy.check_worldstate_validity_on_own_graph(insert_index)
        del(graphcopy)

        return validity

    def apply_joint_rule(self, joint_rule, characters, location_list, applyonce=False, target_require=[], target_replace=[], character_grouping=[]):

        if joint_rule.joint_type == JointType.JOIN:
            self.apply_joining_joint_rule(joint_rule, characters, location_list, applyonce, target_require=target_require, target_replace=target_replace)
        if joint_rule.joint_type == JointType.CONT:
            self.apply_continuous_joint_rule(joint_rule, characters, location_list, applyonce, target_require=target_require, target_replace=target_replace)
        if joint_rule.joint_type == JointType.SPLIT:
            self.apply_splitting_joint_rule(joint_rule, characters, location_list, character_grouping=character_grouping, applyonce=applyonce)
        self.refresh_longest_path_length()
    

    def add_story_node_to_targets_storyline(self, pot_target, abs_step, story_part):
        if pot_target in self.character_objects:
            self.add_to_story_part_dict(character_name=pot_target.get_name(), abs_step=abs_step, story_part=story_part)

    def joint_continuation(self, loclist, applyonce, joint_node, actors, location=None, target_list=[]):
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

    #This function, given a list of characters and a number of characters that should be a target, returns a dict of actor list and target list.
    #Whenever characters are assigned to a joint node where the target count is not 0, call this to make a split.
    def generate_valid_actor_and_target_split(self, node, abs_step, character_list):

        #Before anything is done, sum the allowed character count with the targets wanted count. If there are more characters than this sum, then it's impossible to fulfill.
        #Of course, if either or both is a -1, this means that it's indefinite therefore no limitations.

        #If both limits are -1, then scramble freely. If one or both limits are normal integers, then take care of the integers first, with priority for targets first.

        #We can probably use the same method for the generate valid character grouping below.

        #Of course, we also need to include an exit clause in the event that all the possible combinations are already exhausted.

        #We do this first. Index 0 is for Actors, Index 1 is for Targets
        list_of_charnames = [x.get_name() for x in character_list]
        all_possible_groupings = all_possible_actor_groupings_with_ranges_and_freesizes([node.charcount, node.target_count], list_of_charnames)

        state_at_step = self.make_state_at_step(abs_step) #This is the state where we will check if the characters are compatible with each of their assigned nodes.
        found_valid_grouping = False

        while (not found_valid_grouping):

            #Return None if we have exhausted all of the possible groupings.
            
            if len(all_possible_groupings) <= 0:
                return None

            #Pick a random possible grouping from the list
            random_grouping_from_list = random.choice(all_possible_groupings)
            # print(len(all_possible_groupings), random_grouping_from_list)

            #Remove it so it's never chosen again
            all_possible_groupings.remove(random_grouping_from_list)

            grouping = {"actor_group":[], "target_group":[]}

            for actor_name in random_grouping_from_list[0]:
                grouping["actor_group"].append(state_at_step.node_dict[actor_name])

            for target_name in random_grouping_from_list[1]:
                grouping["target_group"].append(state_at_step.node_dict[target_name])

            
            actor_validity = node.check_character_compatibility_for_many_characters(grouping["actor_group"])
            target_validity = node.check_target_compatibility_for_many_characters(grouping["target_group"])
            # print(actor_validity, target_validity)

            if actor_validity and target_validity:
                return grouping

    #Please note that Grouping is a list that is used to determine group size. For example, if it is [1, 3], this means one character in the first group and 3 characters in the second group.

    def generate_valid_character_grouping(self, continuations, abs_step, character_list, grouping=[]):
        '''This function can accept -1 and tuple ranges.'''

        #If there is no grouping information, then we only want one character per continuation.
        if grouping == []:
            grouping = [1] * len(character_list)

        #Make the grouping information here.
        list_of_charnames = [x.get_name() for x in character_list]
        all_possible_groupings = all_possible_actor_groupings_with_ranges_and_freesizes(grouping, list_of_charnames)

        state_at_step = self.make_state_at_step(abs_step) #This is the state where we will check if the characters are compatible with each of their assigned nodes.

        found_valid_grouping = False

        while (not found_valid_grouping):

            current_grouping = []
            
            #Return None if we have exhausted all of the possible groupings.
            if len(all_possible_groupings) <= 0:
                return None

            random_chosen_group = random.choice(all_possible_groupings)

            #Remove this so that this exact chosen combination is never chosen again.
            all_possible_groupings.remove(random_chosen_group)

            #Set up the grouping information.
            for subgroup_charname in random_chosen_group:
                
                subgroup_char = []
                
                for charname in subgroup_charname:
                    subgroup_char.append(state_at_step.node_dict[charname])

                current_grouping.append(subgroup_char)

            this_one_is_valid = True

            #Check validity for each of the continuations
            for story_index in range(0, len(continuations)):
                this_one_is_valid = this_one_is_valid and continuations[story_index].check_character_compatibility_for_many_characters(current_grouping[story_index])

            #If it's valid, it can be returned. If not, find new one.
            if this_one_is_valid:
                return current_grouping

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
            #Check if any of the targets exist in self.characters. If there is one, then make sure to add this node to that character's StoryGraph in the same step.
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

    def check_for_pattern_in_storyline(self, pattern_to_test, character_to_extract):

        #preliminary check: check if the character exists inside of the storyline, return false if it does not
        if character_to_extract not in self.character_objects:
            return False, []
        
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
        
    #TODO: Test this function to make sure it's working for sure.
    def remove_parts_by_count(self, start_step, count, actor):
        end_index = start_step + count - 1

        for remove_index in range(start_step, end_index+1):
            self.remove_story_part(actor, start_step)

    #This function checks if there it at least one spot where the rule can be applied.
    def check_rule_validity_for_first_actor(self, actor, rule):

        if rule.is_joint_rule:
            for i in range(0, self.get_longest_path_length_by_character(actor)):
                if self.check_joint_continuity_validity(joint_rule=rule, actors_to_test=[actor], targets_to_test=rule.target_list, insert_index=i):
                    return True
            return False

        is_subgraph, subgraph_locs = self.check_for_pattern_in_storyline(rule.story_condition, actor)

        if not is_subgraph:
            return False
        
        purge_count = 0
        if rule.remove_before_insert:
            purge_count = len(rule.story_condition)

        for story_index in subgraph_locs:
            if self.check_continuation_validity(actor=actor, abs_step_to_cont_from=story_index, cont_list=rule.story_change, target_list=rule.target_list, purge_count=purge_count):
                return True
                
        return False
    
    #Here, we check that there is at least one valid slot for a character in a joint node.
    def check_if_joint_node_is_valid_at_timestep_for_actor(self, actor, joint_node, step):

        #Get the character at that step
        character_at_step = self.make_state_at_step(step).node_dict[actor.get_name()]

        #This function returns if the character can fit in at least as an actor or a target.
        return joint_node.check_actor_or_target_compatibility(character_at_step)


    def check_continuation_validity(self, actor, abs_step_to_cont_from, cont_list, target_list = None, purge_count = 0):
        #TODO: We did the main function, but now we also need to check if the character is being a target, and pull up the requirement for being a target instead if that's the case.
        #This function is meant for use with only the continuation part of a normal non-joint rule. We probably should make a new function to use with the joint rules.

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
        graphcopy.refresh_longest_path_length()

        #We delegate the checking of worldstates fo the worldstate validity function
        validity = graphcopy.check_worldstate_validity_on_own_graph(abs_step_to_cont_from)
        del(graphcopy)

        return validity

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

                                return False
        return True

    def make_list_of_nodes_at_step(self, abs_step):
        list_of_nodes_at_step = []

        for character in self.character_objects:
            if self.story_parts.get((character.get_name(), abs_step), None) is not None:
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
        #A function that checks through the storyline of each character.
        #Assume that the first location is given.
        #Give that Location to each of the absolute step. Until a new RelationshipChange comes up, the location would be the same
        #When the character owning the storyline changes their location, then the location of the story changes.
        #Repeat this for all characters.

        #We will cycle through all the timesteps. Since we know that each node comes with a relChange anyways, we can pull the location information from
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