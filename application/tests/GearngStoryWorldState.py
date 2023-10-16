import sys

sys.path.insert(0,'')

from application.components.StoryObjects import CharacterNode, LocationNode, ObjectNode
from application.components.WorldState import WorldState
from application.components.StoryNode import StoryNode
from application.components.UtilityEnums import *
from application.components.ConditionTest import *
from application.components.RelChange import *

columbo = CharacterNode(name="Columbo", biases={"lawbias":0, "moralbias":0}, tags={"Type":"Character","Species":"Human", "Goal":"Explore New World","Alive":True, "Stranded":True})
iris = CharacterNode(name="Iris", biases={"lawbias":0, "moralbias":0}, tags={"Type":"Character","Species":"Robot", "Goal":"Eradicate Living Beings", "Version":"Old", "Alive":True})
amil = CharacterNode(name="Amil", biases={"lawbias":0, "moralbias":0}, tags={"Type":"Character","Species":"Human", "Goal":"Rescue Mission","PlotArmor":True,"Alive":True})

alien_god = CharacterNode(name="Alien God", biases={"lawbias":100, "moralbias":0}, tags={"Type":"Character","Species":"God", "Alive":True})
apollo = CharacterNode(name="Apollo", biases={"lawbias":100, "moralbias":0}, tags={"Type":"Character","Species":"Robot", "Goal":"Repel Greenland Humans","Version":"New","Alive":False})

earth = LocationNode(name="Earth", tags={"Type":"Location", "Climate":"Hi-Tech", "AlienGodsWill":"Unknown"})
new_world_greenland = LocationNode(name="New World Greenland", tags={"Type":"Location", "Climate":"Lush", "AlienGodsWill":"Preserve"})
tatain = LocationNode(name="Tatain", tags={"Type":"Location", "Climate":"Sandy", "AlienGodsWill":"Destroy"})
death_paradise = LocationNode(name="Death Paradise", tags={"Type":"Location", "Climate":"Poisonous", "AlienGodsWill":"Destroy"})
alien_god_planet = LocationNode(name="Alien God Planet", tags={"Type":"Location", "Climate":"Unknown", "AlienGodsWill":"Unknown"})
outer_space = LocationNode(name="Outer Space", tags={"Type":"Location", "Climate":"Space", "AlienGodsWill":"Unknown"})

greenland_insects = ObjectNode(name="Greenland Insects", tags={"Type":"Mob", "Count":"5", "Behavior":"Aggressive", "EdibleFlesh":True})
tatain_people = ObjectNode(name="Tatain People", tags={"Type":"Mob","Count":5, "Behavior":"Passive"})
death_paradise_robots = ObjectNode(name="Death Paradise Robots", tags={"Type":"Mob","Count":5, "Behavior":"Aggressive"})
enemy_mercenary = ObjectNode(name="Enemy Mercenary", tags={"Type":"Mob","Count":5, "Behavior":"Aggressive"})
earth_army = ObjectNode(name="Earth Army", tags={"Type":"Mob","Count":5, "Behavior":"Passive"})

all_characters = [columbo, iris, amil, apollo, alien_god]
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
world_state.connect(from_node=alien_god_planet, edge_name="holds", to_node=apollo)

world_state.connect(from_node=tatain, edge_name="holds", to_node=tatain_people)
world_state.connect(from_node=death_paradise, edge_name="holds", to_node=death_paradise_robots)
world_state.connect(from_node=outer_space, edge_name="holds", to_node=enemy_mercenary)
world_state.connect(from_node=earth, edge_name="holds", to_node=earth_army)

world_state.connect(from_node=amil, edge_name="commands", to_node=earth_army)
world_state.connect(from_node=earth_army, edge_name="obeys", to_node=amil)

world_state.connect(from_node=alien_god, edge_name="commands", to_node=iris)
world_state.connect(from_node=iris, edge_name="obeys", to_node=alien_god)

world_state.connect(from_node=alien_god, edge_name="commands", to_node=apollo)
world_state.connect(from_node=apollo, edge_name="obeys", to_node=alien_god)

# Nodes
# (All rules require that the characters (both actor and target) be alive unless specified)

actor_alive = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Alive", value=True)
target_alive = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Alive", value=True)

# Resurrect with Data Backup:
# Conditions: Target must be dead, target must be a robot, the actor must command the target, actor must be a god, target must not have tag version:deprecated
# Changes: Target becomes alive, target's location moves to actor's location

target_dead = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Alive", value=False)
target_is_robot = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Species", value="Robot")
actor_commands_target = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="commands", object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True)
actor_is_god = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Species", value="Robot")

target_becomes_alive = TagChange(name="Target Becomes Alive", object_node_name=GenericObjectNode.GENERIC_TARGET, tag="Alive", value=True, add_or_remove=ChangeAction.ADD)

check_if_holding_target = HasEdgeTest(object_from_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name_test="holds", object_to_test=GenericObjectNode.GENERIC_TARGET)
stop_holding_target = RelChange(name="Noli Me Tangere", node_a=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name="holds", node_b=GenericObjectNode.GENERIC_TARGET, value=None, soft_equal=True, add_or_remove=ChangeAction.REMOVE)

