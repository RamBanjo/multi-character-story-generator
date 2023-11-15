from copy import deepcopy
import sys

sys.path.insert(0,'')

from application.components.StoryObjects import CharacterNode, LocationNode, ObjectNode
from application.components.WorldState import WorldState
from application.components.StoryNode import StoryNode
from application.components.UtilityEnums import *
from application.components.ConditionTest import *
from application.components.RelChange import *
from application.components.CharacterTask import *
from application.components.RewriteRuleWithWorldState import ContinuousJointRule, RewriteRule, JoiningJointRule
from application.components.UtilFunctions import copy_story_node_with_extra_conditions
from application.components.StoryGraphTwoWS import StoryGraph, calculate_score_from_char_and_unpopulated_node_with_both_slots
from application.StoryGeneration_NewFlowchart import *

columbo = CharacterNode(name="Columbo", biases={"lawbias":0, "moralbias":0}, tags={"Type":"Character","Job":"Explorer","Species":"Human", "Goal":"Explore New World","Alive":True, "PlotArmor":True, "Stranded":True}, internal_id=0)
iris = CharacterNode(name="Iris", biases={"lawbias":0, "moralbias":0}, tags={"Type":"Character","Job":"Destroyer","Species":"Robot", "Goal":"Eradicate Living Beings", "Version":"Old", "Alive":True}, internal_id=1)
amil = CharacterNode(name="Amil", biases={"lawbias":0, "moralbias":0}, tags={"Type":"Character","Job":"Military","Species":"Human", "Goal":"Rescue Mission","PlotArmor":True,"Alive":True}, internal_id=2)

alien_god = CharacterNode(name="Alien God", biases={"lawbias":100, "moralbias":0}, tags={"Type":"Character","Species":"God", "Alive":True, "Stranded":True}, internal_id=3)
apollo = CharacterNode(name="Apollo", biases={"lawbias":100, "moralbias":0}, tags={"Type":"Character","Job":"Destroyer","Species":"Robot", "Goal":"Repel Greenland Humans","Version":"New","Alive":False}, internal_id=4)

earth = LocationNode(name="Earth", tags={"Type":"Location", "Climate":"Hi-Tech", "AlienGodsWill":"Unknown"}, internal_id=5)
new_world_greenland = LocationNode(name="New World Greenland", tags={"Type":"Location", "Climate":"Lush", "AlienGodsWill":"Preserve"}, internal_id=6)
tatain = LocationNode(name="Tatain", tags={"Type":"Location", "Climate":"Sandy", "AlienGodsWill":"Destroy"}, internal_id=7)
death_paradise = LocationNode(name="Death Paradise", tags={"Type":"Location", "Climate":"Poisonous", "AlienGodsWill":"Destroy"}, internal_id=8)
alien_god_planet = LocationNode(name="Alien God Planet", tags={"Type":"Location", "Climate":"Unknown", "AlienGodsWill":"Unknown"}, internal_id=9)
outer_space = LocationNode(name="Outer Space", tags={"Type":"Location", "Climate":"Space", "AlienGodsWill":"Unknown"}, internal_id=10)

greenland_insects = ObjectNode(name="Greenland Insects", tags={"Type":"Mob", "Count":2, "Behavior":"Aggressive", "EdibleFlesh":True, "Faction":None},internal_id=11)
tatain_people = ObjectNode(name="Tatain People", tags={"Type":"Mob","Count":1, "Behavior":"Passive", "Faction":"Tatain"}, internal_id=12)
death_paradise_robots = ObjectNode(name="Death Paradise Robots", tags={"Type":"Mob","Count":1, "Behavior":"Aggressive", "Faction":"Death Paradise"}, internal_id=13)
enemy_mercenary = ObjectNode(name="Enemy Mercenary", tags={"Type":"Mob","Count":1, "Behavior":"Aggressive", "Faction":"Mercenary"}, internal_id=14)
earth_army = ObjectNode(name="Earth Army", tags={"Type":"Mob","Count":2, "Behavior":"Passive", "Faction":"Earth"}, internal_id=15)

all_characters = [columbo, iris, amil, apollo, alien_god]
all_locations = [earth, new_world_greenland, tatain, death_paradise, outer_space, alien_god_planet]
other_objects = [tatain_people, death_paradise_robots, enemy_mercenary, earth_army, greenland_insects]

all_objects = all_characters + all_locations + other_objects

world_state = WorldState(name="World of Gearngs Story", objectnodes=all_objects)

#Now, we need to make connections

world_state.doubleconnect(nodeA=outer_space, edge_name=world_state.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=tatain)
world_state.doubleconnect(nodeA=outer_space, edge_name=world_state.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=death_paradise)
world_state.doubleconnect(nodeA=outer_space, edge_name=world_state.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=earth)
world_state.doubleconnect(nodeA=outer_space, edge_name=world_state.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=new_world_greenland)
world_state.doubleconnect(nodeA=outer_space, edge_name=world_state.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=alien_god_planet)

world_state.connect(from_node=new_world_greenland, edge_name="holds", to_node=columbo)
world_state.connect(from_node=alien_god_planet, edge_name="holds", to_node=iris)
world_state.connect(from_node=earth, edge_name="holds", to_node=amil)
world_state.connect(from_node=alien_god_planet, edge_name="holds", to_node=alien_god)
world_state.connect(from_node=alien_god_planet, edge_name="holds", to_node=apollo)

world_state.connect(from_node=tatain, edge_name="holds", to_node=tatain_people)
world_state.connect(from_node=death_paradise, edge_name="holds", to_node=death_paradise_robots)
world_state.connect(from_node=outer_space, edge_name="holds", to_node=enemy_mercenary)
world_state.connect(from_node=earth, edge_name="holds", to_node=earth_army)
world_state.connect(from_node=new_world_greenland, edge_name="holds", to_node=greenland_insects)

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

target_is_greenland_insect = ObjectEqualityTest(object_list=[GenericObjectNode.GENERIC_TARGET, greenland_insects])
target_is_death_robots = ObjectEqualityTest(object_list=[GenericObjectNode.GENERIC_TARGET, death_paradise_robots])
target_is_space_mercs = ObjectEqualityTest(object_list=[GenericObjectNode.GENERIC_TARGET, enemy_mercenary])
target_is_tatain_people = ObjectEqualityTest(object_list=[GenericObjectNode.GENERIC_TARGET, tatain_people])
target_is_earth_army = ObjectEqualityTest(object_list=[GenericObjectNode.GENERIC_TARGET, earth_army])

target_becomes_alive = TagChange(name="Target Becomes Alive", object_node_name=GenericObjectNode.GENERIC_TARGET, tag="Alive", value=True, add_or_remove=ChangeAction.ADD)

check_if_holding_target = HasEdgeTest(object_from_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name_test="holds", object_to_test=GenericObjectNode.GENERIC_TARGET)
stop_holding_target = RelChange(name="Noli Me Tangere", node_a=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name="holds", node_b=GenericObjectNode.GENERIC_TARGET, value=None, soft_equal=True, add_or_remove=ChangeAction.REMOVE)

thing_currently_holding_target_no_longer_holds_it = ConditionalChange(name="Thing that holds target no longer holds it", list_of_condition_tests=[check_if_holding_target], list_of_changes=[stop_holding_target])

check_if_holding_actor = HasEdgeTest(object_from_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name_test="holds", object_to_test=GenericObjectNode.GENERIC_ACTOR)
start_holding_target = RelChange(name="Touch Me", node_a=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name="holds", node_b=GenericObjectNode.GENERIC_TARGET, value=None, soft_equal=True, add_or_remove=ChangeAction.ADD)

thing_holding_actor_begins_holding_target = ConditionalChange(name="Thing that holds actor holds target", list_of_condition_tests=[check_if_holding_actor], list_of_changes=[start_holding_target])

