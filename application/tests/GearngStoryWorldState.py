import sys

sys.path.insert(0,'')

from application.components.StoryObjects import CharacterNode, LocationNode, ObjectNode
from application.components.WorldState import WorldState
from application.components.StoryNode import StoryNode
from application.components.UtilityEnums import *
from application.components.ConditionTest import *
from application.components.RelChange import *
from application.components.CharacterTask import *

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

greenland_insects = ObjectNode(name="Greenland Insects", tags={"Type":"Mob", "Count":"5", "Behavior":"Aggressive", "EdibleFlesh":True, "Faction":None})
tatain_people = ObjectNode(name="Tatain People", tags={"Type":"Mob","Count":5, "Behavior":"Passive", "Faction":"Tatain"})
death_paradise_robots = ObjectNode(name="Death Paradise Robots", tags={"Type":"Mob","Count":5, "Behavior":"Aggressive", "Faction":"Death Paradise"})
enemy_mercenary = ObjectNode(name="Enemy Mercenary", tags={"Type":"Mob","Count":5, "Behavior":"Aggressive", "Faction":"Mercenary"})
earth_army = ObjectNode(name="Earth Army", tags={"Type":"Mob","Count":5, "Behavior":"Passive", "Faction":"Earth"})

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

actor_is_alive = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Alive", value=True)
target_is_alive = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Alive", value=True)

# Resurrect with Data Backup:
# Conditions: Target must be dead, target must be a robot, the actor must command the target, actor must be a god, target must not have tag version:deprecated
# Changes: Target becomes alive, target's location moves to actor's location

target_dead = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Alive", value=False)
target_is_robot = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Species", value="Robot")
actor_commands_target = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="commands", object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True)
actor_is_god = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Species", value="God")

target_becomes_alive = TagChange(name="Target Becomes Alive", object_node_name=GenericObjectNode.GENERIC_TARGET, tag="Alive", value=True, add_or_remove=ChangeAction.ADD)

check_if_holding_target = HasEdgeTest(object_from_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name_test="holds", object_to_test=GenericObjectNode.GENERIC_TARGET)
stop_holding_target = RelChange(name="Noli Me Tangere", node_a=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name="holds", node_b=GenericObjectNode.GENERIC_TARGET, value=None, soft_equal=True, add_or_remove=ChangeAction.REMOVE)

thing_currently_holding_target_no_longer_holds_it = ConditionalChange(name="Thing that holds target no longer holds it", list_of_condition_tests=[check_if_holding_target], list_of_changes=[stop_holding_target])

check_if_holding_actor = HasEdgeTest(object_from_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name_test="holds", object_to_test=GenericObjectNode.GENERIC_ACTOR)
start_holding_target = RelChange(name="Touch Me", node_a=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name="holds", node_b=GenericObjectNode.GENERIC_TARGET, value=None, soft_equal=True, add_or_remove=ChangeAction.ADD)

thing_holding_actor_begins_holding_target = ConditionalChange(name="Thing that holds actor holds target", list_of_condition_tests=[check_if_holding_actor], list_of_changes=[start_holding_target])

resurrect_target = StoryNode(name="Resurrect Target", tags={"Type":"Resurrection"}, charcount=1, target_count=1, effects_on_next_ws=[thing_currently_holding_target_no_longer_holds_it, thing_holding_actor_begins_holding_target, target_becomes_alive], required_test_list=[actor_is_alive, target_dead, target_is_robot, actor_is_god, actor_commands_target])

# Kill:
# Conditions: Actor must have a KillReason (Planet Invader, Revenge), Target must be Alive, Target must not have Plot Armor
# Changes: Target becomes dead

actor_has_reason_to_kill_target = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="KillReason", object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True)
target_no_plot_armor = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="PlotArmor", value=True, inverse=True)

target_becomes_dead = TagChange(name="Target Becomes Dead", object_node_name=GenericObjectNode.GENERIC_TARGET, tag="Alive", value=False, add_or_remove=ChangeAction.ADD)

