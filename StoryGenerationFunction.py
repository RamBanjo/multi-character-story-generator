from components import StoryGraph, StoryNode, StoryObjects, RewriteRules, RelChange

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

    # 2. Check if all the routes are at least the minimum length.
    # If all the routes have the right length, exit the loop (Step 9).
    
    # 3. If you're still here, some routes still needs more length. Here, make a list of the characters with shortest routes.

    # 4. Randomly pick one character from the shortest-route-list. We will apply a rule for this character.
    # If this character isn't suppoed to act yet (current timestep would not be their first timestep yet) then they must do the Wait action. Lock this in and skip to step 7.

    # 5. Make a list of all the possible continuations for the chosen character
    # If there is a metric, then rank them and limit the list to the top picks according to those metrics

    # 6. Randomly choose one rule from the list to apply
    # If the rule is a joint one, then check other characters in the shortest-route-list and make a list of characters that can join the joint.
    #    If there aren't enough characters to satisfy this, then eliminate this rule from the list and return to choosing.
    # If there is at least one constraint, check if applying this rule would violate the constraint.
    #    If there is a violation, eliminate this rule from the list and return to choosing.

    # 7. If you're here, the chosen rule has past the tests given above, therefore it will be applied.

    # 8. Jump back to step 2.
    
    # 9. Return the completed story graph.
    
    pass