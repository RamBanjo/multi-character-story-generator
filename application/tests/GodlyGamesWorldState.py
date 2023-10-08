import sys

sys.path.insert(0,'')

from application.components.StoryObjects import CharacterNode, LocationNode, ObjectNode
from application.components.WorldState import WorldState
from application.components.StoryNode import StoryNode
from application.components.ConditionTest import *
from application.components.RelChange import *
from application.components.RewriteRuleWithWorldState import *

honest_harry = CharacterNode(name="Honest Harry", biases={"lawbias":40, "moralbias":50}, tags={"Type":"Character", "Hometown":"Duality", "CharacterRole":"Main", "Alive":True, "has_knowledge_of_cheating":True})
justice_john = CharacterNode(name="Justice John", biases={"lawbias":30, "moralbias":60}, tags={"Type":"Character", "Hometown":"Duality", "CharacterRole":"Main", "Alive":True})
mysterious_misty = CharacterNode(name="Mysterious Misty", biases={"lawbias":-75, "moralbias":0}, tags={"Type":"Character", "Hometown":"Starlight", "CharacterRole":"Main", "Alive":True, "Criminal":"thief"})

god_of_light = CharacterNode(name="God of Light", biases={"lawbias":0, "moralbias":0}, tags={"Type":"Character", "Hometown":"Duality", "CharacterRole":"Support", "Alive":True, "IsAuthorityFigure":True})
god_of_dark = CharacterNode(name="God of Darkness", biases={"lawbias":0, "moralbias":0}, tags={"Type":"Character", "Hometown":"Duality", "CharacterRole":"Support", "Alive":True, "IsAuthorityFigure":True})
dicey_darren = CharacterNode(name="Dicey Darren", biases={"lawbias":-30, "moralbias":-30}, tags={"Type":"Character", "Hometown":"Starlight", "CharacterRole":"Support", "Alive":True, "Criminal":"gang_leader"})
knower = CharacterNode(name="The Knower", biases={"lawbias":0, "moralbias":0}, tags={"Type":"Character", "Hometown":"Starlight", "CharacterRole":"Support", "Alive":True, "has_knowledge_of_redmond": True})
shady_samuel = CharacterNode(name="Shady Samuel", biases={"lawbias":0, "moralbias":-50}, tags={"Type":"Character", "Hometown":"Central Realm", "CharacterRole":"Support", "Alive":True, "Criminal":"hire_hitman", "has_knowledge_of_redmond_location": True})
blackmailer = CharacterNode(name="Blackmailer", biases={"lawbias":0, "moralbias":-50}, tags={"Type":"Character", "Hometown":"Central Realm", "CharacterRole":"Support", "Alive":False})
ravenous_redmond = CharacterNode(name="Ravenous Redmond", biases={"lawbias":-100, "moralbias":-50}, tags={"Type":"Character", "Hometown":"Starlight", "CharacterRole":"Support", "Alive":True, "Criminal":"serial_killer"})

#While these objects are "human characters", we only reserve Character Nodes for characters with storylines and interactions. These characters are "Mobs" and thus won't have 
cheater_light = ObjectNode(name="Light Faction Cheaters", tags={"Type":"Mob", "Count":5})
cheater_dark = ObjectNode(name="Dark Faction Cheaters", tags={"Type":"Mob", "Count":5})
dicey_gang_member = ObjectNode(name="Dicey Gang Mambers", tags={"Type":"Mob", "Count":5})

light_weapons = ObjectNode(name="Light Faction Weapons", tags={"Type":"Weapon", "Status":"Working"})
dark_weapons = ObjectNode(name="Dark Faction Weapons", tags={"Type":"Weapon", "Status":"Working"})

#Sub locations can be accessed through the main location only, there is no need to "nest" locations because making charts would be confusing
duality = LocationNode(name="Duality", tags={"Type":"Location"})
duality_god_temple = LocationNode(name="Duality Temple", tags={"Type":"Location"})
duality_battle_arena = LocationNode(name="Duality Battle Arena", tags={"Type":"Location"})

central_realm = LocationNode(name="Central Realm", tags={"Type":"Location"})
central_realm_library = LocationNode(name="Central Realm Library", tags={"Type":"Location"})
central_relam_prison = LocationNode(name="Central Realm Prison", tags={"Type":"Location"})
central_realm_alley = LocationNode(name="Central Realm Alley", tags={"Type":"Location"})

starlight = LocationNode(name="Starlight", tags={"Type":"Location"})
dicey_den = LocationNode(name="Dicey Den", tags={"Type":"Location"})
knowers_abode = LocationNode(name="Knower's Abode", tags={"Type":"Location"})