target_is_old_version = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Version", value="Old")
resurrect_target = StoryNode(name="Resurrect Target", tags={"Type":"Resurrection"}, charcount=1, target_count=1, effects_on_next_ws=[target_becomes_alive], required_test_list=[actor_is_alive, target_dead, actor_is_god, target_is_old_version])

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

attack_inhabitants_insects = copy_story_node_with_extra_conditions(base_node=attack_inhabitants, new_node_name="Attack Inhabitants - Insects", extra_condition_list=[target_is_greenland_insect])
attack_inhabitants_robots = copy_story_node_with_extra_conditions(base_node=attack_inhabitants, new_node_name="Attack Inhabitants - Robots", extra_condition_list=[target_is_death_robots])
attack_inhabitants_mercs = copy_story_node_with_extra_conditions(base_node=attack_inhabitants, new_node_name="Attack Inhabitants - Mercs", extra_condition_list=[target_is_space_mercs])
attack_inhabitants_army = copy_story_node_with_extra_conditions(base_node=attack_inhabitants, new_node_name="Attack Inhabitants - Army", extra_condition_list=[target_is_earth_army])
attack_inhabitants_tatain = copy_story_node_with_extra_conditions(base_node=attack_inhabitants, new_node_name="Attack Inhabitants - Tatain", extra_condition_list=[target_is_tatain_people])

# Kill Mob for Food:
# Conditions: Actor's Goal must be to Explore New World, Target is a mob, Target has tag Edible Flesh: True, target's count is greater than 0, follows Get Ambushed By Mob, actor and target shares location
# Changes: Target's count reduces by 1

actors_goal_is_explore = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Goal", value="Explore New World")
target_flesh_is_edible = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="EdibleFlesh", value=True)
reduce_target_count_by_1 = RelativeTagChange(name="Reduce Count by One", object_node_name=GenericObjectNode.GENERIC_TARGET, tag="Count", value_delta=-1)
kill_mob_for_food = StoryNode(name="Kill Mob For Food", required_test_list=[actors_goal_is_explore, target_flesh_is_edible, target_is_mob, target_count_greater_than_0, actor_shares_location_with_target], effects_on_next_ws=[reduce_target_count_by_1])

kill_mob_for_food_insects = copy_story_node_with_extra_conditions(base_node=kill_mob_for_food, new_node_name="Kill for Food - Insects", extra_condition_list=[target_is_greenland_insect])

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

iris_is_dead = HasTagTest(object_to_test=iris, tag="Alive", value=False)
eradicate_mob_with_godly_power = StoryNode(name="Eradicate Mobs With God Power", tags={"Type":"Destruction"}, effects_on_next_ws=[target_count_zeros], required_test_list=[iris_is_dead, actor_is_god, target_count_greater_than_0, target_is_mob])      
massacre_mob = StoryNode(name="Massacre Mobs", tags={"Type":"Destruction"}, effects_on_next_ws=[target_count_zeros], required_test_list=[actor_shares_location_with_target, actors_goal_is_eradication, target_count_greater_than_0, target_is_mob])      

god_kills_insects = copy_story_node_with_extra_conditions(base_node=eradicate_mob_with_godly_power, new_node_name="God Kills Insects", extra_condition_list=[target_is_greenland_insect])
god_kills_robots = copy_story_node_with_extra_conditions(base_node=eradicate_mob_with_godly_power, new_node_name="God Kills Robots", extra_condition_list=[target_is_death_robots])
god_kills_mercs = copy_story_node_with_extra_conditions(base_node=eradicate_mob_with_godly_power, new_node_name="God Kills Mercs", extra_condition_list=[target_is_space_mercs])
god_kills_army = copy_story_node_with_extra_conditions(base_node=eradicate_mob_with_godly_power, new_node_name="God Kills Army", extra_condition_list=[target_is_earth_army])

massacre_insects = copy_story_node_with_extra_conditions(base_node=attack_inhabitants, new_node_name="Massacre Insects", extra_condition_list=[target_is_greenland_insect])
massacre_robots = copy_story_node_with_extra_conditions(base_node=attack_inhabitants, new_node_name="Massacre Robots", extra_condition_list=[target_is_death_robots])
massacre_mercs = copy_story_node_with_extra_conditions(base_node=attack_inhabitants, new_node_name="Massacre Mercs", extra_condition_list=[target_is_space_mercs])
massacre_army = copy_story_node_with_extra_conditions(base_node=attack_inhabitants, new_node_name="Massacre Army", extra_condition_list=[target_is_earth_army])
massacre_tatain = copy_story_node_with_extra_conditions(base_node=attack_inhabitants, new_node_name="Massacre Tatain", extra_condition_list=[target_is_tatain_people])

# Get Attacked by Mob (one rule object for each aggressive mob):
# Conditions: Actor and target share location, The Target is a Mob, The Target has tag Behavior: Aggressive Or the Target must have KillReason edge towards Actor.

something_is_aggressive = HasTagTest(object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, tag="Behavior", value="Aggressive")
something_has_reason_to_kill_actor = HasEdgeTest(object_from_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name_test="KillReason", object_to_test=GenericObjectNode.GENERIC_ACTOR, soft_equal=True)

target_is_aggressive_or_has_kill_reason = ObjectPassesAtLeastOneTestTest(list_of_tests_with_placeholder=[something_is_aggressive, something_has_reason_to_kill_actor], object_to_test=GenericObjectNode.GENERIC_TARGET)

attacked_by_mob = StoryNode(name="Attacked by Mob", tags={"Type":"Fight"}, required_test_list=[target_count_greater_than_0, target_is_mob, target_is_aggressive_or_has_kill_reason, actor_shares_location_with_target, target_is_mob])

attacked_by_insects = copy_story_node_with_extra_conditions(base_node=attacked_by_mob, new_node_name="Attacked by Insects", extra_condition_list=[target_is_greenland_insect])
attacked_by_robots = copy_story_node_with_extra_conditions(base_node=attacked_by_mob, new_node_name="Attacked by Robots", extra_condition_list=[target_is_death_robots])
attacked_by_mercs = copy_story_node_with_extra_conditions(base_node=attacked_by_mob, new_node_name="Attacked by Mercs", extra_condition_list=[target_is_space_mercs])
attacked_by_army = copy_story_node_with_extra_conditions(base_node=attacked_by_mob, new_node_name="Attacked by Army", extra_condition_list=[target_is_earth_army])

# Killed by Mob (one for each aggressive mob):
# Conditions: Actor must not have tag Plot Armor: True. Actor and Target shares location. This node follows Attack Inhabitants or Get Ambushed by Mob.
# Changes: Actor gets tag Alive: False

actor_has_no_plot_armor = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="PlotArmor", value=True, inverse=True)
actor_becomes_dead = TagChange(name="Target Becomes Dead", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="Alive", value=False, add_or_remove=ChangeAction.ADD)

killed_by_mob = StoryNode(name="Get Killed by Mob", effects_on_next_ws=[actor_becomes_dead], required_test_list=[actor_is_alive, actor_has_no_plot_armor, actor_shares_location_with_target, target_count_greater_than_0])

killed_by_insect = copy_story_node_with_extra_conditions(base_node=killed_by_mob, new_node_name="Killed by Insects", extra_condition_list=[target_is_greenland_insect])
killed_by_robots =  copy_story_node_with_extra_conditions(base_node=killed_by_mob, new_node_name="Killed by Robots", extra_condition_list=[target_is_death_robots])
killed_by_mercs =  copy_story_node_with_extra_conditions(base_node=killed_by_mob, new_node_name="Killed by Mercs", extra_condition_list=[target_is_space_mercs])
killed_by_army =  copy_story_node_with_extra_conditions(base_node=killed_by_mob, new_node_name="Killed by Army", extra_condition_list=[target_is_earth_army])