thing_currently_holding_target_no_longer_holds_it = ConditionalChange(name="Thing that holds target no longer holds it", list_of_condition_tests=[check_if_holding_target], list_of_changes=[stop_holding_target])
current_location_holds_target = RelChange(name="Current Location Holds Target", node_a=GenericObjectNode.GENERIC_LOCATION, edge_name="holds", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.ADD, value=None)

resurrect_target = StoryNode

# Kill:
# Conditions: Actor must have a KillReason (Planet Invader, Revenge), Target must be Alive, Target must not have Plot Armor
# Changes: Target becomes dead

actor_has_reason_to_kill_target = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="KillReason", object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True)
target_no_plot_armor = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="PlotArmor", value=True, inverse=True)

target_has_no_plot_armor = HasTagTest


kill_another_actor = StoryNode

# Attack Inhabitants:
# Conditions: Actor's goal must be to Eradicate Living Beings, Actor share location with Target, Target is a Mob, target's count is greater than 0

attack_inhabitants = StoryNode

# Kill Mob for Food:
# Conditions: Actor's Goal must be to Explore New World, Target is a mob, Target has tag Edible Flesh: True, target's count is greater than 0, follows Get Ambushed By Mob
# Changes: Target's count reduces by 1

kill_greenland_insect_for_food = StoryNode

# Eradicate Inhabitants (one for each mob type):
# Conditions: Target is a mob, target's count is greater than 0, actor either shares a location with target or is a god. Actor must command someone who is dead.
# Changes: Target's Count goes to Zero

eradicate_mob = StoryNode      

# Get Attacked by Mob (one for each aggressive mob):
# Conditions: Actor and mob share location, The Target is a Mob, The Target has tag Behavior: Aggressive Or the Target must have KillReason edge towards Actor.

attacked_by_mob = StoryNode

# Killed by Mob (one for each aggressive mob):
# Conditions: Actor must not have tag Plot Armor: True. This node follows Attack Inhabitants or Get Ambushed by Mob.
# Changes: Actor gets tag Alive: False

killed_by_mob = StoryNode

# Kill Mob as Defense (one for each aggressive mob):
# Conditions: This node follows Get Attacked by Mob. Target must be a mob. Target's count must be greater than 0.
# Changes: Target's count reduces by 1.

kill_mob_as_defense = StoryNode

# NoticeInvader
# Conditions: Actor shares location with Target. Location has tag "AlienGodsWill" : "Preserve" Target is a human.
# Changes: New Edge: Actor --KillReason (PlanetInvader)--> Target

notice_invader = StoryNode

# Explore World
# Conditions: Actor's Goal is to Explore New World
# Changes: Actor has knowledge of the world

explore_world = StoryNode

# Command Army to Attack
# Conditions: Actor must command something that is a mob. That something must have a count of greater than one.
# Changes: Conditional Change: All objects tagged as Mob that the Actor commands will have Kill Reason towards Target (Following Orders)

command_army_attack = StoryNode

# Record Data of Earth's Army
# Conditions: Actor must be a robot. This node follows Get Attacked By Mob. 

record_earth_army_data = StoryNode

# Create Apollo
# Conditions: Target must be a Robot. Actor must command Target. Actor must command someone, who has data of Earth Army. Actor must NOT command anyone alive. Actor must become alive.
# Changes: Target becomes alive. Conditional Change: Any character that the Actor Commands that has version:old instead will have version:deprecated

create_apollo = StoryNode

# Wait
# Conditions -

DEFAULT_WAIT_NODE = StoryNode(name="Wait", biasweight=0, tags= {"Type":"Placeholder"}, charcount=1)

# (For Amil after killing Iris) Settle in New World
# Conditions:
# Changes: Remove Amil's plot armor

# Extra Movement Requirement:
# Actor must NOT have tag Stranded:True

# Tasks
# Rescue Columbo
# Source: Get Command From Higher Ups
# Requirement: Columbo must be alive.
# Placeholder Actors: "columbo" -> Stranded Human
#
# Destroy Tatain
# Source: Alien God
# Requirement: Alien God must not have knowledge of Destroy Tatain Task.
# Action: (Tatain): Attack Inhabitants
#
# Destory Death Paradise
# Source: Alien God
# Requirement: Alien God must not have knowledge of Destroy Death Pardise Task.
# Actions: (Death Paradise): Attacked by Mob
#
# Preserve Greenland
# Source: Alien God
# Requirement: Alien God must not have knowledge of Preserve Greenland Task.
# Actions: (New World Greenland): Notice Invader
# Placeholder Actors: "columbo" -> Stranded Human

# Starting Story Graph:
# Non Main Characters will wait
# Main Characters:
#
# Columbo is in New World / Greenland in Timestep 0, and is waiting in Timestep 1
# Iris is in Alien God Planet in Timestep 0 getting task to Destroy Tatain, and is waiting in Timestep 1
# Amil is Waiting at Earth in Timestep 0, and gets the task to rescue Columbo in Timestep 1