kill_another_actor = StoryNode(name="Actor Kills Actor", tags={"Type":"Murder"}, charcount=1, target_count=1, effects_on_next_ws=[target_becomes_dead], required_test_list=[actor_has_reason_to_kill_target, target_no_plot_armor])

# Attack Inhabitants:
# Conditions: Actor's goal must be to Eradicate Living Beings, Actor share location with Target, Target is a Mob, target's count is greater than 0

actors_goal_is_eradication = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Goal", value="Eradicate Living Beings")
actor_shares_location_with_target = SameLocationTest(list_to_test=[GenericObjectNode.GENERIC_ACTOR, GenericObjectNode.GENERIC_TARGET])
target_is_mob = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Type", value="Mob")
target_count_greater_than_0 = TagValueInRangeTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Count", value_min=1, value_max=999)

attack_inhabitants = StoryNode(name="Attack Inhabitants", tags={"Type":"Fight"}, required_test_list=[actors_goal_is_eradication, actor_shares_location_with_target, target_is_mob, target_count_greater_than_0])

# Kill Mob for Food:
# Conditions: Actor's Goal must be to Explore New World, Target is a mob, Target has tag Edible Flesh: True, target's count is greater than 0, follows Get Ambushed By Mob, actor and target shares location
# Changes: Target's count reduces by 1

actors_goal_is_explore = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Goal", value="Explore New World")
target_flesh_is_edible = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="EdibleFlesh", value=True)
reduce_target_count_by_1 = RelativeTagChange(name="Reduce Count by One", object_node_name=GenericObjectNode.GENERIC_TARGET, tag="Count", value_delta=-1)
kill_mob_for_food = StoryNode(name="Kill Mob For Food", required_test_list=[actors_goal_is_explore, target_flesh_is_edible, target_is_mob, target_count_greater_than_0, actor_shares_location_with_target], effects_on_next_ws=[reduce_target_count_by_1])

# Eradicate Inhabitants (one rule object for each mob type):
# Conditions: Target is a mob, target's count is greater than 0, actor either shares a location with target or is a god. If Actor is God, Actor must also command something dead.
# Changes: Target's Count goes to Zero

something_shares_location_with_target = SameLocationTest(list_to_test=[GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, GenericObjectNode.GENERIC_TARGET])
something_is_god = HasTagTest(object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, tag="Species", value="Robot")

actor_with_target_or_actor_is_god = ObjectPassesAtLeastOneTestTest(list_of_tests_with_placeholder=[something_is_god, something_shares_location_with_target], object_to_test=GenericObjectNode.GENERIC_ACTOR)

# something_is_dead = HasTagTest(object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, tag="Alive", value=False)
# actor_commands_something = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="commands", object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, soft_equal=True)

# actor_commands_something_dead = IntersectObjectExistsTest(list_of_tests_with_placeholder=[something_is_dead, actor_commands_something])

target_count_zeros = TagChange(name="Target Count Zeros", object_node_name=GenericObjectNode.GENERIC_TARGET, tag="Count", value=0, add_or_remove=ChangeAction.ADD)

eradicate_mob_with_godly_power = StoryNode(name="Eradicate Mobs With God Power", tags={"Type":"Destruction"}, effects_on_next_ws=[target_count_zeros], required_test_list=[actor_is_god, target_count_greater_than_0, target_is_mob])      
massacre_mob = StoryNode(name="Massacre Mobs", tags={"Type":"Destruction"}, effects_on_next_ws=[target_count_zeros], required_test_list=[actor_shares_location_with_target, actors_goal_is_eradication, target_count_greater_than_0, target_is_mob])      

# Get Attacked by Mob (one rule object for each aggressive mob):
# Conditions: Actor and target share location, The Target is a Mob, The Target has tag Behavior: Aggressive Or the Target must have KillReason edge towards Actor.