# Kill Mob as Defense (one for each aggressive mob):
# Conditions: This node follows Get Attacked by Mob. Target must be a mob. Target's count must be greater than 0. Actor and Target must share location.
# Changes: Target's count reduces by 1.

kill_mob_as_defense = StoryNode(name="Kill Mob as Defense", effects_on_next_ws=[reduce_target_count_by_1], required_test_list=[actor_is_alive, target_is_mob, target_count_greater_than_0, actor_shares_location_with_target])

self_defense_kill_insect = copy_story_node_with_extra_conditions(base_node=kill_mob_as_defense, new_node_name="Self Defense Kill - Insects", extra_condition_list=[target_is_greenland_insect])
self_defense_kill_robots =  copy_story_node_with_extra_conditions(base_node=kill_mob_as_defense, new_node_name="Self Defense Kill - Robots", extra_condition_list=[target_is_death_robots])
self_defense_kill_mercs =  copy_story_node_with_extra_conditions(base_node=kill_mob_as_defense, new_node_name="Self Defense Kill - Mercs", extra_condition_list=[target_is_space_mercs])
self_defense_kill_army =  copy_story_node_with_extra_conditions(base_node=kill_mob_as_defense, new_node_name="Self Defense Kill - Army", extra_condition_list=[target_is_earth_army])

# NoticeInvader
# Conditions: Actor shares location with Target. Location has tag "AlienGodsWill" : "Preserve" Target is a human.
# Changes: New Edge: Actor --KillReason (PlanetInvader)--> Target

#We should drop Location has Preserve Will because we already set the location in the Tasks
# location_has_preserve_will = HasTagTest(object_to_test=GenericObjectNode.GENERIC_LOCATION, tag="AlienGodsWill", value="Preserve")
target_is_human = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Species", value="Human")
actor_gets_kill_reason_towards_target_invasion = RelChange(name="Gain Invasion Kill Reason", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="KillReason", node_b=GenericObjectNode.GENERIC_TARGET, soft_equal="PlanetInvader", add_or_remove=ChangeAction.ADD)
target_loses_plot_armor = TagChange(name="Target Loses Plot Armor", object_node_name=GenericObjectNode.GENERIC_TARGET, tag="PlotArmor", value=True, add_or_remove=ChangeAction.REMOVE)

notice_invader = StoryNode(name="Notice Planet Invader", charcount=1, target_count=1, effects_on_next_ws=[actor_gets_kill_reason_towards_target_invasion, target_loses_plot_armor], required_test_list=[actor_is_alive, target_is_alive, actor_shares_location_with_target, target_is_human])

# Explore World
# Conditions: Actor's Goal is to Explore New World, current location has Lush climate

# location_is_lush = HasTagTest(object_to_test=GenericObjectNode.GENERIC_LOCATION, tag="Climate", value="Lush")
explore_world = StoryNode(name="Explore World", required_test_list=[actor_is_alive, actors_goal_is_explore])

# Command Army to Attack
# Conditions: Actor must command something that is a mob. That something must have a count of greater than one.
# Changes: Conditional Change: All objects tagged as Mob that the Actor commands will have Kill Reason towards Target (Following Orders)

something_is_a_mob = HasTagTest(object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, tag="Type", value="Mob")
actor_commands_something = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="commands", object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, soft_equal=True)
somethings_count_is_greater_than_0 = TagValueInRangeTest(object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, tag="Count", value_min=1, value_max=999)
actor_commands_a_mob_with_greater_count = IntersectObjectExistsTest(list_of_tests_with_placeholder=[something_is_a_mob, actor_commands_something, somethings_count_is_greater_than_0])

something_gets_kill_reason_towards_target_orders = RelChange(name="Gain Invasion Kill Reason", node_a=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name="KillReason", node_b=GenericObjectNode.GENERIC_TARGET, soft_equal="FollowingOrders", add_or_remove=ChangeAction.ADD)
if_commanded_by_actor_then_kill_target_reason = ConditionalChange(name="If Commanded then Kill Reason", list_of_condition_tests=[something_is_a_mob, actor_commands_something], list_of_changes=[something_gets_kill_reason_towards_target_orders])

command_army_attack = StoryNode(name="Command Army to Attack", target_count=1, effects_on_next_ws=[if_commanded_by_actor_then_kill_target_reason], required_test_list=[actor_is_alive, actor_has_reason_to_kill_target, actor_commands_a_mob_with_greater_count])

# Record Data of Earth's Army
# Conditions: Actor must be a robot. Actor shares location with something that is a mob and also belongs to the faction Earth. This node follows Get Attacked By Mob. 
# Changes: Actor gains data of Earth Army.

somethings_faction_is_earth = HasTagTest(object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, tag="Faction", value="Earth")
actor_shares_location_with_something = SameLocationTest(list_to_test=[GenericObjectNode.GENERIC_ACTOR, GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER])
actor_not_have_earth_army_data = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="HasEarthArmyData", value=True, inverse=True)

actor_shares_location_with_mob_from_earth = IntersectObjectExistsTest(list_of_tests_with_placeholder=[something_is_a_mob, somethings_faction_is_earth, actor_shares_location_with_something])

actor_gains_earth_army_data = TagChange(name="Gain Earth Army Data", tag="HasEarthArmyData", value=True, object_node_name=GenericObjectNode.GENERIC_ACTOR, add_or_remove=ChangeAction.ADD)

record_earth_army_data = StoryNode(name="Record Earth Army Data", required_test_list=[actor_is_alive, actor_shares_location_with_mob_from_earth, actor_not_have_earth_army_data], effects_on_next_ws=[actor_gains_earth_army_data])

# Create Apollo
# Conditions: Target must be a Robot. Actor must command Target. Actor must command someone, who has data of Earth Army. Actor must NOT command anyone alive.
# Changes: Target becomes alive. Conditional Change: Any charatecr that the Actor Commands that has version:old instead will have version:deprecated

something_has_data_of_earths_army = HasTagTest(object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, tag="HasEarthArmyData", value=True)

actor_commands_someone_with_earth_army_data = IntersectObjectExistsTest(list_of_tests_with_placeholder=[something_has_data_of_earths_army, actor_commands_something])

actor_commands_something = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="commands", object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, soft_equal=True)
something_is_alive = HasTagTest(object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, tag="Alive", value=True)

actor_does_not_command_anyone_alive = IntersectObjectExistsTest(list_of_tests_with_placeholder=[actor_commands_something, something_is_alive], inverse=True)

something_is_old_version = HasTagTest(object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, tag="Version", value="Old")
something_version_is_deprecated = TagChange(name="Deprecate", object_node_name=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, tag="Version", value="Deprecated", add_or_remove=ChangeAction.ADD)

change_version_of_actor_commanded_objects = ConditionalChange(name="Change Version of Actor Commanded Objects", list_of_condition_tests=[something_is_old_version, actor_commands_something], list_of_changes=[something_version_is_deprecated])

target_is_apollo = ObjectEqualityTest(object_list=[apollo, GenericObjectNode.GENERIC_TARGET])
create_apollo = StoryNode(name="Birth of Apollo", required_test_list=[target_is_robot, actor_commands_target, actor_commands_someone_with_earth_army_data, actor_does_not_command_anyone_alive, actor_is_alive], effects_on_next_ws=[change_version_of_actor_commanded_objects, target_becomes_alive])

# Actor Attacks Actor
# Conditions: Actor and Target are alive. Actor has reason to kill Target. Actor and Target share a location.
# Changes: Target gains reason to kill Actor. (Self Preservation)

target_gains_kill_reason = RelChange(name="Target Gains Self Preserve Kill Reason", edge_name="KillReason", value="SelfPreserve", add_or_remove=ChangeAction.ADD, node_a=GenericObjectNode.GENERIC_ACTOR, node_b=GenericObjectNode.GENERIC_TARGET)
actor_attack_another_actor = StoryNode(name="Actor Attacks Another Actor", target_count=1, effects_on_next_ws=[target_gains_kill_reason], required_test_list=[actor_shares_location_with_target, actor_has_reason_to_kill_target, actor_is_alive, target_is_alive])

