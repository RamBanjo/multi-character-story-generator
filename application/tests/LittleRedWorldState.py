import sys
sys.path.insert(0,'')

from application.components.StoryObjects import *
from application.components.WorldState import *
from application.components.CharacterTask import *
from application.components.StoryGraphTwoWS import *
from application.components.StoryNode import *
from application.components.RelChange import *
from application.components.UtilityEnums import *
from application.components.RewriteRuleWithWorldState import *

from application.StoryGeneration_NewFlowchart_WithMetrics import make_base_graph_from_previous_graph

#Oh holy shit there are many characters. The generation will take *forever*.
#Maybe some of these characters should be treated as Objects instead??? Like characters with no storyline of their own???
#But some of these characters do need to take actions sometimes...

#Only the characters who can act will be classified as characters, The rest will become Object Nodes with Type "NoStoryCharacter"
red = CharacterNode(name="Red", tags={"Type":"Character", "Age":"Child", "Alive":True}, internal_id=0)
wolf = CharacterNode(name="Wolf", biases={"moralbias":-50, "lawbias":-50}, tags={"Type":"Character", "Age":"Adult", "EatsChildren":True, "EatsNonChildren":True, "Alive":True, "CanKill":"Fangs"}, internal_id=1)
brick_pig = CharacterNode(name="Brick", tags={"Type":"Character", "Age":"Adult", "Pacifist":True, "Alive":True}, internal_id=2)
grandma = CharacterNode(name="Grandma", biases={"moralbias":-50, "lawbias":0}, tags={"Type":"Character", "Age":"Adult", "Alive":True, "LikesKnowledge":True, "CanKill":"Knife"}, internal_id=3)

hunter = CharacterNode(name="Hunter", tags={"Type":"Character", "Age":"Adult", "Alive":True, "CanKill":"Gun"}, internal_id=4)
mom = ObjectNode(name="Red's Mom", tags={"Type":"NoStoryCharacter", "Age":"Adult", "Alive":True}, internal_id=5)
wood_pig = ObjectNode(name="Wood Pig", tags={"Type":"NoStoryCharacter", "Age":"Child", "Alive":True}, internal_id=6)

#Hay Pig doesn't even do anything and he's just dead, his inclusion might not be needed
# hay_pig = ObjectNode(name="Hay Pig", tags={"Type":"NoStoryCharacter", "Age":"Child", "Alive":False, "NoCorpse":True}, internal_id=7)

papabear = CharacterNode(name="Papa Bear", tags={"Type":"Character", "Age":"Adult", "Alive":True, "CanKill":"Claws"}, internal_id=8)

#These two don't have much point to exist, but Baby Bear might be important because he could get eaten by the Witch or Wolf.
mamabear = ObjectNode(name="Mama Bear", tags={"Type":"NoStoryCharacter", "Age":"Adult", "Alive":True}, internal_id=9)
babybear = ObjectNode(name="Baby Bear", tags={"Type":"NoStoryCharacter", "Age":"Child", "Alive":True}, internal_id=10)

witch = CharacterNode(name="Witch", tags={"Type":"Character", "Age":"Adult", "Alive":True, "EatsChildren":True, "LikesKnowledge":True, "CanKill":"Magic"}, internal_id=11)

protection_pillar = ObjectNode(name="Protection Pillar", tags={"Type":"Object", "ProtectsHomes":True, "Active":False}, internal_id=12)
columbo_diary = ObjectNode(name="Columbo's Diary", tags={"Type":"Object", "KnowledgeObject":True}, internal_id=13)
golden_goose = ObjectNode(name="Golden Goose", tags={"Type":"Object", "Valuable":True}, internal_id=14)
singing_harp = ObjectNode(name="Singing Harp", tags={"Type":"Object", "Valuable":True}, internal_id=15)
# hunter_weps = ObjectNode(name="Hunter's Weapon", tags={"Type":"Weapon", "CanKill":True}, internal_id=7)

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

list_of_objects = [red, wolf, brick_pig,grandma, hunter, mom, wood_pig, papabear, mamabear, babybear, witch, protection_pillar, columbo_diary, golden_goose, singing_harp, forest_village, bear_house, grandma_house, brick_pig_house, witch_candy_house, random_forest, forest_path, plains_village, mountain_valley, mountain_village, wood_pig_house, magic_temple, red_house, hunter_house]

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
# reds_world_state.connect(from_node=hunter, edge_name="holds", to_node=hunter_weps)
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

