from components.StoryNode import StoryNode
from components.StoryObjects import CharacterNode

alice = CharacterNode(name="Alice", biases={"lawbias":-20, "moralbias":30}, tags={"Job":"Spellcaster", "Wanted":True})

kill_pursuer = StoryNode("Kill Pursuer", 3, {"Type":"Escape", "Death":True}, 1, suggested_bias_range={"lawbias":(-100, -0)}, suggested_excluded_tags={"KillingAverse":True}, suggested_included_tags={"Wanted":True})
print(kill_pursuer.calculate_weight_score(alice))

#TODO: Ah, I knew it wouldn't be as easy as I initially thought~ There just happens to be the matter of the absolute step where it would take place, so we also need to take care of that.
#TODO: New idea: use the moving world states to test for time-specificity for each rule. Like this:
# 1. Rule A, Abs Step 2 (Score: 5)
# 2. Rule A, Abs Step 5 (Score: 3)
# 3. Rule A, Abs Step 12 (Score: 2)
#TODO: That works for one node, but remember, character's state changes inbetween world states, so we need to account for that as well. If we're testing for the score of a sequence of story nodes, we can assume that character will change according to the sequences of that node.
#For example:
#
# Insering a sequence of [X, Y, Z] at (Alice, 4) should net the following:
# Use Alice from WS5 to calculate score for X
# Use Alice from WS6 to calculate score for Y
# Use Alice from WS7 to calculate score for Z
# Therefore, we need to make yet another story graph function. Yaaaay~