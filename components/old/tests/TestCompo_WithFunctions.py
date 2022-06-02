from components import StoryObjects as story_objects
from components import Edge
from components import StoryNode
from components import UtilFunctions

'''Characters:
Alice: Hero on quest in Town A
Bob: Quest giver, asks Alice to deliver letter to Charlie
Charlie: NPC in Town B, waiting for letter.

Objects:
Letter: Letter that Bob carries
Bag of Coins: Money that Bob carries

Plot

Alice and Bob are in Town A
Charlie is in Town B

Alice talks to Bob
Bob gives Alice letter
Alice goes to Town B
Alice gives letter to Charlie
Alice goes to Town A
Alice talks to Bob
Bob gives Alice bag of coins as reward'''

alice = story_objects.ObjectNode("Alice", "Character", 100, {"Race":"Human", "Job":"Spellcaster", "Life":"Alive", "Gender":"Female"}, biases={'lawbias': 0, 'moralbias': 0}, start_timestep=5)
bob = story_objects.ObjectNode("Bob", "Character", 101, {"Race":"Human", "Job":"Blacksmith", "Life":"Alive", "Gender":"Male"}, biases={'lawbias': 0, 'moralbias': 20}, start_timestep=5)
charlie = story_objects.ObjectNode("Charlie", "Character", 102, {"Race":"Human", "Job":"Librarian", "Life":"Alive", "Gender":"Male"}, biases={'lawbias': 60, 'moralbias': 40}, start_timestep=5)
letter = story_objects.ObjectNode("Letter", "Object", 200, {"Type":"Document", "Value":"Worthless"})
money = story_objects.ObjectNode("Bag of Coins", "Object", 201, {"Type":"Currency", "Value":"Expensive"})
town = story_objects.ObjectNode("Townsville", "Location", 300, {"Type":"Town", "Population":"Small"})
town_2 = story_objects.ObjectNode("Coolsville", "Location", 301, {"Type":"Town", "Population":"Medium"})


print('Step 1: Initialize everyone')
UtilFunctions.init_object(alice, town)
UtilFunctions.init_object(bob, town)
UtilFunctions.init_object(charlie, town_2)
UtilFunctions.init_object(letter, bob)
UtilFunctions.init_object(money, bob)

nodestoprint = [alice, bob, charlie, letter, money, town, town_2]

print("Initial relationships:")
UtilFunctions.print_all_outgoing(nodestoprint)
print("-----")
print('Step 2: Alice talks to Bob')

talk_bob = StoryNode.StoryNode("Talk Together", None, ["Conversation"], 2)

talk_bob.actor.add(alice)
talk_bob.actor.add(bob)

a_know_b = Edge.Edge("knows", alice, bob)
b_know_a = Edge.Edge("knows", bob, alice)

UtilFunctions.add_relationship(alice, bob, a_know_b)
UtilFunctions.add_relationship(bob, alice, b_know_a)

letter_is_in = letter.get_incoming_edge("holds")[0]

letter_is_in.from_node.outgoing_edges.remove(letter_is_in)
letter_is_in.from_node = alice
alice.outgoing_edges.add(letter_is_in)

print("Current relationships:")
UtilFunctions.print_all_outgoing(nodestoprint)

print("-----")
print('Step 3: Alice goes from Townsville to Coolsville')

go_town_2 = StoryNode.StoryNode("Go To", None, ["Travel"], 1)

go_town_2.actor.add(alice)
go_town_2.target.add(town_2)
go_town_2.previous_nodes[alice.unique_id] = talk_bob
talk_bob.next_nodes[alice.unique_id] = go_town_2

alice_is_in = alice.get_incoming_edge("holds")[0]

alice_is_in.from_node.outgoing_edges.remove(alice_is_in)
alice_is_in.from_node = town_2
town_2.outgoing_edges.add(alice_is_in)

print("Current relationships:")
UtilFunctions.print_all_outgoing(nodestoprint)

print("-----")
print('Step 4: Alice gives letter to Charlie')

give_letter = StoryNode.StoryNode("Give Letter", None, ["Quest"], 1)

give_letter.actor.add(alice)
give_letter.target.add(charlie)
give_letter.previous_nodes[alice.unique_id] = go_town_2
go_town_2.next_nodes[alice.unique_id] = give_letter

a_know_c = Edge.Edge("knows", alice, charlie)
c_know_a = Edge.Edge("knows", charlie, alice)

UtilFunctions.add_relationship(alice, charlie, a_know_c)
UtilFunctions.add_relationship(charlie, alice, c_know_a)

letter_is_in = letter.get_incoming_edge("holds")[0]

letter_is_in.from_node.outgoing_edges.remove(letter_is_in)
letter_is_in.from_node = charlie
charlie.outgoing_edges.add(letter_is_in)

print("Current relationships:")
UtilFunctions.print_all_outgoing(nodestoprint)

print("-----")
print('Step 5: Alice goes from Coolsville to Townsville')
      
go_town = StoryNode.StoryNode("Go To", None, ["Travel"], 1)

go_town.actor.add(alice)
go_town.target.add(town)
go_town.previous_nodes[alice.unique_id] = give_letter
give_letter.next_nodes[alice.unique_id] = go_town

alice_is_in = alice.get_incoming_edge("holds")[0]

alice_is_in.from_node.outgoing_edges.remove(alice_is_in)
alice_is_in.from_node = town
town.outgoing_edges.add(alice_is_in)

print("Current relationships:")
UtilFunctions.print_all_outgoing(nodestoprint)

print("-----")
print('Step 6: Bob gives bag of gold to Alice')

give_gold = StoryNode.StoryNode("Give Gold", None, ["Quest"], 1)

give_gold.actor.add(bob)
give_gold.target.add(alice)
give_gold.previous_nodes[alice.unique_id] = go_town
go_town.next_nodes[alice.unique_id] = give_gold

gold_is_in = money.get_incoming_edge("holds")[0]

gold_is_in.from_node.outgoing_edges.remove(gold_is_in)
gold_is_in.from_node = alice
alice.outgoing_edges.add(gold_is_in)

print("Current relationships:")
UtilFunctions.print_all_outgoing(nodestoprint)

print("----- END OF STORY -----")

#Relationship for multiple actors: Everyone is mutual, parallel between all actors. Together action between all actors
#Alice gives Bob a letter: Only include the main target (Bob)
#Find more references on GPT-3
#GPT-3 cannot control generation smoothly and cannot control the direction the story is going in.
#GPT-3 openness is also a problem