reds_world_state.connect(from_node=brick_pig, edge_name="owns", to_node=brick_pig_house)
reds_world_state.connect(from_node=witch, edge_name="owns", to_node=witch_candy_house)
reds_world_state.connect(from_node=papabear, edge_name="owns", to_node=bear_house)
reds_world_state.connect(from_node=grandma, edge_name="owns", to_node=grandma_house)
reds_world_state.connect(from_node=hunter, edge_name="owns", to_node=hunter_house)
reds_world_state.connect(from_node=wood_pig, edge_name="owns", to_node=wood_pig_house)
reds_world_state.connect(from_node=mom, edge_name="owns", to_node=red_house)

# Actions
# Eat (It's a messy action.)

actor_is_alive = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Alive", value=True)
target_is_alive = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Alive", value=True)
actor_is_not_unconscious =HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Unconscious", value=True, inverse=True)
actor_is_unconscious =HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Unconscious", value=True)
target_is_not_unconscious = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Unconscious", value=True, inverse=True)
target_is_unconscious = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Unconscious", value=True)
actor_and_target_shares_location = SameLocationTest(list_to_test=[GenericObjectNode.GENERIC_ACTOR, GenericObjectNode.GENERIC_TARGET])

actor_eats_children = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="EatsChildren", value=True)
target_is_child = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Age", value="Child")

target_becomes_dead = TagChange(name="Target Becomes Dead", object_node_name=GenericObjectNode.GENERIC_TARGET, tag="Alive", value=False, add_or_remove=ChangeAction.ADD)
target_leaves_no_corpse = TagChange(name="Target Leaves No Body", object_node_name=GenericObjectNode.GENERIC_TARGET, tag="NoCorpse", value=True, add_or_remove=ChangeAction.ADD)

eat_and_kill = StoryNode(name="Eat and Kill", tags={"Type":"Murder", "costly":True}, charcount=1, target_count=1, effects_on_next_ws=[target_becomes_dead, target_leaves_no_corpse], required_test_list=[actor_is_alive, target_is_alive, actor_eats_children, target_is_child, actor_and_target_shares_location])

# Kill (Needs to carry weapon, wolf's weapon is his claws)
actor_has_reason_to_kill_target = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="KillReason", object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True, score=10)
actor_has_killing_tool = HasTagTest(holder_to_test=GenericObjectNode.GENERIC_ACTOR, tag_to_test="CanKill", soft_equal=True, score=10)

kill_another_actor = StoryNode(name="Actor Kills Actor", tags={"Type":"Murder", "costly":True}, charcount=1, target_count=1, effects_on_next_ws=[target_becomes_dead], required_test_list=[actor_is_alive, target_is_alive, actor_is_not_unconscious, actor_and_target_shares_location], suggested_test_list=[actor_has_killing_tool, actor_has_reason_to_kill_target])

# Scare (Makes a character leave home, works on children and adults, has a chance to cause adults to fight back instead (This is a Rule))

actor_has_reason_to_scare_target = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="ScareReason", object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True)

#Hey, maybe we should make becoming scared to be a thing on its own? A rule? Just a suggestion

scare = StoryNode(name="Actor Scares Target", tags={"Type":"Threaten"}, charcount=1, target_count=1, required_test_list=[actor_has_reason_to_scare_target, actor_is_alive, target_is_alive, actor_and_target_shares_location])

# Fight (Has a chance to end up with either character being killed or defeated.)
# (They must share location.)

fight = StoryNode(name="Fight", tags={"Type":"Fight"}, charcount=1, target_count=1, required_test_list=[actor_and_target_shares_location])

# Defeat (A defeated character becomes unconscious)
# Unconscious characters cannot act, but they can wake up after a while. (With Patternless Rule)

target_becomes_unconscious = TagChange(name="Target Becomes Unconscious", object_node_name=GenericObjectNode.GENERIC_TARGET, tag="Unconscious", value=True, add_or_remove=ChangeAction.ADD)
defeat = StoryNode(name="Defeat", tags={"Type":"Fight"}, charcount=1, target_count=1, required_test_list=[actor_and_target_shares_location, actor_is_alive, target_is_alive, actor_is_not_unconscious, target_is_not_unconscious], effects_on_next_ws=[target_becomes_unconscious])

