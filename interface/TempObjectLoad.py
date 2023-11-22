from application.components.StoryObjects import *

columbo = CharacterNode(name="Columbo", biases={"lawbias":0, "moralbias":0}, tags={"Type":"Character","Job":"Explorer","Species":"Human", "Goal":"Explore New World","Alive":True, "PlotArmor":True, "Stranded":True}, internal_id=1)
iris = CharacterNode(name="Iris", biases={"lawbias":0, "moralbias":0}, tags={"Type":"Character","Job":"Destroyer","Species":"Robot", "Goal":"Eradicate Living Beings", "Version":"Old", "Alive":True}, internal_id=2)
amil = CharacterNode(name="Amil", biases={"lawbias":0, "moralbias":0}, tags={"Type":"Character","Job":"Military","Species":"Human", "Goal":"Rescue Mission","PlotArmor":True,"Alive":True}, internal_id=3)

alien_god = CharacterNode(name="Alien God", biases={"lawbias":100, "moralbias":0}, tags={"Type":"Character","Species":"God", "Alive":True, "Stranded":True}, internal_id=4)
apollo = CharacterNode(name="Apollo", biases={"lawbias":100, "moralbias":0}, tags={"Type":"Character","Job":"Destroyer","Species":"Robot", "Goal":"Repel Greenland Humans","Version":"New","Alive":False}, internal_id=5)

earth = LocationNode(name="Earth", tags={"Type":"Location", "Climate":"Hi-Tech", "AlienGodsWill":"Unknown"}, internal_id=1)
new_world_greenland = LocationNode(name="New World Greenland", tags={"Type":"Location", "Climate":"Lush", "AlienGodsWill":"Preserve"}, internal_id=2)
tatain = LocationNode(name="Tatain", tags={"Type":"Location", "Climate":"Sandy", "AlienGodsWill":"Destroy"}, internal_id=3)
death_paradise = LocationNode(name="Death Paradise", tags={"Type":"Location", "Climate":"Poisonous", "AlienGodsWill":"Destroy"}, internal_id=4)
alien_god_planet = LocationNode(name="Alien God Planet", tags={"Type":"Location", "Climate":"Unknown", "AlienGodsWill":"Unknown"}, internal_id=5)
outer_space = LocationNode(name="Outer Space", tags={"Type":"Location", "Climate":"Space", "AlienGodsWill":"Unknown"}, internal_id=6)

greenland_insects = ObjectNode(name="Greenland Insects", tags={"Type":"Mob", "Count":2, "Behavior":"Aggressive", "EdibleFlesh":True, "Faction":None},internal_id=1)
tatain_people = ObjectNode(name="Tatain People", tags={"Type":"Mob","Count":1, "Behavior":"Passive", "Faction":"Tatain"}, internal_id=2)
death_paradise_robots = ObjectNode(name="Death Paradise Robots", tags={"Type":"Mob","Count":1, "Behavior":"Aggressive", "Faction":"Death Paradise"}, internal_id=3)
enemy_mercenary = ObjectNode(name="Enemy Mercenary", tags={"Type":"Mob","Count":1, "Behavior":"Aggressive", "Faction":"Mercenary"}, internal_id=4)
earth_army = ObjectNode(name="Earth Army", tags={"Type":"Mob","Count":2, "Behavior":"Passive", "Faction":"Earth"}, internal_id=5)

all_characters = [columbo, iris, amil, alien_god, apollo]
all_locations = [earth, new_world_greenland, tatain, death_paradise, outer_space, alien_god_planet]
other_objects = [greenland_insects, tatain_people, death_paradise_robots, enemy_mercenary, earth_army]