# Wait
# Conditions -

DEFAULT_WAIT_NODE = StoryNode(name="Wait", biasweight=0, tags= {"Type":"Placeholder"}, charcount=1)

# (For Amil after killing Iris) Settle in New World
# Conditions: Character is in a location with a Lush climate. Character has plot armor.
# Changes: Remove Amil's plot armor

# Extra Movement Requirement:
# Actor must NOT have tag Stranded:True

actor_is_not_stranded = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Stranded", value=True, inverse=True)
task_owner_is_dead = HasTagTest(object_to_test=GenericObjectNode.TASK_OWNER, tag="Alive", value=False)

# Tasks
# Rescue Columbo
# Source: Get Command From Higher Ups
# Owner: Amil
# Requirement: Columbo must be alive.
# Placeholder Actors: "columbo" -> Stranded Human

find_columbo = StoryNode(name="Find Columbo", tags={"Type":"Conversation"}, target_count=1, actor=[GenericObjectNode.TASK_OWNER], target=["columbo"])

# Order Army Follow: Orders the earth army to follow. Amil "carries" the Army.
# Dismiss Army Follow: Orders the earth army to stop following. Amil stops "carrying" the Army and the Army is now in whatever location Amil is in.

location_stop_carrying_target = RelChange(name="Location stop Carrying Target", node_a=earth, edge_name="holds", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.REMOVE, soft_equal=True)
actor_carry_target = RelChange(name="Actor Carrying Target", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="holds", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.ADD)

actor_stop_carrying_target = RelChange(name="Actor stop Carrying Target", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="holds", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.REMOVE, soft_equal=True)
location_carry_target = RelChange(name="Location Carrying Target", node_a=new_world_greenland, edge_name="holds", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.ADD)

order_army_follow = StoryNode(name="Order Army Follow", actor=[GenericObjectNode.TASK_OWNER], target=[earth_army], effects_on_next_ws=[location_stop_carrying_target, actor_carry_target])
dismiss_army_follow = StoryNode(name="Dismiss Army Follow", actor=[GenericObjectNode.TASK_OWNER], target=[earth_army], effects_on_next_ws=[actor_stop_carrying_target, location_carry_target])

order_army_follow_task = CharacterTask(task_name="Order Army Follow Task", task_actions=[order_army_follow], avoidance_state=[task_owner_is_dead], task_location_name="Earth")
dismiss_army_follow_task = CharacterTask(task_name="Dismiss Army Follow Task", task_actions=[dismiss_army_follow], avoidance_state=[task_owner_is_dead], task_location_name="New World Greenland")

columbo_is_not_alive = HasTagTest(object_to_test="columbo", tag="Alive", value=False)
find_columbo_task = CharacterTask(task_name="Find Columbo Task", task_actions=[find_columbo], actor_placeholder_string_list=["columbo"], avoidance_state=[task_owner_is_dead, columbo_is_not_alive], task_location_name="New World Greenland")

columbo_is_columbo = ObjectEqualityTest(object_list=["columbo", columbo])
columbo_is_alive = HasTagTest(object_to_test="columbo", tag="Alive", value=True)

find_columbo_stack = TaskStack(stack_name="Find Columbo Stack", task_stack=[order_army_follow_task, dismiss_army_follow_task, find_columbo_task], task_stack_requirement=[columbo_is_alive, columbo_is_columbo])

get_rescue_columbo_taskchange = TaskChange(name="Get Rescue Columbo Task", task_giver_name=None, task_owner_name=GenericObjectNode.GENERIC_ACTOR, task_stack=find_columbo_stack)

get_command_from_higher_up = StoryNode(name="Get Command from Higher Up", effects_on_next_ws=[get_rescue_columbo_taskchange], required_test_list=[actor_is_alive])

# Destroy Tatain
# Source: Alien God
# Owner: Iris
# Requirement: Alien God must not have knowledge of Destroy Tatain Task.
# Action: (Tatain): Attack Inhabitants

attack_inhabitants_tatain_with_characters = deepcopy(attack_inhabitants_tatain)
attack_inhabitants_tatain_with_characters.actor.append(GenericObjectNode.TASK_OWNER)
attack_inhabitants_tatain_with_characters.target.append(tatain_people)

attack_tatain_task = CharacterTask(task_name="Attack Tatain Task", task_actions=[attack_inhabitants_tatain_with_characters], avoidance_state=[task_owner_is_dead], task_location_name="Tatain")

task_giver_not_know_about_tatain_task = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="HasGivenTatainTask", value=True, inverse=True)
task_giver_know_about_tatain = TagChange(name="Target Knows of Tatain Task", object_node_name=GenericObjectNode.GENERIC_TARGET, tag="HasGivenTatainTask", value=True, add_or_remove=ChangeAction.ADD)

attack_tatain_stack = TaskStack(stack_name="Attack Tatain Stack", task_stack=[attack_tatain_task])

get_attack_tatain_taskchange = TaskChange(name="Get Attack Tatain Task", task_giver_name=GenericObjectNode.GENERIC_TARGET, task_owner_name=GenericObjectNode.GENERIC_ACTOR, task_stack=attack_tatain_stack)

get_tatain_task_node = StoryNode(name="Get Tatain Node", effects_on_next_ws=[get_attack_tatain_taskchange, task_giver_know_about_tatain], required_test_list=[actor_is_alive, task_giver_not_know_about_tatain_task], target_count=1)

# Destory Death Paradise
# Source: Alien God
# Owner: Iris
# Requirement: Alien God must not have knowledge of Destroy Death Pardise Task.
# Actions: (Death Paradise): Attacked by Mob

attacked_by_robots_with_characters = deepcopy(attacked_by_robots)
attacked_by_robots_with_characters.actor.append(GenericObjectNode.TASK_OWNER)
attacked_by_robots_with_characters.target.append(death_paradise_robots)

get_attacked_by_robots_task = CharacterTask(task_name="Attacked by Robots Task", task_actions=[attacked_by_robots_with_characters], avoidance_state=[task_owner_is_dead], task_location_name="Death Paradise")

task_giver_not_know_about_dp_task = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="HasGivenDeathParaTask", value=True, inverse=True)
task_giver_know_about_death_paradise = TagChange(name="Target Knows of DP Task", object_node_name=GenericObjectNode.GENERIC_TARGET, tag="HasGivenDeathParaTask", value=True, add_or_remove=ChangeAction.ADD)

get_attacked_by_robots_stack = TaskStack(stack_name="Get Attacked by Bots Stack", task_stack=[get_attacked_by_robots_task])

get_attacked_by_robots_taskchange = TaskChange(name="Get Attacked by Bots Task", task_giver_name=GenericObjectNode.GENERIC_TARGET, task_owner_name=GenericObjectNode.GENERIC_ACTOR, task_stack=get_attacked_by_robots_stack)

get_dp_task_node = StoryNode(name="Get DP Node", required_test_list=[actor_is_alive, task_giver_not_know_about_dp_task], effects_on_next_ws=[get_attacked_by_robots_taskchange, task_giver_know_about_death_paradise], target_count=1)

# Preserve Greenland
# Source: Alien God
# Owner: Iris
# Requirement: Alien God must not have knowledge of Preserve Greenland Task.
# Actions: (New World Greenland): Notice Invader
# Placeholder Actors: "columbo" -> Stranded Human

notice_invader_with_characters = deepcopy(notice_invader)
notice_invader_with_characters.actor.append(GenericObjectNode.TASK_OWNER)
notice_invader_with_characters.target.append("columbo")