# Threaten (Can cause the target to either become scared or become defiant, either way this forms a new relationship between target and actor)
# Become Scared
actor_becomes_scared_of_target = RelChange(name="Actor fears Target", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="fears", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.ADD, value="Threatened")

actor_is_child = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Age", value="Child", score=10)
actor_is_not_child_gives_bad_score = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Age", value="Child", inverse=True, score=-10)

actor_scared_of_target = StoryNode(name="Actor becomes scared of Target", tags={"Type":"Fight"}, charcount=1, target_count=1, effects_on_next_ws=[actor_becomes_scared_of_target], suggested_test_list=[actor_is_child, actor_is_not_child_gives_bad_score], required_test_list=[actor_and_target_shares_location, actor_is_alive, target_is_alive, actor_is_not_unconscious, target_is_not_unconscious])

# Become Defiant
actor_becomes_defiant_of_target = RelChange(name="Actor fears Target", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="defies", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.ADD, value="Threatened")

actor_defies_target = StoryNode(name="Actor becomes defiant of Target", tags={"Type":"Fight", "important_action":True}, charcount=1, target_count=1, effects_on_next_ws=[actor_becomes_defiant_of_target], required_test_list=[actor_is_alive, target_is_alive, actor_is_not_unconscious, target_is_not_unconscious, actor_and_target_shares_location])

# Attack (Can lead to a fight, killing, or can lead to the target escaping from the attacker)
# Someone would attack target if they have a reason to kill the other person, or if 
actor_attacks_target = StoryNode(name="Actor attacks Target", tags={"Type":"Fight"}, charcount=1, target_count=1, required_test_list=[actor_is_alive, target_is_alive, actor_is_not_unconscious, target_is_not_unconscious, actor_and_target_shares_location], suggested_test_list=[])

# Escape from Attacker (This makes them scared of attacker, and thus more likely to run away)
actor_escapes_from_attacking_target = StoryNode(name="Actor Flees Target", tags={"Type":"Fight"}, charcount=1, target_count=1, required_test_list=[actor_is_alive, target_is_alive, actor_is_not_unconscious, target_is_not_unconscious, actor_and_target_shares_location], effects_on_next_ws=[actor_becomes_scared_of_target])

# Get Armed (Requires Red to have some fear of the wolf and share location with Mom)

actor_fears_wolf = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="fears", object_to_test=wolf)
actor_is_child_of_target = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="child_of", object_to_test=GenericObjectNode.GENERIC_TARGET)
target_is_redsmom = ObjectEqualityTest(object_list=[GenericObjectNode.GENERIC_TARGET, mom])

actor_becomes_armed = StoryNode(name="Actor Becomes Armed by Target", tags={"Type":"Conversation"}, charcount=1, target_count=1, required_test_list=[actor_is_alive, target_is_alive, actor_is_not_unconscious, target_is_not_unconscious, actor_and_target_shares_location])

# Destroy House (Owner must not be home. There must not be an active rod. This adds Home Destruction Tag to the actor. The tag goes away when the action is complete.)

current_location_is_home = HasTagTest(object_to_test=GenericObjectNode.GENERIC_LOCATION, tag="Home", value=True)
actor_shares_location_with_someone = SameLocationTest(list_to_test=[GenericObjectNode.GENERIC_ACTOR, GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER])
actor_shares_location_with_no_one = SomethingPassesAllGivenTestsTest(list_of_tests_with_placeholder=[actor_shares_location_with_someone], inverse=True)
actor_does_not_own_home = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="owns", object_to_test=GenericObjectNode.GENERIC_LOCATION, inverse=True)
location_is_destroyed = HasTagTest(object_to_test=GenericObjectNode.GENERIC_LOCATION, tag="")

actor_is_destroying_home_change = TagChange(name="Actor is Destroying Home", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="DestroyingHome", value=True, add_or_remove=ChangeAction.ADD)
home_is_destroyed_change = TagChange(name="Home is Destroyed", tag="Demolished", value=True, add_or_remove=ChangeAction.ADD)

home_is_being_destroyed = TagChange(name="Home Under Destroy Process", object_node_name=GenericObjectNode.GENERIC_LOCATION, tag="UnderDestroyProcess", value=True, add_or_remove=ChangeAction.ADD)
home_finishes_being_destroyed = TagChange(name="Home No LongerUnder Destroy Process", object_node_name=GenericObjectNode.GENERIC_LOCATION, tag="UnderDestroyProcess", value=True, add_or_remove=ChangeAction.REMOVE)

