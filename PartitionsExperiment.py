import itertools
from components.UtilFunctions import *
from components.StoryObjects import CharacterNode
# x = [1, 1, 2]
# y = list(set(list(itertools.permutations(x))))

# print(y)

#print(permute_all_possible_groups(4, 2))

# alice = CharacterNode("Alice")
# bob = CharacterNode("Bob")
# charlie = CharacterNode("Charlie")
# daniel = CharacterNode("Daniel")

# charcter_list = [("Alice", 3), ("Bob", 3), ("Charlie", 3), ("Daniel", 3)]
# all_possible_actor_groupings((2,1,1), charcter_list)

test_range = [1, 2, -1, 5, (3,4), -1, 2, -1, (1, 2), (1, 6)]
wanted_sum = 20

permute_all_possible_groups_with_ranges_and_freesize(size_list=test_range, required_sum=wanted_sum)