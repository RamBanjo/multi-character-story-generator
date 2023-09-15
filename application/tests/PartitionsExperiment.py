import itertools
import sys
sys.path.insert(0,'')

from application.components.UtilFunctions import list_all_good_combinations_from_joint_join_pattern
# from application.components.StoryObjects import CharacterNode


# x = ["A", "B", "C", "D", "E", "F"]
# # y = all_possible_actor_groupings_with_ranges_and_freesizes([20, -1], x)
# # z = [squib[0] for squib in y]
# w = []


# w.extend(list(itertools.permutations(x)))

# print(w)

# print(permute_all_possible_groups(4, 2))

# alice = CharacterNode("Alice")
# bob = CharacterNode("Bob")
# charlie = CharacterNode("Charlie")
# daniel = CharacterNode("Daniel")

# charcter_list = [("Alice", 3), ("Bob", 3), ("Charlie", 3), ("Daniel", 3)]
# all_possible_actor_groupings((2,1,1), charcter_list)

# test_range = [1, 2, -1, 5, (3,4), -1, 2, -1, (1, 2), (1, 6)]
# test_range_2 = [5, 15]
# test_range_3 = [(1, 20), (1,20)]
# test_range_4 = [-1, -1, -1]
# test_range_5 = [1, 3, 1]
# wanted_sum = 5

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

# lista = permute_actor_list_for_joint_with_variable_length("A",["b","c","d","e","f"], 4,4)
# listb = all_possible_actor_groupings_with_ranges_and_freesizes([1, 1, 2], ["A","b","c","d"])
# listc = all_possible_actor_groupings_with_ranges_and_freesizes([-1, -1], ["A","b","c"])


# for item in lista:
#     print(item)

# def getfirst(e):
#     return e[0]

# testdict = {"NodeA" : ["A", "B", "C"], "AAAANodeB": ["D","E"]}
# print(sorted(list(testdict.items()), key=getfirst))

testdict = {"NodeA":["Alice", "Eve"], "NodeB":["Bob", "Charlie"], "NodeC":["Daniel", "Frankie"]}
print(list_all_good_combinations_from_joint_join_pattern(current_actor_name=None, dict_of_base_nodes=testdict, actors_wanted=3))

# suggested_included_tags={"Job":"Swordmaster", "Job":"Warrior", "Job":"Fighter"}
# print(suggested_included_tags)

# list_d = [["a","b","c"], [], ["g","h"]]
# list_e = [["a","b","c"]]

# def perumute_all_combinations_from_each_list(given_list):

#     if len(given_list) == 1:
#         for item in given_list[0]:
#             yield [item]
#     else:
#         for item in given_list[0]:
#             for gen_item in perumute_all_combinations_from_each_list(given_list[1:]):
#                 yield [item] + gen_item

# for x in permute_full_range_list(list_d):
#     print(x)

# testdict = {"Foo":1, "Bar":2, "Baz":3, "Honeycomb":16}

# print(testdict.keys())

# print("Foo" in testdict.keys())
# print("Brisket" in testdict.keys())