actor_not_destroying_home_change = TagChange(name="Actor is Destroying Home", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="DestroyingHome", value=True, add_or_remove=ChangeAction.REMOVE)

home_is_being_destroyed_check = HasTagTest(object_to_test=GenericObjectNode.GENERIC_LOCATION, tag="UnderDestroyProcess", value=True)
actor_is_destroying_home_check = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="DestroyingHome", value=True)

location_not_hold_rod_check = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_TARGET, edge_name_test="holds", object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, inverse=True)
rod_is_not_active_check = HasTagTest(object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, tag="Active", value=True, inverse=True)
target_no_rod_or_rod_not_active = [location_not_hold_rod_check, rod_is_not_active_check]

no_active_rod_exists_here_check = ObjectPassesAtLeastOneTestTest(list_of_tests_with_placeholder=target_no_rod_or_rod_not_active, object_to_test=protection_pillar)

actor_destroys_house = StoryNode(name="Actor Starts Destroying House", tags={"Type":"Destruction", "costly":True}, required_test_list=[actor_is_alive, actor_is_not_unconscious, current_location_is_home, actor_shares_location_with_no_one, actor_does_not_own_home], effects_on_next_ws=[home_is_being_destroyed, actor_is_destroying_home_change, no_active_rod_exists_here_check])
actor_finishes_destroy_house = StoryNode(name="Actor Finishes Destroying House", tags={"Type":"Destruction"}, required_test_list=[home_is_being_destroyed_check, actor_is_destroying_home_check])

target_is_destroying_house_check = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="DestroyingHome", value=True)

# Attack Intruder (If sharing location with home destruction tag character)
killreason_homedestroyanger = RelChange(name="Gain Kill Reason HomeDestroy", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="KillReason", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.ADD, value="anger_destroyhome")
attack_home_intruder = StoryNode(name="Attack Home Intruder", tags={"Type":"Fight", "important_action":True}, charcount=1, target_count=1, required_test_list=[actor_is_alive, target_is_alive, actor_is_not_unconscious, target_is_not_unconscious, actor_and_target_shares_location, target_is_destroying_house_check], effects_on_next_ws=[killreason_homedestroyanger])

# Rebuild House (House must have been destroyed)
actor_owns_home = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="owns", object_to_test=GenericObjectNode.GENERIC_LOCATION)
house_is_destroyed_check = HasTagTest(object_to_test=GenericObjectNode.GENERIC_LOCATION, tag="Demolished", value=True)
home_is_rebuilt_change = TagChange(name="Home is Destroyed", tag="Demolished", value=False, add_or_remove=ChangeAction.ADD)

home_is_not_being_destroyed_check = HasTagTest(object_to_test=GenericObjectNode.GENERIC_LOCATION, tag="UnderDestroyProcess", value=True, inverse=True)
rebuild_house = StoryNode(name="Rebuild House", tags={"Type":"Rebuilding"}, required_test_list=[actor_owns_home, house_is_destroyed_check, actor_is_alive, actor_is_not_unconscious, home_is_not_being_destroyed_check], effects_on_next_ws=[home_is_rebuilt_change])

# Fight for Rod (if sharing location with someone else carrying rod and not scared of target, must be morally questionible)
character_less_than_50_lawful_rewarded = InBiasRangeTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, bias_axis="moral", max_accept=-50, score=20)
target_holds_rod_check = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_TARGET, edge_name_test="holds", object_to_test=protection_pillar)

fight_for_rod = StoryNode(name="Fight for Rod", tags={"Type":"Fight"}, charcount=1, target_count=1, required_test_list=[target_holds_rod_check, actor_is_alive, target_is_alive, actor_is_not_unconscious, target_is_not_unconscious], suggested_test_list=[character_less_than_50_lawful_rewarded])

# Defeat for Rod (follows up Fight for Rod if the character holding rod loses, follow up with normal defeat if character holding rod wins)
target_no_longer_holds_rod = RelChange(name="Target Stop Hold Rod", node_a=GenericObjectNode.GENERIC_TARGET, edge_name="holds", node_b=protection_pillar, add_or_remove=ChangeAction.REMOVE)
actor_holds_rod = RelChange(name="Actor Hold Rod", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="holds", node_b=protection_pillar, add_or_remove=ChangeAction.ADD)