notice_invader_task = CharacterTask(task_name="Notice Invader Task", task_actions=[notice_invader_with_characters], avoidance_state=[task_owner_is_dead, columbo_is_not_alive], task_location_name="New World Greenland", actor_placeholder_string_list=["columbo"])

task_giver_not_know_about_greenland_task = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="HasGivenGreenlandTask", value=True, inverse=True)
task_giver_know_about_greenland = TagChange(name="Task Giver Knows of Greenland Task", object_node_name=GenericObjectNode.GENERIC_TARGET, tag="HasGivenGreenlandTask", value=True, add_or_remove=ChangeAction.ADD)

notice_invader_stack = TaskStack(stack_name="Notice Invader Stack", task_stack=[notice_invader_task], task_stack_requirement=[columbo_is_columbo, columbo_is_alive])

notice_invader_taskchange = TaskChange(name="Get Notice Invader Task", task_giver_name=GenericObjectNode.GENERIC_TARGET, task_owner_name=GenericObjectNode.GENERIC_ACTOR, task_stack=notice_invader_stack)

get_greenland_task_node = StoryNode(name="Get Greenland Task 1 Node", effects_on_next_ws=[notice_invader_taskchange, task_giver_know_about_greenland], required_test_list=[actor_is_alive, task_giver_not_know_about_greenland_task], target_count=1)

# Invade Greenland
# Source: Alien God
# Owner: Apollo
# Requirement: Alien God must not have knowledge of the Invade Greenland task
# Actions: (New World Greenland): Attack Amil, Amil commands army to kill 

# (The nodes that give away these tasks will in itself give knowledge of the task to the giver)

task_giver_not_know_about_attack_greenland_task = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="HasGivenAttackGreenlandTask", value=True, inverse=True)
task_giver_know_about_attack_greenland_task = TagChange(name="Task Giver Knows of Attack Greenland Task", object_node_name=GenericObjectNode.GENERIC_TARGET,tag="HasGivenAttackGreenlandTask", value=True, add_or_remove=ChangeAction.ADD)

attack_amil = deepcopy(actor_attack_another_actor)

attack_amil.effects_on_next_ws.append(target_loses_plot_armor)
attack_amil.actor.append(GenericObjectNode.TASK_OWNER)
attack_amil.target.append("amil")

amil_command_army_attack_quest_owner = deepcopy(command_army_attack)
amil_command_army_attack_quest_owner.actor.append("amil")
amil_command_army_attack_quest_owner.target.append(GenericObjectNode.TASK_OWNER)

amil_job_is_military = HasTagTest(object_to_test="amil", tag="Job", value="Military")
amil_is_alive = HasTagTest(object_to_test="amil", tag="Alive", value=True)

attack_amil_task = CharacterTask(task_name="Attack Amil and Get Attacked", task_requirement=[amil_job_is_military, amil_is_alive], actor_placeholder_string_list=["amil"], task_location_name="New World Greenland", task_actions=[attack_amil, amil_command_army_attack_quest_owner])

attack_greenland_stack = TaskStack(stack_name="Attack Greenland Stack", task_stack=[attack_amil_task])

get_attack_greenland_stack = TaskChange(name="Get Attack Greenland Stack", task_giver_name=GenericObjectNode.GENERIC_TARGET, task_owner_name=GenericObjectNode.GENERIC_ACTOR, task_stack=attack_greenland_stack)

actor_is_apollo = ObjectEqualityTest(object_list=[apollo, GenericObjectNode.GENERIC_ACTOR])
get_attack_greenland_node = StoryNode(name="Get Greenland Task 2 Node", effects_on_next_ws=[get_attack_greenland_stack,task_giver_know_about_attack_greenland_task], required_test_list=[actor_is_alive, task_giver_not_know_about_attack_greenland_task, actor_is_apollo], target_count=1)
# Rules

# Rewrite Rule

# For each type of mob rule we are going to add one for each mob type.

# Reminder of mob types
# - Greenland Insects
# - Tatain People
# - Death Paradise Robots
# - Enemy Mercenary 
# - Earth Army

rule_list = []
# Attacked by Mob -+> Kill Mob as Defense

kill_insect_defense_followup = RewriteRule(name="Attacked by Insects -+> Kill Insects as Defense", story_condition=[attacked_by_insects], story_change=[self_defense_kill_insect], remove_before_insert = False, target_list=[[greenland_insects]])
kill_robot_defense_followup = RewriteRule(name="Attacked by Robots -+> Kill Robots as Defense", story_condition=[attacked_by_robots], story_change=[self_defense_kill_robots], remove_before_insert = False, target_list=[[death_paradise_robots]])
kill_mercs_defense_followup = RewriteRule(name="Attacked by Mercs -+> Kill Mercs as Defense", story_condition=[attacked_by_mercs], story_change=[self_defense_kill_mercs], remove_before_insert = False, target_list=[[enemy_mercenary]])
kill_army_defense_followup = RewriteRule(name="Attacked by Army -+> Kill Army as Defense", story_condition=[attacked_by_army], story_change=[self_defense_kill_army], remove_before_insert = False, target_list=[[earth_army]])

rule_list.extend([kill_insect_defense_followup, kill_robot_defense_followup, kill_mercs_defense_followup, kill_army_defense_followup])

# Attacked by Mob -+> Kill Mob for Food

kill_insect_for_food_followup = RewriteRule(name="Attacked by Insects -+> Kill Insects for Food", story_condition=[attacked_by_insects], story_change=[kill_mob_for_food_insects], target_list=[[greenland_insects]])
rule_list.append(kill_insect_for_food_followup)

# Attacked by Mob -+> Record Earth Army Data

attack_mob_then_record_followup = RewriteRule(name="Attacked by Army -+> Record Army Data", story_condition=[attacked_by_army], story_change=[record_earth_army_data], target_list=[[earth_army]])
rule_list.append(attack_mob_then_record_followup)

# Attacked by Mob -+> Killed by Mob

# attacked_and_killed_insect_followup = RewriteRule(name="Attacked by Insects -+> Killed by Insects", story_condition=[attacked_by_insects], story_change=[killed_by_insect], target_list=[[greenland_insects]])
attacked_and_killed_robot_followup = RewriteRule(name="Attacked by Robots -+> Killed by Robots", story_condition=[attacked_by_robots], story_change=[killed_by_robots], target_list=[[death_paradise_robots]])
attacked_and_killed_mercs_followup = RewriteRule(name="Attacked by Mercs -+> Killed by Mercs", story_condition=[attacked_by_mercs], story_change=[killed_by_mercs], target_list=[[enemy_mercenary]])
attacked_and_killed_army_followup = RewriteRule(name="Attacked by Army -+> Killed by Army", story_condition=[attacked_by_army], story_change=[killed_by_army], target_list=[[earth_army]])

rule_list.extend([attacked_and_killed_army_followup, attacked_and_killed_mercs_followup, attacked_and_killed_robot_followup])

# Attacked by Mob -+> Massacre Mobs

attacked_and_massacre_insect_followup = RewriteRule(name="Attacked by Insects -+> Massacre Insects", story_condition=[attacked_by_insects], story_change=[massacre_insects], target_list=[[greenland_insects]])
attacked_and_massacre_robot_followup = RewriteRule(name="Attacked by Robots -+> Massacre Robots", story_condition=[attacked_by_robots], story_change=[massacre_robots], target_list=[[death_paradise_robots]])
attacked_and_massacre_mercs_followup = RewriteRule(name="Attacked by Mercs -+> Massacre Mercs", story_condition=[attacked_by_mercs], story_change=[massacre_mercs], target_list=[[enemy_mercenary]])
attacked_and_massacre_army_followup = RewriteRule(name="Attacked by Army -+> Massacre Army", story_condition=[attacked_by_army], story_change=[massacre_army], target_list=[[earth_army]])

