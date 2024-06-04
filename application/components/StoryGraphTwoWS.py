import sys

sys.path.insert(0,'')

import random
import statistics
from application.components.ConditionTest import HasEdgeTest, HeldItemTagTest, SameLocationTest
from application.components.RelChange import *
from application.components.RewriteRuleWithWorldState import JointType
from application.components.StoryNode import *
from application.components.StoryObjects import *
from copy import deepcopy
from application.components.UtilFunctions import *
from application.components.UtilityEnums import GenericObjectNode, TestType
from application.components.CharacterTask import CharacterTask, TaskStack
from application.components.StoryMetrics import MetricMode, MetricType, StoryMetric

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

DEFAULT_INVALID_SCORE = -999

class StoryGraph:
    def __init__(self, name, character_objects, starting_ws):
        self.name = name
        self.character_objects = character_objects
        self.story_parts = dict()
        self.longest_path_length = 0
        self.starting_ws = starting_ws
        
        self.list_of_changes = []
        self.latest_ws = self.make_latest_state()

        # Key: A tuple consisting of (Task Owner Name, Task Stack Name)
        # Value: Dict that matches placeholder string to actor names
        # Whenever a task with no preset dict found here is being added, generate a valid dict and add it here
        # Whenever a task with a preset dict here is being added, use that preset dict as input
        self.placeholder_dicts_of_tasks = dict()

    def export_object_as_dict(self) -> dict:

        export_dict = dict()

        export_dict["name"] = self.name
        export_dict["character_object_name_list"] = []

        for thing in self.character_objects:
            export_dict["character_object_name_list"].append(thing.get_name())

        #Not exporting Starting WS, there should be only one World State attached to the file when exporting (You already know which one)
        return export_dict
    
    def add_to_story_part_dict(self, character_name, abs_step, story_part):
        story_part.abs_step = abs_step
        self.story_parts[(character_name, abs_step)] = story_part

    #Copy=False would be used in the case of joint.
    def add_story_part(self, part, character, location=None, timestep=0, copy=True, targets=[]):
        
        #first we need to get the last entry in this character's story
        character_path_length = self.get_longest_path_length_by_character(character)

        new_part = self.add_story_part_at_step(part=part, character=character, location=location, absolute_step=character_path_length, timestep=timestep, copy=copy, targets=targets)

        # if character_path_length > 0:
        #     self.story_parts[(char_name, character_path_length-1)].add_next_node(new_part, character)

        self.refresh_longest_path_length()

        return new_part

    def add_story_part_at_step(self, part, character, location=None, absolute_step=0, timestep=0, copy=True, targets=[], verbose=False):

        relevant_ws = self.make_state_at_step(stopping_step=absolute_step)[0]

        char_name = None

        if character is not None:
            char_name = character.get_name()

        if copy:
            new_part = deepcopy(part)
        else:
            new_part = part

        character_from_ws = relevant_ws.node_dict[char_name]

        # if char_name == "Amil":
        #     print("Amil Tasks at Step (He is Actor)", absolute_step, character_from_ws.get_incomplete_task_stack_names())

        new_part.add_actor(character_from_ws)
        new_part.timestep = timestep
        new_part.abs_step = absolute_step

        if verbose:
            print(character.name, "added to", part.name)

        if location is not None:
            location_from_ws = relevant_ws.node_dict[location.get_name()]
            new_part.set_location(location_from_ws)

        for target in targets:
            
            # if type(target) == CharacterNode and target.name == "Amil":
            #     print("Amil Tasks at Step (He is Target)", absolute_step, target.get_incomplete_task_stack_names())

            target_from_ws = relevant_ws.node_dict[target.get_name()]
            new_part.add_target(target_from_ws)

        new_part.effects_on_next_ws = []

        modded_taskobj_list = dict()
        for change in part.effects_on_next_ws:
            if change.changetype == ChangeType.TASKCHANGE:
                modded_taskobj = self.modify_taskchange_object_on_add(abs_step=absolute_step, story_node=new_part, taskchange_object=change)
                if modded_taskobj[0]:
                    change.task_object = modded_taskobj[1]
                    modded_taskobj_list[modded_taskobj[1].stack_name] = modded_taskobj[1]


            change_copy = deepcopy(change)
            new_part.effects_on_next_ws.append(change_copy)

            #Look I don't know why these have to be assigned again but apparently they do. Sue me.

        for i in range(0, len(new_part.effects_on_next_ws)):
            if new_part.effects_on_next_ws[i].changetype == ChangeType.TASKCHANGE:
                stack_name = new_part.effects_on_next_ws[i].task_stack.stack_name
                new_part.effects_on_next_ws[i].task_stack.copy_all_attributes(modded_taskobj_list[stack_name])


        self.add_to_story_part_dict(character_name=char_name, abs_step=absolute_step, story_part=new_part)

        self.refresh_longest_path_length()


        return new_part

    def remove_story_part(self, character, absolute_step):

        char_name = None

        if character is not None:
            char_name = character.get_name()

        removed = self.story_parts.pop((char_name, absolute_step), None)

        if removed is not None:

            current_longest = self.get_longest_path_length_by_character(character)

            # prevnode = None
            # nextnode = None

            #if there is a previous node, remove references to this node
            # if absolute_step-1 >= 0:
                # prevnode = self.story_parts[(char_name, absolute_step-1)]
                # prevnode.remove_next_node(character)
            
            #if the removed thing is not the last thing, then we need to move stuff down
            if absolute_step < current_longest:

                # nextnode = self.story_parts[(char_name, absolute_step+1)]

                for i in range(absolute_step+1, current_longest+1):
                
                    move_down = self.story_parts.pop((char_name, i))

                    self.add_to_story_part_dict(character_name=char_name, abs_step=i-1, story_part=move_down)

            #finally, if both conditions are met, then those two must be connected
            # if prevnode is not None and nextnode is not None:
                # prevnode.add_next_node(nextnode, character)
        
        self.refresh_longest_path_length()

    def insert_story_part(self, part, character, location=None, absolute_step=0, copy=True, targets=[], timestep=None):

        #check if this would be the last storypart in the list, if it is, then call add story part like normal
        char_name = None

        if character is not None:
            char_name = character.get_name()

        if timestep == None:
            if self.story_parts.get((char_name, absolute_step-1), None) is None:
                timestep = 0
            else:
                timestep = self.story_parts[(char_name, absolute_step-1)].timestep

        character_path_length = self.get_longest_path_length_by_character(character)

        if absolute_step >= character_path_length:
            return_node = self.add_story_part(part=part, character=character, location=location, timestep=timestep, copy=copy, targets=targets)
        else:
            #first, we need to move everything that comes after this part up by one
            for i in range(character_path_length-1, absolute_step-1, -1):
                move_up = self.story_parts.pop((char_name, i))
                self.add_to_story_part_dict(character_name=char_name, abs_step=i+1, story_part=move_up)

            #then, we add a new story part at the spot
            return_node = self.add_story_part_at_step(part, character, location, absolute_step, timestep, copy, targets)

            # #Connect to Other Nodes.
            # #Firstly, if this isn't the first node, we will connect to the previous node.
            # #The previous node severs its ties with its previous next node and now considers the current node to be its next node.
            # if absolute_step-1 >= 0:
            #     prevnode =  self.story_parts[(char_name, absolute_step-1)]
            #     prevnode.remove_next_node(character)
            #     prevnode.add_next_node(return_node, character)

            # #Secondly, since to get here we established that a next node exists, we need to add the next node as the current node's next node.
            # return_node.add_next_node(self.story_parts[(char_name, absolute_step+1)], character)

        self.refresh_longest_path_length()

        return return_node

    def insert_multiple_parts(self, part_list, character, location_list=None, absolute_step=0, copy=True, targets=None):

        index = 0

        for item in part_list:

            cur_loc = None
            cur_tar = []

            if location_list != None:
                cur_loc = location_list[index]
            if targets != None:
                cur_tar = targets[index]

            self.insert_story_part(part=item, character=character, location=cur_loc, absolute_step=absolute_step+index, copy=copy, targets=cur_tar)

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
        return self.story_parts.get((character.get_name(), self.get_longest_path_length_by_character(character)-1), None)

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
    # TODO (Extra Features, Testing): Test this function. (There is no need to test this because it's not used. We can return to testing if we end up using this.)
    # ...where is this function used again?
    
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
        
        self.refresh_longest_path_length()
        
        latest_state_tuple = self.make_state_at_step(self.longest_path_length, state_name)
        return latest_state_tuple[0]

    def make_state_at_step(self, stopping_step, state_name = None):
        #Same as make_latest_state, but you can choose the step where to stop.
        #In fact, make_latest_state should call this function but set the stopping step as the last step.
        self.update_list_of_changes()

        traveling_state = deepcopy(self.starting_ws)
        
        if state_name is None:
            state_name = "State at abs_step " + str(stopping_step)
        traveling_state.name = state_name

        # print("Begin Making State: " + state_name)

        world_state_validity = True

        for index in range(0, stopping_step):
            # print(index, "Amil List of Tasks", traveling_state.node_dict["Amil"].get_incomplete_task_stack_names())
            for change in self.list_of_changes[index]:
                frozen_current_state = deepcopy(traveling_state)
                # TaskChange will call apply_task_change from the traveling_state
                # (We assume that dict is already added to the TaskStack in the change when it was called)
                # TaskAdvanceChange will call apply_task_advance_change from the traveling_state
                # TaskCancelChange will call apply_task_cancel_change from the traveling_state
                # if change.changetype == ChangeType.TASKCHANGE:
                    # print(index, change)
                match change.changetype:              
                    case ChangeType.CONDCHANGE:
                        world_state_validity = world_state_validity and traveling_state.apply_conditional_change(change, frozen_current_state)
                    case ChangeType.TASKCHANGE:
                        world_state_validity = world_state_validity and traveling_state.apply_task_change(taskchange_object=change)
                    case ChangeType.TASKADVANCECHANGE:
                        world_state_validity = world_state_validity and traveling_state.apply_task_advance_change(taskadvancechange_object=change, abs_step = index)
                    case ChangeType.TASKCANCELCHANGE:
                        world_state_validity = world_state_validity and traveling_state.apply_task_cancel_change(taskcancelchange_object=change)
                    case _:
                        world_state_validity = world_state_validity and traveling_state.apply_some_change(change)

        return traveling_state, world_state_validity

    # Join Joint and Cont Joint: The score is the max between the actor slot and the target slot.
    # Split Joint: The score is the max among all the given splits.

    #TODO (Important): Rule. Rule. Of Course. We should have return the fail value if there is no pattern.
    #Obviously we aren't going to let the user use those bad bad horrible no good rules.

    #PLEASE NOTE that the insert_index always refers to the location where the first node will be inserted
    def calculate_score_from_rule_char_and_cont(self, actor, insert_index, rule, mode=0):

        # For the non-joint rule we can use self.check_for_pattern_in_storyline() to see if there is a pattern.
        # For the cont joint and split joint we can uses the same.
        # For the join joint, there has to be a pattern for at least one of the nodes listed.

        pattern_found_at_step = False
        if not rule.is_joint_rule:
            test_result_tuple = self.check_for_pattern_in_storyline(pattern_to_test=rule.story_condition, character_to_extract=actor)
            pattern_found_at_step = insert_index in test_result_tuple[1]

            cont_valid = False
            if pattern_found_at_step:
                purge_count = 0
                insert_point = insert_index

                if rule.remove_before_insert:
                    purge_count = len(rule.story_condition)
                else:
                    insert_point += len(rule.story_condition)
                    
                cont_valid = self.check_continuation_validity(actor=actor, abs_step_to_cont_from=insert_point, cont_list=rule.story_change, target_list=rule.target_list, purge_count=purge_count)
            pattern_found_at_step = pattern_found_at_step and cont_valid

        else:
            if rule.joint_type == JointType.JOIN:
                #Want to know if there is at least one pattern.
                #Note that if no base pattern is given, then pattern is always found at step.

                if rule.is_patternless_join():
                    pattern_found_at_step = True
                else:   
                    for potential_joint in rule.base_actions:
                        test_result_tuple = self.check_for_pattern_in_storyline(pattern_to_test=[potential_joint], character_to_extract=actor)
                        pattern_found_at_step = pattern_found_at_step or insert_index-1 in test_result_tuple[1]

            else:
                test_result_tuple = self.check_for_pattern_in_storyline(pattern_to_test=[rule.base_joint], character_to_extract=actor)
                pattern_found_at_step = insert_index-1 in test_result_tuple[1]

        if not pattern_found_at_step:
            return DEFAULT_INVALID_SCORE
            
        # There is no need to test if the rule fits this spot, because by the point that this function is called, all the unsuitable rules should have been removed from the list.
        # Hey guess how poorly this statement above has aged lol. Screw this.

        #If it's a normal type of rule then we can use the normal calculate score function do do this.
        if not rule.is_joint_rule:
            purge_count = 0
            insert_point = insert_index

            if rule.remove_before_insert:
                purge_count = len(rule.story_condition)
            else:
                insert_point += len(rule.story_condition)

            return self.calculate_score_from_char_and_cont(actor=actor, insert_index=insert_point, contlist=rule.story_change, mode=mode, purge_count=purge_count, target_list=rule.target_list)
        else:

            #Get character information from the relevant step.
            current_ws = self.make_state_at_step(insert_index)[0]
            character_from_ws = current_ws.node_dict[actor.get_name()]

            if rule.joint_type == JointType.SPLIT:
                #We need to figure out if it's a split joint. If it is, then check the max/avg among all splits depending on the mode.

                list_of_split_scores = []

                for node in rule.split_list:
                    max_of_joint = calculate_score_from_char_and_unpopulated_node_with_both_slots(actor=character_from_ws, node=node, world_state=current_ws)
                    list_of_split_scores.append(max_of_joint)

                if mode == 1:
                    return statistics.mean(list_of_split_scores)
                
                else:
                    return max(list_of_split_scores)

            else:
                #If not, then max between actor slot and target slot for the only joint node.
                return calculate_score_from_char_and_unpopulated_node_with_both_slots(actor=character_from_ws, node=rule.joint_node, world_state=current_ws, mode=mode)

    def calculate_score_from_next_task_in_task_stack(self, actor_name, task_stack_name, task_perform_index, mode=0):

        #First we must recognize if the task is already completed or not
        #If it's not already completed at the given task_perform_index, then get the appropriate task actions then calculate that cont

        completeness = self.test_task_completeness(task_stack_name=task_stack_name, actor_name=actor_name, abs_step=task_perform_index)
        
        # Advance Task -> 0 or Equivalent to Completing Task By Ourself?
        # Cancel Task -> DEFAULT_INVALID_SCORE

        match completeness:
            case "task_step_can_advance":
                current_ws = self.make_state_at_step(task_perform_index)[0]
                actor = current_ws.node_dict[actor_name]

                self.find_last_step_of_task_stack_from_actor

                task_stack_obj = actor.get_task_stack_by_name(task_stack_name)
                current_task = task_stack_obj.get_current_task()

                task_actions = current_task.task_actions
                translated_nodes = []
                
                for node in task_actions:
                    translated_nodes.append(replace_placeholders_in_story_node(story_node=node, placeholder_dict=self.placeholder_dicts_of_tasks[(actor_name, task_stack_name)], list_of_actor_objects=self.character_objects)) 
                    
                return self.calculate_score_from_char_and_cont(actor=actor, insert_index=task_perform_index, contlist=translated_nodes, has_joint_in_contlist=True, mode=mode)
            case "task_step_already_completed":
                return 
            case _:
                return DEFAULT_INVALID_SCORE

    def calculate_score_from_char_and_cont(self, actor, insert_index, contlist, mode=0, purge_count=0, has_joint_in_contlist = False, target_list = None):
        '''Mode is an int, depending on what it is, this function will do different things:
        mode = 0: return max between all the cont list.
        mode = 1: return average between all the cont list.
        
        if the mode integer is not listed here it will default to mode 0'''
        score = []
        
        graphcopy = deepcopy(self)
        
        #This is the part where nodes are removed/inserted from the Graph Copy. If this is correct, it won't have to be changed.
        if purge_count > 0:
            graphcopy.remove_parts_by_count(start_step=insert_index, count=purge_count, actor=actor)

        if has_joint_in_contlist:
            graphcopy.insert_multiple_parts_with_joint_and_nonjoint(node_list=contlist, main_character=actor, abs_step=insert_index)
        else:
            graphcopy.insert_multiple_parts(part_list=contlist, character = actor, absolute_step=insert_index, targets=target_list)

        graphcopy.fill_in_locations_on_self()

        #This is the part where score calculations are done.
        #Since we already added actor information when calling insert_multiple_parts and insert_multiple_parts_with_joint_and_nonjoint we don't have to add actor information here again.
        for current_index in range(insert_index, insert_index+len(contlist)):
            current_state = graphcopy.make_state_at_step(current_index)[0]
            current_node = graphcopy.story_parts[(actor.get_name(), current_index)]

            #By default the score is invalid, but if all the nodes are valid then this score will be replaced by an actual biasweight score.
            score_to_append = DEFAULT_INVALID_SCORE

            if current_state.test_story_compatibility_with_storynode(current_node):
                score_to_append = current_state.get_score_from_story_node(current_node) + current_node.biasweight
            
            score.append(score_to_append)

        # print("-----")
        # for thing in graphcopy.make_story_part_list_of_one_character(actor):
        #     print(thing)

        del(graphcopy)

        #Since we're looking to use this entire sequence for a character, if we get a value of -999 it means that it cannot be used so we need to return this value to signify such a case.
        if DEFAULT_INVALID_SCORE in score:
            return DEFAULT_INVALID_SCORE

        if mode == 1:
            return statistics.mean(score)
        else:
            return max(score)

    #Is this function necessary or used? We might be able to deprecate this if it's not used (because we can always call make state from the beginning)
    #LOL LMAO This is basically functionally the same as making the state at the length of the timesteps minus the number of reverses
    #Consider the following: There are 5 steps [0, 1, 2, 3, 4], and we want the step from final step reversed two times. We can either reverse twice into 2, or go forward 5-2-1 = 2 steps into 2. 
    def reverse_steps(self, number_of_reverse, state_name = "Reversed State"):
        #Returns a World State, reversing the changes for steps equal to number_of_reverse from the last state

        return self.make_state_at_step(len(self.list_of_changes) - number_of_reverse - 1, state_name=state_name)[0]

        # traveling_state = deepcopy(self.latest_ws)
        # traveling_state.name = state_name

        # for index in range(len(self.list_of_changes)-1, len(self.list_of_changes)-1-number_of_reverse, -1):
        #     for change in self.list_of_changes[index]:
        #         traveling_state.apply_some_change(change, reverse=True)

        # return traveling_state

    #...we definitely don't need Apply Once. The new Rewrite Rules don't use it, and our generation system specifies clearly the absolute step every single time.
    def apply_rewrite_rule(self, rule, character, location_list = None, abs_step = -1, verbose=True):
        '''
        If abs_step is set as -1, this will choose a random valid spot, if able.
        '''
        #Check for that specific character's storyline
        #Check if Rule applies (by checking if the rule is a subgraph of this graph)
        #Check if the rule that will be applied is a valid continuation in each of the subgraph loc
        #Should return true or false so we know whether there is at least one good insertion point.

        good_insertion_found = False

        is_subgraph, subgraph_locs = self.check_for_pattern_in_storyline(rule.story_condition, character)

        #In order to apply the rule, we need a valid graph location, if we set it to not be "Any".
        
        # for banned_loc in banned_subgraph_locs:
        #     subgraph_locs.remove(banned_loc)

        #Here, we will check each loc in subgraph_locs to see if the continuation from that point on is valid.
        valid_insert_points = []
        
        for potential_insert_point in subgraph_locs:

            purge_count = 0

            if rule.remove_before_insert:
                purge_count = len(rule.story_condition)
            else:
                potential_insert_point += len(rule.story_condition)

            if self.check_continuation_validity(actor=character, abs_step_to_cont_from=potential_insert_point, cont_list=rule.story_change, target_list=rule.target_list, purge_count=purge_count):
                valid_insert_points.append(potential_insert_point)

        check_step = abs_step
        if not rule.remove_before_insert:
            check_step += len(rule.story_condition)

        if check_step not in valid_insert_points and abs_step != -1:
            if verbose:
                print("Pattern not found. Returning False.")
            return False
        
        if len(valid_insert_points) > 0:
            if verbose:
                print("There is at least one valid insert point. Applying Rule.")

            insert_point = abs_step
            if insert_point == -1:
                insert_point = random.choice(subgraph_locs)

            if rule.remove_before_insert:
                #Remove the parts
                self.remove_parts_by_count(insert_point, len(rule.story_condition), character)
            else:
                insert_point += len(rule.story_condition)

            #add the right parts
            #But if we didn't purge anything, we should move our insertion point forward equal to the length of the condition we would've purged
            self.insert_multiple_parts(part_list=rule.story_change, character=character, location_list=location_list, absolute_step=insert_point, copy=True, targets=rule.target_list)
            good_insertion_found = True

        else:
            if verbose:
                print("There are no valid insert points. Rule is not applied.")
        self.refresh_longest_path_length()

        return good_insertion_found

    #Remake this function so that it has basically the same arguments and functionality as add_multiple_characters_to_part because by god this is so outdated.
    #references apply_joint_node and insert_joint_node should be fixed because apparently I screw up in so, so many spots.
    #This function basically works like normal insert story part if the node is not a joint node. How convenient!
    def insert_joint_node(self, joint_node, main_actor=None, other_actors=[], location=None, targets=[], absolute_step=0, copy=True, make_main_actor_a_target = False, timestep=None):
        if make_main_actor_a_target:
            targets.append(main_actor)

        if main_actor is None or make_main_actor_a_target:
            main_actor = other_actors.pop(0)
        
        new_node = self.insert_story_part(part=joint_node, character=main_actor, location=location, absolute_step=absolute_step, copy=copy, targets=targets, timestep=timestep)
        
        #TODO (Important): These two should insert instead of entirely replacing the node.
        for additional_actor in other_actors:
            self.insert_story_part(part=new_node, character=additional_actor, location=location, absolute_step=absolute_step, copy=False, timestep=timestep)
        
        for target in targets:
            self.insert_story_node_for_target(target=target, abs_step=absolute_step, story_part=new_node)
        # self.add_targets_to_storynode(node = new_node, abs_step=absolute_step, target_list=targets)

        return new_node

    #This function only adds a part to a certain step, but it doesn't change the order of other story nodes.
    #This function is going to be deprecated

    # def add_multiple_characters_to_part(self, main_actor, other_actors, part, location=None, targets=[], abs_step=0, timestep=0, copy=True):

    #     new_part = self.add_story_part_at_step(part=part, character=main_actor, location=location, absolute_step=abs_step, timestep=timestep, targets=targets, copy=copy)

    #     for additional_actor in other_actors:
    #         self.add_story_part_at_step(part=new_part, character=additional_actor, location=location, absolute_step=abs_step, timestep=timestep, copy=False)

    #     for target in new_part.target:
    #         self.add_story_node_to_targets_storyline(pot_target=target, abs_step=abs_step, story_part=new_part)

    #     return new_part
    
    '''
    This function is for making the character's next node some node that already exists in another character's path.

    It probably should also check for time paradoxes (to be defined)

    Alright, to prevent time paradoxes, we will not allow joining into any nodes where the timestep numbers are different.

    Lol as it turns out this retains the same wording but now has a different meaning, thanks to the new way to handle timesteps (lol)

    There should be three of these, one for each type of Joint Rule.
    '''

    #To clarify: Targets to test are all actors.
    #This function should assume that all all needed actors and targets are already given.
    #A lot of checks done in the Apply Joint Rule section are redundant, because they are already done here. We might be able to deprecate the checks done in there, just apply the node if it passes the tests in here.
    
    def check_joint_continuity_validity(self, joint_rule, main_character, grouping_split, insert_index, verbose=False):
        
        #First, we must check a few prerequisites. If any characters mentioned in actors_to_test don't exist in the storyline, then we definitely cannot continue the storyline.
        entire_character_list = []
        entire_character_name_list = []

        for split in grouping_split:
            for actor in split["actor_group"]:
                if actor not in self.character_objects:
                    if verbose:
                        print(actor, ": This actor is not found!")
                    return False
                else:
                    entire_character_list.append(actor)
                    entire_character_name_list.append(actor.get_name())
            for target in split["target_group"]:
                if target not in self.character_objects:
                    if verbose:
                        print(actor, ": This target is not found!")
                    return False
                else:
                    entire_character_list.append(target)
                    entire_character_name_list.append(target.get_name())

        #Before anything else, if we're trying to test for cont or split, we must make sure that the node at the insert index fulfill the following conditions:
        # All the actors mentioned share the same node at the given insert_index
        # (That's it that's the only condition)

        # for thing in entire_character_list:
        #     print(thing, main_character, main_character == thing)
        if main_character not in entire_character_list:
            if verbose:
                print("Main character is not among the character list!")
            return False
        
        patternless_join = False

        if joint_rule.joint_type == JointType.JOIN:
            patternless_join = joint_rule.is_patternless_join()

        assumed_node = self.story_parts.get((main_character.get_name(), insert_index-1), None)
        #Oh yeah---to follow a rule there has to be a base graph, therefore, logically there has to be a "previous node". Failing that means there is none graph!
        # TODO: add a little caveat here that if a joinjoint has no pattern it could possibly be used for this purpose.

        if not patternless_join:
            if assumed_node is None:
                if verbose:
                    print("Rule cannot be applied because there is no previous node!")
                return False

        if joint_rule.joint_type == JointType.CONT or joint_rule.joint_type == JointType.SPLIT:

            #If the node at the insert index doesn't have the same characters as the given actors and targets: return False
            #We just need to take the first character from the actors to test, find out what node they're in, and check it for existence of other characters
            #(It does not matter whether they are actors or targets, as long as it's the same characters)
            for actor in entire_character_list:
                if not assumed_node.check_if_character_exists_in_node(actor):
                    if verbose:
                        print(actor, ": This actor is not in the joint story node!")
                    return False

        # If we are doing the Split rule, we must validate that each of the character in actors to test and targets to test are performing nodes included in the base nodes.
        # Before this can be done, we must decide what style of Joint Split we should be doing.
        # We have decided. (See check if abs step has joint pattern)
        if joint_rule.joint_type == JointType.JOIN or joint_rule.joint_type == JointType.CONT:

            # For each of the actors in actors_to_test and target_to_test, turn them into one list. Then, call the list_all_good_combinations_from_joint_join_pattern from UtilFunctions to get a list.
            # After we get the list of all possible combinations, we then look for whether or not our specific combination of actors and targets exist in that list. If not, then return False. Otherwise continue with the check.

            # list_of_testing_actor_names = set()

            # for actor in actors_to_test:
            #     list_of_testing_actor_names.add(actor.get_name())
            # for target in targets_to_test:
            #     list_of_testing_actor_names.add(target.get_name())
            if not patternless_join:
                if joint_rule.joint_type == JointType.JOIN:
                    joint_pattern_check = self.check_if_abs_step_has_joint_pattern(required_story_nodes_list=joint_rule.base_actions, character_name_list=entire_character_name_list, absolute_step_to_search=insert_index-1)
                else:
                    joint_pattern_check = self.check_if_abs_step_has_joint_pattern(required_story_nodes_list=[joint_rule.base_joint], character_name_list=entire_character_name_list, absolute_step_to_search=insert_index-1)
                
                if not joint_pattern_check[0]:
                    if verbose:
                        print("The absolute step doesn't match joint pattern!")
                    return False
                
                list_of_possible_combis = list_all_good_combinations_from_joint_join_pattern(dict_of_base_nodes=joint_pattern_check[1], actors_wanted=joint_rule.joint_node.charcount, current_actor_name=main_character.get_name())
                # print(list_of_possible_combi)

                found_exact_set = False
                for combi in list_of_possible_combis:
                    if set(combi) == set(entire_character_name_list):
                        found_exact_set = True

                if not found_exact_set:
                    if verbose:
                        print("This joint pattern is impossible!")
                    return False
            
        #Might end up with a sampling method for now (Test one random combination to see if it works out). If it doesn't cause too many problems then we can do it this way.
        #Consider: create a list of good splits and then look through to see if there is at least one good split there, if the sampling method doesn't work.
        validity = True
        cont_list = []

        if joint_rule.joint_type == JointType.JOIN or joint_rule.joint_type == JointType.CONT:
            cont_list.append(joint_rule.joint_node)
        if joint_rule.joint_type == JointType.SPLIT:
            cont_list += joint_rule.split_list
        

        # sampled_grouping = self.generate_valid_character_grouping(continuations=cont_list, abs_step=insert_index, character_list = entire_character_list)

        #We already have the grouping, because our input is the grouping (duh)
        #For some reason check add joint validity and check add split validity consumes actor input. I'm making a copy here to prevent that.
        
        if joint_rule.joint_type == JointType.JOIN or joint_rule.joint_type == JointType.CONT:
            if verbose:
                print("Validity is based on Add Joint Validity function")
            validity = validity and self.check_add_joint_validity(joint_node = joint_rule.joint_node, actors_to_test = grouping_split[0]["actor_group"], targets_to_test = grouping_split[0]["target_group"], insert_index=insert_index)
        if joint_rule.joint_type == JointType.SPLIT:
            if verbose:
                print("Validity is based on Add Split Validity function")
            validity = validity and self.check_add_split_validity(split_list=cont_list, chargroup_list=grouping_split, insert_index=insert_index)
            #validity = validity and self.check_add_joint_validity(joint_node = cont_list[test_index], actors_to_test = sampled_grouping[test_index]["actor_group"], targets_to_test = sampled_grouping[test_index]["target_group"], insert_index=insert_index)
        
        # del(copy_of_split)
        
        return validity
    
    #This function is for testing if an absolute step contains a pattern that is suitable for a join joint.
    # Returns true if all of the characters in the soecific timestep are performing 
    def check_if_abs_step_has_joint_pattern(self, required_story_nodes_list, character_name_list, absolute_step_to_search):
        
        dict_of_chars_with_nodename_as_key = dict()

        #List of valid nodes are taken from the required node list. This is taken from 
        valid_nodename_list = [snode.get_name() for snode in required_story_nodes_list]

        for charname in character_name_list:
            found_actor_in_invalid_node = False
            found_node = self.story_parts.get((charname, absolute_step_to_search), None)
            if found_node is not None:
                nodename = found_node.get_name()
                if nodename in valid_nodename_list:
                    if dict_of_chars_with_nodename_as_key.get(nodename, None) == None:
                        dict_of_chars_with_nodename_as_key[nodename] = [charname]
                    else:
                        dict_of_chars_with_nodename_as_key[nodename].append(charname)

                # Case where one of the required characters are seen doing a node
                # that's not one of the valid nodes
                else:
                    found_actor_in_invalid_node = True

        if  found_actor_in_invalid_node:
            return False, dict_of_chars_with_nodename_as_key

        found_node_names = dict_of_chars_with_nodename_as_key.keys()
        for req_node in required_story_nodes_list:
            req_node_name = req_node.get_name()

            #Case where we don't find any characters in one of the required nodes
            if req_node_name not in found_node_names:
                return False, dict_of_chars_with_nodename_as_key
            
        return True, dict_of_chars_with_nodename_as_key

    def check_for_jointrule_location_in_storyline(self, actor, joint_rule):
        if joint_rule.joint_type == JointType.JOIN:

            #For each of the possible base action, at any point if this character is seen performing the base action then add it to the list.
            valid_locs = []

            if joint_rule.is_patternless_join():
                for i in range(0, self.get_longest_path_length_by_character(actor)):
                    valid_locs.append(i)

                    return len(valid_locs) > 0, sorted(list(set(valid_locs)))
            else:
                for base_node in joint_rule.base_actions:
                    valid_locs += self.check_for_pattern_in_storyline([base_node], actor)[1]
                    return len(valid_locs) > 0, sorted(list(set(valid_locs)))

            return self.check_for_pattern_in_storyline()
        if joint_rule.joint_type == JointType.CONT or joint_rule.joint_type == JointType.SPLIT:
            return self.check_for_pattern_in_storyline([joint_rule.base_joint], actor)
        
        return False, []

    def check_add_joint_validity(self, joint_node, actors_to_test, targets_to_test, insert_index):

        graphcopy = deepcopy(self)
        # print(insert_index)
        graphcopy.joint_continuation(abs_step=insert_index, joint_node=joint_node, actors=actors_to_test, target_list=targets_to_test, location=None)
        graphcopy.fill_in_locations_on_self()

        # print("GRAPHCOPY")
        # graphcopy.print_all_node_beautiful_format()
        # print("END GRAPHCOPY")

        validity = graphcopy.check_worldstate_validity_on_own_graph(insert_index)

        actorlist = [x for x in actors_to_test + targets_to_test if type(x) == CharacterNode]

        found_dupe_with_this_name_adjacent = graphcopy.test_if_anyone_in_list_has_adjacent_duped_node_with_given_name(actor_list=actorlist, dupe_node_name=joint_node.name)

        del(graphcopy)

        return validity and not found_dupe_with_this_name_adjacent
    
    def test_if_anyone_in_list_has_adjacent_duped_node_with_given_name(self, actor_list, dupe_node_name):

        for actor in actor_list:
            part_list = self.make_story_part_list_of_one_character(actor)

            if len(part_list) > 1:
                for index in range(0, len(part_list)-1):
                    current_part = part_list[index]
                    next_part = part_list[index+1]
                    # print(current_part.name, next_part.name, dupe_node_name)

                    if current_part.name == next_part.name and current_part.name == dupe_node_name:
                        return True

        return False

    def check_add_split_validity(self, split_list, chargroup_list, insert_index):
        
        graphcopy = deepcopy(self)
        graphcopy.split_continuation(split_list=split_list, chargroup_list=chargroup_list, abs_step=insert_index)
        # graphcopy.split_continuation(split_list, actors_to_test, insert_index, None, target_replace=targets_to_test)
        graphcopy.fill_in_locations_on_self()

        validity = graphcopy.check_worldstate_validity_on_own_graph(insert_index)
        
        del(graphcopy)

        return validity

    def add_story_node_to_targets_storyline(self, pot_target, abs_step, story_part):
        if pot_target in self.character_objects:
            self.add_to_story_part_dict(character_name=pot_target.get_name(), abs_step=abs_step, story_part=story_part)

    #In all cases, we assume that the story part is already populated by all other information except for target information. This function is here for that.
    def insert_story_node_for_target(self, target, abs_step, story_part):
        
        character_path_length = self.get_longest_path_length_by_character(target)
        char_name = target.get_name()

        if abs_step >= character_path_length:

            self.add_story_node_to_targets_storyline(pot_target=target, abs_step=abs_step, story_part=story_part)

        else:
            #first, we need to move everything that comes after this part up by one
            for i in range(character_path_length-1, abs_step-1, -1):
                move_up = self.story_parts.pop((char_name, i))
                self.add_to_story_part_dict(character_name=char_name, abs_step=i+1, story_part=move_up)

            #then, we add a new story part at the spot
            self.add_story_node_to_targets_storyline(pot_target=target, abs_step=abs_step, story_part=story_part)

            # #Connect to Other Nodes.
            # #Firstly, if this isn't the first node, we will connect to the previous node.
            # #The previous node severs its ties with its previous next node and now considers the current node to be its next node.
            # if abs_step-1 >= 0:
            #     prevnode =  self.story_parts[(char_name, abs_step-1)]
            #     prevnode.remove_next_node(target)
            #     prevnode.add_next_node(story_part, target)

            # #Secondly, since to get here we established that a next node exists, we need to add the next node as the current node's next node.
            # story_part.add_next_node(self.story_parts[(char_name, abs_step+1)], target)

        self.refresh_longest_path_length()

    def joint_continuation(self, abs_step, joint_node, actors, location=None, target_list=[]):

        #Applying here is inserting the next node to be the Joint Node for the first character, then having the second character and so on Join in.
        #This is where the copy=false in the add node function comes in handy.
        self.insert_joint_node(joint_node=joint_node, other_actors=actors, location=location, absolute_step=abs_step, targets=target_list)

    def split_continuation(self, split_list, chargroup_list, abs_step, location_list = None, additional_targets_list = []):
        for i in range(0, len(chargroup_list)):
            new_joint = deepcopy(split_list[i])
            new_joint.remove_all_actors()

            current_location = None
            if location_list != None:
                current_location = location_list[i]

            current_target_list = chargroup_list[i]["target_group"]
            if additional_targets_list != None and len(additional_targets_list) != 0:
                current_target_list += additional_targets_list[i]

            self.insert_joint_node(joint_node=split_list[i], main_actor=None, other_actors=chargroup_list[i]["actor_group"], location=current_location, targets=current_target_list, absolute_step=abs_step)

    def generate_all_valid_actor_and_target_splits(self, node, abs_step, character_list):
        list_of_charnames = [x.get_name() for x in character_list]
        all_possible_groupings = all_possible_actor_groupings_with_ranges_and_freesizes([node.charcount, node.target_count], list_of_charnames)
        #print(all_possible_groupings)
        state_at_step = self.make_state_at_step(abs_step)[0] #This is the state where we will check if the characters are compatible with each of their assigned nodes.

        entire_list_of_split_dicts = []
        for current_grouping in all_possible_groupings:
            grouping_dict = {"actor_group":[], "target_group":[]}

            for actor_name in current_grouping[0]:
                grouping_dict["actor_group"].append(state_at_step.node_dict[actor_name])

            for target_name in current_grouping[1]:
                grouping_dict["target_group"].append(state_at_step.node_dict[target_name])

            populated_node = deepcopy(node)
            populated_node.actor.extend(grouping_dict["actor_group"])
            populated_node.actor.extend(grouping_dict["target_group"])

            if state_at_step.test_story_compatibility_with_storynode(populated_node):
                entire_list_of_split_dicts.append(grouping_dict)

        return entire_list_of_split_dicts

    #This function, given a list of characters and a number of characters that should be a target, returns a dict of actor list and target list.
    #Whenever characters are assigned to a joint node where the target count is not 0, call this to make a split.
    def generate_valid_actor_and_target_split(self, node, abs_step, character_list):

        #Before anything is done, sum the allowed character count with the targets wanted count. If there are more characters than this sum, then it's impossible to fulfill.
        #Of course, if either or both is a -1, this means that it's indefinite therefore no limitations.

        #If both limits are -1, then scramble freely. If one or both limits are normal integers, then take care of the integers first, with priority for targets first.

        #We can probably use the same method for the generate valid character grouping below.

        #Of course, we also need to include an exit clause in the event that all the possible combinations are already exhausted.

        #We do this first. Index 0 is for Actors, Index 1 is for Targets

        entire_approved_list = self.generate_all_valid_actor_and_target_splits(node=node, abs_step=abs_step, character_list=character_list)
        #print(entire_approved_list)

        if len(entire_approved_list) == 0:
            return None
        
        random_grouping_from_list = random.choice(entire_approved_list)
        return random_grouping_from_list


    #Generate ALL Valid Character Grouping for use in validity testing, in order to ensure at least one valid case exists.
    def generate_all_valid_character_grouping_for_splitting(self, continuations, abs_step, character_list):

        grouping_size_list = []
        for node in continuations:
            grouping_size_list.append(actor_count_sum(node.charcount, node.target_count))

        list_of_charnames = [x.get_name() for x in character_list]
        all_possible_groupings = all_possible_actor_groupings_with_ranges_and_freesizes(grouping_size_list, list_of_charnames)

        state_at_step = self.make_state_at_step(abs_step)[0] #This is the state where we will check if the characters are compatible with each of their assigned nodes.

        all_valid_groupings = []
        for current_group in all_possible_groupings:
            current_group_with_current_state_charnodes = []

            for current_subgroup in current_group:
                subgroup_char = []
                for charname in current_subgroup:
                    subgroup_char.append(state_at_step.node_dict[charname])
                current_group_with_current_state_charnodes.append(subgroup_char)

            list_of_possible_splits_for_each_cont = []
            for story_index in range(0, len(continuations)):
                current_subgroup_indexed = current_group_with_current_state_charnodes[story_index]
                current_node = continuations[story_index]
                list_of_all_actor_target_split_for_current_cont = self.generate_all_valid_actor_and_target_splits(node=current_node, abs_step=abs_step, character_list=current_subgroup_indexed)
                list_of_possible_splits_for_each_cont.append(list_of_all_actor_target_split_for_current_cont)

            #In the case that there are certain nodes with characters who has no valid spots, permute full range list will not generate anything and the list will be empty
            for item in permute_full_range_list(list_of_possible_splits_for_each_cont):
                all_valid_groupings.append(item)

        # There is no need to run this test again because generate_all_valid_actor_and_target_splits already generates the splits so that each character has a valid spot to stay
        #
        # for grouping_to_test in list_of_combis_to_test:
        #     this_grouping_is_valid = True
        #     for story_index in range(0, len(continuations)):

        #         current_subgroup_to_test = grouping_to_test[story_index]
        #         current_node_to_test = continuations[story_index]

        #         actor_grouping = current_subgroup_to_test["actor_group"]
        #         target_grouping = current_subgroup_to_test["target_group"]

        #         char_compatibility = current_node_to_test.check_character_compatibility_for_many_characters(actor_grouping)
        #         target_compatibility = current_node_to_test.check_target_compatibility_for_many_characters(target_grouping)

        #         this_grouping_is_valid = this_grouping_is_valid and char_compatibility and target_compatibility

        #     #if this grouping is valid after testing all the nodes then it is valid, add it to the list of valid groupings
        #     if this_grouping_is_valid:
        #         all_valid_groupings.append(grouping_to_test)
        # print(list_of_combis_to_test == all_valid_groupings)

        return all_valid_groupings

    def pick_one_random_valid_character_grouping_from_all_valid_groupings(self, continuations, abs_step, character_list, verbose=False):

        character_list_from_ws = []
        current_ws = self.make_state_at_step(stopping_step=abs_step)[0]
        for character in character_list:
            character_list_from_ws.append(current_ws.node_dict[character.get_name()])

        entire_approved_list = self.generate_all_valid_character_grouping_for_splitting(continuations=continuations, abs_step=abs_step, character_list=character_list_from_ws)
        
        if verbose:
            groupingno = 0
            for approved_grouping in entire_approved_list:
                groupno = 0
                for actor_tar_group in approved_grouping:
                    for actor in actor_tar_group["actor_group"]:
                        print("Grouping", groupingno, "NodeGroup", groupno, "Actor", actor)
                    for target in actor_tar_group["target_group"]:
                        print("Grouping", groupingno, "NodeGroup", groupno, "Target", target)
                    groupno += 1
                groupingno += 1

        if len(entire_approved_list) == 0:
            return None
        
        random_grouping_from_list = random.choice(entire_approved_list)
        return random_grouping_from_list


    #Please note that Grouping is a list that is used to determine group size. For example, if it is [1, 3], this means one character in the first group and 3 characters in the second group.
    #This function can now handle targets!
    #Congratulations! This functions works as all is intended. We're all good now on this department.
    def generate_valid_character_grouping(self, continuations, abs_step, character_list):

        # Grouping information is based on the continuations of the story nodes we were given.
        #This also includes the target slots.
        grouping = []

        for node in continuations:
            grouping.append(actor_count_sum(node.charcount, node.target_count))
        
        #print(grouping)
        # #If there is no grouping information, then we only want one character per continuation.
        # if grouping == []:
        #     grouping = [1] * len(character_list)

        #Make the grouping information here.
        list_of_charnames = [x.get_name() for x in character_list]
        all_possible_groupings = all_possible_actor_groupings_with_ranges_and_freesizes(grouping, list_of_charnames)
        #print(all_possible_groupings)

        state_at_step = self.make_state_at_step(abs_step)[0] #This is the state where we will check if the characters are compatible with each of their assigned nodes.

        found_valid_grouping = False

        while (not found_valid_grouping):

            grouping_with_actor_target_info = []
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

                actor_grouping = current_grouping[story_index]
                target_grouping = []
                actor_target_split = self.generate_valid_actor_and_target_split(node=continuations[story_index], abs_step=abs_step, character_list=current_grouping[story_index])
                grouping_with_actor_target_info.append(actor_target_split)

                if continuations[story_index].target_count != 0:
                    #First, we need to ensure there is at least one possible actor/target divide if it just so happens that target slots are needed.
                    if actor_target_split is not None:
                        #In the case that a good actor/target split exists, we use the split information to split them up and put them into different groups.
                        actor_grouping = actor_target_split["actor_group"]
                        target_grouping = actor_target_split["target_group"]
                    else:
                        #In the case that there are no good splits at all, this cannot work. It's not valid and we should use a different grouping.
                        this_one_is_valid = False

                this_one_is_valid = this_one_is_valid and continuations[story_index].check_character_compatibility_for_many_characters(actor_grouping)
                this_one_is_valid = this_one_is_valid and continuations[story_index].check_target_compatibility_for_many_characters(target_grouping)
                #print(current_grouping, this_one_is_valid)

            #If it's valid, it can be returned. If not, find new one.
            if this_one_is_valid:
                return grouping_with_actor_target_info

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
        print("LIST OF NODES IN ", self.name)
        for node in self.story_parts:
            print(node)
            print("Node Name:", self.story_parts[node].get_name())
            print("Timestep", self.story_parts[node].timestep)
            print("Actors:", self.story_parts[node].get_actor_names())
            print("Targets:", self.story_parts[node].get_target_names())
            print("Location:", self.story_parts[node].location.get_name())
            print("----------")
    
    def print_all_nodes_from_characters_storyline(self, actor):
        print("ENTIRE STORYLINE OF", actor.get_name(), "IN", self.name)
        for thing in self.make_story_part_list_of_one_character(character_to_extract=actor):
            print(thing)

    def return_all_nodes_from_characters_storyline_as_stringlist_prettyformat(self, actor):
        return_list = []
        return_list.append("ENTIRE STORYLINE OF " + actor.get_name() + " IN " + self.name)
        for thing in self.make_story_part_list_of_one_character(character_to_extract=actor):
            return_list.append(str(thing) + " " + str(thing.abs_step))
            return_list.append("Node Name: " + thing.get_name())
            return_list.append("Timestep " + str(thing.timestep))
            return_list.append("Actors: " + thing.get_actor_names())
            return_list.append("Targets: " + thing.get_target_names())
            return_list.append("Location: " + thing.location.get_name())
            return_list.append("----------")

        return return_list

    def print_graph_nodes_to_text_file(self, directory, verbose = False):
        if verbose:
            print("Printing Results to Text Files...")

        for actor in self.character_objects:
            if verbose:
                print("Current Character:", actor.get_name())
            stringlist = self.return_all_nodes_from_characters_storyline_as_stringlist_prettyformat(actor=actor)
            
            path_name = directory + actor.get_name() + ".txt"
            f = open(path_name, "w")

            for thing in stringlist:
                f.write(thing)
                f.write("\n")
            
            if verbose:
                print("Character Done:", actor.get_name())

        if verbose:
            print("Finish printing results.")

    def print_all_nodes_from_characters_storyline_beautiful_format(self, actor):
        print("ENTIRE STORYLINE OF", actor.get_name(), "IN", self.name)
        step = 0
        for thing in self.make_story_part_list_of_one_character(character_to_extract=actor):
            print(thing, thing.abs_step)
            print("Node Name:", thing.get_name())
            print("Timestep", thing.timestep)
            print("Actors:", thing.get_actor_names())
            print("Targets:", thing.get_target_names())
            print("Location:", thing.location.get_name())
            print("----------")

    def check_for_pattern_in_storyline(self, pattern_to_test, character_to_extract, verbose=False):

        #preliminary check: check if the character exists inside of the storyline, return false if it does not
        if character_to_extract not in self.character_objects:
            return False, []
        
        #This will return the length of subgraph locs and the list of subgraph locs, just like the function above it.
        #The only difference is that we will require way, way less inputs.
        character_storyline = self.make_story_part_list_of_one_character(character_to_extract)

        #print(character_storyline)

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
        keys_for_this_char = sorted(keys_for_this_char, key=getsecond)

        for cur_index in range(0, len(keys_for_this_char)):
            list_of_char_parts.append(self.story_parts[keys_for_this_char[cur_index]])

        return list_of_char_parts
        
    def remove_parts_by_count(self, start_step, count, actor):
        end_index = start_step + count - 1

        for remove_index in range(start_step, end_index+1):
            self.remove_story_part(actor, start_step)

    #Deprecated function. Since we are doing validity check after the score check, we can just test validity with all the characters present in actors and targets.
    #This function checks if there it at least one spot where the rule can be applied.
    # def check_rule_validity_for_first_actor(self, actor, rule):

    #     if rule.is_joint_rule:
    #         for i in range(0, self.get_longest_path_length_by_character(actor)):

    #             valid_as_actor = self.check_joint_continuity_validity(joint_rule=rule, actors_to_test=[actor], targets_to_test=rule.target_list, insert_index=i)
    #             valid_as_target = self.check_joint_continuity_validity(joint_rule=rule, actors_to_test=[])

    #             if self.check_joint_continuity_validity(joint_rule=rule, actors_to_test=[actor], targets_to_test=rule.target_list, insert_index=i):
    #                 return True
    #         return False

    #     is_subgraph, subgraph_locs = self.check_for_pattern_in_storyline(rule.story_condition, actor)

    #     if not is_subgraph:
    #         return False
        
    #     purge_count = 0
    #     if rule.remove_before_insert:
    #         purge_count = len(rule.story_condition)

    #     for story_index in subgraph_locs:
    #         if self.check_continuation_validity(actor=actor, abs_step_to_cont_from=story_index, cont_list=rule.story_change, target_list=rule.target_list, purge_count=purge_count):
    #             return True
                
    #     return False
    
    #Here, we check that there is at least one valid slot for a character in a joint node.
    def check_if_joint_node_is_valid_at_timestep_for_actor(self, actor, joint_node, step):

        #Get the character at that step
        character_at_step = self.make_state_at_step(step)[0].node_dict[actor.get_name()]

        #This function returns if the character can fit in at least as an actor or a target.
        return joint_node.check_actor_or_target_compatibility(character_at_step)


    def check_continuation_validity(self, actor, abs_step_to_cont_from, cont_list, target_list = None, purge_count = 0, has_joint_in_contlist = False, perform_dupe_check = True):
        #We did the main function, but now we also need to check if the character is being a target, and pull up the requirement for being a target instead if that's the case.
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
        if has_joint_in_contlist:
            graphcopy.insert_multiple_parts_with_joint_and_nonjoint(node_list=cont_list, main_character=actor, abs_step=abs_step_to_cont_from)
        else:
            graphcopy.insert_multiple_parts(cont_list, actor, None, abs_step_to_cont_from, targets=target_list)

        if perform_dupe_check:
            for node in cont_list:
                if graphcopy.test_if_anyone_in_list_has_adjacent_duped_node_with_given_name(actor_list=[actor], dupe_node_name=node.get_name()):
                    return False
        
        graphcopy.fill_in_locations_on_self()
        graphcopy.update_list_of_changes()
        graphcopy.refresh_longest_path_length()

        #We delegate the checking of worldstates fo the worldstate validity function
        validity = graphcopy.check_worldstate_validity_on_own_graph(abs_step_to_cont_from)
        del(graphcopy)

        return validity

    #Help lmao I forgot if this check worldstate validity also includes itself
    #If it does then I have no reason to add another check before adding nodes (we already check ws validity while running apply rule)
    def check_worldstate_validity_on_own_graph(self, start_step=0):
        self.refresh_longest_path_length()

        for check_index in range(start_step, self.longest_path_length):

            #Make the world state
            current_ws_and_validity = self.make_state_at_step(check_index)

            # if not current_ws_and_validity[1]:
            #     return False

            current_ws = current_ws_and_validity[0]

            for current_char in self.character_objects:
                current_step = self.story_parts.get((current_char.get_name(), check_index))
                current_char_at_current_step = current_ws.node_dict[current_char.get_name()]

                if current_step is not None:

                    if (current_char_at_current_step not in current_step.actor) and (current_char_at_current_step not in current_step.target):
                        return False

                    #These two are outdated, because character compatibility and target compatibility are already merged into test_story_compatibility_with_conditiontest 
                    # if current_char_at_current_step in current_step.actor:
                    #     if not current_step.check_character_compatibility(current_char_at_current_step):
                    #         return False

                    # if current_char_at_current_step in current_step.target:
                    #     if not current_step.check_target_compatibility(current_char_at_current_step):
                    #         return False

                    for current_test_to_convert in current_step.required_test_list:

                        equivalent_tests = translate_generic_test(current_test_to_convert, current_step)

                        for current_test_to_check in equivalent_tests:
                            # print(current_test_to_check)
                            if not current_ws.test_story_compatibility_with_conditiontest(current_test_to_check):
                                # print("failed test", current_test_to_check)
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
            
            cur_state = self.make_state_at_step(index)[0]

            for story_char in self.character_objects:

                current_step = self.story_parts.get((story_char.get_name(), index), None)

                if current_step is not None:

                    #Pull the location information from cur_state
                    char_in_ws = cur_state.node_dict[story_char.get_name()]
                    # print(char_in_ws, index)
                    location_holding_char = char_in_ws.get_holder()
                    current_step.set_location(location_holding_char)

    def test_task_validity(self, task: CharacterTask, actor: CharacterNode, abs_step: int):
        #Do all of these things:
        # Make the world state according to the abs_step.
        # Translate generic changes, then test the conditions in the task at the abs_step.
        # Test if the actor is in the same location as the required location.
        # Test if the story nodes in the task action are compatible.
        # ...huh, how do we make it compatible with multiple characters?
        #
        # Something about tasks doesn't play nice with multiple characters... I need a way to manage it somehow
        # 
        # Return true if it passes all the test, return false if it fails even one test.

        #There's also placeholder characters in play. We need to take that into account as well.

        current_ws = self.make_state_at_step(abs_step)[0]

        if task.task_location_name is not None:
            current_loc = current_ws.node_dict.get(task.task_location_name, None)
            if current_loc is None:
                return False
        
        location_has_actor = current_ws.check_connection(node_a = current_loc, edge_name = current_ws.DEFAULT_HOLD_EDGE_NAME, node_b = actor, soft_equal = True)

        placeholder_charname_dict = task.placeholder_info_dict
        placeholder_charobj_pair = [(x[0], current_ws.node_dict[x[1]]) for x in placeholder_charname_dict.items()]
        
        task_valid = True
        for test in task.task_requirement:
            # if test == None:
            #     print(test, task.task_name)
            replaced_test = replace_multiple_placeholders_with_multiple_test_takers(test, placeholder_charobj_pair)
            task_valid = task_valid and current_ws.test_story_compatibility_with_conditiontest(replaced_test)

        translated_task = []
        for story_node in task.task_actions:
            # print(placeholder_charname_dict)
            translated_task.append(replace_placeholders_in_story_node(story_node=story_node, placeholder_dict=placeholder_charname_dict, list_of_actor_objects=self.character_objects))
                                                          
        cont_valid = self.check_continuation_validity(actor=actor, abs_step_to_cont_from=abs_step, cont_list=translated_task, has_joint_in_contlist=True, perform_dupe_check=True)

        # print(cont_valid)
        return location_has_actor and cont_valid

    def get_task_stack_from_actor_at_absolute_step(self, task_stack_name, actor_name, abs_step):
        
        current_ws = self.make_state_at_step(stopping_step=abs_step)[0]
        character_object = current_ws.node_dict.get(actor_name, None)

        if character_object is None:
            return None
        
        return character_object.get_task_stack_by_name(task_stack_name)
    
    def get_list_of_task_stack_names_from_latest_step(self, actor_name):

        last_ws = self.make_latest_state()
        current_actor = last_ws.node_dict[actor_name]
        return current_actor.get_incomplete_task_stack_names()

    '''
    Returns a dict with the following information:

    "last_task_step": The current step of the taskstack. If the value is -1, the task stack is completed.
    "last_update_step": The last step that the task got updated, meaning that the next step of the task advancing should be after this step.
    '''
    def find_last_step_of_task_stack_from_actor(self, task_stack_name, actor_name, verbose=False):

        self.refresh_longest_path_length()

        #The index of the current task in the task list.
        last_task_step = 0
        first_task_step = None
        
        #The absolute step that contains the latest instance of a TaskAdvance Object that affects this task.
        last_graph_step_with_graph_update = 0

        for current_index in range(0, self.longest_path_length+1):

            current_ws = self.make_state_at_step(current_index)[0]
            actor_from_ws = current_ws.node_dict.get(actor_name, None)

            if actor_from_ws is not None:
  
                task_stack_from_ws = actor_from_ws.get_task_stack_by_name(task_stack_name)

                if task_stack_from_ws is not None:
                    if first_task_step == None:
                        first_task_step = current_index
                    if verbose:
                        print("current task index at index ", current_index, "is", task_stack_from_ws.current_task_index)
                    new_last_task_step = task_stack_from_ws.current_task_index
                    
                    if new_last_task_step != last_task_step:
                        last_graph_step_with_graph_update = current_index
                    last_task_step = new_last_task_step

        if verbose:
            print({"last_task_step":last_task_step, "last_update_step":last_graph_step_with_graph_update, "first_task_step":first_task_step-1})
        return {"last_task_step":last_task_step, "last_update_step":last_graph_step_with_graph_update, "first_task_step":first_task_step-1}

    #In order to perform a task, it must both be incomplete and be completable. Otherwise, it's not a valid option to take.
    def test_task_stack_advance_validity(self, task_stack_name, actor_name, abs_step):
        #For the task advancement to be valid:
        #The stack must already not be complete, and the task itself must not already be complete either, and must take place after the last update step
        completeness = self.test_task_completeness(task_stack_name=task_stack_name, actor_name=actor_name, abs_step=abs_step)

        if completeness != "task_step_can_advance":
            return False, completeness
        
        current_ws = self.make_state_at_step(abs_step)[0]
        char_at_ws = current_ws.node_dict[actor_name]
        task_stack = char_at_ws.get_task_stack_by_name(task_stack_name)
        current_task = task_stack.get_current_task()

        #The current task itself must be valid
        
        test_result = self.test_task_validity(task=current_task, actor=char_at_ws, abs_step=abs_step)
        return test_result, completeness
    
    def insert_multiple_parts_with_joint_and_nonjoint(self, node_list, main_character, abs_step, location=None):
        for index in range(0, len(node_list)):

                current_story_part = node_list[index]
                current_insert_index = abs_step+index
                current_location = location

                if current_location is None:
                    current_location = current_story_part.location 

                #If the node is a joint node, apply it like a joint node
                #If it's not a joint node, apply it like a normal node
                if current_story_part.check_if_joint_node():

                    #To do this, we need to check whether the main character is a target or a main character
                    actor_list = []
                    target_list = []
                    make_main_char_target = False

                    if main_character in current_story_part.target:
                        make_main_char_target = True

                        actor_list = [x for x in current_story_part.actor]
                        target_list = [x for x in current_story_part.target if x != main_character]
                    else:
                        actor_list = [x for x in current_story_part.actor if x != main_character]
                        target_list = [x for x in current_story_part.target]                       
                    
                    #We need to reset the character slots when adding story parts, because they already come with translated story nodes.
                    current_story_part.actor = []
                    current_story_part.target = []
                    newnode = self.insert_joint_node(joint_node=current_story_part, main_actor=main_character, other_actors=actor_list, location=current_location, targets=target_list, absolute_step=current_insert_index, make_main_actor_a_target=make_main_char_target)
                else:
                    #We need to reset the character slots when adding story parts, because they already come with translated story nodes.
                    current_story_part.actor = []
                    newnode = self.insert_story_part(part=current_story_part, character=main_character, location=current_location, absolute_step=current_insert_index)

                    
    def attempt_advance_task_stack(self, task_stack_name, actor_name, abs_step, verbose=False):
        # Get the Task Stack Object.
        
        current_ws = self.make_state_at_step(abs_step)[0]
        actor_object = current_ws.node_dict.get(actor_name, None)

        #Return False on Actor None
        if actor_object is None:
            if verbose:
                print("This Actor Object does not Exist!")
            return False
        
        #Return False on Task Stack Object None
        task_stack_object = actor_object.get_task_stack_by_name(task_stack_name)
        if task_stack_object is None:
            if verbose:
                print("This Task Stack doesn't exist!")
            return False    

        # Use test_task_stack_advance_validity to test if task stack can be advanced here

        advance_valid = self.test_task_stack_advance_validity(task_stack_name=task_stack_name, actor_name=actor_name, abs_step=abs_step)
        
        #Task advance is true, we will add the action from the stack's current task to the story node
        if advance_valid[0]:
            if verbose:
                print("Task Step can Advance")
            current_task = task_stack_object.get_current_task()
            story_nodes_to_add = current_task.task_actions

            #do a translation
            translated_nodes = []
            for node in story_nodes_to_add:

                #print(self.placeholder_dicts_of_tasks[(actor_name, task_stack_name)])
                translated_nodes.append(replace_placeholders_in_story_node(story_node=node, placeholder_dict=self.placeholder_dicts_of_tasks[(actor_name, task_stack_name)], list_of_actor_objects=self.character_objects))

            #Insert the task advance stack to the last story node
            last_story_node = translated_nodes[-1]

            task_advance_name = "task_advance_for_" + actor_name + "_" + task_stack_name
            advance_stack_object = TaskAdvance(name=task_advance_name, actor_name=actor_name, task_stack_name=task_stack_name)

            if advance_stack_object not in last_story_node.effects_on_next_ws:
                last_story_node.effects_on_next_ws.append(advance_stack_object)

            #Now, insert each of the story nodes into the story

            #We forgot to account for parts that have multiple characters here. Whoopie!
            #We might need to check if something is a joint node then choose to either self.insert_story_part or self.insert_joint_node
            #
            # Fixed! We now have insert_multiple_parts_with_joint_and_nonjoint which we also use for task validation

            #self.insert_multiple_parts(part_list=translated_nodes, character=actor_object, absolute_step=abs_step, copy=True)
            task_location = current_ws.node_dict[current_task.task_location_name]

            self.insert_multiple_parts_with_joint_and_nonjoint(node_list=translated_nodes, main_character=actor_object, abs_step=abs_step, location=task_location)
            # for index in range(0, len(translated_nodes)):

            #     current_story_part = translated_nodes[index]
            #     current_insert_index = abs_step+index

            #     #If the node is a joint node, apply it like a joint node
            #     #If it's not a joint node, apply it like a normal node
            #     if current_story_part.check_if_joint_node():

            #         #To do this, we need to check whether the main character is a target or a main character
            #         actor_list = []
            #         target_list = []
            #         make_main_char_target = False
 
            #         if actor_object in current_story_part.target:
            #             make_main_char_target = True

            #             actor_list = [x for x in current_story_part.actor]
            #             target_list = [x for x in current_story_part.target if x is not actor_object]
            #         else:
            #             actor_list = [x for x in current_story_part.actor if x is not actor_object]
            #             target_list = [x for x in current_story_part.target]                       
                        
            #         self.insert_joint_node(joint_node=current_story_part, main_actor=actor_object, other_actors=actor_list, location=current_story_part.location, targets=target_list, absolute_step=current_insert_index, make_main_actor_a_target=make_main_char_target)

            #     else:
            #         self.insert_story_part(part=current_story_part, character=actor_object, location=current_story_part.location, absolute_step=current_insert_index, targets=current_story_part.target)

            return True
        else:
            match advance_valid[1]:

                # WS 0 -> Step 0 -> WS 1 -> Step 1 -> WS 2 (Final)...
                #
                # When we're saying that a WorldState is already in a completed state, can something in the past change it so that the quest isn't complete?
                #
                # The quest is for Alice to kill Bob
                # Bob died due to unrelated reasons
                # Alice arrives to see Bob die from unrelated reasons, considers the quest complete
                # Bob gets revived before Alice arrives
                # Quest turns out to be incomplete?!
                #
                # We need to prevent such scenarios from being violated from the first place. We could technically add a "Realize Quest step" which has certain requirements
                # So that when something that would modify the story to be invalid happens before the quest is realized, it can be seen as invalid?
                # Alternatively: Just stuff it in with the node that travels to that location
                #
                #Add a condition check to the location where we also add the Task Advance stack
                #
                #TODO (Extra Features): By technicality there shouldn't be anyone with already a task in WS0, but we can think of a way to handle that later.
                #Get the story node before this step and add task_advance to it
                case "task_step_already_completed":
                    if verbose:
                        print("Task Step is Already Completed, Task Auto Advanced")
                    task_advance_name = "task_advance_for_" + actor_name + "_" + task_stack_name

                    advance_stack_object = TaskAdvance(name=task_advance_name, actor_name=actor_name, task_stack_name=task_stack_name)

                    current_task = task_stack_object.get_current_task()
                    task_advance_node = StoryNode(name=task_advance_name, effects_on_next_ws=[advance_stack_object], required_test_list=current_task.goal_state)

                    self.insert_story_part(part=task_advance_node, character=actor_object, absolute_step=abs_step)
                    self.fill_in_locations_on_self()
                    # previous_story_node.effects_on_next_ws.append(advance_stack_object)
                    return True
                
                #Get the story node at this step and add task_cancel to it
                case "task_step_already_failed":
                    if verbose:
                        print("Task Step is Already Failed, Task Cancelled")
                    task_cancel_name = "task_cancel_for_" + actor_name + "_" + task_stack_name
                    cancel_stack_object = TaskCancel(name=task_cancel_name, actor_name=actor_name, task_stack_name=task_stack_name)

                    current_task = task_stack_object.get_current_task()
                    cancel_task_node = StoryNode(name=task_cancel_name, effects_on_next_ws=[cancel_stack_object], required_test_list=current_task.avoidance_state)

                    self.insert_story_part(part=cancel_task_node, character=actor_object, absolute_step=abs_step)
                    self.fill_in_locations_on_self()
                    # previous_story_node.effects_on_next_ws.append(cancel_stack_object)
                    return True
                
                #Nothing is modified because the task cannot be advanced here
                case _:
                    if verbose:
                        print("Task Step Can't Advance Because",advance_valid[1])
                    return False

        # If true, advance it and add TaskAdvance to the last action of the task. Return True.
        # If false, determine the reason with the completeness output
        # - task_stack_cleared, incompatible: Do Nothing
        # - task_step_already_completed: Add a TaskAdvance in the action before the worldstate in abs_step
        # - task_step_already_failed: Add a TaskCancel in the action before the worldstate in abs_step
        # Return False if it's task_stack_cleared or incompatible. Otherwise, return True.
    
    def test_task_completeness(self, task_stack_name, actor_name, abs_step):

        #Check the last worldstate if they have this task at all. If it doesn't exist in the last world state, then if it doesn't exist in the final world state, return "not_exist"

        latest_ws = self.make_latest_state()
        latest_actor = latest_ws.node_dict[actor_name]

        if latest_actor.get_task_stack_by_name(task_stack_name) is None:
            return "not_exist"

        if latest_actor.get_task_stack_by_name(task_stack_name).remove_from_pool:
            return "already_cancelled"

        #Get the current task step, see how far the task has progressed
        last_task_step = self.find_last_step_of_task_stack_from_actor(task_stack_name=task_stack_name, actor_name=actor_name)

        #Return "task_stack_cleared" if entire stack already completed (last task step is -1)
        if last_task_step["last_task_step"] == -1:
            return "task_stack_cleared"

        #Return "incompatible" if the abs_step chosen is before the last update step (cannot update before the latest change)
        #Also return "incompatible" if the abs_step chosen is equal to the first task step (to prevent accidents)
        if abs_step < last_task_step["last_update_step"] or abs_step == last_task_step["first_task_step"]:
            return "incompatible"
        
        current_ws = self.make_state_at_step(abs_step)[0]
        actor_at_ws = current_ws.node_dict[actor_name]
        task_stack_at_ws = actor_at_ws.get_task_stack_by_name(task_stack_name)

        if actor_at_ws.get_task_stack_by_name(task_stack_name) is None:
            return "not_exist"

        #Return "wrong_location" if the character in the current state isn't in the right location for the task step.
        character_current_location_name = current_ws.get_actor_current_location(actor_at_ws).name
        
        current_task = task_stack_at_ws.task_stack[last_task_step["last_task_step"]]
        if current_task.task_location_name is not None:
            if current_task.task_location_name != character_current_location_name:
                return "wrong_location"

        #Return "task_step_already_completed" if the tests in goal state all return true

        #If there are no goals, then it should return false by default.
        goal_reached = True

        placeholder_charname_dict = task_stack_at_ws.placeholder_info_dict
        placeholder_charobj_pair = [(x[0], current_ws.node_dict[x[1]]) for x in placeholder_charname_dict.items()]

        for test in current_task.goal_state:
            replaced_test = replace_multiple_placeholders_with_multiple_test_takers(test, placeholder_charobj_pair)
            goal_reached = goal_reached and current_ws.test_story_compatibility_with_conditiontest(replaced_test)

        if len(current_task.goal_state) == 0:
            goal_reached = False

        if goal_reached:
            return "task_step_already_completed"
        
        #Return "task_step_already_failed" if the tests in avoidance_state all return true
        #This can never be True if there are no conditions to fail the task.
        task_failed = True

        for test in current_task.avoidance_state:
            replaced_test = replace_multiple_placeholders_with_multiple_test_takers(test, placeholder_charobj_pair)
            
            task_failed = task_failed and current_ws.test_story_compatibility_with_conditiontest(replaced_test)

        if len(current_task.avoidance_state) == 0:
            task_failed = False

        if task_failed:
            return "task_step_already_failed"
        
        #If none of the above conditions are true, return "task_step_can_advance"
        return "task_step_can_advance"

    # This function will be called whenever a story node with a TaskChange object is added to the StoryGraph
    #
    # First, make the world state from that absolute_step
    # Then, we need to fill in the blanks for the TaskStack in the TaskChange object
    # - The Placeholder Dict will be blank and that has to be modified
    #   - With the nature of how insert story part is, we will need to use self.placeholder_dicts_of_tasks to keep any dicts that we have ever created
    #
    # - The Stack Owner and Stack Giver names might be blank and that has to be modified
    #   - Stack Giver is always the story node's actor
    #   - Stack Owner is always the story node's target
    #   - Also, we must force the nodes with have task change to have only one actor/target.
    #
    # After filling in these blanks, return a new TaskChange object with the modified TaskStack

    #Return False and no Task Stack Object vs Return True and a Task Stack Object
    def modify_taskchange_object_on_add(self, abs_step, story_node, taskchange_object):

        current_ws = self.make_state_at_step(abs_step)[0]
        new_task_stack = deepcopy(taskchange_object.task_stack)

        #Setting stack owner and stack giver names, according to the storynode.
        #TODO (Extra Features): There is a case where instead of getting a task from another character (being a target) the character gains a task by interacting with some objects
        #In that case, we change this function below
        #Actually---would it be better to use placeholder objects. It would, wouldn't it?

        #We will disallow multiple characters getting tasks at once, which means task changes can only be used on nodes with 1 or 2 actors.

        equivalent_taskchange = translate_generic_taskchange(taskchange_object, story_node)

        new_task_stack.stack_giver_name = equivalent_taskchange[0].task_giver_name
        new_task_stack.stack_owner_name = equivalent_taskchange[0].task_owner_name

        #We're checking here if theres already a dict here. If not then we're going to create a new one
        task_placeholder_dict = self.placeholder_dicts_of_tasks.get((new_task_stack.stack_owner_name, new_task_stack.stack_name), None)

        if task_placeholder_dict == None:

            task_placeholder_list = current_ws.make_list_of_possible_task_stack_character_replacements(new_task_stack)

            if len(task_placeholder_list) <= 0:
                return False, None
            
            task_placeholder_dict = random.choice(task_placeholder_list)
            self.placeholder_dicts_of_tasks[(new_task_stack.stack_owner_name, new_task_stack.stack_name)] = task_placeholder_dict

        new_task_stack.placeholder_info_dict = task_placeholder_dict

        for task in new_task_stack.task_stack:
            task.placeholder_info_dict = task_placeholder_dict

        return True, new_task_stack

    def return_current_task_from_task_stack_for_actor(self, absolute_step, actor_name, task_stack_name):

        stack = self.get_task_stack_from_actor_at_absolute_step(abs_step=absolute_step, actor_name=actor_name, task_stack_name=task_stack_name)

        if stack is None:
            return None
        
        return stack.get_current_task()

    # def perform_next_task_from_task_stack_for_actor(self, absolute_step, actor, task_stack_name):
        #First, get the world state at the abs step

        #Check if the task with this name exists at the task stack name. If not, return False.

        #Check if the conditions of the task is already fulfilled, if it is, put the task advance object in this worldstate, then return True.
        #Check if the conditions for failing the task is already fulfilled, if it is, return False.

        #Check the validity of the task stack with self.test_task_validity. If it's valid, then add all the story nodes to the absolute step, then apply the task advance object in this world state. Return True.
    
    # TODO: Test this function
    def task_object_setup_for_character(self, character_name):
        list_of_tasks = []
        latest_ws = self.make_latest_state()
        char_from_ws = latest_ws.node_dict[character_name]

        for stack_name in char_from_ws.get_incomplete_task_stack_names():
            task_stack_info = self.find_last_step_of_task_stack_from_actor(task_stack_name=stack_name, actor_name=character_name)
            new_task_stack = TaskStack(stack_name=stack_name)
            new_task_stack.char_from_ws.copy_all_attributes(char_from_ws.get_task_stack_by_name(stack_name))
            new_task_stack.task_stack = new_task_stack.task_stack[task_stack_info["last_task_step"]:]

            list_of_tasks.append(new_task_stack)

        return list_of_tasks
    
    #To measure Cost and Preference (Cost by finding "Important" actions, Encounter by finding nodes with an "Encounter", Preference by countings things that aren't marked with "Filler" i.e. moving and waiting)
    def count_story_nodes_with_tag_in_characters_story_line(self, character, desired_tag_list = [], soft_equal=False, intersect_instead_of_union=False):

        list_of_nodes = self.make_story_part_list_of_one_character(character_to_extract=character)

        node_with_tag_count = 0
        for node in list_of_nodes:

            node_qualifies = False

            tag_list = node.tags.keys()

            all_tags_found = True
            one_tag_found = False

            for check_pair in desired_tag_list:
                story_node_tag = check_pair[0]
                story_node_value = check_pair[1]
                
                all_tags_found = all_tags_found and story_node_tag in tag_list
                one_tag_found = one_tag_found or story_node_tag in tag_list

                if not soft_equal and node.tags.get(story_node_tag, None) is not None:
                    all_tags_found = all_tags_found and node.tags[story_node_tag] == story_node_value
                    one_tag_found = all_tags_found or node.tags[story_node_tag] == story_node_value
            
            if intersect_instead_of_union:
                node_qualifies = all_tags_found
            else:
                node_qualifies = one_tag_found

            if node_qualifies:
                node_with_tag_count += 1

        return node_with_tag_count

    #To measure Uniqueness
    def count_unique_story_nodes_in_characters_story_line(self, character):
        
        seen_nodes = []

        list_of_nodes = self.make_story_part_list_of_one_character(character_to_extract=character)

        for node in list_of_nodes:

            if node not in seen_nodes:
                seen_nodes.append(node)
        
        return len(seen_nodes)

    # To measure Jointability
    def count_jointable_nodes_in_characters_story_line(self, character):

        joint_nodes = []

        list_of_nodes = self.make_story_part_list_of_one_character(character_to_extract=character)

        for node in list_of_nodes:

            if node.check_if_joint_node():
                joint_nodes.append(node)
        
        return len(joint_nodes)
    
    def get_metric_score(self, metric_type : MetricType, character:CharacterNode):

        character_story_length = self.get_longest_path_length_by_character(character=character)

        relevant_nodes_found = 0
        match metric_type:
            case MetricType.COST:
                relevant_nodes_found = self.count_story_nodes_with_tag_in_characters_story_line(character=character, desired_tag_list=[("costly", True)])
            case MetricType.UNIQUE:
                relevant_nodes_found = self.count_unique_story_nodes_in_characters_story_line(character=character)
            case MetricType.JOINTS:
                relevant_nodes_found = self.count_jointable_nodes_in_characters_story_line(character=character)
            case MetricType.PREFER:
                relevant_nodes_found = self.count_story_nodes_with_tag_in_characters_story_line(character=character, desired_tag_list=[("important_action", True)])

        return round((relevant_nodes_found / character_story_length), 2) * 100
            
    # score_retention: How much the program cares about past graphs?
    # 0 score_retention (Always forgets past graphs --- only remembers the current graph)
    # 1 score_retention (Always remembers past graphs)
    # Any number in between: Past graph's scores are multiplied by that value to the power of the number of graphs that succeeds it.

    # Example: score_retention 0.8 with 5 graph would mean this:
    # Graph 1 * 0.8^4
    # Graph 2 * 0.8^3
    # Graph 3 * 0.8^2
    # Graph 4 * 0.8^1
    # Graph 5 * 0.8^0
    
    def get_multigraph_metric_score(self, metric_type:MetricType, character:CharacterNode, previous_graphs = [], score_retention = 0):
        
        current_score = self.get_metric_score(metric_type=metric_type, character=character)

        if score_retention > 1:
            score_retention = 1
        if score_retention < 0:
            score_retention = 0

        if len(previous_graphs) > 0 and score_retention > 0:
            past_score_times_len = []
            forgotten_past_score_times_len = []
            past_graph_total_nodes = []
            forgotten_past_graph_total_nodes = []

            for past_graph in previous_graphs:
                this_graphscore = past_graph.get_metric_score(metric_type=metric_type, character=character)
                this_graphlength = past_graph.get_longest_path_length_by_character(character)
                past_score_times_len.append(this_graphscore * this_graphlength)
                past_graph_total_nodes.append(this_graphlength)

            forgetfulness_exponent = len(past_score_times_len)

            for index in range(0, len(previous_graphs)):
                
                forgetfulness_multiplier = math.pow(score_retention, forgetfulness_exponent)
                forgotten_past_score_times_len.append(past_score_times_len[index] * forgetfulness_multiplier)
                forgotten_past_graph_total_nodes.append(past_graph_total_nodes[index] * forgetfulness_multiplier)
                forgetfulness_exponent -= 1

            current_graphlength = self.get_longest_path_length_by_character(character=character)
            current_score_multed = current_score * self.get_longest_path_length_by_character(character=character)
            current_score = sum(forgotten_past_score_times_len, start=current_score_multed) / sum(forgotten_past_graph_total_nodes, start=current_graphlength)

        return current_score

    def test_if_given_node_list_will_follow_metric_rule(self, metric : StoryMetric, node_list, step, purge_count = 0, previous_graphs = [], score_retention = 0, verbose = False):
        
        graphcopy = deepcopy(self)
        if purge_count > 0:
            graphcopy.remove_parts_by_count(start_step=step, count=purge_count, actor = metric.character_object)
        graphcopy.insert_multiple_parts(part_list=node_list, character=metric.character_object, absolute_step=step)

        current_score = self.get_metric_score(metric_type=metric.metric_type, character=metric.character_object)
        new_score = graphcopy.get_metric_score(metric_type=metric.metric_type, character=metric.character_object)

        #Index 0 has past graph's score and index 1 has that graph's length

        #This works like how it would used to as long as there is a score_retention of greater than 0 and no previous graph.
        if len(previous_graphs) > 0 and score_retention > 0:
            
            current_score = self.get_multigraph_metric_score(metric_type=metric.metric_type, character=metric.character_object, previous_graphs=previous_graphs, score_retention=score_retention)
            new_score = graphcopy.get_multigraph_metric_score(metric_type=metric.metric_type, character=metric.character_object, previous_graphs=previous_graphs, score_retention=score_retention)

            if verbose:
                print("Calculated Scores (current -> new) :", current_score, "->", new_score)

        score_delta = new_score - current_score
        follows_metric_rule = False

        match metric.metric_mode:
            case MetricMode.LOWER:
                follows_metric_rule = score_delta <= 0 or new_score <= metric.value
            case MetricMode.HIGHER:
                follows_metric_rule = score_delta >= 0 or new_score >= metric.value
            case MetricMode.STABLE:
                if current_score > metric.value:
                    follows_metric_rule = score_delta <= 0 or new_score <= metric.value
                elif current_score < metric.value:
                    follows_metric_rule = score_delta >= 0 or new_score >= metric.value
                else:
                    follows_metric_rule = abs(score_delta) <= 5
        if verbose:
            print("follows_metric_rule value:", follows_metric_rule)
        return follows_metric_rule
        #TODO: Test if the new score follows the metrics' rules. Reminder:
        # Keep Lower: Decreasing the score is not allowed if doing so would take the score out of the acceptable range.
        # Keep Higher: Increasing the score is not allowed if doing so would take the score out of the acceptable range.
        # Keep Stable: If current score is greater than the desired score, acts as Keep Lower. If current score is lesser than the desired score, acts as Keep Higher.
            

