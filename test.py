from application.components.StoryGraphTwoWS import StoryGraph
from application.components.WorldState import WorldState
from application.components.CharacterTask import CharacterTask, TaskStack
from application.components.StoryNode import StoryNode
from application.components.StoryObjects import CharacterNode, LocationNode

# Testing Conditions

# hey = [1,2,3,4,5]

# #expect:
# #First Step 0
# last_task_step = -1
# print(hey[last_task_step:])

alice = CharacterNode("Alice")
bob = CharacterNode("Bob")
charlie = CharacterNode("Charlie", tags={"Type":"Character", "Job":"Police"})
daniel = CharacterNode("Daniel")

town = LocationNode("Town")

world_state = WorldState(name="World State", objectnodes=[alice, bob, charlie, daniel])

world_state.connect(from_node=town, edge_name="holds", to_node=alice)
world_state.connect(from_node=town, edge_name="holds", to_node=bob)
world_state.connect(from_node=town, edge_name="holds", to_node=charlie)
world_state.connect(from_node=town, edge_name="holds", to_node=daniel)
world_state.connect(from_node=bob, edge_name="rivals", to_node=daniel)
world_state.connect(from_node=daniel, edge_name="rivals", to_node=bob)

# Bob gives a task to Alice. Bob wants to get Daniel in legal trouble.
# - Alice goes to Daniel and plants evidence on him.
# - Alice reports it to Charlie.