from components import StoryObjects as story_objects
from components import Edge
from components import StoryNode

alice = story_objects.ObjectNode("Alice", "Character", 100, {"Race":"Human", "Job":"Spellcaster", "Life":"Alive", "Gender":"Female"}, biases={'lawbias': 0, 'moralbias': 0}, start_timestep=5)

print("Character: Alice")
print(alice.name)
print(alice.nodetype)
print(alice.unique_id)
print(alice.tags)
print(alice.biases)
print(alice.start_timestep)

print()
sword = story_objects.ObjectNode("Excalibur", "Object", 200, {"Type":"Weapon", "Value":"Invaluable"})

print("Object: Excalibur")
print(sword.name)
print(sword.nodetype)
print(sword.unique_id)
print(sword.tags)
print(sword.biases)
print(sword.start_timestep)

print()
town = story_objects.ObjectNode("Townsville", "Location", 300, {"Type":"Town", "Population":"Small"})

print("Location: Townsville")
print(town.name)
print(town.nodetype)
print(town.unique_id)
print(town.tags)
print(town.biases)
print(town.start_timestep)

#so if we want to define that Alice is in Townsville, we would do this:

is_in = Edge.Edge("is_in", alice, town)
alice.outgoing_edges.add(is_in)
town.incoming_edges.add(is_in)

#and if we want to define that Alice is carrying the Excalibur, we would do this

carries_object = Edge.Edge("carries_object", alice, sword)
alice.outgoing_edges.add(carries_object)
town.incoming_edges.add(carries_object)

print(is_in)
print(carries_object)





