import sys
sys.path.insert(0,'')

from application.components.StoryObjects import *
from application.components.WorldState import *
from application.components.CharacterTask import *
from application.components.StoryGraphTwoWS import *
from application.components.StoryNode import *
from application.components.RelChange import *
from application.components.UtilityEnums import *

from application.StoryGeneration_NewFlowchart_WithMetrics import make_base_graph_from_previous_graph

mailman = CharacterNode(name="Mailman", internal_id=0)

alice = CharacterNode(name="Alice", tags={"Type":"Character","HasLetter":False}, internal_id=1)
bob = CharacterNode(name="Bob", tags={"Type":"Character","HasLetter":False}, internal_id=2)
charlie = CharacterNode(name="Charlie", tags={"Type":"Character","HasLetter":False}, internal_id=3)
david = CharacterNode(name="David", tags={"Type":"Character","HasLetter":False}, internal_id=4)
eve = CharacterNode(name="Eve", tags={"Type":"Character","HasLetter":False}, internal_id=5)

post_office = LocationNode(name="Post Office", internal_id=6)
the_streets = LocationNode(name="Streets", internal_id=7)
alice_house = LocationNode(name="Alice House", internal_id=8)
charlie_house = LocationNode(name="Charlie House", internal_id=9)
eve_house = LocationNode(name="Eve House", internal_id=10)

world_state = WorldState("Test WS", objectnodes=[mailman, alice, bob, charlie, david, eve, post_office, the_streets, alice_house, charlie_house, eve_house])

world_state.doubleconnect(from_node=post_office, edge_name="connects", to_node=the_streets)
world_state.doubleconnect(from_node=alice_house, edge_name="connects", to_node=the_streets)
world_state.doubleconnect(from_node=charlie_house, edge_name="connects", to_node=the_streets)
world_state.doubleconnect(from_node=eve_house, edge_name="connects", to_node=the_streets)

world_state.connect(from_node=post_office, edge_name="holds", to_node=mailman)
world_state.connect(from_node=alice_house, edge_name="holds", to_node=alice)
world_state.connect(from_node=alice_house, edge_name="holds", to_node=bob)
world_state.connect(from_node=charlie_house, edge_name="holds", to_node=charlie)
world_state.connect(from_node=charlie_house, edge_name="holds", to_node=david)
world_state.connect(from_node=eve_house, edge_name="holds", to_node=eve)
#The mailman has a task to deliver letters to each of these characters. Once the letter is delivered, HasLetter will be set to True.

actor_shares_location_with_target = SameLocationTest(list_to_test=[GenericObjectNode.GENERIC_ACTOR, GenericObjectNode.GENERIC_TARGET])
target_doesnt_have_mail = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="HasLetter", value=True, inverse=True)
target_gets_mail = TagChange(name="Target Gets Mail", object_node_name=GenericObjectNode.GENERIC_TARGET, tag="HasLetter", value=True, add_or_remove=ChangeAction.ADD)

deliver_mail = StoryNode(name="Deliver Mail", required_test_list=[actor_shares_location_with_target, target_doesnt_have_mail], effects_on_next_ws=[target_gets_mail])

deliver_mail_to_alice = StoryNode(name="Deliver Mail To Alice", required_test_list=[actor_shares_location_with_target, target_doesnt_have_mail], effects_on_next_ws=[target_gets_mail], actor=[GenericObjectNode.TASK_OWNER], target=[alice])
deliver_mail_to_bob = StoryNode(name="Deliver Mail To Bob", required_test_list=[actor_shares_location_with_target, target_doesnt_have_mail], effects_on_next_ws=[target_gets_mail], actor=[GenericObjectNode.TASK_OWNER], target=[bob])
deliver_mail_to_charlie = StoryNode(name="Deliver Mail To Charlie", required_test_list=[actor_shares_location_with_target, target_doesnt_have_mail], effects_on_next_ws=[target_gets_mail], actor=[GenericObjectNode.TASK_OWNER], target=[charlie])
deliver_mail_to_david = StoryNode(name="Deliver Mail To David", required_test_list=[actor_shares_location_with_target, target_doesnt_have_mail], effects_on_next_ws=[target_gets_mail], actor=[GenericObjectNode.TASK_OWNER], target=[david])
deliver_mail_to_eve = StoryNode(name="Deliver Mail To Eve", required_test_list=[actor_shares_location_with_target, target_doesnt_have_mail], effects_on_next_ws=[target_gets_mail], actor=[GenericObjectNode.TASK_OWNER], target=[eve])

