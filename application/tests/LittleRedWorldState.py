import sys
sys.path.insert(0,'')

from application.components.StoryObjects import *
from application.components.WorldState import *
from application.components.CharacterTask import *
from application.components.StoryGraphTwoWS import *
from application.components.StoryNode import *
from application.components.RelChange import *
from application.components.UtilityEnums import *

from application.StoryGeneration_NewFlowchart_WithMetrics import make_base_graph_from_previous_graph

#Oh holy shit there are many characters. The generation will take *forever*.
#Maybe some of these characters should be treated as Objects instead??? Like characters with no storyline of their own???
#But some of these characters do need to take actions sometimes...

#Only the characters who can act will be classified as characters, The rest will become Object Nodes with Type "NoStoryCharacter"
red = CharacterNode(name="Red", tags={"Type":"Character", "Age":"Child", "Alive":True}, internal_id=0)
wolf = CharacterNode(name="Wolf", biases={"moralbias":-50, "lawbias":-50}, tags={"Type":"Character", "Age":"Adult", "EatsChildren":True, "EatsNonChildren":True, "Alive":True}, internal_id=1)
brick_pig = CharacterNode(name="Brick", tags={"Type":"Character", "Age":"Adult", "Pacifist":True, "Alive":True}, internal_id=2)
grandma = CharacterNode(name="Grandma", biases={"moralbias":-50, "lawbias":0}, tags={"Type":"Character", "Age":"Adult", "Alive":True, "LikesKnowledge":True}, internal_id=3)

hunter = ObjectNode(name="Hunter", tags={"Type":"NoStoryCharacter", "Age":"Adult", "Alive":True}, internal_id=4)
mom = ObjectNode(name="Red's Mom", tags={"Type":"NoStoryCharacter", "Age":"Adult", "Alive":True}, internal_id=5)
wood_pig = ObjectNode(name="Wood Pig", tags={"Type":"NoStoryCharacter", "Age":"Child", "Alive":True}, internal_id=6)

#Hay Pig doesn't even do anything and he's just dead, his inclusion might not be needed
# hay_pig = ObjectNode(name="Hay Pig", tags={"Type":"NoStoryCharacter", "Age":"Child", "Alive":False, "NoCorpse":True}, internal_id=7)

papabear = CharacterNode(name="Papa Bear", tags={"Type":"Character", "Age":"Adult", "Alive":True}, internal_id=8)
mamabear = ObjectNode(name="Mama Bear", tags={"Type":"NoStoryCharacter", "Age":"Adult", "Alive":True}, internal_id=9)
babybear = ObjectNode(name="Baby Bear", tags={"Type":"NoStoryCharacter", "Age":"Child", "Alive":True}, internal_id=10)

witch = CharacterNode(name="Witch", tags={"Type":"Character", "Age":"Adult", "Alive":True, "EatsChildren":True, "LikesKnowledge":True}, internal_id=11)

protection_pillar = ObjectNode(name="Protection Pillar", tags={"Type":"Object", "ProtectsHomes":True}, internal_id=12)
columbo_diary = ObjectNode(name="Columbo's Diary", tags={"Type":"Object", "KnowledgeObject":True}, internal_id=13)
golden_goose = ObjectNode(name="Golden Goose", tags={"Type":"Object", "Valuable":True}, internal_id=14)
singing_harp = ObjectNode(name="Singing Harp", tags={"Type":"Object", "Valuable":True}, internal_id=15)
hunter_weps = ObjectNode(name="Hunter's Weapon", tags={"Type":"Weapon", "CanKill":True}, internal_id=7)

