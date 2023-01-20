import itertools
from components.UtilFunctions import *
from components.StoryObjects import CharacterNode
# x = [1, 1, 2]
# y = list(set(list(itertools.permutations(x))))

# print(y)

# print(permute_all_possible_groups(4, 2))

# alice = CharacterNode("Alice")
# bob = CharacterNode("Bob")
# charlie = CharacterNode("Charlie")
# daniel = CharacterNode("Daniel")

# charcter_list = [("Alice", 3), ("Bob", 3), ("Charlie", 3), ("Daniel", 3)]
# all_possible_actor_groupings((2,1,1), charcter_list)

test_range = [1, 2, -1, 5, (3,4), -1, 2, -1, (1, 2), (1, 6)]
test_range_2 = [5, 15]
test_range_3 = [(1, 20), (1,20)]
test_range_4 = [-1, -1, -1]
wanted_sum = 20

for x in permute_all_possible_groups_with_ranges_and_freesize(size_list=test_range_2, required_sum=wanted_sum):
    print(x, sum(x))

# rangelist=[(1,2),(1,4),(1,3)]

# for item in permute_full_range_list(range_number_to_range_list(rangelist)):
#     print(item)