rule_list.extend([attacked_and_massacre_insect_followup, attacked_and_massacre_robot_followup, attacked_and_massacre_mercs_followup, attacked_and_massacre_army_followup])

# Attack Inhabitants -+> Killed by Mob

attack_inhab_killed_insect_followup = RewriteRule(name="Attack Insects -+> Killed by Insects", story_condition=[attack_inhabitants_insects], story_change=[killed_by_insect], target_list=[[greenland_insects]])
attack_inhab_killed_robots_followup = RewriteRule(name="Attack Robots -+> Killed by Robots", story_condition=[attack_inhabitants_robots], story_change=[killed_by_robots], target_list=[[death_paradise_robots]])
attack_inhab_killed_mercs_followup = RewriteRule(name="Attack Mercs -+> Killed by Mercs", story_condition=[attack_inhabitants_mercs], story_change=[killed_by_mercs], target_list=[[enemy_mercenary]])
attack_inhab_killed_army_followup = RewriteRule(name="Attack Army -+> Killed by Army", story_condition=[attack_inhabitants_army], story_change=[killed_by_army], target_list=[[earth_army]])

rule_list.extend([attack_inhab_killed_army_followup, attack_inhab_killed_insect_followup, attack_inhab_killed_mercs_followup, attack_inhab_killed_robots_followup])

# Attack Inhabitants -+> Massacre Mobs

attack_inhab_massacre_insect_followup = RewriteRule(name="Attack Insects -+> Massacre Insects", story_condition=[attack_inhabitants_insects], story_change=[massacre_insects], target_list=[[greenland_insects]])
attack_inhab_massacre_robots_followup = RewriteRule(name="Attack Robots -+> Massacre Robots", story_condition=[attack_inhabitants_robots], story_change=[massacre_robots], target_list=[[death_paradise_robots]])
attack_inhab_massacre_mercs_followup = RewriteRule(name="Attack Mercs -+> Massacre Mercs", story_condition=[attack_inhabitants_mercs], story_change=[massacre_mercs], target_list=[[enemy_mercenary]])
attack_inhab_massacre_army_followup = RewriteRule(name="Attack Army -+> Massacre Army", story_condition=[attack_inhabitants_army], story_change=[massacre_army], target_list=[[earth_army]])
attack_inhab_massacre_tatain_followup = RewriteRule(name="Attack Tatain -+> Massacre Tatain", story_condition=[attack_inhabitants_tatain], story_change=[massacre_tatain], target_list=[[tatain_people]])

rule_list.extend([attack_inhab_massacre_army_followup, attack_inhab_massacre_insect_followup, attack_inhab_massacre_mercs_followup, attack_inhab_massacre_robots_followup, attack_inhab_massacre_tatain_followup])

# (Nothing) -> Attack Inhabitants

attack_inhab_insect_begin = RewriteRule(name="Begin Attack Insects", story_condition=[], story_change=[attack_inhabitants_insects], target_list=[[greenland_insects]])
attack_inhab_robots_begin = RewriteRule(name="Begin Attack Robots", story_condition=[], story_change=[attack_inhabitants_robots], target_list=[[death_paradise_robots]])
attack_inhab_mercs_begin = RewriteRule(name="Begin Attack Mercs", story_condition=[], story_change=[attack_inhabitants_mercs], target_list=[[enemy_mercenary]])
attack_inhab_army_begin = RewriteRule(name="Begin Attack Army", story_condition=[], story_change=[attack_inhabitants_army], target_list=[[earth_army]])
attack_inhab_tatain_begin = RewriteRule(name="Begin Attack Tatain", story_condition=[], story_change=[attack_inhabitants_tatain], target_list=[[tatain_people]])

rule_list.extend([attack_inhab_army_begin, attack_inhab_mercs_begin, attack_inhab_insect_begin, attack_inhab_robots_begin, attack_inhab_tatain_begin])

# (Nothing) -> Eradicate Mob With God Power

eradicate_insects_begin = RewriteRule(name="Eradicate Insects Begin", story_condition=[], story_change=[god_kills_insects], target_list=[[greenland_insects]])
eradicate_robots_begin = RewriteRule(name="Eradicate Robots Begin", story_condition=[], story_change=[god_kills_robots], target_list=[[death_paradise_robots]])
eradicate_mercs_begin = RewriteRule(name="Eradicate Mercs Begin", story_condition=[], story_change=[god_kills_mercs], target_list=[[enemy_mercenary]])
eradicate_army_begin = RewriteRule(name="Eradicate Army Begin", story_condition=[], story_change=[god_kills_army], target_list=[[earth_army]])

rule_list.extend([eradicate_army_begin, eradicate_insects_begin, eradicate_robots_begin, eradicate_mercs_begin])

# (Nothing) -> Attacked by Mob

# attacked_by_insects_begin = RewriteRule(name="Attacked by Insects Begin", story_condition=[], story_change=[attacked_by_insects], target_list=[[greenland_insects]])
attacked_by_robots_begin = RewriteRule(name="Attacked by Robots Begin", story_condition=[], story_change=[attacked_by_robots], target_list=[[death_paradise_robots]])
attacked_by_mercs_begin = RewriteRule(name="Attacked by Mercs Begin", story_condition=[], story_change=[attacked_by_mercs], target_list=[[enemy_mercenary]])
attacked_by_army_begin = RewriteRule(name="Attacked by Army Begin", story_condition=[], story_change=[attacked_by_army], target_list=[[earth_army]])

rule_list.extend([attacked_by_robots_begin, attacked_by_mercs_begin, attacked_by_army_begin])

# JoiningJointRule
# (Nothing) -> Kill Actor
# (Nothing) -> Create Apollo
# (Nothing) -> Data Backup Resurrection
# (Nothing) -> Command Army to Attack

start_kill_actor = JoiningJointRule(rule_name="Start Kill Actor", base_actions=[], joint_node=kill_another_actor)
start_create_apollo = JoiningJointRule(rule_name="Start Create Apollo", base_actions=[], joint_node=create_apollo)
start_data_backup_resurrection = JoiningJointRule(rule_name="Start Resurrect", base_actions=[], joint_node=resurrect_target)
start_command_army = JoiningJointRule(rule_name="Start Command Army", base_actions=[], joint_node=command_army_attack)

# ContJointRule

# Create Apollo -> Greenland Task 2

create_apollo_and_give_task = ContinuousJointRule(rule_name="Create Apollo then Give Task", base_joint=create_apollo, joint_node=get_attack_greenland_node)

# SplitJointRule
# None Yet

rule_list.extend([start_kill_actor, start_create_apollo, start_data_backup_resurrection, start_command_army, create_apollo_and_give_task])

#TODO: Set up the initial Story Graph. (Please work I am BEGGING)
story_graph = StoryGraph(name="Gearng Story Graph", character_objects=all_characters, location_objects=all_locations, starting_ws=world_state)

# Starting Story Graph:
# Non Main Characters will wait
# Main Characters:

# TS0
# Columbo: Explore World
# Iris: Get Destroy Tatain Task
# Amil: Wait
graph2 = deepcopy(story_graph)

story_graph.insert_story_part(part=explore_world, character=columbo, location=new_world_greenland, absolute_step=0, timestep=0)
story_graph.insert_joint_node(joint_node=get_tatain_task_node, main_actor=iris, targets=[alien_god], location=alien_god_planet, absolute_step=0, timestep=0)
story_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=amil, location=earth, absolute_step=0, timestep=0)
story_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=apollo, location=alien_god_planet, absolute_step=0, timestep=0)

# TS1
# Columbo: Attacked by Insects
# Iris: Get Destroy Death Paradise Task
# Amil: Wait

story_graph.insert_story_part(part=attacked_by_insects, character=columbo, location=new_world_greenland, absolute_step=1, timestep=0, targets=[greenland_insects])
story_graph.insert_joint_node(joint_node=get_dp_task_node, main_actor=iris, targets=[alien_god], location=alien_god_planet, absolute_step=1, timestep=0)
story_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=amil, location=earth, absolute_step=1, timestep=0)
story_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=apollo, location=alien_god_planet, absolute_step=1, timestep=0)

