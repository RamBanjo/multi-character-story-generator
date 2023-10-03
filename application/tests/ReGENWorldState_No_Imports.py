import sys
sys.path.insert(0,'')

from application.components.StoryObjects import CharacterNode, LocationNode, ObjectNode

brave_dave = CharacterNode(name="Brave_Dave", biases={"lawbias":50, "moralbias":0}, tags={"Type":"NPC", "Rank":"Knight", "Alive":True})
smug_smith = CharacterNode(name="Smug_Smith", biases={"lawbias":10, "moralbias":-20}, tags={"Type":"NPC", "Rank":"Lord", "Alive":True})
fancy_fanny = CharacterNode(name="Fancy_Fanny", biases={"lawbias":40, "moralbias":0}, tags={"Type":"NPC", "Rank":"Queen", "Alive":True})
regal_regis = CharacterNode(name="Regal_Regis", biases={"lawbias":100, "moralbias":0}, tags={"Type":"NPC", "Rank":"King", "Alive":True})
smelly_sally = CharacterNode(name="Smelly_Sally", biases={"lawbias":-20, "moralbias":30}, tags={"Type":"NPC", "Rank":"Peasant", "Alive":True})
filthy_phil = CharacterNode(name="Filthy_Phil", biases={"lawbias":-10, "moralbias":0}, tags={"Type":"NPC", "Rank":"Peasant", "Alive":True})
sly_fry = CharacterNode(name="Sly_Fry", biases={"lawbias":-80, "moralbias":10}, tags={"Type":"NPC", "Rank":"Thief", "Alive":True})
rich_ritchie = CharacterNode(name="Rich_Ritchie", biases={"lawbias":0, "moralbias":30}, tags={"Type":"NPC", "Rank":"Tax Collector", "Alive":True})
player_art = CharacterNode(name="Adventure_Arthur", biases={"lawbias":40, "moralbias":0}, tags={"Type":"Player", "Rank":"Knight", "Alive":True})
player_rob = CharacterNode(name="Robber_Robin", biases={"lawbias":-40, "moralbias":0}, tags={"Type":"Player", "Rank":"Ranger", "Alive":True})

royal_castle = LocationNode
main_town = LocationNode
peasant_village = LocationNode
large_forest = LocationNode
goblin_city = LocationNode
orc_cave = LocationNode

excalibur = ObjectNode
golden_mirror = ObjectNode
dirty_shovel = ObjectNode
tax_income = ObjectNode
royal_sceptre = ObjectNode
royal_crown = ObjectNode

goblin = ObjectNode
goblin_king = ObjectNode
bandits = ObjectNode
orc = ObjectNode