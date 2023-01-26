from components.StoryObjects import *
from components.StoryNode import *
from components.RewriteRules_old_2 import RewriteRule
from components.StoryGraph_old_2 import StoryGraph

#The story is simple:
#Bob finds a item.
#This node will be replaced with:
#Bob goes to store
#Bob buys sword
#Bob goes to town
#Therefore, the targets will be [sword] and [[store], [sword], [town] respectively.

bob = CharacterNode("Bob")
sword = ObjectNode("Sword")
store = LocationNode("Store")
town = LocationNode("Town")

dummy = CharacterNode("Dummy Character")
dumloc = LocationNode("Dummy Location")

find_item = StoryNode("find_item", None, None, None, 1)
go_to_location = StoryNode("find_item", None, None, None, 1)
buy_item = StoryNode("buy_item", None, None, None, 1)

lhs_graph = StoryGraph("rule_lhs", [dummy], [dumloc])
rhs_graph = StoryGraph("rule_rhs", [dummy], [dumloc])
main_graph = StoryGraph("Main Story", [bob], [store, town])

main_graph.add_story_part(find_item, bob, town, 0, targets=[sword])

lhs_graph.add_story_part(find_item, dummy, dumloc, 0, copy=True)
rhs_graph.add_story_part(go_to_location, dummy, dumloc, 0, copy=True)
rhs_graph.add_story_part(buy_item, dummy, dumloc, 0, copy=True)
rhs_graph.add_story_part(go_to_location, dummy, dumloc, 0, copy=True)

buy_at_shop_instead = RewriteRule(lhs_graph, rhs_graph, dummy, "Buy at Shop Instead")

main_graph.apply_rewrite_rule(buy_at_shop_instead, bob, [town, store, store], [[sword]], [[store], [sword], [town]])

main_graph.print_all_nodes()

#Only the 2nd item would be the sword
print(main_graph.story_parts[('Bob', 0)].target[0].get_name())
print(main_graph.story_parts[('Bob', 1)].target[0].get_name())
print(main_graph.story_parts[('Bob', 2)].target[0].get_name())