# TS2
# Columbo: Wait
# Iris: Get Preserve Greenland Task
# Amil: Wait

story_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=columbo, location=new_world_greenland, absolute_step=2, timestep=0)
story_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=amil, location=earth, absolute_step=2, timestep=0)
story_graph.insert_joint_node(joint_node=get_greenland_task_node, main_actor=iris, targets=[alien_god], location=alien_god_planet, absolute_step=2, timestep=0)
story_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=apollo, location=alien_god_planet, absolute_step=2, timestep=0)

# TS3
# Columbo and Iris: Notice Invader 
# Amil: Get Rescue Columbo Task

story_graph.insert_story_part(part=get_command_from_higher_up, character=amil, location=earth, absolute_step=3, timestep=0)
story_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=columbo, location=new_world_greenland, absolute_step=3, timestep=0)
story_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=iris, location=new_world_greenland, absolute_step=3, timestep=0)
story_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=alien_god, location=alien_god_planet, absolute_step=3, timestep=0)
story_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=apollo, location=alien_god_planet, absolute_step=3, timestep=0)

# TS4
# Columbo and Iris: Iris kills Columbo
# Amil: Wait

# story_graph.insert_joint_node(joint_node=kill_another_actor, main_actor=iris, targets=[columbo], absolute_step=4, timestep=0, location=new_world_greenland)
# story_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=amil, location=earth, absolute_step=4, timestep=0)
# story_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=alien_god, location=alien_god_planet, absolute_step=4, timestep=0)
# story_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=apollo, location=alien_god_planet, absolute_step=4, timestep=0)

extra_movement = [actor_is_not_stranded, actor_is_alive]

generated_graph = generate_story_from_starter_graph(init_storygraph=story_graph, list_of_rules=rule_list, required_story_length=10, extra_movement_requirement_list=extra_movement, verbose=True, extra_attempts=-1)

print("Abridged Story Nodes")
print("==COLUMBO==")
generated_graph.print_all_nodes_from_characters_storyline(columbo)
print("==IRIS==")
generated_graph.print_all_nodes_from_characters_storyline(iris)
print("==AMIL==")
generated_graph.print_all_nodes_from_characters_storyline(amil)
print("==ALIEN GOD==")
generated_graph.print_all_nodes_from_characters_storyline(alien_god)
print("==APOLLO==")
generated_graph.print_all_nodes_from_characters_storyline(apollo)

# ======= BELOW IS TESTING AREA AND DOES NOT CONTRIBUTE TO ANYTHING ABOVE =======

# kill_another_actor can do Actor even though Columbo does not have Kill Reason towards anyone.
# To prove that it's impossible for Columbo to be the actor or target in these situations, we must test Columbo against every other Characters in the WorldState to prove that nobody else can have this relation.
# command_army_attack can do Target even though nobody has Kill Reason towards Columbo.

# world_state_2 = WorldState(name="Test WS", objectnodes=[amil, iris, columbo, alien_god, earth, earth_army])

# world_state_2.connect(from_node=earth, edge_name="holds", to_node=columbo)
# world_state_2.connect(from_node=earth, edge_name="holds", to_node=iris)
# world_state_2.connect(from_node=earth, edge_name="holds", to_node=amil)
# world_state_2.connect(from_node=earth, edge_name="holds", to_node=alien_god)
# world_state_2.connect(from_node=alien_god, edge_name="commands", to_node=iris)
# world_state_2.connect(from_node=iris, edge_name="obeys", to_node=alien_god)

# story_graph_2 = StoryGraph(name="Test Graph", character_objects=[amil, iris, columbo, alien_god], location_objects=[earth], starting_ws=world_state_2)

# iris.tags["Alive"] = False

# story_graph_2.add_story_part(part=DEFAULT_WAIT_NODE, character=iris, location=earth)
# story_graph_2.add_story_part(part=DEFAULT_WAIT_NODE, character=alien_god, location=earth)

# attempt_apply_rule(rule_object=start_data_backup_resurrection, perform_index=1, target_story_graph=story_graph_2, character_object=iris, shortest_path_charname_list=["Alien God", "Iris"])

# story_graph_2.fill_in_locations_on_self()
# story_graph_2.print_all_node_beautiful_format()
# mini_find_columbo_stack
# mini_

# world_state_2.connect(from_node=earth, edge_name="holds", to_node=earth_army)
# world_state_2.connect(from_node=amil, edge_name="KillReason", to_node=iris, value="self_defense")
# world_state_2.connect(from_node=amil, edge_name="commands", to_node=earth_army)

# calculate_score_from_char_and_unpopulated_node_with_both_slots(actor=iris, node=command_army_attack, world_state=world_state_2)

# print(attempt_apply_rule(rule_object=attacked_by_insects_begin, perform_index=1, target_story_graph=story_graph, character_object=columbo, shortest_path_charname_list=["Columbo"]))

# print(attempt_apply_rule(rule_object=kill_insect_for_food_followup, perform_index=1, target_story_graph=story_graph, character_object=columbo, shortest_path_charname_list=["Columbo"]))
# story_graph.fill_in_locations_on_self()
# story_graph.insert_story_part(part=DEFAULT_WAIT_NODE, character=columbo, absolute_step=2)
# story_graph.fill_in_locations_on_self()
# print(attempt_apply_rule(rule_object=kill_insect_for_food_followup, perform_index=1, target_story_graph=story_graph, character_object=columbo, shortest_path_charname_list=["Columbo"]))
# story_graph.fill_in_locations_on_self()

# story_graph.print_all_nodes_from_characters_storyline_beautiful_format(columbo)
# story_graph.calculate_score_from_char_and_cont(actor=apollo, insert_index=0, contlist=[])
# world_state.test_story_compatibility_with_storynode(kill_another_actor)

# attempt_apply_rule(rule_object=start_data_backup_resurrection, perform_index=4, target_story_graph=story_graph, character_object=alien_god, shortest_path_charname_list=["Columbo", "Iris", "Amil", "Alien God", "Apollo"])

# print(story_graph.calculate_score_from_rule_char_and_cont(actor=columbo, insert_index=1, rule=kill_insect_for_food_followup))
# print(attempt_apply_rule(rule_object=kill_insect_for_food_followup, perform_index=1, target_story_graph=story_graph, character_object=columbo, shortest_path_charname_list=["Columbo", "Iris", "Alien God", "Amil", "Apollo"]))
# print(attempt_apply_rule(rule_object=kill_insect_defense_followup, perform_index=1, target_story_graph=story_graph, character_object=columbo, shortest_path_charname_list=["Columbo", "Iris", "Alien God", "Amil", "Apollo"]))
# print(story_graph.calculate_score_from_rule_char_and_cont(actor=columbo, insert_index=1, rule=kill_insect_for_food_followup))
# print(story_graph.calculate_score_from_rule_char_and_cont(actor=columbo, insert_index=1, rule=kill_insect_defense_followup))

# story_graph.print_all_nodes_from_characters_storyline(columbo)
# print(story_graph.check_continuation_validity(actor=columbo, abs_step_to_cont_from=2, cont_list=[kill_mob_for_food_insects], target_list=[[greenland_insects]]))

# print(story_graph.longest_path_length)
# print(story_graph.check_add_joint_validity(joint_node=resurrect_target, actors_to_test=[alien_god], targets_to_test=[apollo], insert_index=3))

# print("==ALIEN GOD==")
# story_graph.print_all_nodes_from_characters_storyline(alien_god)
# print("==APOLLO==")
# story_graph.print_all_nodes_from_characters_storyline(apollo)

# story_graph.print_all_node_beautiful_format()
# for rule in rule_list:
#     print(rule)

