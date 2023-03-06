import random
from components.StoryGraph_old_2 import StoryNode
from components.StoryGraph_old_2 import StoryGraph
from components.StoryNode import StoryNode
from components.StoryObjects import ObjectNode
from components.StoryObjects import CharacterNode
from components.StoryObjects import LocationNode
from components.RewriteRules_old_2 import *
from components.UtilFunctions import RelationshipChange

'''
This function will return a story graph that is generated according to the given specifications.

Returns StoryGraph object.

Arguments:
base_story (StoryGrpah): The base story graph that the story will be built around.
minimum_satisfy_length (int): The minimum length that the generation should generate up to. Once this length is reached for all character routes, the generation stops.
rules_to_use (list, containing RewriteRules): The rules that can be applied to the story. The rules applied to the story will be chosen from this list.
(optional) constraint_list (list, containing Constraints): The list of constraints to be checked against. If applying a rule would violate one of these constraints, a different rule should be chosen.
(optional) metrics_to_measure (list, containing Metrics): The metrics we are using to measure the story. Scoring will help choose the best rules to apply.
'''
def generate_story_from_starting_graph(base_story, minimum_satisfy_length, rules_to_use, constraint_list=[], metrics_to_measure=[], top_picks=0):
    # 1. First, take in the base story.

    # This dict will be used to check story length. It will also be updated as replacement rules are applied to it.
    route_lengths = dict()

    for character in base_story.character_objects:
        route_lengths[character.get_name()] = base_story.get_longest_path_length_by_character(character)

    # 2. Check if all the routes are at least the minimum length
    # If all the routes have the right length, exit the loop (Step 9).
    while(check_if_all_values_in_list_exceed(route_lengths.values, minimum_satisfy_length)):

        # 3. If you're still here, some routes still needs more length. Here, make a list of the characters with shortest routes.
        shortest_route_length = min(route_lengths.values)
        characters_with_shortest_routes = [shortchar for shortchar in base_story.character_objects if base_story.get_longest_path_length_by_character(shortchar) == shortest_route_length]
        
        # 4. Randomly pick one character from the shortest-route-list. We will apply a rule for this character.
        current_char = random.choice(characters_with_shortest_routes)

        # If this character isn't suppoed to act yet (current timestep would not be their first timestep yet) then they must do the Wait action. Lock this in and skip to step 7.
        if current_char.start_timestep > shortest_route_length+1:
            new_story_node = StoryNode("Wait", None, None, {"Action": "Do Nothing"}, 1)
            previous_node = base_story.story_parts[(current_char.get_name(), shortest_route_length)]
            base_story.add_story_part(new_story_node, current_char, previous_node.get_location(), previous_node.timestep, copy=True)
            route_lengths[current_char.get_name()] = base_story.get_longest_path_length_by_character(current_char)
        else:


            list_of_applicable_rules = []

        # 5. Make a list of all the possible continuations for the chosen character.
        #   A rule is considered applicable if it is compatible with the character and has at least 1 subgraph.
            for rule in rules_to_use:

                subgraph_exists, subgraph_locs = StoryGraph.is_subgraph(rule.story_condition, base_story, rule.dummychar, current_char)

                if rule.check_compatibility(current_char) and subgraph_exists:
                   list_of_applicable_rules.append((rule, subgraph_locs))

        # If there is a metric, then rank them and limit the list to the top picks according to those metrics

            if len(metrics_to_measure) > 0:
                pass

            new_story_added = False
        # 6. Randomly choose one rule from the list to apply
            while len(list_of_applicable_rules) > 0:
                current_rule_loc_tuple = random.choice(list_of_applicable_rules)
                current_rule, current_loclist = current_rule_loc_tuple[0], current_rule_loc_tuple[1]
                rule_validity = True

        # If there is at least one constraint, check if applying this rule would violate the constraint.
        #    If there is a violation, eliminate this rule from the list and return to choosing.
                if len(constraint_list) > 0:
                    pass

        # Check that there is at least one spot to properly apply the rule to without it violating the story that has already been generated.
        #   For example, if this replacement rule would cause another character to be dead at Absolute Step 3, then the dead character should have no more actions after that step.
        #   If there are no valid placement positions at all, this rule isn't valid. Remove this rule from the list and return to choosing.
                
                coord_validity = False
                invalid_rule_coords = []

                for potential_coord in current_loclist:
                    #Replace True with a function that checks the coord's validity
                    coord_validity = coord_validity or True

                    #Also, if a coord isn't valid due to it violating future world states, add it to this list.
                    if True:
                        invalid_rule_coords.append(potential_coord)
                    pass

                if not coord_validity:
                    #None of these coords present a valid scenario, so we'll have to remove this rule from the list.
                    rule_validity = False
        
        # If the rule is a joint one, check what kind of joint it is.
        # Joining Joint: Check other characters in the shortest-route-list and make a list of characters that can join the joint in that step.
        # Eligible characters are characters who are not locked in by other actions
        # (such as nodes marked with tags that would not let them come join this node) in that absolute step
        # For example:
        # Char. A has a Joint Node where he talks to someone at a bar, but Char. B can't join because he's fighting a dragon and he can't leave the fight to talk to A, and then go back to the fight.
        #    If there aren't enough characters to satisfy this, then eliminate this rule from the list and return to choosing.
        # Continuous Joint: We don't assign actor_list yet, we will assign it once the absolute step is chosen.
        # Splitting Joint: Same as above.
                actor_list = []
                if current_rule.is_joint_rule:
                    pass
                
        # This line checks if the rule is not valid. If it's not, then it gets removed from the possible list.
                if not rule_validity:
                    list_of_applicable_rules.remove(current_rule_loc_tuple)

        # 7. If you're here, the chosen rule has past the tests given above, therefore it will be applied.
        # Keep in mind, any invalid coords will be excluded.
                else:
        
        # The location needs to be decided.
        # Check the Potential Replacement if it's a node that changes the location.
        # If there is, then for each one of those, pick a valid location. Then, from that point on that character's location will change.
        # To dictate this change, add a RelChange object to this node.
        # At the end of sorting out 

                    

                    if current_rule.is_joint_rule:

                        # Check what kind of Joint Rule it is

                        old_location = base_story.story_nodes[(current_char.get_name, shortest_route_length-1)].get_location()
                        new_location = old_location

                        # List of relationship changes given the node keys and values
                        # Function:
                        # Input: Input the List of NodeKey, NodeValue, and RelationshipChanges.
                        # Output: Return None if there is no Relationship Change, Return List of Relationship Change Objects if there is a Relationship Change
                        
                        if base_story.base_joint.tags.get("movement", None) == "change_location":
                            new_rl_edge = "is_in"

                            #pick new random location
                            new_location = base_story.world_states[shortest_route_length-1]

                            #Apply this for each of the actors in the joint node.
                            #Remove the old location,
                            new_relchange = RelationshipChange()

                        #if base_story.base_joint.tags.get("item", None) == "pick_up":
                        #    new_rl_edge = "holds"

                        #if base_story.base_joint.tags.get("item", None) == "drop":
                        #    new_rl_edge = "holds"

                        #... and so on.

                        # If it does, randomize the next location, put the new location as base joint's target
                        # If it's a splitting joint, each of the new node's locations are random, then add all those new locations as targets in base joint

                        base_story.apply_joint_rule(current_rule, actor_list, )
                    else:

                        # Check entire length of rule
                        # For each rule that has no "change_location" tag, the location stays the same
                        # If there is a "change_location" tag, then a random adjacent location is chosen for the next node
                        # This new location will also be

                        base_story.apply_rewrite_rule()

        # This will also update the world states. Since WorldState is no longer tied to the StoryGraph, it must be updated separately.
        # To do this, we must check if the step where the worldstate is added already has a world state.
        # If there isn't one, copy the world state from the previous absolute step.
        # After that, apply the relationship changes that the stories in the previous steps had to offer.
        # If there is one, only apply the relationship change that the newly-added node had to offer.

        # 8. Jump back to step 2.

    # 9. Return the completed story graph.


def check_if_all_values_in_list_exceed(checklist, checkvalue):
    result = True

    for current in checklist:
        result = result and current > checkvalue

    return result