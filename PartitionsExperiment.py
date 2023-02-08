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
test_range_5 = [1, 3, 1]
wanted_sum = 5

# for x in all_possible_actor_groupings([1, 1, 3], ["Ace", "Brent", "Chad", "Dan", "Eggs"]):
#     print (x)

# for x in all_possible_actor_groupings_with_ranges_and_freesizes(test_range_5, ["Ace", "Brent", "Chad", "Dan", "Eggs"]):
#     print(x)

# for x in permute_all_possible_groups_with_ranges_and_freesize(size_list=test_range_4, required_sum=wanted_sum):
#     print(x, sum(x))

# rangelist=[(1,2),(1,4),(1,3)]

# for item in permute_full_range_list(range_number_to_range_list(rangelist)):
#     print(item)

# print(all_possible_actor_groupings_with_ranges_and_freesizes([-1, -1], ["Alice", "Bob", "Charlie"]))

# print(actor_count_sum(1, 2))
# print(actor_count_sum(-1, 2))
# print(actor_count_sum(1, -1))
# print(actor_count_sum((3, 6), 2))
# print(actor_count_sum(1, (2, 4)))
# print(actor_count_sum((3, 6), (2, 4)))
# print(actor_count_sum((3, 6), -1))
# print(actor_count_sum(-1, (2, 4)))

# print(all_possible_actor_groupings_with_ranges_and_freesizes([-1, -1], ["A","B","C","D"]))

# testlist = [0,1,2,3,4,5]

# print(testlist[:0])

lista = permute_actor_list_for_joint_with_variable_length("A",["b","c","d","e","f"], 2,4)
#listb = all_possible_actor_groupings_with_ranges_and_freesizes([1, 1, 2], ["A","b","c","d"])

for item in lista:
    print(item)