forest_village = LocationNode(name="Forest Village", tags={"Type":"Location"}, internal_id=15)
bear_house = LocationNode(name="Bear House", tags={"Type":"Location", "Home":True, "Demolished":False}, internal_id=16)
grandma_house = LocationNode(name="Grandma House", tags={"Type":"Location", "Home":True, "Demolished":False}, internal_id=17)
brick_pig_house = LocationNode(name="Brick House", tags={"Type":"Location", "Home":True, "Demolished":False}, internal_id=18)
witch_candy_house = LocationNode(name="Witch Candy House", tags={"Type":"Location", "Home":True, "Demolished":False}, internal_id=19)
random_forest = LocationNode(name="Random Forest", tags={"Type":"Location"}, internal_id=20)
forest_path = LocationNode(name="Forest Path", tags={"Type":"Location"}, internal_id=21)
plains_village = LocationNode(name="Plains Village", tags={"Type":"Location"}, internal_id=22)
mountain_village = LocationNode(name="Mountain Village", tags={"Type":"Location"}, internal_id=23)
mountain_valley = LocationNode(name="Mountain Valley", tags={"Type":"Location"}, internal_id=24)
wood_pig_house = LocationNode(name="Wood House", tags={"Type":"Location", "Home":True, "Demolished":False}, internal_id=25)
magic_temple = LocationNode(name="Magic Temple", tags={"Type":"Location", "Home":True, "Demolished":False}, internal_id=26)
red_house = LocationNode(name="Red House", tags={"Type":"Location", "Home":True, "Demolished":False}, internal_id=27)
hunter_house = LocationNode(name="Hunter House", tags={"Type":"Location", "Home":True, "Demolished":False}, internal_id=28)

list_of_objects = [red, wolf, brick_pig,grandma, hunter, mom, wood_pig, hunter_weps, papabear, mamabear, babybear, witch, protection_pillar, columbo_diary, golden_goose, singing_harp, forest_village, bear_house, grandma_house, brick_pig_house, witch_candy_house, random_forest, forest_path, plains_village, mountain_valley, mountain_village, wood_pig_house, magic_temple, red_house, hunter_house]

reds_world_state = WorldState(name="Reds World State", objectnodes=list_of_objects)

reds_world_state.doubleconnect(from_node=forest_village, edge_name="connects", to_node=bear_house)
reds_world_state.doubleconnect(from_node=forest_village, edge_name="connects", to_node=forest_path)
reds_world_state.doubleconnect(from_node=forest_village, edge_name="connects", to_node=grandma_house)
reds_world_state.doubleconnect(from_node=forest_village, edge_name="connects", to_node=brick_pig_house)
reds_world_state.doubleconnect(from_node=forest_village, edge_name="connects", to_node=witch_candy_house)
reds_world_state.doubleconnect(from_node=random_forest, edge_name="connects", to_node=forest_path)
reds_world_state.doubleconnect(from_node=plains_village, edge_name="connects", to_node=forest_path)
reds_world_state.doubleconnect(from_node=mountain_valley, edge_name="connects", to_node=forest_path)
reds_world_state.doubleconnect(from_node=mountain_valley, edge_name="connects", to_node=magic_temple)
reds_world_state.doubleconnect(from_node=mountain_valley, edge_name="connects", to_node=mountain_village)
reds_world_state.doubleconnect(from_node=wood_pig_house, edge_name="connects", to_node=mountain_village)
reds_world_state.doubleconnect(from_node=plains_village, edge_name="connects", to_node=red_house)
reds_world_state.doubleconnect(from_node=plains_village, edge_name="connects", to_node=hunter_house)

reds_world_state.connect(from_node=mom, edge_name="parent_of", to_node=red)
reds_world_state.connect(from_node=red, edge_name="child_of", to_node=mom)
reds_world_state.connect(from_node=grandma, edge_name="parent_of", to_node=mom)
reds_world_state.connect(from_node=mom, edge_name="child_of", to_node=grandma)

reds_world_state.connect(from_node=papabear, edge_name="parent_of", to_node=babybear)
reds_world_state.connect(from_node=babybear, edge_name="child_of", to_node=papabear)
reds_world_state.connect(from_node=mamabear, edge_name="parent_of", to_node=babybear)
reds_world_state.connect(from_node=babybear, edge_name="child_of", to_node=mamabear)