something_is_aggressive = HasTagTest(object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, tag="Behavior", value="Aggressive")
something_has_reason_to_kill_actor = HasEdgeTest(object_from_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name_test="KillReason", object_to_test=GenericObjectNode.GENERIC_ACTOR, soft_equal=True)

target_is_aggressive_or_has_kill_reason = ObjectPassesAtLeastOneTestTest(list_of_tests_with_placeholder=[something_is_aggressive, something_has_reason_to_kill_actor], object_to_test=GenericObjectNode.GENERIC_TARGET)

attacked_by_mob = StoryNode(name="Attacked by Mob", tags={"Type":"Fight"}, required_test_list=[target_is_mob, actor_has_reason_to_kill_target, actor_shares_location_with_target, target_is_mob])

# Killed by Mob (one for each aggressive mob):
# Conditions: Actor must not have tag Plot Armor: True. Actor and Target shares location. This node follows Attack Inhabitants or Get Ambushed by Mob.
# Changes: Actor gets tag Alive: False

actor_has_no_plot_armor = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="PlotArmor", value=True, inverse=True)
actor_becomes_dead = TagChange(name="Target Becomes Dead", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="Alive", value=False, add_or_remove=ChangeAction.ADD)

killed_by_mob = StoryNode(name="Get Killed by Mob", effects_on_next_ws=[actor_becomes_dead], required_test_list=[actor_is_alive, actor_has_no_plot_armor, actor_shares_location_with_target])

# Kill Mob as Defense (one for each aggressive mob):
# Conditions: This node follows Get Attacked by Mob. Target must be a mob. Target's count must be greater than 0. Actor and Target must share location.
# Changes: Target's count reduces by 1.

kill_mob_as_defense = StoryNode(name="Kill Mob as Defense", effects_on_next_ws=[reduce_target_count_by_1], required_test_list=[actor_is_alive, target_is_mob, target_count_greater_than_0, actor_shares_location_with_target])

# NoticeInvader
# Conditions: Actor shares location with Target. Location has tag "AlienGodsWill" : "Preserve" Target is a human.
# Changes: New Edge: Actor --KillReason (PlanetInvader)--> Target

location_has_preserve_will = HasTagTest(object_to_test=GenericObjectNode.GENERIC_LOCATION, tag="AlienGodsWill", value="Preserve")
target_is_human = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Species", value="Human")
actor_gets_kill_reason_towards_target_invasion = RelChange(name="Gain Invasion Kill Reason", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="KillReason", node_b=GenericObjectNode.GENERIC_TARGET, soft_equal="PlanetInvader", add_or_remove=ChangeAction.ADD)

notice_invader = StoryNode(name="Notice Planet Invader", charcount=1, target_count=1, effects_on_next_ws=[actor_gets_kill_reason_towards_target_invasion], required_test_list=[actor_is_alive, target_is_alive, actor_shares_location_with_target, location_has_preserve_will, target_is_human])

# Explore World
# Conditions: Actor's Goal is to Explore New World, current location has Lush climate

location_is_lush = HasTagTest(object_to_test=GenericObjectNode.GENERIC_LOCATION, tag="Climate", value="Lush")
explore_world = StoryNode(name="Explore World", required_test_list=[actor_is_alive, location_is_lush, actors_goal_is_explore])

# Command Army to Attack
# Conditions: Actor must command something that is a mob. That something must have a count of greater than one.
# Changes: Conditional Change: All objects tagged as Mob that the Actor commands will have Kill Reason towards Target (Following Orders)

something_is_a_mob = HasTagTest(object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, tag="Type", value="Mob")
actor_commands_something = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="commands", object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, soft_equal=True)
somethings_count_is_greater_than_0 = TagValueInRangeTest(object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, tag="Count", value_min=1, value_max=999)
actor_commands_a_mob_with_greater_count = IntersectObjectExistsTest(list_of_tests_with_placeholder=[something_is_a_mob, actor_commands_something, somethings_count_is_greater_than_0])

