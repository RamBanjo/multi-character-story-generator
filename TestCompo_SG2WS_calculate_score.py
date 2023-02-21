# Calculate Alice's score!
# Alice is a swordmaster with average wealth. Her Lawbias is at 50, and her moral bias is at 30.
# Action A has a base score of 3. Bonus score for being a Swordmaster. She should get 4 from here.
# Action B has a base score of 2. Bonus score for being a Thief. She should get 2 from here, no bonus score.
# Action C has a base score of 3. Bonus score for Lawbias [0, 100], Bonus score for Moralbias [50, 100]. Bonus score of 1. Total 4.
#
# If we choose max, we should get 4. If we average, we should get 3.333...

from components.StoryGraphTwoWS import StoryGraph
from components.StoryNode import StoryNode
from components.StoryObjects import CharacterNode, LocationNode
from components.WorldState import WorldState

alice = CharacterNode(name="Alice", biases={"lawbias":50, "moralbias":30}, tags={"Type":"Character", "Job":"Swordmaster"})
placeholderloc = LocationNode(name="Placeholder Location")

base_action_x = StoryNode(name="BaseAction X", tags={"Type":"Placeholder"}, biasweight=0, charcount=1)
action_a = StoryNode(name="Action A", tags={"Type":"Placeholder"}, charcount=1, biasweight=3, suggested_included_tags=[("Job","Swordmaster")])
action_b = StoryNode(name="Action B", tags={"Type":"Placeholder"}, charcount=1, biasweight=2, suggested_included_tags=[("Job","Thief")])
action_c = StoryNode(name="Action C", tags={"Type":"Placeholder"}, charcount=1, biasweight=3, suggested_bias_range={"lawbias":(0,100), "moralbias":(50,100)})

starting_ws = WorldState(name="StartWS", objectnodes=[alice, placeholderloc])

test_sg = StoryGraph(name="Test SG", character_objects=[alice], location_objects=[placeholderloc], starting_ws=starting_ws)

test_sg.add_story_part(base_action_x, alice, placeholderloc)

print("Max mode, expected to get 4:", test_sg.calculate_score_from_char_and_cont(alice, 1, [action_a, action_b, action_c]))
print("Avg mode, expected to get 3.33:", test_sg.calculate_score_from_char_and_cont(alice, 1, [action_a, action_b, action_c], 1))

#TESTING DONE!