reds_world_state.connect(from_node=red_house, edge_name="holds", to_node=mom)
reds_world_state.connect(from_node=red_house, edge_name="holds", to_node=red)
reds_world_state.connect(from_node=hunter_house, edge_name="holds", to_node=hunter)
reds_world_state.connect(from_node=hunter, edge_name="holds", to_node=hunter_weps)
reds_world_state.connect(from_node=grandma_house, edge_name="holds", to_node=grandma)
reds_world_state.connect(from_node=bear_house, edge_name="holds", to_node=papabear)
reds_world_state.connect(from_node=bear_house, edge_name="holds", to_node=mamabear)
reds_world_state.connect(from_node=bear_house, edge_name="holds", to_node=babybear)
reds_world_state.connect(from_node=witch_candy_house, edge_name="holds", to_node=witch)
reds_world_state.connect(from_node=brick_pig_house, edge_name="holds", to_node=brick_pig)
reds_world_state.connect(from_node=wood_pig_house, edge_name="holds", to_node=wood_pig)
# reds_world_state.connect(from_node=wood_pig_house, edge_name="holds", to_node=hay_pig)
reds_world_state.connect(from_node=forest_village, edge_name="holds", to_node=wolf)

reds_world_state.connect(from_node=magic_temple, edge_name="holds", to_node=protection_pillar)
reds_world_state.connect(from_node=random_forest, edge_name="holds", to_node=columbo_diary)
reds_world_state.connect(from_node=random_forest, edge_name="holds", to_node=singing_harp)
reds_world_state.connect(from_node=random_forest, edge_name="holds", to_node=golden_goose)

# Actions
# Eat (It's a messy action)

actor_is_alive = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Alive", value=True)
target_is_alive = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Alive", value=True)
actor_is_not_unconscious =HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Unconscious", value=True, inverse=True)
target_is_not_unconscious = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Unconscious", value=True, inverse=True)

actor_eats_children = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="EatsChildren", value=True)
target_is_child = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Age", value="Child")

target_becomes_dead = TagChange(name="Target Becomes Dead", object_node_name=GenericObjectNode.GENERIC_TARGET, tag="Alive", value=False, add_or_remove=ChangeAction.ADD)
target_leaves_no_corpse = TagChange(name="Target Leaves No Body", object_node_name=GenericObjectNode.GENERIC_TARGET, tag="NoCorpse", value=True, add_or_remove=ChangeAction.ADD)

eat_and_kill = StoryNode(name="Eat and Kill", tags={"Type":"Murder", "costly":True}, charcount=1, target_count=1, effects_on_next_ws=[target_becomes_dead, target_leaves_no_corpse], suggested_test_list=[actor_is_alive, target_is_alive, actor_eats_children, target_is_child])

# Kill (Needs to carry weapon or be a wolf)
actor_has_reason_to_kill_target = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="KillReason", object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True)
actor_has_killing_tool = HeldItemTagTest(holder_to_test=GenericObjectNode.GENERIC_ACTOR, tag_to_test="CanKill", value_to_test=True)

kill_another_actor = StoryNode(name="Actor Kills Actor", tags={"Type":"Murder"}, charcount=1, target_count=1, effects_on_next_ws=[target_becomes_dead], required_test_list=[actor_has_reason_to_kill_target, actor_has_killing_tool, actor_is_alive, target_is_alive])

# Scare (Makes a character leave home, works on children and adults, has a chance to cause adults to fight back instead (This is a Rule))

actor_has_reason_to_scare_target = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="ScareReason", object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True)