deliver_mail_to_alice_task = CharacterTask(task_name="Deliver Mail to Alice", task_actions=[deliver_mail_to_alice], task_location_name="Alice House")
deliver_mail_to_bob_task = CharacterTask(task_name="Deliver Mail to Bob", task_actions=[deliver_mail_to_bob], task_location_name="Alice House")
deliver_mail_to_charlie_task = CharacterTask(task_name="Deliver Mail to Charlie", task_actions=[deliver_mail_to_charlie], task_location_name="Charlie House")
deliver_mail_to_david_task = CharacterTask(task_name="Deliver Mail to David", task_actions=[deliver_mail_to_david], task_location_name="Charlie House")
deliver_mail_to_eve_task = CharacterTask(task_name="Deliver Mail to Eve", task_actions=[deliver_mail_to_eve], task_location_name="Eve House")

deliver_mail_stack = TaskStack(stack_name="Mail Run", task_stack=[deliver_mail_to_alice_task, deliver_mail_to_bob_task, deliver_mail_to_charlie_task, deliver_mail_to_david_task, deliver_mail_to_eve_task])
get_mail_stack = TaskChange(name="Get Mail Stack", task_giver_name=None, task_owner_name=GenericObjectNode.GENERIC_ACTOR, task_stack=deliver_mail_stack)

DEFAULT_WAIT_NODE = StoryNode(name="Wait", biasweight=0, tags= {"Type":"Placeholder"}, charcount=1)
mailman_starts_mail_run_node = StoryNode(name="Start Mail Run", effects_on_next_ws=[get_mail_stack])

test_graph = StoryGraph(name="Test Graph", character_objects=[mailman, alice, bob, charlie, david, eve], starting_ws=world_state)

test_graph.insert_story_part(part=mailman_starts_mail_run_node, character=mailman, location=post_office, absolute_step=0)
test_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=alice, location=alice_house, absolute_step=0)
test_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=bob, location=alice_house, absolute_step=0)
test_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=charlie, location=charlie_house, absolute_step=0)
test_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=david, location=charlie_house, absolute_step=0)
test_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=eve, location=eve_house, absolute_step=0)
test_graph.fill_in_locations_on_self()
# test_graph.make_latest_state().print_all_edges()

#Alright the initial world state has been set up, let's advance the task a bit!

print("Status of Mail Delivery before Alice's Mail Task:")
latest_state = test_graph.make_latest_state()
print("Alice has letter:", latest_state.node_dict["Alice"].tags["HasLetter"])
print("Bob has letter:", latest_state.node_dict["Bob"].tags["HasLetter"])
print("Charlie has letter:", latest_state.node_dict["Charlie"].tags["HasLetter"])
print("David has letter:", latest_state.node_dict["David"].tags["HasLetter"])
print("Eve has letter:", latest_state.node_dict["Eve"].tags["HasLetter"])
print("-----")
#Mailman will move to Alice's house and do the mail delivery task with Alice and Bob, who both live there. Then, the world state should say both of them had their mails delivered.

leave_current_location = RelChange(name="Leave Current Location", node_a=GenericObjectNode.GENERIC_LOCATION, edge_name="holds", node_b=GenericObjectNode.GENERIC_ACTOR, add_or_remove=ChangeAction.REMOVE)
go_to_streets = RelChange(name="Go to Streets", node_a=the_streets, edge_name="holds", node_b=GenericObjectNode.GENERIC_ACTOR, add_or_remove=ChangeAction.ADD)
go_to_alice_house = RelChange(name="Go to Alice House", node_a=alice_house, edge_name="holds", node_b=GenericObjectNode.GENERIC_ACTOR, add_or_remove=ChangeAction.ADD)
go_to_charlie_house = RelChange(name="Go to Charlie House", node_a=charlie_house, edge_name="holds", node_b=GenericObjectNode.GENERIC_ACTOR, add_or_remove=ChangeAction.ADD)
current_location_adjacent_to_streets = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_LOCATION, edge_name_test="connects", object_to_test=the_streets)
current_location_adjacent_to_alice_house = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_LOCATION, edge_name_test="connects", object_to_test=alice_house)
current_location_adjacent_to_charlie_house = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_LOCATION, edge_name_test="connects", object_to_test=charlie_house)