something_gets_kill_reason_towards_target_orders = RelChange(name="Gain Invasion Kill Reason", node_a=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name="KillReason", node_b=GenericObjectNode.GENERIC_TARGET, soft_equal="FollowingOrders", add_or_remove=ChangeAction.ADD)
if_commanded_by_actor_then_kill_target_reason = ConditionalChange(name="If Commanded then Kill Reason", list_of_condition_tests=[something_is_a_mob, actor_commands_something], list_of_changes=[something_gets_kill_reason_towards_target_orders])

command_army_attack = StoryNode(name="Command Army to Attack", effects_on_next_ws=[if_commanded_by_actor_then_kill_target_reason], required_test_list=[actor_is_alive, actor_commands_a_mob_with_greater_count])

# Record Data of Earth's Army
# Conditions: Actor must be a robot. Actor shares location with something that is a mob and also belongs to the faction Earth. This node follows Get Attacked By Mob. 
# Changes: Actor gains data of Earth Army.

somethings_faction_is_earth = HasTagTest(object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, tag="Faction", value="Earth")
actor_shares_location_with_something = SameLocationTest(list_to_test=[GenericObjectNode.GENERIC_ACTOR, GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER])

actor_shares_location_with_mob_from_earth = IntersectObjectExistsTest(list_of_tests_with_placeholder=[something_is_a_mob, somethings_faction_is_earth, actor_shares_location_with_something])

actor_gains_earth_army_data = TagChange(name="Gain Earth Army Data", tag="HasEarthArmyData", value=True)

record_earth_army_data = StoryNode(name="Record Earth Army Data", required_test_list=[actor_is_alive, actor_shares_location_with_mob_from_earth], effects_on_next_ws=[actor_gains_earth_army_data])

# Create Apollo
# Conditions: Target must be a Robot. Actor must command Target. Actor must command someone, who has data of Earth Army. Actor must NOT command anyone alive.
# Changes: Target becomes alive. Conditional Change: Any character that the Actor Commands that has version:old instead will have version:deprecated

something_has_data_of_earths_army = HasTagTest(object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, tag="HasEarthArmyData", value=True)

actor_commands_someone_with_earth_army_data = IntersectObjectExistsTest(list_of_tests_with_placeholder=[something_has_data_of_earths_army, actor_commands_something])

actor_commands_something = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="commands", object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, soft_equal=True)
something_is_alive = HasTagTest(object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, tag="Alive", value=True)

actor_does_not_command_anyone_alive = IntersectObjectExistsTest(list_of_tests_with_placeholder=[actor_commands_something, something_is_alive], inverse=True)

something_is_old_version = HasTagTest(object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, tag="Version", value="Old")
something_version_is_deprecated = TagChange(name="Deprecate", object_node_name=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, tag="Version", value="Deprecated", add_or_remove=ChangeAction.ADD)

change_version_of_actor_commanded_objects = ConditionalChange(name="Change Version of Actor Commanded Objects", list_of_condition_tests=[something_is_old_version, actor_commands_something], list_of_changes=[something_version_is_deprecated])

create_apollo = StoryNode(name="Birth of Apollo", required_test_list=[target_is_robot, actor_commands_target, actor_commands_someone_with_earth_army_data, actor_does_not_command_anyone_alive, actor_is_alive], effects_on_next_ws=[change_version_of_actor_commanded_objects, target_becomes_alive])

# Wait
# Conditions -

DEFAULT_WAIT_NODE = StoryNode(name="Wait", biasweight=0, tags= {"Type":"Placeholder"}, charcount=1)

# (For Amil after killing Iris) Settle in New World
# Conditions: Character is in a location with a Lush climate. Character has plot armor.
# Changes: Remove Amil's plot armor

# Extra Movement Requirement:
# Actor must NOT have tag Stranded:True

