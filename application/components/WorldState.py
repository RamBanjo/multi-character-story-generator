from copy import deepcopy
import random
from application.components.CharacterTask import CharacterTask, TaskStack
import sys
sys.path.insert(0,'')

from application.components.Edge import Edge
from application.components.RelChange import *
from application.components.StoryNode import *
from application.components.StoryObjects import CharacterNode, LocationNode, ObjectNode
from application.components.UtilFunctions import *
from application.components.UtilityEnums import *

class WorldState:
    def __init__(self, name, objectnodes=[], DEFAULT_HOLD_EDGE_NAME = "holds", DEFAULT_ADJACENCY_EDGE_NAME = "connects"):

        '''
        Graph properties
        Name: Name of the graph
        objectnodes: The list of nodes!
        node_dict: The list of nodes, which can be looked up by name in the node dict
        '''
        self.name = name
        self.objectnodes = objectnodes
        self.edges = []
        self.node_dict = dict()
        self.make_node_dict()

        self.DEFAULT_HOLD_EDGE_NAME = DEFAULT_HOLD_EDGE_NAME
        self.DEFAULT_ADJACENCY_EDGE_NAME = DEFAULT_ADJACENCY_EDGE_NAME

    '''
    Node Attributes
    '''

    def export_object_as_dict(self) -> dict:

        export_dict = dict()
        export_dict["name"] = self.name
        export_dict["object_node_dicts"] = []

        for story_object in self.objectnodes:
            export_dict["object_node_dicts"].append(story_object.export_object_as_dict())

        export_dict["edges"] = []

        for my_edge in self.edges:
            export_dict["edges"].append(my_edge.export_object_as_json())

        #Not exporting Node Dict itself, you can build it later with the object nodes here
        return export_dict

    def set_node_name(self, node: ObjectNode, new_name):
        del self.node_dict[node.get_name]
        self.node_dict[new_name] = node
        node.set_name = new_name

    def add_node(self, node: ObjectNode):
        self.objectnodes.append(node)
        self.node_dict[node.get_name()] = node

    def add_nodes(self, nodes: list):
        for thing in nodes:
            self.add_node(thing)

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

    def check_connection(self, node_a: ObjectNode, node_b: ObjectNode, edge_name=None, edge_value=None, soft_equal=False):

        node_a_retrieved = self.node_dict.get(node_a.get_name(), None)
        node_b_retrieved = self.node_dict.get(node_b.get_name(), None)
        
        if node_a_retrieved is None or node_b_retrieved is None:
            return False

        check_name = True

        if edge_name is None:
            check_name = False

        for edge in self.edges:
            if not soft_equal and (edge.from_node == node_a_retrieved and edge.to_node == node_b_retrieved and edge.get_value() == edge_value) and (not check_name or edge.get_name() == edge_name):
                return True
            if soft_equal and (edge.from_node == node_a_retrieved and edge.to_node == node_b_retrieved) and (not check_name or edge.get_name() == edge_name):
                return True
        
        return False

    def check_double_connection(self, node_a: ObjectNode, node_b: ObjectNode, edge_name=None, edge_value=None, soft_equal = False):
        return self.check_connection(node_a, node_b, edge_name, edge_value, soft_equal) and self.check_connection(node_b, node_a, edge_name, edge_value, soft_equal)

    def check_unique_incoming(self, node: ObjectNode, edge_name : str):
        node_retrieved = self.node_dict.get(node.get_name(), None)

        if node_retrieved is None:
            return False
        
        list_of_incoming = node_retrieved.get_incoming_edge(edgename = edge_name)
        return len(list_of_incoming) == 1
    
    def check_unique_outgoing(self, node: ObjectNode, edge_name : str):
        node_retrieved = self.node_dict.get(node.get_name(), None)

        if node_retrieved is None:
            return False
        
        list_of_outgoing = node_retrieved.get_outgoing_edge(edgename = edge_name)
        return len(list_of_outgoing) == 1

    def list_location_adjacencies(self):
        print("Location Adjacencies:")

        locations_in_dict = [loco for loco in self.node_dict.values() if ('Type', 'Location') in loco.tags.items()]

        for location in locations_in_dict:
            adjacencies = self.node_dict[location.get_name()].get_adjacent_locations_list(self.DEFAULT_ADJACENCY_EDGE_NAME)

            texttoprint = location.get_name()
            texttoprint += " -> "

            for in_edge in adjacencies:
                texttoprint += in_edge.from_node.get_name()
                texttoprint += ", "
            if len(adjacencies) > 0:
                print(texttoprint[:-2])
            else:
                print(location.get_name(), "has no adjacencies!")

    def make_list_of_nodes_from_tag(self, tag, value):
        
        list_of_applicable_object_nodes = []

        for objectnode in self.node_dict.values():
            if objectnode.tags[tag] == value:
                list_of_applicable_object_nodes.append(objectnode)

        return list_of_applicable_object_nodes

    '''
    connect
    '''
    def connect(self, from_node: ObjectNode, edge_name, to_node: ObjectNode, value = None):

        #new edge
        new_edge = Edge(edge_name, from_node, to_node, value)
        
        #don't add if there are dupes
        if new_edge in self.edges:
            return

        #add stuff to the nodes
        from_node.add_outgoing_edge(new_edge)
        to_node.add_incoming_edge(new_edge)

        self.edges.append(new_edge)

    def doubleconnect(self, from_node: ObjectNode, edge_name, to_node: ObjectNode, value = None):

        self.connect(from_node = from_node, edge_name = edge_name, to_node = to_node, value = value)
        self.connect(from_node = to_node, edge_name = edge_name, to_node = from_node, value = value)

    def disconnect(self, from_node, edge_name, to_node, value = None, soft_equal = False):

        to_remove = Edge(edge_name, from_node, to_node, value)

        for my_edge in self.edges:
            if (not soft_equal and my_edge == to_remove) or (soft_equal and to_remove.soft_equal(my_edge)):
                my_edge.from_node.outgoing_edges.remove(to_remove)
                my_edge.to_node.incoming_edges.remove(to_remove)
                self.edges.remove(to_remove)


    def is_subgraph(self, other_world_state):
        #Okay, same deal with the other subgraph functions here:
        #If everything in self is contained in the other graph then it is a subgraph
        #To do this, we check every node and edge in this graph to see if it's contained within the other world state

        #TODO (Extra Features): Use HashTable/Dict to optimize speed if it turns out this is super inefficient later on

        result = True

        for node in self.objectnodes:
            result = result and node in other_world_state.objectnodes

        for edge in self.edges:
            result = result and edge in other_world_state.edges

        return result

    def apply_some_change(self, changeobject, reverse=False):
        if changeobject.changetype == ChangeType.RELCHANGE:
            return self.apply_relationship_change(changeobject, reverse)
        if changeobject.changetype == ChangeType.TAGCHANGE:
            return self.apply_tag_change(changeobject, reverse)
        if changeobject.changetype == ChangeType.RELATIVETAGCHANGE:

            current_object = self.node_dict.get(changeobject.object_node_name, None)
            current_value = current_object.tags.get(changeobject.tag, None)
            
            if current_object is None or current_value is None:
                return False

            multiplier = 1
            if reverse:
                multiplier = -1

            new_value = current_value + (changeobject.value_delta * multiplier)

            equivalent_changeobject = TagChange(name="Equivalent Tagchange", object_node_name=changeobject.object_node_name, tag=changeobject.tag, value=new_value, add_or_remove=ChangeAction.ADD)

            return self.apply_tag_change(tagchange_object=equivalent_changeobject, reverse=False)

        if changeobject.changetype == ChangeType.RELATIVEBIASCHANGE:

            current_object = self.node_dict.get(changeobject.object_node_name, None)

            if current_object == None:
                return False

            if type(current_object) == CharacterNode:
                current_value = current_object.biases[changeobject.bias]

                multiplier = 1
                if reverse:
                    multiplier = -1

                new_value = current_value + (changeobject.biasvalue_delta * multiplier)

                if new_value > 100:
                    new_value = 100
                if new_value < -100:
                    new_value = -100

                current_object.biases[changeobject.bias] = new_value

            return True

    # For each item in this world state, find the corresponding object in the previous WorldState. Then, run tests given in the conditionalchange, replacing the placeholder token with the object.
    # If all the tests are passed, apply the change, by calling apply relationship change and apply tag change from this very same worldstate. Phew!

    # Note: We need to look at the state of the Previous World State, not this current world state. The changes should only be applied if and only if the previous world state passed those tests.
    def apply_conditional_change(self, condchange_object, previous_ws, reverse=False):

        for item in self.node_dict.values():

            item_name = item.name
            current_object = previous_ws.node_dict[item_name]
            
            pass_test = previous_ws.check_if_this_object_passes_all_tests(test_list_with_placeholder=condchange_object.list_of_condition_tests, object_to_test=current_object)

            if pass_test:
                for change in condchange_object.list_of_changes:
                    translated_change = replace_placeholder_object_with_change_haver(changeobject=change, change_haver=current_object, placeholder_object=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER)
                    self.apply_some_change(translated_change, reverse=reverse)

        return True

    # Make it address for the case where the input is a list instead of a node. All of the members of the list would need to be addressed.
    # Not needed: We can simply loop through the entire list and run this function for each item in the list.
    def apply_relationship_change(self, relchange_object, reverse=False):
        # print(relchange_object)
        if (relchange_object.add_or_remove == ChangeAction.ADD and not reverse) or (relchange_object.add_or_remove == ChangeAction.REMOVE and reverse):
            #If the intention is to add, then we add a connection between the nodes
            #If either nodes don't exist already, then they must be added to the list of nodes.
            #Checks if either nodes already exists in the node dict
            #If it doesn't exist, add it to the node dict
            # print(relchange_object)
            if relchange_object.node_a.get_name() not in self.node_dict:
                self.node_dict[relchange_object.node_a.get_name()] = relchange_object.node_a
            if relchange_object.node_b.get_name() not in self.node_dict:
                self.node_dict[relchange_object.node_b.get_name()] = relchange_object.node_b
            #After adding nodes that don't already exist, make the connections and add it to the list of edges

            if relchange_object.two_way:
                # print("Yippee, we are Doubleconnecting!")
                self.doubleconnect(from_node=self.node_dict[relchange_object.node_a.get_name()], edge_name = relchange_object.edge_name, to_node = self.node_dict[relchange_object.node_b.get_name()], value=relchange_object.value)
            else:
                self.connect(from_node=self.node_dict[relchange_object.node_a.get_name()], edge_name = relchange_object.edge_name, to_node = self.node_dict[relchange_object.node_b.get_name()], value=relchange_object.value)
            
        if (relchange_object.add_or_remove == ChangeAction.REMOVE and not reverse) or (relchange_object.add_or_remove == ChangeAction.ADD and reverse):
            #If the intention is to remove, then we remove this specific edge between the nodes (if it exists)
            #Don't delete the nodes, though
            #Check if this exact edge between these exact nodes exists
            
            node_a_retrieved = self.node_dict.get(relchange_object.node_a.get_name(), None)
            node_b_retrieved = self.node_dict.get(relchange_object.node_b.get_name(), None) #if self.check_connection(node_a=node_a_retrieved, node_b=node_b_retrieved, edge_name=relchange_object.edge_name, edge_value=relchange_object.value, soft_equal=relchange_object.soft_equal):
            
            
            self.disconnect(from_node=node_a_retrieved, edge_name=relchange_object.edge_name, to_node=node_b_retrieved, value=relchange_object.value, soft_equal=relchange_object.soft_equal)
            if relchange_object.two_way:
                self.disconnect(from_node=node_b_retrieved, edge_name=relchange_object.edge_name, to_node=node_a_retrieved, value=relchange_object.value, soft_equal=relchange_object.soft_equal)

            # check_edge = Edge(relchange_object.edge_name, relchange_object.node_a, relchange_object.node_b)

            # for my_edge in self.edges:
            #     if my_edge == check_edge:
            #         my_edge.from_node.outgoing_edges.remove(check_edge)
            #         my_edge.to_node.incoming_edges.remove(check_edge)
            #         self.edges.remove(check_edge)

        return True

    def apply_tag_change(self, tagchange_object, reverse=False):

        tagchange_object_from_ws = self.node_dict.get(tagchange_object.object_node_name, None)
        if tagchange_object_from_ws == None:
            return False

        if (tagchange_object.add_or_remove == ChangeAction.ADD and not reverse) or (tagchange_object.add_or_remove == ChangeAction.REMOVE and reverse):
            self.node_dict[tagchange_object.object_node_name].set_tag(tagchange_object.tag, tagchange_object.value)
        if (tagchange_object.add_or_remove == ChangeAction.REMOVE and not reverse) or (tagchange_object.add_or_remove == ChangeAction.ADD and reverse):
            self.node_dict[tagchange_object.object_node_name].remove_tag(tagchange_object.tag)

        return True

    #It does this for each of the placeholder listed in actor_placeholder_string_list:
    #It cycles through (oh this again?) all the characters excluding the task giver and the task owner to put as the placeholder
    #It will return as a list of dict with the placeholder as key and the name of the character as value (all possible dicts)
    #This inclusion isn't final, we still need to test with the story graphs (where replacements will also be done)
    #TODO (Extra Features): Do we really need this? Discuss
    def make_list_of_possible_task_character_replacements(self, taskobject):

        eligible_character_names = [x.get_name() for x in self.node_dict.values() if x.tags["Type"] == "Character"]

        #The character performing this task and the character who gave this task aren't legible placeholders
        eligible_character_names.remove(taskobject.task_owner_name)
        eligible_character_names.remove(taskobject.task_giver_name)

        #Determine how many placeholders we need to fill by measuring the length of placeholders needed
        number_of_placeholder_chars_needed = len(taskobject.actor_placeholder_string_list)

        if number_of_placeholder_chars_needed > len(eligible_character_names):
            return []
        
        possible_combs = all_possible_actor_groupings_with_ranges_and_freesizes([number_of_placeholder_chars_needed, -1], eligible_character_names)
        possible_combs = [thing[0] for thing in possible_combs]
        permuted_possible_combs = []

        for thing in possible_combs:
            permuted_possible_combs.extend(thing)

        valid_comb_dict_list = []
        #We will replace the placeholders with the actual characters to see if they pass the condition. If they do pass the condition, they're added to valid comb list.
        for unchecked_comb in permuted_possible_combs:
            placeholder_charname_zip = zip(taskobject.actor_placeholder_string_list, unchecked_comb)
            placeholder_charname_zip.append((GenericObjectNode.TASK_GIVER, taskobject.task_giver_name))
            placeholder_charname_zip.append((GenericObjectNode.TASK_OWNER, taskobject.task_owner_name))
            placeholder_charobj_zip = [(x[0], self.node_dict[x[1]]) for x in placeholder_charname_zip]

            validity = True
            for test in taskobject.task_requirement:
                
                translated_test = replace_multiple_placeholders_with_multiple_test_takers(test=test, placeholder_tester_pair_list=placeholder_charobj_zip)
                validity = validity and self.test_story_compatibility_with_conditiontest(translated_test)

            if validity:
                valid_comb_dict_list.append(unchecked_comb)

        return valid_comb_dict_list
    
    def make_list_of_possible_task_stack_character_replacements(self, task_stack_object: TaskStack):

        eligible_character_names = [x.get_name() for x in self.node_dict.values() if x.tags["Type"] == "Character"]

        #The character performing this task and the character who gave this task aren't legible placeholders

        if task_stack_object.stack_giver_name in eligible_character_names:
            eligible_character_names.remove(task_stack_object.stack_giver_name)
        if task_stack_object.stack_owner_name in eligible_character_names:
            eligible_character_names.remove(task_stack_object.stack_owner_name)
        
        task_stack_object.make_placeholder_string_list()

        #Determine how many placeholders we need to fill by measuring the length of placeholders needed
        number_of_placeholder_chars_needed = len(task_stack_object.actor_placeholder_string_list)

        if number_of_placeholder_chars_needed > len(eligible_character_names):
            return []

        possible_combs = permute_actor_for_task_stack_requirements(actor_name_list=eligible_character_names, placeholder_fill_slots=number_of_placeholder_chars_needed)
        permuted_possible_combs = []

        for thing in possible_combs:
            permuted_possible_combs.extend(list(itertools.permutations(thing)))

        valid_comb_dict_list = []

        #We will replace the placeholders with the actual characters to see if they pass the condition. If they do pass the condition, they're added to valid comb list.

        for unchecked_comb in permuted_possible_combs:
            placeholder_charname_zip = list(zip(task_stack_object.actor_placeholder_string_list, unchecked_comb))

            if task_stack_object.stack_giver_name is not None:
                placeholder_charname_zip.append((GenericObjectNode.TASK_GIVER, task_stack_object.stack_giver_name))
            if task_stack_object.stack_owner_name is not None:
                placeholder_charname_zip.append((GenericObjectNode.TASK_OWNER, task_stack_object.stack_owner_name))

            return_dict = dict(placeholder_charname_zip)

            placeholder_charobj_zip = [(x[0], self.node_dict[x[1]]) for x in placeholder_charname_zip]

            validity = True

            for stack_require_test in task_stack_object.task_stack_requirement:
                translated_test = replace_multiple_placeholders_with_multiple_test_takers(test=stack_require_test, placeholder_tester_pair_list=placeholder_charobj_zip)
                validity = validity and self.test_story_compatibility_with_conditiontest(translated_test)

                #print(translated_test, validity)
            #Editing this to take into account changes in World State and moving characters to proper locations

            simulated_ws = deepcopy(self)

            for task_index in range(0, len(task_stack_object.task_stack)):
                #We will do the movement of character / transformation of world state / testing validity with the simulated WS so it doesn't affect the main WS

                #First we move our current character to the correct task location if they aren't already there
                task_object = task_stack_object.task_stack[task_index]
                task_owner_object = simulated_ws.node_dict[task_stack_object.stack_owner_name]
                current_location = simulated_ws.get_actor_current_location(task_owner_object)
                task_location = simulated_ws.node_dict[task_object.task_location_name]

                if current_location != task_location:
                    simulated_ws.disconnect(from_node=current_location, edge_name=self.DEFAULT_HOLD_EDGE_NAME, to_node=task_owner_object)
                    simulated_ws.connect(from_node=task_location, edge_name=self.DEFAULT_HOLD_EDGE_NAME, to_node=task_owner_object)

                frozen_current_state = deepcopy(simulated_ws)

                if task_index > 0:
                    for story_node in task_stack_object.task_stack[task_index-1].task_actions:

                        story_node.location = current_location

                        for change in story_node.effects_on_next_ws:
                            equivalent_change = translate_generic_change(change=change, populated_story_node=story_node)

                            for equiv_change in equivalent_change:
                                translated_change = replace_multiple_placeholders_with_multiple_change_havers(change=equiv_change, placeholder_tester_pair_list=placeholder_charobj_zip)
                                match change.changetype:
                                    case ChangeType.CONDCHANGE:
                                        simulated_ws.apply_conditional_change(translated_change, frozen_current_state)
                                    case _:
                                        simulated_ws.apply_some_change(translated_change)

                #Finally, run all the tests that apply to the current world state.
                for test in task_stack_object.task_stack[task_index].task_requirement:
                    
                    translated_test = replace_multiple_placeholders_with_multiple_test_takers(test=test, placeholder_tester_pair_list=placeholder_charobj_zip)
                    validity = validity and self.test_story_compatibility_with_conditiontest(translated_test)


            if validity:
                valid_comb_dict_list.append(return_dict)

        return valid_comb_dict_list

    #Not here, it will be for the SG2WS
    # def replace_task_placeholders(self, taskobject, replacements):
    #     pass

    # Reverse not Implemented
    #
    # Actually...yeah I think we need to test the change in world state with the Story Graph. Oof.
    def apply_task_change(self, taskchange_object, verbose=False):

        
        task_stack = deepcopy(taskchange_object.task_stack)
        
        if verbose:
            print("TaskStack Object", task_stack)

        possible_list = self.make_list_of_possible_task_stack_character_replacements(task_stack)
        if len(possible_list) <= 0:
            if verbose:
                print("There are no possible combs! Returning False")
            return False
        
        #This will be assigned before coming here.
        if task_stack.placeholder_info_dict is None:
            if verbose:
                print("There is no dict assigned! Returning False")
            return False
        
        actor = self.node_dict[taskchange_object.task_owner_name]
        actor.add_task_stack(task_stack)
        if verbose:
            print("Nothing is wrong---task stack is added. Returning True.")
        return True

    #This is going to be a problem---because we call all the changes from the same function, there's no way to call this properly...
    #There is no need to make modifications here because SG2WS already takes into account the extra arg. Wooh yeah!

    #Reverse not Implemented
    def apply_task_advance_change(self, taskadvancechange_object, abs_step = 0):
        actor = self.node_dict.get(taskadvancechange_object.actor_name, None)

        if actor is None:
            return False
        
        task_stack = actor.get_task_stack_by_name(taskadvancechange_object.task_stack_name)

        if task_stack is None:
            return False
        
        if not task_stack.mark_current_task_as_complete(completion_step = abs_step):
            return False

        return True

    def apply_task_cancel_change(self, taskcancelchange_object):
        actor = self.node_dict[taskcancelchange_object.actor_name]

        if actor is None:
            return False
        
        task_stack = actor.get_task_stack_by_name(taskcancelchange_object.task_stack_name)

        if task_stack is None:
            return False
        
        task_stack.remove_from_pool = True

        return True

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

    def return_all_edges_as_string_list(self):
        string_list = []
        string_list.append("=== List of Edges in {} ===".format(self.name))
        for edge in self.edges:
            string_list.append("- {}".format(edge))
        
        return string_list
    
    def print_wsedges_to_text_file(self, directory, verbose = False):
        if verbose:
            print("Printing World State...")

        strings_to_print = self.return_all_edges_as_string_list()

        path_name = directory + self.name + ".txt"
        f = open(path_name, "w")

        for thing in strings_to_print:
            f.write(thing)
            f.write("\n")

        f.close()    
        if verbose:
            print("Finish printing results.")

    def test_story_compatibility_with_storynode(self, story_node):

        compatibility_result = True
        
        test_list = []

        for test in story_node.required_test_list:
            equivalent_test = translate_generic_test(test, story_node)
            test_list.extend(equivalent_test)

        for condtest in test_list:
            compatibility_result = compatibility_result and self.test_story_compatibility_with_conditiontest(condtest)

        return compatibility_result
    
    #Returns true if there is at least one configuration for the StoryNode that makes the conditions correct
    def test_story_compatibility_with_actor_slot_of_node(self, story_node, actor):
        
        actor_from_ws = self.node_dict[actor.get_name()]
        current_location = self.get_actor_current_location(actor=actor)
        for target_slot_actor in self.get_all_actors():
            if actor_from_ws != target_slot_actor:
                nodecopy = deepcopy(story_node)
                nodecopy.set_location(current_location)
                nodecopy.add_actor(actor_from_ws)
                nodecopy.add_target(target_slot_actor)

                if self.test_story_compatibility_with_storynode(nodecopy):
                    del(nodecopy)
                    return True

        del(nodecopy)
        return False
                

    def test_story_compatibility_with_target_slot_of_node(self, story_node, actor):

        actor_from_ws = self.node_dict[actor.get_name()]
        current_location = self.get_actor_current_location(actor=actor)
        for actor_slot_actor in self.get_all_actors():
            if actor_from_ws != actor_slot_actor:
                nodecopy = deepcopy(story_node)
                nodecopy.set_location(current_location)
                nodecopy.add_actor(actor_slot_actor)
                nodecopy.add_target(actor_from_ws)

                if self.test_story_compatibility_with_storynode(nodecopy):
                    del(nodecopy)
                    return True

        del(nodecopy)
        return False
                
    def get_score_from_story_node(self, story_node):
        test_list = []

        for test in story_node.suggested_test_list:
            
            equivalent_test = translate_generic_test(test, story_node)
            test_list.extend(equivalent_test)

        return self.get_score_from_list_of_test(test_list)

    def get_score_from_list_of_test(self, list_of_tests):
        score = 0

        for test in list_of_tests:
            if self.test_story_compatibility_with_conditiontest(test):
                score += test.score

        return score

    def test_story_compatibility_with_conditiontest(self, test):

        #Check what kind of test is going to be done here
        test_type = test.test_type
        test_result = False

        match test_type:
            case TestType.HELD_ITEM_TAG:
                test_result = self.held_item_tag_check(holder_test=test.holder_to_test, value_test=test.tag_to_test, tag_test=test.value_to_test)
            case TestType.SAME_LOCATION:
                test_result = self.same_location_check(check_list=test.list_to_test)
            case TestType.HAS_EDGE:
                if not test.only_test_uniqueness:
                    if not test.two_way:
                        test_result = self.check_connection(node_a=test.object_from_test, node_b=test.object_to_test, edge_name=test.edge_name_test, edge_value=test.value_test, soft_equal=test.soft_equal)
                    else:
                        test_result = self.check_double_connection(node_a=test.object_from_test, node_b=test.object_to_test, edge_name=test.edge_name_test, edge_value=test.value_test, soft_equal=test.soft_equal)
                if test.unique_incoming_test:
                    test_result = self.check_unique_incoming(node=test.object_to_test, edge_name=test.edge_name_test)
                if test.unique_outgoing_test:
                    test_result = self.check_unique_outgoing(node=test.object_from_test, edge_name=test.edge_name_test)
            case TestType.HAS_TAG:
                test_result = self.has_tag_test(object_to_test=test.object_to_test, tag=test.tag, value=test.value, soft_equal=test.soft_equal)
            case TestType.IN_BIAS_RANGE:
                test_result = self.bias_range_check(object_to_test=test.object_to_test, bias_axis=test.bias_axis, min_accept=test.min_accept, max_accept=test.max_accept)
            case TestType.TAG_VALUE_IN_RANGE:
                test_result = self.tag_value_in_range_test(object_to_test=test.object_to_test, tag=test.tag, value_min = test.value_min, value_max = test.value_max)
            case TestType.SOMETHING_PASSES_ALL:
                test_result = self.check_at_least_one_object_pass_all_tests(test_list_with_placeholder=test.list_of_tests_with_placeholder)
            case TestType.OBJECT_PASSES_ONE:
                test_result = self.check_if_this_object_passes_at_least_one_test(test_list_with_placeholder=test.list_of_tests_with_placeholder, object_to_test=test.object_to_test)
            case TestType.OBJECT_EQUALITY:
                test_result = self.object_equality_from_ws(object_list=test.object_list)
            # case TestType.HAS_DOUBLE_EDGE:
            #     test_result = self.check_double_connection(test.object_from_test, test.object_to_test, test.edge_name_test, test.value_test, test.soft_equal)
            case _:
                test_result = False

        if test.inverse:
            return not test_result
            
        return test_result

    def object_equality_from_ws(self, object_list):
        
        previous_object = None
        for thing in object_list:
            # print(thing)
            thing_from_ws = self.node_dict[thing.name]
            
            if previous_object is not None:
                if thing_from_ws != previous_object:
                    return False
            
            previous_object = thing_from_ws
    
        return True
    
    #In order to ensure that all nodes called are from the worldstate directly, we will use the object name to invoke them
    def same_location_check(self, check_list):
        list_from_this_ws = []

        for item in check_list:
            list_from_this_ws.append(self.node_dict.get(item.get_name(), None))
            list_from_this_ws = list(filter(lambda a: a is not None, list_from_this_ws))
        
        return WorldState.check_items_in_same_location(list_from_this_ws)

    def held_item_tag_check(self, holder_test, tag_test, soft_equal, value_test=None):
        holder = self.node_dict.get(holder_test.get_name(), None)

        if holder is None:
            return False

        return holder.check_if_this_item_holds_item_with_tag(tag=tag_test, value=value_test, soft_equal=soft_equal, holds_rel_name=self.DEFAULT_HOLD_EDGE_NAME)

    def bias_range_check(self, object_to_test, bias_axis, min_accept, max_accept):
        object_node = self.node_dict.get(object_to_test.get_name(), None)

        if object_node is None:
            return False
        
        if type(object_node) != CharacterNode:
            return False
        
        return object_node.check_bias_range(bias_axis=bias_axis, min_accept=min_accept, max_accept=max_accept)
    
    def has_tag_test(self, object_to_test, tag, value, soft_equal):

        if object_to_test is None:
            return False

        object_node = self.node_dict.get(object_to_test.get_name(), None)

        if object_node is None:
            return False
        
        return object_node.check_if_this_item_has_tag(tag=tag, value=value, soft_equal=soft_equal)
    
    def tag_value_in_range_test(self, object_to_test, tag, value_min, value_max):
        object_node = self.node_dict.get(object_to_test.get_name(), None)

        if object_node is None:
            return False
        
        tag_value = object_node.tags.get(tag)

        if tag_value is None:
            return False
        
        if tag_value < value_min or tag_value > value_max:
            return False

        return True

    def check_at_least_one_object_pass_all_tests(self, test_list_with_placeholder):

        for object_node in self.node_dict.values():
            if self.check_if_this_object_passes_all_tests(test_list_with_placeholder=test_list_with_placeholder, object_to_test=object_node):
                return True
            
        return False

    def check_if_this_object_passes_all_tests(self, test_list_with_placeholder, object_to_test):

        for test in test_list_with_placeholder:
            translated_test = replace_placeholder_object_with_test_taker(test=test, test_taker=object_to_test, placeholder_object=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER)
            
            if not self.test_story_compatibility_with_conditiontest(translated_test):
                return False
            
        return True
    
    def check_if_this_object_passes_at_least_one_test(self, test_list_with_placeholder, object_to_test):

        for test in test_list_with_placeholder:
            translated_test = replace_placeholder_object_with_test_taker(test=test, test_taker=object_to_test, placeholder_object=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER)

            if self.test_story_compatibility_with_conditiontest(translated_test):
                return True
            
        return False

    @staticmethod
    def check_items_in_same_location(item_checklist):
        #If there is one item or less in the list, return true
        if len(item_checklist) <= 1:
            return True
        else:
            #If it's not empty, first get the location of the first item in the list
            location_to_check = item_checklist[0].get_holder()
            list_of_things_at_checkloc = location_to_check.get_list_of_things_held_by_this_item()
            same_location = True

            for check_thing in item_checklist:
                same_location = same_location and check_thing in list_of_things_at_checkloc

            return same_location

    def make_split_joint_grouping_from_current_state(self, split_nodes, potential_actor_names):

        actor_count = len(potential_actor_names)

        grouping_info = []

        for node in split_nodes:
            grouping_info.append(actor_count_sum(node.charcount, node.target_count))

        possible_grouping_lists = permute_all_possible_groups_with_ranges_and_freesize(grouping_info, actor_count)

        print(possible_grouping_lists)

    def make_list_of_reachable_locations_from_location(self, starting_location):
        seen_locations = [starting_location]
        queue = [starting_location]
        
        while len(queue) > 0:
            current_loc = self.node_dict[queue.pop().get_name()]
            adjacent_locs = current_loc.get_adjacent_locations_list(adjacent_rel_name=self.DEFAULT_ADJACENCY_EDGE_NAME, return_as_objects=True)

            #Add to Queue if the locations weren't already seen
            queue_extend = [x for x in adjacent_locs if x not in seen_locations]
            queue.extend(queue_extend)

            #Mark the locations adjacent to current as seen   
            unseen_adjacent_locs = [x for x in adjacent_locs if x not in seen_locations]
            seen_locations.extend(unseen_adjacent_locs)

        return seen_locations
    
    def count_reachable_locations_from_location(self, starting_location):
        return len(self.make_list_of_reachable_locations_from_location(starting_location=starting_location))
    
    def test_reachability(self, starting_location, destination):

        fixed_destination = self.node_dict[destination.get_name()]
        seen_locations = [starting_location]
        queue = [starting_location]
        
        while len(queue) > 0:
            current_loc = self.node_dict[queue.pop().get_name()]
            adjacent_locs = current_loc.get_adjacent_locations_list(adjacent_rel_name=self.DEFAULT_ADJACENCY_EDGE_NAME, return_as_objects=True)

            #Add to Queue if the locations weren't already seen
            queue_extend = [x for x in adjacent_locs if x not in seen_locations]
            queue.extend(queue_extend)

            #Mark the locations adjacent to current as seen
            unseen_adjacent_locs = [x for x in adjacent_locs if x not in seen_locations]
            seen_locations.extend(unseen_adjacent_locs)
            if fixed_destination in seen_locations:
                return True

        return False
    
    def measure_distance_between_two_locations(self, starting_location, destination, verbose=False):

        if starting_location == destination:
            return 0
        
        if not self.test_reachability(starting_location=starting_location, destination=destination):
            return -1

        fixed_destination = self.node_dict[destination.get_name()]
        seen_locations = [starting_location]
        queue = [starting_location]
        distance_dict = dict()
        distance_dict[starting_location.get_name()] = 0

        while len(queue) > 0:
            current_loc = self.node_dict[queue.pop().get_name()]
            adjacent_locs = current_loc.get_adjacent_locations_list(adjacent_rel_name=self.DEFAULT_ADJACENCY_EDGE_NAME, return_as_objects=True)

            #Add to Queue if the locations weren't already seen
            queue_extend = [x for x in adjacent_locs if x not in seen_locations]
            queue.extend(queue_extend)

            #Mark the locations adjacent to current as seen
            unseen_adjacent_locs = [x for x in adjacent_locs if x not in seen_locations]
            
            for unseenloc in unseen_adjacent_locs:                
                min_adjacent_distance = 1e7
                loc_adjacents = unseenloc.get_adjacent_locations_list(adjacent_rel_name=self.DEFAULT_ADJACENCY_EDGE_NAME, return_as_objects=True)

                for adj in loc_adjacents:
                    adj_distance = distance_dict.get(adj.get_name(), None)
                    if adj_distance != None and adj_distance < min_adjacent_distance:
                        min_adjacent_distance = adj_distance + 1
                if verbose:
                    print(starting_location.get_name(),"->",unseenloc.get_name(),"=",min_adjacent_distance)
                distance_dict[unseenloc.get_name()] = min_adjacent_distance
            seen_locations.extend(unseen_adjacent_locs)

            if fixed_destination.get_name() in distance_dict.keys():
                return distance_dict[destination.get_name()]

        return -1

    #What this function should do: return one of the many possible paths to get to that location.
    # The path is formatted like [A, B, ..., C] where A is the current location and C is the destination location
    #If there's no possible path, then return None
    #I think this can be done using recursion?

    #Wait no frick, do we really have to do the shortest path? Maybe the shortest path could be more dangerous and it would be more practical to take the longer path in that case?
    #Or maybe the main character would take the shortest path, but they would also want to be smart about it and take a slight detour to do another task, then return on the main path to do the quest?
    
    #Okay, okay, I got an idea, and I'm writing this down even though this isn't normally my workday. I'm doing so so I don't forget about this later.
    # 1. Check for tasks in current location
    # 1.1 If there are tasks in current location, do those tasks
    # 1.2 If there aren't any tasks in current location, look for tasks in adjacent locations
    # 1.2.1 If there are tasks in adjacent locations, head to one of the locations with tasks to do randomly, weighted by number of tasks
    # 1.2.2 If there are not any tasks in adjacent locations, look for tasks in one of the adjacent-adjacent locations, excluding the places we have already looked, starting with one of the adjacent locations randomly, repeat until a task is found or all nodes are found without tasks
    # 2. The final output should be a tuple with the following information: (Task Location, Number of Tasks, Path towards that Location, Actions to Take At the Location)
    # 2.1 To get the task location, follow algorithm written in 
    # 2.2 To get the Number of Tasks, do 2.1 and grab the number of tasks there.
    # 2.3 To get the path towards location, each time 1.2.1 and 1.2.2 are called, add the current location to the path, so all locations have the path getting there from base location at all times.
    # 3. How to Manage Tasks?
    # 3.1 We can add a new property to CharacterNode called List of Tasks
    # 3.2 We can add a new ChangeObject called TaskChange that Adds or Removes tasks
    # 3.3 Task Management sounds a bit tough. 
    # (SG2WS) Write a function called Perform Task, where if the character is in the correct location, it will add the task's actions to the character's storyline and mark the task as complete.
    # def get_path_towards_target_location(self, current_location, target_location, current_path = []):

    #     current_path.append(current_location)
    #     if current_location == target_location:
    #         return current_path

    #If the current location has tasks, return the current location.
    #If the current location does not have tasks but at least one adjacent location has tasks, return an adjacent location.
    #If the current location does not have tasks and adjacent locations don't have tasks either, continue looking for tasks, recording the distance towards nearest task. When a task is found, attempt to pick a location with the lowest number..
    #If there are no tasks at all, return return one random reachable location, including the current location.
    #
    # (Note that some tasks don't have locations therefore cannot be located, and must be done based on other conditions)

    def get_actor_current_location(self, actor):

        actor_from_ws = self.node_dict[actor.get_name()]
        return actor_from_ws.get_incoming_edge(self.DEFAULT_HOLD_EDGE_NAME)[0].from_node
    
    def get_optimal_location_towards_task(self, actor, verbose=False, return_all_possibilities=False, extra_probability_to_wait_if_no_valid = 0):
        actor_from_ws = self.node_dict[actor.name]        
        actor_task_stacks = [x for x in actor_from_ws.list_of_task_stacks if not x.remove_from_pool]
        current_location = self.get_actor_current_location(actor=actor)
        
        names_of_locations_with_tasks = set()
        task_location_count_dict = dict()
        list_of_current_tasks = []

        #We're getting all the task locations from here
        for task_list in actor_task_stacks:
            if task_list.current_task_index != -1:
                list_of_current_tasks.append(task_list.get_current_task())

        for task in list_of_current_tasks:
            if task.task_location_name is None:
                continue
            elif task.task_location_name not in names_of_locations_with_tasks:
                names_of_locations_with_tasks.add(task.task_location_name)
                task_location_count_dict[task.task_location_name] = 1
            else:
                task_location_count_dict[task.task_location_name] += 1

        reachable_location_list = self.make_list_of_reachable_locations_from_location(current_location)
        reachable_location_names = set([x.get_name() for x in reachable_location_list])

        names_of_reachable_locations_with_tasks = names_of_locations_with_tasks.intersection(reachable_location_names)

        #If the current location has tasks, return the current location.
        if current_location.get_name() in names_of_reachable_locations_with_tasks:
            if verbose:
                print("Current location has a task.")
            if return_all_possibilities:
                return [current_location]
            return current_location
        
        #If there aren't anywhere with tasks, return one random reachable location.
        if len(names_of_reachable_locations_with_tasks) == 0:
            valid_locations = current_location.get_adjacent_locations_list(adjacent_rel_name=self.DEFAULT_ADJACENCY_EDGE_NAME, return_as_objects=True)
            valid_locations.append(current_location)
            if verbose:
                print("There are no reachable locations with tasks found.")

            if extra_probability_to_wait_if_no_valid > 0:
                diceroll = random.random()
                if diceroll <= extra_probability_to_wait_if_no_valid:
                    if verbose:
                        print("The RNG says: Make This One Wait")
                    if return_all_possibilities:
                        return [current_location]
                    return current_location

            if return_all_possibilities:
                return valid_locations
            
            return random.choice(valid_locations)
        
        #If there's no tasks in the current location, look for tasks that are in adjacent locations.
        adjacent_locations = current_location.get_adjacent_locations_list(adjacent_rel_name=self.DEFAULT_ADJACENCY_EDGE_NAME, return_as_objects=True)

        names_of_adjacent_locations = set()
        for loc in adjacent_locations:
            names_of_adjacent_locations.add(loc.get_name())      

        if current_location.get_name() not in names_of_reachable_locations_with_tasks:
            names_of_adjacent_locations_with_tasks = names_of_adjacent_locations.intersection(names_of_reachable_locations_with_tasks)

            if len(names_of_adjacent_locations_with_tasks) > 0:
                if verbose:
                    print("At least one adjacent location has a task.")
                if return_all_possibilities:
                    return [self.node_dict[x] for x in names_of_adjacent_locations_with_tasks]
                return self.node_dict[random.choice(list(names_of_adjacent_locations_with_tasks))]
            
        #If all previous tests fail, then we need to find the closest path towards the next task, because there certainly is one that doesn't include our own.
        adjacent_locations = current_location.get_adjacent_locations_list(adjacent_rel_name=self.DEFAULT_ADJACENCY_EDGE_NAME, return_as_objects=True)

        #Finding distance from here and locations with task. Find distance between all adjacent nodes and all locations with tasks. For each location that's at minimum, add as candidate.
        if verbose:
            print("There is a task but it's not in an adjacent location. Finding closest route towards task.")
        
        distance_dict = dict()
        minimum_distance = 1e7
        for task_location_name in names_of_reachable_locations_with_tasks:
            
            task_location = self.node_dict[task_location_name]

            distance_dict[task_location_name] = self.measure_distance_between_two_locations(current_location, task_location)
            if distance_dict[task_location_name] < minimum_distance:
                distance_dict[task_location_name] = minimum_distance

        #This line finds the locations with tasks that have the least distance between current location and the task locations
        names_of_taskloc_with_min_distance = [x[0] for x in distance_dict.items() if x[1] == minimum_distance]

        min_distance_of_adj_loc_dict = dict()

        for adjlocname in names_of_adjacent_locations:
            min_distance_of_adj_loc_dict[adjlocname] = 1e7

        overall_min_dist_towards_task = 1e7

        for adjlocname in names_of_adjacent_locations:
            minimum_distance_to_find_task_from_adjloc = 1e7

            for mindisttasklocname in names_of_taskloc_with_min_distance:
                mindistloc = self.node_dict[mindisttasklocname]
                adjloc = self.node_dict[adjlocname]

                distance = self.measure_distance_between_two_locations(adjloc, mindistloc)

                if distance < minimum_distance_to_find_task_from_adjloc:
                    minimum_distance_to_find_task_from_adjloc = distance

            min_distance_of_adj_loc_dict[adjlocname] = minimum_distance_to_find_task_from_adjloc

            if minimum_distance_to_find_task_from_adjloc < overall_min_dist_towards_task:
                overall_min_dist_towards_task = minimum_distance_to_find_task_from_adjloc

        #This line finds the locations adjacent to current location that have the least distance between itself and at least one of the task locations
        next_location_candidate_names = [x[0] for x in min_distance_of_adj_loc_dict.items() if x[1] == overall_min_dist_towards_task]
        
        if return_all_possibilities:
            return [self.node_dict[x] for x in next_location_candidate_names]
        
        return self.node_dict[random.choice(next_location_candidate_names)]
    
    def make_all_actors_forget_tasks(self):
        all_actors = self.get_all_actors()

        for actor in all_actors:
            actor.remove_all_task_stacks()

    def get_all_locations(self):
        return [x for x in self.node_dict.values() if type(x) == LocationNode]
    
    def get_all_actors(self):
        return [x for x in self.node_dict.values() if type(x) == CharacterNode]
    
    def get_all_location_names(self):
        return [x.get_name() for x in self.node_dict.values() if type(x) == LocationNode]




            
            