def make_list_of_changes_from_list_of_story_nodes(story_node_list):
    # print("Begin Making List of Changes")
    changeslist = []
    
    dupeless_node_list = remove_dupe_nodes(story_node_list)

    for snode in dupeless_node_list:
        for change in snode.effects_on_next_ws:
            changes_from_snode = translate_generic_change(change, snode)
            changeslist.extend(changes_from_snode)

    return changeslist
        
def remove_dupe_nodes(node_list):
    sanitized_list = []

    for node in node_list:
        if node not in sanitized_list:
            sanitized_list.append(node)

    return sanitized_list

def calculate_score_from_char_and_unpopulated_node_with_both_slots(actor, node, world_state, mode=0):

    # If one of the slots is BAD, then return the good slot.
    # If BOTH slots are bad, return Default Invalid Value

    target_populated_node = deepcopy(node)
    target_populated_node.target.append(actor)

    actor_populated_node = deepcopy(node)
    actor_populated_node.actor.append(actor)

    calculate_list = []

    if world_state.test_story_compatibility_with_actor_slot_of_node(story_node = node, actor = actor):
        calculate_list.append(world_state.get_score_from_story_node(actor_populated_node))

    if world_state.test_story_compatibility_with_target_slot_of_node(story_node = node, actor = actor):
        calculate_list.append(world_state.get_score_from_story_node(target_populated_node))

    if len(calculate_list) <= 0:
        return DEFAULT_INVALID_SCORE

    if mode == 1:
        return statistics.mean(calculate_list) + node.biasweight
    
    else:
        return max(calculate_list) + node.biasweight
    

    