# graph2.insert_multiple_parts(part_list=[DEFAULT_WAIT_NODE, DEFAULT_WAIT_NODE, attacked_by_insects, attacked_by_insects], location_list=[new_world_greenland, new_world_greenland, new_world_greenland, new_world_greenland, new_world_greenland], absolute_step=0, targets=[[],[],[greenland_insects],[greenland_insects]], character=columbo)

# graph2.print_all_node_beautiful_format()

# print(graph2.test_if_anyone_in_list_has_adjacent_duped_node_with_given_name(actor_list=[columbo], dupe_node_name="Attacked by Insects"))

#TODO: Hey the tasks are not tasking for some reason. Can we fix this? Yes we can!
# story_graph.fill_in_locations_on_self()
# available_task_name_list = story_graph.get_list_of_task_stack_names_from_latest_step(actor_name = "Iris")
# print(available_task_name_list)

# print(story_graph.calculate_score_from_rule_char_and_cont(actor=columbo, insert_index=1, rule=kill_insect_defense_followup))

# print("Can Apply Step 1 of Find Columbo Stack", attempt_apply_task(stack_name="Find Columbo Stack", attempt_index=4, target_story_graph=story_graph, current_character=amil))
# story_graph.fill_in_locations_on_self()

# print(story_graph.print_all_nodes_from_characters_storyline_beautiful_format(amil))

# sg2 = deepcopy(story_graph)

# print(sg2.story_parts[("Amil", 3)].effects_on_next_ws)
# print(sg2.make_latest_state().node_dict["Amil"].get_incomplete_task_stack_names())

# print("Attempt Apply Rule", attempt_apply_rule(rule_object=start_kill_actor, perform_index=3, target_story_graph=story_graph, character_object=alien_god, shortest_path_charname_list=["Alien God", "Amil"]))
# print("Can Move Towards Task Location", attempt_move_towards_task_loc(target_story_graph=story_graph, current_character=amil, movement_index=5, extra_movement_requirements=extra_movement))
# story_graph.fill_in_locations_on_self()
# print("Can Move Towards Task Location", attempt_move_towards_task_loc(target_story_graph=story_graph, current_character=amil, movement_index=6, extra_movement_requirements=extra_movement))
# story_graph.fill_in_locations_on_self()
# story_graph.add_story_part(part=DEFAULT_WAIT_NODE, character=iris)
# story_graph.add_story_part(part=DEFAULT_WAIT_NODE, character=iris)
# story_graph.add_story_part(part=DEFAULT_WAIT_NODE, character=iris)
# print(story_graph.check_add_joint_validity(joint_node=actor_attack_another_actor, actors_to_test=[iris], targets_to_test=[amil], insert_index=7))

# story_graph.fill_in_locations_on_self()

# amil_tasks = story_graph.make_latest_state().node_dict["Amil"].get_incomplete_task_stack_names()
# print(amil_tasks)

# amil_nodes = story_graph.make_story_part_list_of_one_character(amil)
# for snode in amil_nodes:
#     print(snode.name)
#     for thing in snode.effects_on_next_ws:
#         print(thing)
#     print("=====")

# print("Can Apply Step 2 of Find Columbo Stack", attempt_apply_task(stack_name="Find Columbo Stack", attempt_index=7, target_story_graph=story_graph, current_character=amil))
# story_graph.fill_in_locations_on_self()
# print("Can Apply Step 3 of Find Columbo Stack (it doesn't exist)", attempt_apply_task(stack_name="Find Columbo Stack", attempt_index=7, target_story_graph=story_graph, current_character=amil))
# print(story_graph.make_latest_state().get_actor_current_location(amil))
# story_graph.print_all_nodes_from_characters_storyline_beautiful_format(amil)

# generated_graph.print_all_nodes_from_characters_storyline(apollo)

# stacks = ["Attack Tatain Stack", "Get Attacked by Bots Stack", "Notice Invader Stack"]
# stacks = ["Find Columbo Stack"]

# print(story_graph.longest_path_length)

# for i in range(0, story_graph.longest_path_length+1):
#     for stack_name in stacks:
#         print(stack_name, i)
#         print(story_graph.test_task_stack_advance_validity(task_stack_name=stack_name, actor_name="Amil", abs_step=i))
#         print(story_graph.calculate_score_from_next_task_in_task_stack(actor_name="Amil", task_stack_name=stack_name, task_perform_index=i, mode=0))


# print(story_graph.make_latest_state().get_actor_current_location(iris))

# current_ws = world_state

# optimal_location_object = outer_space

# go_to_new_location_change = RelChange(name="Go To Task Loc", node_a=optimal_location_object, edge_name=current_ws.DEFAULT_HOLD_EDGE_NAME, node_b=GenericObjectNode.GENERIC_ACTOR, value=None, add_or_remove=ChangeAction.ADD)

# # not_be_in_current_location_change = RelChange("Leave Current Loc", node_a=GenericObjectNode.GENERIC_LOCATION, edge_name=current_ws.DEFAULT_HOLD_EDGE_NAME, node_b=character_at_step, add_or_remove=ChangeAction.REMOVE)
# not_be_in_current_location_change = RelChange(name="Leave Current Loc", node_a=GenericObjectNode.GENERIC_LOCATION, edge_name=current_ws.DEFAULT_HOLD_EDGE_NAME, node_b=GenericObjectNode.GENERIC_ACTOR, add_or_remove=ChangeAction.REMOVE, soft_equal=True, value=None)

# all_requirements = deepcopy(extra_movement)
# target_location_adjacent_to_current_location = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_LOCATION, edge_name_test=current_ws.DEFAULT_ADJACENCY_EDGE_NAME, object_to_test=optimal_location_object, soft_equal=True)
# all_requirements.append(target_location_adjacent_to_current_location)

# move_towards_task_location_node = StoryNode(name="Move Towards Outer Space", biasweight=0, tags={"Type":"Movement"}, charcount=1, effects_on_next_ws=[not_be_in_current_location_change, go_to_new_location_change], required_test_list=all_requirements)

# movement_validity = story_graph.check_continuation_validity(actor=alien_god, abs_step_to_cont_from=0, cont_list=[move_towards_task_location_node])

# print(movement_validity)

# Current Problems
# We don't know how to define score properly. Whoops?
# Use Default Scoring for now
# 
# Scoring Schemes:
# 1. Default (Everything is a 0)
# 2. Deaths Give Points
# 3. Deaths Take Points
#
# Maybe change initial graph state to encourage different ways of generating the story?
#
# For the Tasks that refer to objects in the world (and not placeholders), we need to actually have it point towards the object in the current world state. (Actually already Handled?)


# We also want tasks without placeholders to skip whenever the Task Owner or the Task Giver is None (DONE)

# find_columbo_stack_2 = deepcopy(find_columbo_stack)
# find_columbo_stack_2.stack_owner_name = "Amil"

# world_state.make_list_of_possible_task_stack_character_replacements(find_columbo_stack_2)

# For non-joint nodes we need a way to address included target nodes in the rule.
#
# Test Here: Calculate score for applying a non-actor target nodes (Apollo being Attacked by Space Pirates) (DONE)
# print(story_graph.calculate_score_from_rule_char_and_cont(actor=apollo, insert_index=0, rule=attacked_by_mercs_begin))

# Something is wrong with the JointNodes. We need to fix it
#
# Test Here: 

# print(story_graph.get_characters_with_shortest_path_length())
# attempt_apply_rule(rule_object=start_kill_actor, perform_index=0, target_story_graph=story_graph, character_object=columbo, shortest_path_charname_list=["Columbo"])
# print(permute_actor_list_for_joint_with_range_and_freesize(current_actor="Columbo", other_actors=[], size=2))

# For Attempt Move Towards Task Location, we need to do something with the GenericObjectNodes not changing?