#Here's what's going to Happen
#Alice has a red paperclip. Bob wants a red paperclip and has a pen. Charlie wants a pen and has a book. Daniel wants a book and has a chess set. Eliza wants a chess set and has a laptop.
#Alice's goal is to get the Laptop by trading.
#Alice has a task to trade with Bob, Charlie, Daniel, and Eliza. (The latter four are written as NoStoryCharacter).
#Length of StoryNode for each graph is 5. Alice will start with tasks to trade with Bob, Charlie, Daniel, and Eliza. The map is formatted like a star where each person lives in a house connected to a hub.

from datetime import datetime
import sys
sys.path.insert(0,'')

from application.components.StoryObjects import *
from application.components.WorldState import *
from application.components.CharacterTask import *
from application.components.StoryGraphTwoWS import *
from application.components.StoryNode import *
from application.components.RelChange import *
from application.components.UtilityEnums import *
from application.components.RewriteRuleWithWorldState import *

from application.StoryGeneration_NewFlowchart_WithMetrics import generate_story_from_starter_graph, make_base_graph_from_previous_graph, generate_multiple_graphs

alice = CharacterNode(name="Alice", internal_id=0)
bob = ObjectNode(name="Bob", tags={"Type":"NoStoryCharacter"}, internal_id=1)
charlie = ObjectNode(name="Charlie", tags={"Type":"NoStoryCharacter"}, internal_id=2)
daniel = ObjectNode(name="Daniel", tags={"Type":"NoStoryCharacter"}, internal_id=3)
eliza = ObjectNode(name="Eliza", tags={"Type":"NoStoryCharacter"}, internal_id=4)

rpc = ObjectNode(name="Red Paperclip", tags={"Type":"BarteringResource"}, internal_id=5)
pen = ObjectNode(name="Pen", tags={"Type":"BarteringResource"}, internal_id=6)
book = ObjectNode(name="Book", tags={"Type":"BarteringResource"}, internal_id=7)
chess = ObjectNode(name="Chessboard", tags={"Type":"BarteringResource"}, internal_id=8)
laptop = ObjectNode(name="Laptop", tags={"Type":"BarteringResource"}, internal_id=9)

hub = LocationNode(name="Hub", internal_id=10)
a_house = LocationNode(name="Alice House", internal_id=11)
b_house = LocationNode(name="Bob House", internal_id=12)
c_house = LocationNode(name="Charlie House", internal_id=13)
d_house = LocationNode(name="Daniel House", internal_id=14)
e_house = LocationNode(name="Eliza House", internal_id=15)

test_ws = WorldState(name="Test WS", objectnodes=[alice, bob, charlie, daniel, eliza, rpc, pen, book, chess, laptop, hub, a_house, b_house, c_house, d_house, e_house])

test_ws.connect(from_node=alice, edge_name="holds", to_node=rpc)
test_ws.connect(from_node=bob, edge_name="holds", to_node=pen)
test_ws.connect(from_node=charlie, edge_name="holds", to_node=book)
test_ws.connect(from_node=daniel, edge_name="holds", to_node=chess)
test_ws.connect(from_node=eliza, edge_name="holds", to_node=laptop)

test_ws.connect(from_node=a_house, edge_name="holds", to_node=alice)
test_ws.connect(from_node=b_house, edge_name="holds", to_node=bob)
test_ws.connect(from_node=c_house, edge_name="holds", to_node=charlie)
test_ws.connect(from_node=d_house, edge_name="holds", to_node=daniel)
test_ws.connect(from_node=e_house, edge_name="holds", to_node=eliza)

test_ws.doubleconnect(from_node=a_house, edge_name="connects", to_node=hub)
test_ws.doubleconnect(from_node=b_house, edge_name="connects", to_node=hub)
test_ws.doubleconnect(from_node=c_house, edge_name="connects", to_node=hub)
test_ws.doubleconnect(from_node=d_house, edge_name="connects", to_node=hub)
test_ws.doubleconnect(from_node=e_house, edge_name="connects", to_node=hub)