defeat_and_take_rod_target_unconscious = StoryNode(name="Defeat and Steal Rod", tags={"Type":"Fight"}, charcount=1, target_count=1, required_test_list=[actor_and_target_shares_location, actor_is_alive, target_is_alive, actor_is_not_unconscious, target_is_not_unconscious, target_holds_rod_check], effects_on_next_ws=[target_becomes_unconscious, target_no_longer_holds_rod, actor_holds_rod])
actor_takes_rod_while_target_flees = StoryNode(name="Actor Takes Rod While Target Flees", tags={"Type":"Fight"}, charcount=1, target_count=1, required_test_list=[actor_is_alive, target_is_alive, actor_is_not_unconscious, target_is_not_unconscious, actor_and_target_shares_location, target_holds_rod_check], effects_on_next_ws=[actor_becomes_scared_of_target, target_no_longer_holds_rod, actor_holds_rod])

character_less_than_minus80_lawful_rewarded = InBiasRangeTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, bias_axis="moral", max_accept=-80, score=20)
character_more_than_minus80_lawful_punished = InBiasRangeTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, bias_axis="moral", min_accept=-80, score=-100)

kill_for_rod = StoryNode(name="Kill for Rod", tags={"Type":"Murder", "costly":True}, charcount=1, target_count=1, effects_on_next_ws=[target_becomes_dead, target_no_longer_holds_rod, actor_holds_rod], required_test_list=[actor_has_reason_to_kill_target, actor_has_killing_tool, actor_is_alive, target_is_alive, actor_is_not_unconscious, actor_and_target_shares_location, target_holds_rod_check])

# Take Rod if rod is on ground (you can also take from other people's houses)
actor_shares_location_with_rod = SameLocationTest(list_to_test=[GenericObjectNode.GENERIC_ACTOR, protection_pillar])
location_no_longer_holds_rod = RelChange(name="Location Stop Hold Rod", node_a=GenericObjectNode.GENERIC_LOCATION, edge_name="holds", node_b=protection_pillar, add_or_remove=ChangeAction.REMOVE)

take_rod = StoryNode(name="Take Rod", tags={"Type":"Find Treasure"}, charcount=1, target=[protection_pillar], required_test_list=[rod_is_not_active_check, actor_shares_location_with_rod], effects_on_next_ws=[actor_holds_rod, location_no_longer_holds_rod])

# Install Rod (If a house has a rod installed, other characters cannot destroy the house. Rod becomes active. It cannot be picked up in the active state.)
actor_holds_rod_check = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="holds", object_to_test=protection_pillar)
actor_stops_holding_rod = RelChange(name="Actor Stop Holds Rod", node_a=GenericObjectNode.GENERIC_TARGET, edge_name="holds", node_b=protection_pillar, add_or_remove=ChangeAction.REMOVE)
location_starts_holding_rod = RelChange(name="Location Holds Rod", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="holds", node_b=protection_pillar, add_or_remove=ChangeAction.ADD)
rod_becomes_active = TagChange(name="Rod is Activated", object_node_name=protection_pillar, tag="Activated", value=True, add_or_remove=ChangeAction.ADD)

install_rod = StoryNode(name="Install Rod", type={"Type":"Defense"}, charcount=1, required_test_list=[actor_is_alive, actor_is_not_unconscious, actor_holds_rod_check, actor_owns_home], effects_on_next_ws=[actor_stops_holding_rod, location_starts_holding_rod, rod_becomes_active])

# Tell Mom about Missing Grandma (Must have witnessed wolf in grandma's house)
# Gives Kill Reason towards Wolf, also gives CanKill to Red
actor_is_red = ObjectEqualityTest(object_list=[GenericObjectNode.GENERIC_ACTOR, red])
actor_seenwolf_change = TagChange(name="Seen the Wolf", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="SeenWolf", value=True, add_or_remove=ChangeAction.ADD)
actor_missingrandma_change = TagChange(name="Seen the Missing Grandma", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="SeenMissingGrandma", value=True, add_or_remove=ChangeAction.ADD)
target_is_actors_parent = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="child_of", object_to_test=GenericObjectNode.GENERIC_TARGET)

actor_knows_missing_grandma_check = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="SeenMissingGrandma", value=True)
actor_knows_wolf_check = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="SeenWolf", value=True)

