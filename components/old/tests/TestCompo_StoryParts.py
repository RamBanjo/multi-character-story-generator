from components import StoryObjects as story_objects
from components import Edge
from components import StoryNode

alice = story_objects.ObjectNode("Alice", "Character", 100, {"Race":"Human", "Job":"Spellcaster", "Life":"Alive", "Gender":"Female"}, biases={'lawbias': 0, 'moralbias': 0}, start_timestep=5)
sword = story_objects.ObjectNode("Excalibur", "Object", 200, {"Type":"Weapon", "Value":"Invaluable"})
town = story_objects.ObjectNode("Townsville", "Location", 300, {"Type":"Town", "Population":"Small"})
town_2 = story_objects.ObjectNode("Coolsville", "Location", 301, {"Type":"Town", "Population":"Medium"})

travel = StoryNode.StoryNode("Travel", None, {"Movement"}, 1)
take_item = StoryNode.StoryNode("Take Item", {"Gain_Item"}, None, 1)
travel_2 = StoryNode.StoryNode("Travel", None, {"Movement"}, 1)

#Story: Alice starts in Townsville, goes to Coolsville, take the sword, and bring it back to Townsville

#Step 1: Initialize Alice in Townsville
#Simplify: Add an initialize function
is_in = Edge.Edge("is_in", alice, town)
alice.outgoing_edges.add(is_in)
town.incoming_edges.add(is_in)

#Step 2: Initialize Excalibur in Coolsville
#Simplify: Add an initialize function
is_in_2 = Edge.Edge("is_in", sword, town_2)
sword.outgoing_edges.add(is_in_2)
town_2.incoming_edges.add(is_in_2)

#Step 3: Alice travels to Coolsville, changes relationship with Townsville and Coolsville
#Simplify: Add a relationship change function
is_in.to_node = town_2
town.incoming_edges.remove(is_in)
town_2.incoming_edges.add(is_in)

#Simplify: Add a take action function
travel.actor.add(alice)
travel.target.add(town_2)

#Step 4: Alice picks up Excalibur, chnages relationship with Sword. Sword changes relationship with Coolsville
#Simplify: Add a relationship change function
carry = Edge.Edge("carries", alice, sword)

alice.outgoing_edges.add(carry)
sword.incoming_edges.add(carry)

sword.outgoing_edges.remove(is_in_2)
town_2.incoming_edges.remove(is_in_2)

#Simplify: Add a take action function
take_item.actor.add(alice)
take_item.target.add(sword)
take_item.previous_nodes[alice.unique_id] = travel
travel.next_nodes[alice.unique_id] = take_item

#Step 5: Alice travels to Townsville, changes relationship with Townsville and Coolsville
#Simplify: Add a relationship change function
is_in.to_node = town
town_2.incoming_edges.remove(is_in)
town.incoming_edges.add(is_in)

#Simplify: Add a take action function
travel_2.actor.add(alice)
travel_2.target.add(town)
travel_2.previous_nodes[alice.unique_id] = take_item
take_item.next_nodes[alice.unique_id] = travel_2




#Conclution:
#Need to define change in relationship in StoryNode