all_characters = [honest_harry, justice_john, mysterious_misty, god_of_light, god_of_dark, dicey_darren,knower, shady_samuel, blackmailer, ravenous_redmond]
all_locations = [duality, duality_god_temple, duality_battle_arena, central_realm, central_realm_library, central_realm_alley, central_relam_prison, starlight, dicey_den, knowers_abode]
other_objects = [cheater_dark, cheater_light, dicey_gang_member, light_weapons, dark_weapons]

all_objects = all_characters + all_locations + other_objects

world_state = WorldState(name="World of Godly Games", objectnodes=all_objects)

world_state.connect(from_node=duality, edge_name=world_state.DEFAULT_HOLD_EDGE_NAME, to_node=honest_harry)
world_state.connect(from_node=duality, edge_name=world_state.DEFAULT_HOLD_EDGE_NAME, to_node=justice_john)
world_state.connect(from_node=starlight, edge_name=world_state.DEFAULT_HOLD_EDGE_NAME, to_node=mysterious_misty)

world_state.connect(from_node=duality_god_temple, edge_name=world_state.DEFAULT_HOLD_EDGE_NAME, to_node=god_of_light)
world_state.connect(from_node=duality_god_temple, edge_name=world_state.DEFAULT_HOLD_EDGE_NAME, to_node=god_of_dark)
world_state.connect(from_node=dicey_den, edge_name=world_state.DEFAULT_HOLD_EDGE_NAME, to_node=dicey_darren)
world_state.connect(from_node=knowers_abode, edge_name=world_state.DEFAULT_HOLD_EDGE_NAME, to_node=knower)
world_state.connect(from_node=central_realm_library, edge_name=world_state.DEFAULT_HOLD_EDGE_NAME, to_node=shady_samuel)
world_state.connect(from_node=central_realm_library, edge_name=world_state.DEFAULT_HOLD_EDGE_NAME, to_node=blackmailer)
world_state.connect(from_node=central_realm_alley, edge_name=world_state.DEFAULT_HOLD_EDGE_NAME, to_node=ravenous_redmond)

world_state.connect(from_node=duality, edge_name=world_state.DEFAULT_HOLD_EDGE_NAME, to_node=cheater_light)
world_state.connect(from_node=duality, edge_name=world_state.DEFAULT_HOLD_EDGE_NAME, to_node=cheater_dark)
world_state.connect(from_node=dicey_den, edge_name=world_state.DEFAULT_HOLD_EDGE_NAME, to_node=dicey_gang_member)
world_state.connect(from_node=duality_battle_arena, edge_name=world_state.DEFAULT_HOLD_EDGE_NAME, to_node=light_weapons)
world_state.connect(from_node=duality_battle_arena, edge_name=world_state.DEFAULT_HOLD_EDGE_NAME, to_node=dark_weapons)

world_state.doubleconnect(nodeA=duality, edge_name=world_state.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=central_realm)
world_state.doubleconnect(nodeA=duality, edge_name=world_state.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=starlight)

world_state.doubleconnect(nodeA=duality, edge_name=world_state.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=duality_battle_arena)
world_state.doubleconnect(nodeA=duality, edge_name=world_state.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=duality_god_temple)

world_state.doubleconnect(nodeA=central_realm, edge_name=world_state.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=central_realm_library)
world_state.doubleconnect(nodeA=central_realm, edge_name=world_state.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=central_realm_alley)
world_state.doubleconnect(nodeA=central_realm, edge_name=world_state.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=central_relam_prison)

world_state.doubleconnect(nodeA=starlight, edge_name=world_state.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=dicey_den)
world_state.doubleconnect(nodeA=starlight, edge_name=world_state.DEFAULT_ADJACENCY_EDGE_NAME, nodeB=knowers_abode)

#Now, we need to make connections between charcters.
world_state.doubleconnect(nodeA=honest_harry, edge_name="friends", nodeB=justice_john, value="hate_cheaters")
world_state.doubleconnect(nodeA=mysterious_misty, edge_name="friends", nodeB=dicey_darren, value="business_partners")
world_state.connect(from_node=knower, edge_name="fears", to_node=dicey_darren, value="criminal")
world_state.connect(from_node=shady_samuel, edge_name="fears", to_node=dicey_darren, value="criminal")


world_state.connect(from_node=shady_samuel, edge_name="hates",to_node=blackmailer, value="blackmailer")
world_state.connect(from_node=shady_samuel, edge_name="client_of", to_node=ravenous_redmond, value="hitman")

world_state.connect(from_node=ravenous_redmond, edge_name="hates", to_node=mysterious_misty, value="old_grudge")

world_state.doubleconnect(nodeA=god_of_dark, edge_name="rivals", nodeB=god_of_light, value="power_struggle")