actor_gains_killing_tool = TagChange(name="Gain Killing Tool", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="CanKill", value="Knife")
actor_gains_kill_reason_to_wolf_for_grandma_endanger = RelChange(name="Wolf Kill Reason for Grandma Endanger", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="KillReason", node_b=wolf)

#The plan was to have the Hunter go out to hunt the wolf, but since we turned the Hunter into no story, he cannot take quests. We need to do something about no Grandma here.
tell_mom_missing_grandma = StoryNode(name="Tell Mom Missing Grandma", tags={"Type":"Conversation"}, charcount=1, target_count=1, required_test_list=[actor_is_alive, target_is_alive, actor_is_not_unconscious, target_is_not_unconscious, actor_and_target_shares_location, target_is_actors_parent, actor_knows_missing_grandma_check], effects_on_next_ws=[actor_gains_killing_tool])

target_is_wolf = ObjectEqualityTest(object_list=[GenericObjectNode.GENERIC_TARGET, wolf])
witness_wolf = StoryNode(name="Witness Wolf", tags={"Type":"Witness"}, charcount=1, target_count=1, required_test_list=[actor_is_red, actor_is_alive, actor_is_not_unconscious, target_is_alive, target_is_not_unconscious, target_is_wolf], effects_on_next_ws=[actor_seenwolf_change])

location_is_grandma_home = ObjectEqualityTest(object_list=[GenericObjectNode.GENERIC_LOCATION, grandma_house])
location_not_hold_grandma = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_LOCATION, edge_name_test="holds", object_to_test=grandma, inverse=True)

notice_no_grandma = StoryNode(name="Notice Missing Grandma", tags={"Type":"Witness"}, charcount=1, required_test_list=[actor_is_red, actor_is_alive, actor_is_not_unconscious, location_is_grandma_home, location_not_hold_grandma], effects_on_next_ws=[actor_missingrandma_change])
tell_mom_wolf_exists = StoryNode(name="Tell Mom Wolf Real", tags={"Type":"Conversation"}, charcount=1, target_count=1, required_test_list=[actor_is_alive, target_is_alive, actor_is_not_unconscious, target_is_not_unconscious, actor_and_target_shares_location, target_is_actors_parent])

# Witness House Destruction
witness_home_destruction = StoryNode(name="Witnessing Home Destruction", tags={"Type":"Fight", "important_action":True}, charcount=1, target_count=1, required_test_list=[actor_is_alive, target_is_alive, actor_is_not_unconscious, target_is_not_unconscious, actor_and_target_shares_location, target_is_destroying_house_check], effects_on_next_ws=[killreason_homedestroyanger])

# Kidnap (carries another unconscious character, holding them instead of the location. Characters can only hold one character at a time)
actor_is_not_holding_a_character = HeldItemTagTest(holder_to_test=GenericObjectNode.GENERIC_ACTOR, tag_to_test="Type", value_to_test="Character", inverse=True)
actor_is_not_holding_a_nscharacter = HeldItemTagTest(holder_to_test=GenericObjectNode.GENERIC_ACTOR, tag_to_test="Type", value_to_test="NoStoryCharacter", inverse=True)

location_stops_holding_target = RelChange(name="Location Stops Holding Target", node_a=GenericObjectNode.GENERIC_LOCATION, edge_name="holds", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.REMOVE)
actor_starts_holding_target = RelChange(name="Actor Starts Holding Target", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="holds", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.ADD)

killreason_kidnapper = RelChange(name="Gain Kill Reason Kidnapper", node_a=GenericObjectNode.GENERIC_TARGET, edge_name="KillReason", node_b=GenericObjectNode.GENERIC_ACTOR, add_or_remove=ChangeAction.ADD, value="self_defense_kidnapper")

kidnap_target = StoryNode(name="Actor Kidnaps Target", tags={"Type":"Fight", "important_action":True}, charcount=1, target_count=1, required_test_list=[actor_is_alive, target_is_alive, actor_is_not_unconscious, target_is_unconscious, actor_and_target_shares_location, actor_is_not_holding_a_character, actor_is_not_holding_a_nscharacter])

# Drop Character (places down an unconscious character you are currently holding)

something_holds_character = HeldItemTagTest(holder_to_test=GenericObjectNode.GENERIC_ACTOR, tag_to_test="Type", value_to_test="Character", inverse=True)
something_holds_nscharacter = HeldItemTagTest(holder_to_test=GenericObjectNode.GENERIC_ACTOR, tag_to_test="Type", value_to_test="NoStoryCharacter", inverse=True)

