import sys

sys.path.insert(0,'')

from application.components.StoryObjects import CharacterNode, LocationNode, ObjectNode
from application.components.WorldState import WorldState

columbo = CharacterNode(name="Columbo", biases={"lawbias":0, "moralbias":0}, tags={"Type":"Character","Species":"Human"})
iris = CharacterNode(name="Iris", biases={"lawbias":0, "moralbias":0}, tags={"Type":"Character","Species":"Robot"})
amil = CharacterNode(name="Amil", biases={"lawbias":0, "moralbias":0}, tags={"Type":"Character","Species":"Human"})
alien_god = CharacterNode(name="Alien God", biases={"lawbias":100, "moralbias":0}, tags={"Type":"Character","Species":"God"})

earth = LocationNode(name="Earth")
new_world_greenland = LocationNode(name="New World Greenland")
tatain = LocationNode(name="Tatain")
death_paradise = LocationNode(name="Death Paradise")
alien_god_planet = LocationNode(name="Alien God Planet")
outer_space = LocationNode(name="Outer Space")

tatain_people = ObjectNode(name="Tatain People", tags={"Type":"Mob","Count":5})
death_paradise_robots = ObjectNode(name="Death Paradise Robots", tags={"Type":"Mob","Count":5})
enemy_mercenary = ObjectNode(name="Enemy Mercenary", tags={"Type":"Mob","Count":5})
earth_army = ObjectNode(name="Earth Army", tags={"Type":"Mob","Count":5})

all_characters = [columbo, iris, amil, alien_god]
all_locations = [earth, new_world_greenland, tatain, death_paradise, outer_space]
other_objects = [tatain_people, death_paradise_robots, enemy_mercenary, earth_army]

all_objects = all_characters + all_locations + other_objects

world_state = WorldState(name="World of Gearngs Story", objectnodes=all_objects)

#Now, we need to make connections

world_state.doubleconnect(nodeA=outer_space, edge_name=world_state.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=tatain)
world_state.doubleconnect(nodeA=outer_space, edge_name=world_state.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=death_paradise)
world_state.doubleconnect(nodeA=outer_space, edge_name=world_state.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=earth)
world_state.doubleconnect(nodeA=outer_space, edge_name=world_state.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=new_world_greenland)
world_state.doubleconnect(nodeA=outer_space, edge_name=world_state.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=alien_god_planet)

world_state.connect(from_node=new_world_greenland, edge_name="holds", to_node=columbo)
world_state.connect(from_node=tatain, edge_name="holds", to_node=iris)
world_state.connect(from_node=earth, edge_name="holds", to_node=amil)
world_state.connect(from_node=alien_god_planet, edge_name="holds", to_node=alien_god)

world_state.connect(from_node=tatain, edge_name="holds", to_node=tatain_people)
world_state.connect(from_node=death_paradise, edge_name="holds", to_node=death_paradise_robots)
world_state.connect(from_node=outer_space, edge_name="holds", to_node=enemy_mercenary)
world_state.connect(from_node=earth, edge_name="holds", to_node=earth_army)

world_state.connect(from_node=amil, edge_name="commands", to_node=earth_army)
world_state.connect(from_node=earth_army, edge_name="obeys", to_node=amil)

world_state.connect(from_node=alien_god, edge_name="commands", to_node=iris)
world_state.connect(from_node=iris, edge_name="obeys", to_node=alien_god)

#Nodes
#Resurrect: Target must be dead, target must be a robot, the actor must command the target