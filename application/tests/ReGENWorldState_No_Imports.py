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

royal_castle = LocationNode(name="Royal_Castle")
main_town = LocationNode(name="Main_Town")
peasant_village = LocationNode(name="Peasant_Village")
large_forest = LocationNode(name="Large_Forest")
goblin_city = LocationNode(name="Goblin_City")
orc_cave = LocationNode(name="Orc_Cave")

excalibur = ObjectNode(name="Excalibur", tags={"Status":"Owned","Type":"Object","Value":"Priceless"})
golden_mirror = ObjectNode(name="Golden_Mirror", tags={"Status":"Owned","Type":"Object","Value":"Valuable"})
dirty_shovel = ObjectNode(name="Dirty_Shovel", tags={"Status":"Owned","Type":"Object","Value":"Worthless"})
tax_income = ObjectNode(name="Tax_Income", tags={"Status":"Owned","Type":"Object","Value":"Valuable"})
royal_sceptre = ObjectNode(name="Royal_Sceptre", tags={"Status":"Owned","Type":"Object","Value":"Priceless"})
royal_crown = ObjectNode(name="Royal_Crown", tags={"Status":"Owned","Type":"Object","Value":"Priceless"})

goblin = ObjectNode(name="Goblin",tags={"Type":"Enemy","Rank":"Peon","Number":3})
goblin_king = ObjectNode(name="Goblin_King",tags={"Type":"Enemy","Rank":"King","Number":1})
bandits = ObjectNode(name="Bandits",tags={"Type":"Enemy","Rank":"Peon","Number":3})
orc = ObjectNode(name="Orc",tags={"Type":"Enemy","Rank":"Peon","Number":3})