actor_holds_target_check = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="holds", object_to_test=GenericObjectNode.GENERIC_TARGET)
location_starts_holding_target = RelChange(name="Location Starts Holding Target", node_a=GenericObjectNode.GENERIC_LOCATION, edge_name="holds", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.ADD)
actor_stops_holding_target = RelChange(name="Actor Stops Holding Target", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="holds", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.REMOVE)

drop_other_actor = StoryNode(name="Actor Drops Target", tags={"Type":"Fight"}, charcount=1, target_count=1, required_test_list=[actor_is_alive, target_is_alive, actor_is_not_unconscious, actor_holds_target_check])

# Pick Up Treasure (If the character LikesTreasure and shares location with a valuable item, they will pick it up)
character_likes_treasure_check = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="LikesTreasure", value=True)
target_is_a_treasure = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Valuable", value=True)

take_singing_harp = StoryNode(name="Take Harp", tags={"Type":"Collect"}, actor=[GenericObjectNode.TASK_OWNER], target=[singing_harp], required_test_list=[character_likes_treasure_check, target_is_a_treasure, actor_and_target_shares_location], effects_on_next_ws=[actor_starts_holding_target, location_stops_holding_target])
take_golden_goose = StoryNode(name="Take Goose", tags={"Type":"Collect"}, actor=[GenericObjectNode.TASK_OWNER], target=[golden_goose], required_test_list=[character_likes_treasure_check, target_is_a_treasure, actor_and_target_shares_location], effects_on_next_ws=[actor_starts_holding_target, location_stops_holding_target])

# Pick Up Knowledge Trinket (If the character LikesKnowledge and shares location with a KnowledgeObject, they will pick it up)
character_likes_knowledge_check = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="LikesKnowledge", value=True)
target_is_a_knowledge = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="KnowledgeObject", value=True)

#TODO: Make one for each knowledge object
take_knowledge_object = StoryNode(name="Take Knowledge Object", tags={"Type":"Collect"}, actor=[GenericObjectNode.TASK_OWNER], target=[columbo_diary], required_test_list=[character_likes_knowledge_check, target_is_a_knowledge, actor_and_target_shares_location], effects_on_next_ws=[actor_starts_holding_target, location_stops_holding_target])

# Gain Consciousness (Unconscious characters wakes up. They must not currently be carried.)
actor_becomes_conscious = TagChange(name="Actor Becomes Conscious", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="Unconscious", value=True, add_or_remove=ChangeAction.REMOVE)
gain_consciousness = StoryNode(name="Gain Consciousness", tags={"Type":"Awaken"}, charcount=1, required_test_list=[actor_is_unconscious], effects_on_next_ws=[actor_becomes_conscious])

# Rules
# Rule: Defeat -> Kill
defeat_into_kill = ContinuousJointRule(base_joint=defeat, joint_node=kill_another_actor, rule_name="Defeat Into Kill")

# Rule: Defeat -> Eat
defeat_into_eat = ContinuousJointRule(base_joint=defeat, joint_node=eat_and_kill, rule_name="Defeat Into Eat")

# Rule: Defeat -> Kidnap
defeat_into_kidnap = ContinuousJointRule(base_joint=defeat, joint_node=kidnap_target, rule_name="Defeat Into Kidnap")

# Rule: Scare -> Fear Scarer (more likely for children) / Defy Scarer (more likely for adults)
scare_into_fear = ContinuousJointRule(base_joint=scare, joint_node=actor_scared_of_target, rule_name="Scare Into Fear")
scare_into_defy = ContinuousJointRule(base_joint=scare, joint_node=actor_defies_target, rule_name="Scare Into Defy")

# Rule: (Patternless) -> Get task to find treasure / knowledge object

random_forest_not_holding_diary_check = HasEdgeTest(object_from_test=random_forest, edge_name_test="holds", object_to_test=columbo_diary, inverse=False)
find_diary_task = CharacterTask(task_name="Find Diary Task", task_actions=[take_knowledge_object], task_location_name="Random Forest", avoidance_state=[random_forest_not_holding_diary])

random_forest_has_diary 

find_diary_task_stack = TaskStack(stack_name="Find Diary Stack", task_stack=[find_diary_task], task_stack_requirement=)
get_find_diary_stack = TaskChange()

