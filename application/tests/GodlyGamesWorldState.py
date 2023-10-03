import sys

sys.path.insert(0,'')

from application.components.StoryObjects import CharacterNode, LocationNode, ObjectNode
from application.components.WorldState import WorldState

honest_harry = CharacterNode(name="Honest Harry", biases={"lawbias":40, "moralbias":50}, tags={"Type":"Character", "Hometown":"Duality", "CharacterRole":"Main", "Alive":True})
justice_john = CharacterNode(name="Justice John", biases={"lawbias":30, "moralbias":60}, tags={"Type":"Character", "Hometown":"Duality", "CharacterRole":"Main", "Alive":True})
mysterious_misty = CharacterNode(name="Mysterious Misty", biases={"lawbias":-75, "moralbias":0}, tags={"Type":"Character", "Hometown":"Starlight", "CharacterRole":"Main", "Alive":True})

god_of_light = CharacterNode(name="God of Light", biases={"lawbias":0, "moralbias":0}, tags={"Type":"Character", "Hometown":"Duality", "CharacterRole":"Support", "Alive":True})
god_of_dark = CharacterNode(name="God of Darkness", biases={"lawbias":0, "moralbias":0}, tags={"Type":"Character", "Hometown":"Duality", "CharacterRole":"Support", "Alive":True})
dicey_darren = CharacterNode(name="Dicey Darren", biases={"lawbias":-30, "moralbias":-30}, tags={"Type":"Character", "Hometown":"Starlight", "CharacterRole":"Support", "Alive":True})
knower = CharacterNode(name="The Knower", biases={"lawbias":0, "moralbias":0}, tags={"Type":"Character", "Hometown":"Starlight", "CharacterRole":"Support", "Alive":True})
shady_samuel = CharacterNode(name="Shady Samuel", biases={"lawbias":0, "moralbias":-50}, tags={"Type":"Character", "Hometown":"Central Realm", "CharacterRole":"Support", "Alive":True})
blackmailer = CharacterNode(name="Blackmailer", biases={"lawbias":0, "moralbias":-50}, tags={"Type":"Character", "Hometown":"Central Realm", "CharacterRole":"Support", "Alive":False})
ravenous_redmond = CharacterNode(name="Ravenous Redmond", biases={"lawbias":-100, "moralbias":-50}, tags={"Type":"Character", "Hometown":"Starlight", "CharacterRole":"Support", "Alive":True})

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

#Now, we need to make connections