
from components.RelChange import TaskAdvance
from components.StoryNode import StoryNode
from components.StoryObjects import CharacterNode, LocationNode
from components.WorldState import WorldState


alice = CharacterNode("Alice")
bob = CharacterNode("Bob")
charlie = CharacterNode("Charlie")
daniel = CharacterNode("Danniel")
eve = CharacterNode("Eve")

town = LocationNode("Town")
castle = LocationNode("Castle")
jail = LocationNode("Jail")

test_ws = WorldState(name="World State", objectnodes=[alice, bob, charlie, daniel, eve, town, castle, jail])

adv1 = TaskAdvance(name="Adv1", actor_name="Alice", task_stack_name="Test Stack")
story_node_1 = StoryNode("Story Node 1", biasweight=0, tags={"Type":"Placeholder"}, charcount=1)

adv2 = TaskAdvance(name="Adv2", actor_name="Alice", task_stack_name="Test Stack")
story_node_2 = StoryNode("Story Node 2", biasweight=0, tags={"Type":"Placeholder"}, charcount=1)