character_gains_diary_task_memory
character_doesnt_have_diary_task_memory_check
patternless_get_find_diary_task = RewriteRule()
patternless_get_find_goose_task = RewriteRule()
patternless_get_find_harp_task = RewriteRule()

# Rule: Witness Home Destruction -> Attack
witness_home_destruction_into_attack = ContinuousJointRule(base_joint=witness_home_destruction, joint_node=attack_home_intruder, rule_name="Witness Home Destruction Into Attack")

# Rule: Attack -> Attacker Defeated or Defender Defeated (No need to put this --- it will automatically pick a character to be defeated)
# Rule: Attack -> Defeat and Take Rod (if the Attacker didn't have rod, but the Defender does)
# Rule: (Patternless) -> Attack (This will happen automatically from ็ave Attack Reason)

# Generic Quests
# Find Rod Quest (We assume characters already know about the rod and will try to get there.)
# Steps: 
# Steal Rod (If Rod is found in someone else's house or on someone else's inventory, if rod is currently active need to deactivate rod to take it)
# Plant Rod (For the one holding an inactive rod: Installs the rod, if the rod is installed then it takes some effort to deactive or destroy)
#
# Failure condition: The rod is no longer in the Temple

# Find Singing Harp
# Steps:
# Grab the Singing Harp at the Random Forest
# 
# Failure condition: The singing harp is not held by the random forest and is not held by you

# Find Golden Goose
# Steps:
# Grab the Golden Goose at the Random Forest
#
# Failure condition: The golden goose is not held by the random forest and is not held by you

# Find Lost Diary
# Steps:
# Grab the Lost Diary at the Random Forest
#
# Failure condition: The lost diary is not held by the random forest and is not held by you

# Brick-Specific Quest
# Run from Wolf to Wood House ()
# Steps:
# Talk to Wood Pig
#
# Failure Condition: Wood Pig dies
# Clear Condition: Wolf dies

# Return Home (After completing the first quest)
# Steps:
# Go Home

# Fight Grandma (After being freed from wolf)
# Steps:
# (shit how do we fight grandma, we don't even have a specific location for grandma)
# This should be a rule instead of a quest
# (Patternless) -> Attack (Condition is that he is in the same location as someone he hates (because of home destruction))

# Red-Specific Quest
# Visit Grandma (First Actual Quest)
# Steps:
# Go to Grandma House
# (might meet wolf on the way)

# Tell Mom about Wolf (Second Quest, gain after witnessing Wolf, First witnessing the wolf gives her a kill reason)
# Steps:
# Go talk to Mom at Red House

get_visit_grandma_task = StoryNode()
realize_wolf_exists_therefore_gain_tell_mom_about_wolf_task = StoryNode()
realize_grandma_not_home_therefore_gain_tell_mom_about_missing_grandma_task = StoryNode()

# Wolf-Specific Quest
# TBH since we don't know these characters' locations they should be rules. Like if Wolf share a location with these guys he will try to scare them
# Threaten Witch
# Steps:

# Threaten Brick
# Steps: 

# Threaten Bears
# Steps:

# And when he is done scaring them he will return to tell Grandma that he is done. For each character he scared he gets a token. There will be a jointless rule that says the wolf can report scaring all the people
# Report All Residents Scared

# Scheme Together (Characters must both have negative moral bias.)
#TODO: This gives quests to Wolf to try to scare people out of the forest. This could be the starting node for the wolf.
scheme_leader_gives_task = StoryNode(name="Scheme Leader Gives Tasks", tags={"Type":"GiveTask"}, charcount=1, target_count=1)


# All three will lead to the target to become defiant, and Wolf can attack them. This might lead to:
# - The target dying
# - The target being eaten (if the target is a child, because the wolf only eats children)
# - The target running away
# - The wolf running away
# - The wolf dying
#
# Report Empty Village (Can be done once Witch, Papa Bear, and Brick are not in village)

# Grandma-Specific Quest
# Destroy Homes (Once Grandma learns that the village is empty from wolf, she will start destroying houses. She will get quests to do so.)

# Initial StoryGraph for the Characters
# Red: Get task to go see Grandma
# Brick, Bear, Witch: Get task where each of them learn about the magic pillar
# Hunter: Wait
# Wolf: Get task to kick the bears, the pig, and the witch out from home

# TODO: Chases and runnning-aways aren't properly defined yet. What do we do with those?