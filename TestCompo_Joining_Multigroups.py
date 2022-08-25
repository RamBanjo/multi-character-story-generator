from components.StoryObjects import *
from components.RewriteRules import *
from components.StoryNode import *
from components.StoryGraph import *

#Example:
#There are 5 characters: Fred, Daphne, Velma, Shaggy, and Scooby
#They will split up into 3 groups: [Fred], [Daphne, Velma], and [Shaggy, Scooby]

fred = CharacterNode("Fred")
daph = CharacterNode("Daphne")
velma = CharacterNode("Velma")
shag = CharacterNode("Shaggy")
scoob = CharacterNode("Scooby")

haunted_house = LocationNode("Haunted House")

move_location = StoryNode("Move To Location", None, None, None, -1)
search_location = StoryNode("Search for Evidence at Location", None, None, None, -1)

story = StoryGraph("Let's Split Up, Gang!", [fred, daph, velma, shag, scoob], [haunted_house])

split_up_to_search_at_location = SplittingJointRule()