someone_is_target = ObjectEqualityTest(object_list=[GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, GenericObjectNode.GENERIC_TARGET])
someone_is_children = HasTagTest(object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, tag="Age", value="Child")
someone_is_scared_of_actor = RelChange(name="Someone Scared of Actor", node_a=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name="fears", node_b=GenericObjectNode.GENERIC_ACTOR, add_or_remove=ChangeAction.ADD, value="threatened")
children_target_becomes_scared = ConditionalChange(name="Children Target Becomes Scared of Actor", list_of_condition_tests=[someone_is_children], list_of_changes=[someone_is_target, someone_is_children, someone_is_scared_of_actor])

scare = StoryNode(name="Actor Scares Actor", tags={"Type":"Murder"}, charcount=1, target_count=1, effects_on_next_ws=[children_target_becomes_scared], required_test_list=[actor_has_reason_to_scare_target, actor_is_alive, target_is_alive])

# Fight (Has a chance to end up with either character being killed or defeated.)
# (They must share location.)

actor_and_target_shares_location = SameLocationTest(list_to_test=[GenericObjectNode.GENERIC_ACTOR, GenericObjectNode.GENERIC_TARGET])
fight = StoryNode(name="Fight", tags={"Type":"Fight"}, charcount=1, target_count=1, required_test_list=[actor_and_target_shares_location])

# Defeat (A defeated character becomes unconscious)
# Unconscious characters cannot act, but they can wake up after a while. (With Patternless Rule)

target_becomes_unconscious = TagChange(name="Target Becomes Unconscious", object_node_name=GenericObjectNode.GENERIC_TARGET, tag="Unconscious", value=True, add_or_remove=ChangeAction.ADD)
defeat = StoryNode(name="Defeat", tags={"Type":"Fight"}, charcount=1, target_count=1, required_test_list=[actor_and_target_shares_location], effects_on_next_ws=[target_becomes_unconscious])

# Threaten (Can cause the target to either become scared or become defiant, either way this forms a new relationship between target and actor)
# Become Scared
# Become Defiant
# Attack (Can lead to a fight, killing, or can lead to the target escaping from the attacker)
# Escape from Attacker
# Get Armed (Requires Red to have some fear of the wolf and share location with Mom)
# Destroy House (Owner must not be home. There must not be an active rod. This adds Home Destruction Tag to the actor. The tag goes away when the action is complete.)
# Attack Intruder (If sharing location with home destruction tag character)
# Rebuild House (House must have been destroyed)
# Fight for Rod (if sharing location with someone else carrying rod and not scared of target, must be morally questionible)
# Install Rod (If a house has a rod installed, other characters cannot destroy the house.)
# Scheme Together (Characters must both have negative moral bias.)
# Tell Mom about Missing Grandma (Must have witnessed wolf in grandma's house)
# Witness House Destruction (Will learn that the target is a criminal)
# Kidnap (carries another unconscious character, holding them instead of the location)
# Pick Up Treasure (If the character LikesTreasure and shares location with a valuable item, they will pick it up)
# Pick Up Knowledge Trinket (If the character LikesKnowledge and shares location with a KnowledgeObject, they will pick it up)

# Generic Quests
# Find Rod Quest (Need knowledge of Rod)
# Steal Rod (If Rod is found in someone else's house)
# Destroy Rod (If you are Grandma)
# Plant Rod (Installs the rod, if the rod is installed then it cannot be destroyed)

# Brick-Specific Quest
# Run from Wolf to Wood House ()
# Return Home (After completing the first quest)
# Fight Grandma (After being freed from wolf)

# Red-Specific Quest
# Visit Grandma (First Actual Quest)
# Tell Mom about Wolf (Second Quest, gain after witnessing Wolf)

# Wolf-Specific Quest
# Threaten Witch
# Threaten Brick
# Threaten Bears
# 
# All three will lead to the target to become defiant, and Wolf can attack them. This might lead to:
# - The target dying
# - The target being eaten (if the target is a child, because the wolf only eats children)
# - The target running away
# - The wolf running away
# - The wolf dying
#
# Chase Red
# Report Empty Village (Can be done once Witch, Papa Bear, and Brick are not in village)
# 

# Grandma-Specific Quest
# Destroy Homes