# TODAY'S GOAL: Complete filling in the information for all these nodes
# Maybe even figure out rules as well
# Worry about whether or not things make sense or has ease of use later because currently it's all gonna be fucked anyways

# Requirements to talk to someone about cheating:
# Actor knows about the cheating
# Target does not know about the cheating
#
# Change
# The Target now has Knowledge of the Cheating
# Actor and Target both gain a task

actor_knows_cheating = HasTagTest()
target_not_know_cheating = HasTagTest()

target_now_knows_cheating = TagChange()
actor_gains_task_to_go_to_starlight = TaskChange()
target_gains_task_to_go_to_central_realm_library = TaskChange()

converse_about_cheating = StoryNode(name="Converse about Cheating", tags={"Type":"Conversation"}, charcount=1, target_count=1)

# Requirements to report cheating
# Actor(s) have evidence
# Target(s) is an Authority Figure
# Target(s) do not know about cheating
#
# Change
# Targets now know about the cheating

all_actors_knows_cheating = HasTagTest()
target_is_authority_figure = HasTagTest()

report_cheating = StoryNode

# Requirement to talk about library murder:
# Actor knows about the library murder
# Target does not know about library murder
#
# Change
# The Target now has Knowledge of the Library Murder

actor_knows_library_murder = HasTagTest()
target_not_know_library_murder = HasTagTest()

target_now_knows_library_murder = TagChange()

converse_about_library_murder = StoryNode

# Requirement to talk about redmond:
# Actor knows about Redmond
# Target does not know about Redmond
#
# Change
# Target now has knowledge about 

actor_knows_about_redmond = HasTagTest
target_not_know_about_redmond = HasTagTest

target_now_know_about_redmond = TagChange

converse_about_redmond = StoryNode

# Requirement to talk about Attacker:
# Actor has lost a fight
# 
# Change
# Target gains a new relationship to attack the attacker for revenge.
# Target gains a task to encounter someone for combat. (Placeholder is tested by won_against_in_a_fight)

actor_lost_fight = HasTagTest

target_now_has_provoke_reason = RelChange
target_gains_encounter_task = RelChange

converse_about_attacker = StoryNode

# Requirement to fight gang members:
# There is at least 1 gang member
# Actor and gang members share locations
#
# Change
# Dice gang member reduces by 1 (Depends on the writer, they could die or become unconscious)

one_conscious_gang_member = TagValueInRangeTest
actor_share_location_with_gang_member = SameLocationTest

reduce_gang_member = RelativeTagChange
fight_dice_gang_members = StoryNode

# Requirement to encounter someone for combat:
# There is an edge that says "HasProvokeReason"
# For example Misty's towards Harry would be Revenge, Harry towards Darren would be Investigation

actor_has_provoke_reason = HasEdgeTest
encounter_for_combat = StoryNode

# Requirement for someone to defeat another person:
# Preceded by Encounter for Combat (Make this a Joint Cont Rule)
# Winner is randomly determined
#
# Changes
# The actor has a relationship that says "won_against_in_a_fight".
win_fight_relationship = RelChange
defeat = StoryNode

defeat_follows_combat_encounter = ContinuousJointRule

# Requirement for someone to threaten another person:
# The target must fear someone who is friends with the threatener.

threaten_with_influence = StoryNode

# Requirement for someone to threaten another person:
# The target must have a relationship where they lost a fight against the attacker.

target_lost_fight_against_actor = HasEdgeTest
threaten_with_combat_victory = StoryNode

# Requirement
# Must be in same location with weapon

actor_share_location_weapon = SameLocationTest
check_weapons = StoryNode

note_all_weapons = StoryNode

# Requirement
# Must be in same location with weapon
# Replaces Note All Weapons
#
# Change
# For each Weapon that is Working, Weapon Status becomes broken
break_working_weapons = ConditionalChange
sabotage_weapons = StoryNode

# Requirement
# There is a dead person here.
dead_person_in_location = HeldItemTagTest
investigate = StoryNode

# Requirement
# Follows an Investigate Node when sharing a location with a Criminal or a Defeat node where the target is a Criminal.
# Target must have committed a crime
# Actor must have non-negative moral bias
target_is_criminal = HasTagTest
arrest = StoryNode

# Initial Story Graph:
# Everyone who's not a main character waits.
#
# Honest Harry is Conversing to Justice John about actions to take about the cheating and both of them gain tasks from this.
# Honest Harry gains a task to fight Dicey Darren.
# Justice John gains a task to investigate the Library.
#
# Mysterious Misty is conversing to Dicey Darren about Ravenous Redmond.
# Mysterious Misty will gain a task to talk to The Knower.