def make_trade_item_charactertask(owned_item, obtained_item, trade_target, trade_location):

    actor_target_share_location_test = SameLocationTest(list_to_test=[GenericObjectNode.GENERIC_ACTOR, GenericObjectNode.GENERIC_TARGET])
    actor_holds_owned_item_test = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="holds", object_to_test=owned_item)
    target_holds_obtained_item_test = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_TARGET, edge_name_test="holds", object_to_test=obtained_item)

    all_tests = [actor_target_share_location_test, actor_holds_owned_item_test, target_holds_obtained_item_test]

    actor_not_have_owned_item_change = RelChange(name="Actor Loses Owned Item", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="holds", node_b=owned_item, add_or_remove=ChangeAction.REMOVE)
    target_have_owned_item_change = RelChange(name="Target Gains Owned Item", node_a=GenericObjectNode.GENERIC_TARGET, edge_name="holds", node_b=owned_item, add_or_remove=ChangeAction.ADD)

    actor_have_obtained_item_change = RelChange(name="Actor Gains Obtained Item", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="holds", node_b=obtained_item, add_or_remove=ChangeAction.ADD)
    target_not_have_obtained_item_change = RelChange(name="Target Loses Obtained Item", node_a=GenericObjectNode.GENERIC_TARGET, edge_name="holds", node_b=obtained_item, add_or_remove=ChangeAction.REMOVE)

    all_changes = [actor_not_have_owned_item_change, target_have_owned_item_change, actor_have_obtained_item_change, target_not_have_obtained_item_change]

    give_owned_item_to_get_their_item = StoryNode(name="Trade Items", actor=[GenericObjectNode.TASK_OWNER], target=[trade_target], required_test_list=all_tests, effects_on_next_ws=all_changes)
    
    trade_item_task = CharacterTask(task_name="Trade Items", task_actions=[give_owned_item_to_get_their_item], task_location_name=trade_location.get_name())

    return trade_item_task

b_trade = make_trade_item_charactertask(owned_item=rpc, obtained_item=pen, trade_target=bob, trade_location=b_house)
c_trade = make_trade_item_charactertask(owned_item=pen, obtained_item=book, trade_target=charlie, trade_location=c_house)
d_trade = make_trade_item_charactertask(owned_item=book, obtained_item=chess, trade_target=daniel, trade_location=d_house)
e_trade = make_trade_item_charactertask(owned_item=chess, obtained_item=laptop, trade_target=eliza, trade_location=e_house)

trading_to_laptop_taskstack = TaskStack(stack_name="Trading Up Laptop", task_stack=[b_trade, c_trade, d_trade, e_trade])
trading_taskchange = TaskChange(name="Trading Taskchange", task_giver_name=GenericObjectNode.GENERIC_ACTOR, task_owner_name=GenericObjectNode.GENERIC_ACTOR, task_stack=trading_to_laptop_taskstack)
get_trading_task_node = StoryNode(name="Get Trading Task", effects_on_next_ws=[trading_taskchange])

test_sg = StoryGraph(name="Test SG", character_objects=[alice], starting_ws=test_ws)
test_sg.insert_story_part(part=get_trading_task_node, character=alice, location=a_house)

# test_sg.print_all_node_beautiful_format()

start_gen_time = datetime.now()
# new_graph = generate_story_from_starter_graph(init_storygraph=test_sg, list_of_rules=[], required_story_length=5, verbose=True)

list_of_graphs = generate_multiple_graphs(initial_graph=test_sg, list_of_rules=[], required_story_length=30, max_storynodes_per_graph=5, verbose=True)

finish_gen_time = datetime.now()

print("xxx")
print("Generation Time:", str(finish_gen_time-start_gen_time))

# new_graph.print_all_node_beautiful_format()
# # new_graph.make_latest_state().print_all_edges()

# latest_alice = new_graph.make_latest_state().node_dict.get("Alice")
# print(latest_alice)

graphno = 1
for graph in list_of_graphs:

    cur_dir = "application/tests/test_output/multigraph_exam/graph_" + str(graphno) + "/" 
    graph.print_graph_nodes_to_text_file(directory=cur_dir)
    graphno += 1

# print(new_graph.make_latest_state().node_dict["Alice"].get_list_of_things_held_by_this_item()[0])