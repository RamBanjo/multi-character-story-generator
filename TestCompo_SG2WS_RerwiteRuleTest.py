import copy
from components.RewriteRuleWithWorldState import *
from components.StoryObjects import *
from components.WorldState import *
from components.StoryNode import *
from components.StoryGraphTwoWS import *
from components.RelChange import *
from components.ConditionTest import *

#Test Scenario:
#Initial WorldState: Alice exists in Town, Sword exists in Shop.
#Abs Step 1: Alice goes to Shop.
#Abs Step 2: Alice takes sword at Shop.

#Replacement Rule
#Take Item + Negative Law Bias -> Steal Item (Replacement True)

#Expected Result:
# Abs Step 1: Alice goes to Shop.
# Abs Step 2: Alice steals sword at Shop.

alice = CharacterNode(name="Alice", biases={"lawbias":-50, "moralbias":0}, tags={"Type":"Character", "Role":"Thief"}, start_timestep=0)
excalibur = ObjectNode(name="Excalibur", tags={"Status":"Owned","Type":"Weapon", "Value":"Priceless"})
town = LocationNode(name="Town", tags={"Type":"Town"})
shop = LocationNode(name="Shop",type={"Type":"Building"})

init_ws = WorldState("Initial WorldState", [alice, excalibur, town, shop])
init_ws.connect(town, "holds", alice)
init_ws.connect(shop, "holds", excalibur)
init_ws.doubleconnect(town, "connects", shop)

shop_hold_character = RelChange(name="Shop Hold Character", node_a=shop, edge_name="holds", node_b=GenericObjectNode.GENERIC_ACTOR, value=None, add_or_remove=ChangeAction.ADD)
current_loc_not_hold_character = RelChange(name="CurLoc Not Hold Character", node_a=GenericObjectNode.GENERIC_LOCATION, edge_name="holds", node_b=GenericObjectNode.GENERIC_ACTOR, value=None, add_or_remove=ChangeAction.REMOVE)
character_hold_sword = RelChange(name="Character Hold Target", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="holds", node_b=GenericObjectNode.GENERIC_TARGET, value=None, add_or_remove=ChangeAction.ADD)
current_loc_not_hold_sword = RelChange(name="CurLoc Not Hold Target", node_a=GenericObjectNode.GENERIC_LOCATION, edge_name="holds", node_b=GenericObjectNode.GENERIC_TARGET, value=None, add_or_remove=ChangeAction.REMOVE)

current_loc_adjacent_shop = HasEdgeTest(GenericObjectNode.GENERIC_LOCATION, "connects", shop, None, soft_equal=True, inverse=False, two_way=True)
same_location_sword = SameLocationTest([GenericObjectNode.GENERIC_TARGET, GenericObjectNode.GENERIC_ACTOR])

go_to_shop = StoryNode(name="Go to Shop", biasweight=None, tags={"Type":"Movement"}, charcount=1, effects_on_next_ws=[shop_hold_character, current_loc_not_hold_character], required_test_list=[current_loc_adjacent_shop])
take_sword = StoryNode(name="Take Item", biasweight=None, tags={"Type":"Take Item"}, charcount=1, effects_on_next_ws=[character_hold_sword, current_loc_not_hold_sword], required_test_list=[same_location_sword])
steal_sword = StoryNode(name="Steal Item", biasweight=5, tags={"Type":"Take Item"}, charcount=1, effects_on_next_ws=[character_hold_sword, current_loc_not_hold_sword], required_test_list=[same_location_sword], bias_range={"lawbias":(-100,-30)})

if_unlawful_then_steal = RewriteRule(story_condition=[deepcopy(take_sword)], story_change=[deepcopy(steal_sword)], name="Unlawful Theft", remove_before_insert=True, target_list=[[excalibur]])

init_sg = StoryGraph("Initial Storygraph", [alice], [town, shop], init_ws)

init_sg.add_story_part(part = go_to_shop, character = alice, location = town, targets = [shop])
init_sg.add_story_part(part = take_sword, character = alice, location = shop, targets = [excalibur])

init_sg.print_all_node_beautiful_format()

init_sg.apply_rewrite_rule(if_unlawful_then_steal, alice, [shop], True)

init_sg.print_all_node_beautiful_format()