move_from_post_office_to_street = StoryNode(name="Go to Streets", effects_on_next_ws=[leave_current_location, go_to_streets], required_test_list=[current_location_adjacent_to_streets])
move_from_street_to_alice_house = StoryNode(name="Go to Alice House", effects_on_next_ws=[leave_current_location, go_to_alice_house], required_test_list=[current_location_adjacent_to_alice_house])
move_from_street_to_charlie_house = StoryNode(name="Go to Charlie House", effects_on_next_ws=[leave_current_location, go_to_charlie_house], required_test_list=[current_location_adjacent_to_charlie_house])

#TODO: I have no idea why but the Mailman changing locations from office to the street removes both alice and bob from the house???? Literally doesn't happen with any other houses
#
#TODO: I apparently made internal ID really integral to this system, huh. Anyways yeah it's because of the Internal ID, so sue me.
#
#TODO: From my understanding the other part that's messing with the generation time is the task with multiple character placeholders.
#TODO: I should probably make my test character a busman instead.
test_graph.insert_story_part(part=move_from_post_office_to_street, character=mailman, absolute_step=1)
test_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=alice, absolute_step=1)
test_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=bob, absolute_step=1)
test_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=charlie, absolute_step=1)
test_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=david, absolute_step=1)
test_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=eve, absolute_step=1)
test_graph.fill_in_locations_on_self()

test_graph.insert_story_part(part=move_from_street_to_alice_house, character=mailman, absolute_step=2)
test_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=alice, absolute_step=2)
test_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=bob, absolute_step=2)
test_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=charlie, absolute_step=2)
test_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=david, absolute_step=2)
test_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=eve, absolute_step=2)
test_graph.fill_in_locations_on_self()

test_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=mailman, absolute_step=3)
test_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=alice, location=alice_house)
test_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=bob, location=alice_house)
test_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=charlie, location=charlie_house)
test_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=david, location=charlie_house)
test_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=eve, location=eve_house)
test_graph.fill_in_locations_on_self()

# test_graph.print_all_nodes_from_characters_storyline_beautiful_format(mailman)

print("We will now attempt to advance this Mailman's stack!")
test_graph.attempt_advance_task_stack(task_stack_name="Mail Run", actor_name="Mailman", abs_step=3, verbose=True)
test_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=bob, location=alice_house)
test_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=charlie, location=charlie_house)
test_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=david, location=charlie_house)
test_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=eve, location=eve_house)
test_graph.fill_in_locations_on_self()

print("Now, the Mailman has delivered Alice's mail. Therefore only Alice should have the mail.")
print("-----")
print("Status of Mail Delivery after Alice's Mail Task:")
latest_state = test_graph.make_latest_state()
print("Alice has letter:", latest_state.node_dict["Alice"].tags["HasLetter"])
print("Bob has letter:", latest_state.node_dict["Bob"].tags["HasLetter"])
print("Charlie has letter:", latest_state.node_dict["Charlie"].tags["HasLetter"])
print("David has letter:", latest_state.node_dict["David"].tags["HasLetter"])
print("Eve has letter:", latest_state.node_dict["Eve"].tags["HasLetter"])
print("-----")

print("Now, we will attempt to create a new graph out of this graph's current state.")

new_graph = make_base_graph_from_previous_graph(previous_graph=test_graph, graph_name="new_graph")

print("Things to check for:")
print("1.) Check if the mail delivery state is correct.")
print("-----")
print("Status of Mail Delivery in new graph:")
latest_state = new_graph.make_latest_state()
print("Alice has letter:", latest_state.node_dict["Alice"].tags["HasLetter"])
print("Bob has letter:", latest_state.node_dict["Bob"].tags["HasLetter"])
print("Charlie has letter:", latest_state.node_dict["Charlie"].tags["HasLetter"])
print("David has letter:", latest_state.node_dict["David"].tags["HasLetter"])
print("Eve has letter:", latest_state.node_dict["Eve"].tags["HasLetter"])
print("-----")


print("2.) Check if the mailman's current task state is correct.")
latest_state_mailman = latest_state.node_dict["Mailman"]
print("Task Status of Latest State's Mailman")
for thing in latest_state_mailman.list_of_task_stacks:
    print(thing)

#YASS I AM FINALLY DONE WITH THIS, NEXT UP IS THE METRICS TESTING