# Tasks
# Rescue Columbo
# Source: Get Command From Higher Ups
# Owner: Amil
# Requirement: Columbo must be alive.
# Placeholder Actors: "columbo" -> Stranded Human

find_columbo = StoryNode(name="Find Columbo", tags={"Type":"Conversation"}, target_count=1, actor=[GenericObjectNode.TASK_OWNER], target=["columbo"])

find_columbo_task = CharacterTask(task_name="Find Columbo Task", task_actions=[find_columbo], actor_placeholder_string_list=["columbo"])

columbo_goal_is_explore_world = HasTagTest(object_to_test="columbo", tag="Goal", value="Explore New World")
find_columbo_stack = TaskStack(stack_name="Find Columbo Stack", task_stack=[find_columbo_task], task_stack_requirement=[columbo_goal_is_explore_world])

get_rescue_columbo_task = TaskChange(name="Get Rescue Columbo Task", task_giver_name=None, task_owner_name="Amil", task_stack=find_columbo_stack)

get_command_from_higher_up = StoryNode(name="Get Command from Higher Up")

# Destroy Tatain
# Source: Alien God
# Owner: Iris
# Requirement: Alien God must not have knowledge of Destroy Tatain Task.
# Action: (Tatain): Attack Inhabitants

task_giver_not_know_about_tatain_task = HasTagTest(object_to_test=GenericObjectNode.TASK_GIVER, tag="HasGivenTatainTask", value=True, inverse=True)

# Destory Death Paradise
# Source: Alien God
# Owner: Iris
# Requirement: Alien God must not have knowledge of Destroy Death Pardise Task.
# Actions: (Death Paradise): Attacked by Mob

task_giver_not_know_about_dp_task = HasTagTest(object_to_test=GenericObjectNode.TASK_GIVER, tag="HasGivenDeathParaTask", value=True, inverse=True)

# Preserve Greenland
# Source: Alien God
# Owner: Iris
# Requirement: Alien God must not have knowledge of Preserve Greenland Task.
# Actions: (New World Greenland): Notice Invader
# Placeholder Actors: "columbo" -> Stranded Human

task_giver_not_know_about_greenland_task = HasTagTest(object_to_test=GenericObjectNode.TASK_GIVER, tag="HasGivenGreenlandTask", value=True, inverse=True)

# Invade Greenland
# Source: Alien God
# Owner: Apollo
# Requirement: Alien God must not have knowledge of the Invade Greenland task
# Actions: (New World Greenland): Attack Greenland

# (The nodes that give away these tasks will in itself give knowledge of the task to the giver)

task_giver_not_know_about_attack_greenland_task = HasTagTest(object_to_test=GenericObjectNode.TASK_GIVER, tag="HasGivenAttackGreenlandTask", value=True, inverse=True)

# Rules

# Ambush -+> Kill Mob as Defense
# Ambush -+> Kill Mob for Food
# Attacked by Mob -+> Record Earth Army Data
# Attacked by Mob -+> Killed by Mob
# Attack Inhabitants -> Killed by Mob
# Attacked by Mob -> Massacre Mobs
# Attack Inhabitants -> Massacre Mobs

# (Nothing) -> Kill Actor
# (Nothing) -> Attack Inhabitants
# (Nothing) -> Command Army to Attack
# (Nothing) -> Eradicate Mob With God Power
# (Nothing) -> Attacked by Mob
# (Nothing) -> Create Apollo
# (Nothing) -> Data Backup Resurrection

# Starting Story Graph:
# Non Main Characters will wait
# Main Characters:
#
# Columbo is in New World / Greenland in Timestep 0 and performing Explore World, and is waiting in Timestep 1
# Iris is in Alien God Planet in Timestep 0 getting task to Destroy Tatain, and is waiting in Timestep 1
# Amil is Waiting at Earth in Timestep 0, and gets the task to rescue Columbo in Timestep 1

# Current Problems
# We don't know how to define score properly. Whoops?
# We need to assign scores to the individual nodes.