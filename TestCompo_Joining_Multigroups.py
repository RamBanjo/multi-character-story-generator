from multiprocessing import dummy
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

dummychar = CharacterNode("Dummy")
dummyloc = LocationNode("DummyLoc")

mystery_van = LocationNode("Mystery Mobile")
haunted_house = LocationNode("Haunted House")
living_room = LocationNode("Living Room")
dining_room = LocationNode("Dining Room")
study = LocationNode("Study")

move_location = StoryNode("Move To Location", None, None, None, -1)
search_location = StoryNode("Search for Evidence at Location", None, None, None, -1)

story = StoryGraph("Let's Split Up, Gang!", [fred, daph, velma, shag, scoob], [haunted_house, mystery_van, living_room, dining_room, study])

enter_house = story.apply_joint_node(move_location, [fred, daph, velma, shag, scoob], mystery_van, 0)
enter_house.add_target(haunted_house)

split_up_to_search_at_location = SplittingJointRule(3, move_location, [search_location, search_location, search_location], "split up and search")

story.apply_splitting_joint_rule(split_up_to_search_at_location, [fred, daph, velma, shag, scoob], [living_room, dining_room, study], [[fred], [shag, scoob], [daph, velma]], applyonce=True)

story.print_all_node_beautiful_format()