from datetime import datetime
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

from application.StoryGeneration_NewFlowchart_WithMetrics import generate_multiple_graphs, generate_story_from_starter_graph, make_base_graph_from_previous_graph
import os

#Oh holy shit there are many characters. The generation will take *forever*.
#Maybe some of these characters should be treated as Objects instead??? Like characters with no storyline of their own???
#But some of these characters do need to take actions sometimes...

#Only the characters who can act will be classified as characters, The rest will become Object Nodes with Type "NoStoryCharacter"
red = CharacterNode(name="Red", tags={"Type":"Character", "Age":"Child", "Alive":True}, internal_id=0)
wolf = CharacterNode(name="Wolf", biases={"moralbias":-50, "lawbias":-50}, tags={"Type":"Character", "Age":"Adult", "EatsChildren":True, "EatsNonChildren":True, "Alive":True, "CanKill":"Fangs"}, internal_id=1)
brick_pig = CharacterNode(name="Brick", biases={"moralbias":50, "lawbias":50}, tags={"Type":"Character", "Age":"Adult", "Pacifist":True, "Alive":True, "LikesTreasure":True, "OwnsForestHome":True}, internal_id=2)
grandma = CharacterNode(name="Grandma", biases={"moralbias":-50, "lawbias":0}, tags={"Type":"Character", "Age":"Adult", "Alive":True, "LikesKnowledge":True, "CanKill":"Knife"}, internal_id=3)

mom = ObjectNode(name="Red's Mom", tags={"Type":"NoStoryCharacter", "Age":"Adult", "Alive":True}, internal_id=5)

papabear = CharacterNode(name="Papa Bear", tags={"Type":"Character", "Age":"Adult", "Alive":True, "CanKill":"Claws", "OwnsForestHome":True}, internal_id=8)
witch = CharacterNode(name="Witch", biases={"moralbias":-50, "lawbias":0}, tags={"Type":"Character", "Age":"Adult", "Alive":True, "EatsChildren":True, "LikesKnowledge":True, "CanKill":"Magic", "OwnsForestHome":True}, internal_id=11)

protection_pillar = ObjectNode(name="Protection Pillar", tags={"Type":"Object", "ProtectsHomes":True, "Active":False}, internal_id=12)
columbo_diary = ObjectNode(name="Columbo's Diary", tags={"Type":"Object", "KnowledgeObject":True}, internal_id=13)
golden_goose = ObjectNode(name="Golden Goose", tags={"Type":"Object", "Valuable":True}, internal_id=14)
singing_harp = ObjectNode(name="Singing Harp", tags={"Type":"Object", "Valuable":True}, internal_id=15)

forest_village = LocationNode(name="Forest Village", tags={"Type":"Location"}, internal_id=15)
random_forest = LocationNode(name="Random Forest", tags={"Type":"Location", "PigHomeStanding":True, "BearHomeStanding":True, "WitchHomeStanding":True}, internal_id=20)
forest_path = LocationNode(name="Forest Path", tags={"Type":"Location"}, internal_id=21)
plains_village = LocationNode(name="Plains Village", tags={"Type":"Location"}, internal_id=22)
mountain_valley = LocationNode(name="Mountain Valley", tags={"Type":"Location"}, internal_id=24)
magic_temple = LocationNode(name="Magic Temple", tags={"Type":"Location"}, internal_id=26)

list_of_objects = [red, wolf, brick_pig, grandma, mom, papabear, witch, protection_pillar, columbo_diary, golden_goose, singing_harp, forest_village, random_forest, forest_path, plains_village, mountain_valley, magic_temple]

reds_world_state = WorldState(name="Reds World State", objectnodes=list_of_objects)

reds_world_state.doubleconnect(from_node=forest_village, edge_name="connects", to_node=forest_path)
reds_world_state.doubleconnect(from_node=random_forest, edge_name="connects", to_node=forest_path)
reds_world_state.doubleconnect(from_node=plains_village, edge_name="connects", to_node=forest_path)
reds_world_state.doubleconnect(from_node=mountain_valley, edge_name="connects", to_node=forest_path)
reds_world_state.doubleconnect(from_node=mountain_valley, edge_name="connects", to_node=magic_temple)

reds_world_state.connect(from_node=mom, edge_name="parent_of", to_node=red)
reds_world_state.connect(from_node=red, edge_name="child_of", to_node=mom)
reds_world_state.connect(from_node=grandma, edge_name="parent_of", to_node=mom)
reds_world_state.connect(from_node=mom, edge_name="child_of", to_node=grandma)

reds_world_state.connect(from_node=plains_village, edge_name="holds", to_node=mom)
reds_world_state.connect(from_node=plains_village, edge_name="holds", to_node=red)
reds_world_state.connect(from_node=forest_village, edge_name="holds", to_node=grandma)
reds_world_state.connect(from_node=forest_village, edge_name="holds", to_node=papabear)
reds_world_state.connect(from_node=forest_village, edge_name="holds", to_node=witch)
reds_world_state.connect(from_node=forest_village, edge_name="holds", to_node=brick_pig)
reds_world_state.connect(from_node=forest_village, edge_name="holds", to_node=wolf)

reds_world_state.connect(from_node=magic_temple, edge_name="holds", to_node=protection_pillar)
reds_world_state.connect(from_node=random_forest, edge_name="holds", to_node=columbo_diary)
reds_world_state.connect(from_node=random_forest, edge_name="holds", to_node=singing_harp)
reds_world_state.connect(from_node=random_forest, edge_name="holds", to_node=golden_goose)

reds_world_state.connect(from_node=wolf, edge_name="has_attack_reason", to_node=red, value="eating_children")
reds_world_state.connect(from_node=wolf, edge_name="has_attack_reason", to_node=brick_pig, value="eating_children")
reds_world_state.connect(from_node=witch, edge_name="has_attack_reason", to_node=red, value="eating_children")
reds_world_state.connect(from_node=witch, edge_name="has_attack_reason", to_node=brick_pig, value="eating_children")

# Actions
# Eat (It's a messy action.)

actor_is_alive = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Alive", value=True)
all_actors_alive = HasTagTest(object_to_test=GenericObjectNode.ALL_ACTORS, tag="Alive", value=True)

target_is_alive = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Alive", value=True)

actor_is_not_unconscious =HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Unconscious", value=True, inverse=True)
all_actors_not_unconscious =HasTagTest(object_to_test=GenericObjectNode.ALL_ACTORS, tag="Unconscious", value=True, inverse=True)

actor_is_unconscious =HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="Unconscious", value=True)
target_is_not_unconscious = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Unconscious", value=True, inverse=True)
target_is_unconscious = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Unconscious", value=True)
actor_and_target_shares_location = SameLocationTest(list_to_test=[GenericObjectNode.GENERIC_ACTOR, GenericObjectNode.GENERIC_TARGET])

actor_eats_children = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="EatsChildren", value=True)
target_is_child = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Age", value="Child")

target_becomes_dead = TagChange(name="Target Becomes Dead", object_node_name=GenericObjectNode.GENERIC_TARGET, tag="Alive", value=False, add_or_remove=ChangeAction.ADD)
target_leaves_no_corpse = TagChange(name="Target Leaves No Body", object_node_name=GenericObjectNode.GENERIC_TARGET, tag="NoCorpse", value=True, add_or_remove=ChangeAction.ADD)

actor_has_defeatinteraction_target_twoway = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="DefeatInteractionOccured", object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True, two_way=True)
actor_loses_defeatinteraction_target_twoway = RelChange(name="Actor Loses Twoway DefeatInteraction", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="DefeatInteractionOccured", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.REMOVE, soft_equal=True, two_way=True)

eat_and_kill = StoryNode(name="Eat and Kill", tags={"Type":"Murder", "costly":True}, charcount=1, target_count=1, effects_on_next_ws=[target_becomes_dead, target_leaves_no_corpse, actor_loses_defeatinteraction_target_twoway], required_test_list=[actor_is_alive, actor_is_not_unconscious, target_is_alive, actor_eats_children, target_is_child, actor_and_target_shares_location, actor_has_defeatinteraction_target_twoway])

# Kill (Needs to carry weapon, wolf's weapon is his claws)
actor_has_reason_to_kill_target = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="KillReason", object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True, score=50)
actor_has_killing_tool = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="CanKill", value=None, soft_equal=True, score=50)

kill_another_actor = StoryNode(name="Actor Kills Actor", tags={"Type":"Murder", "costly":True}, charcount=1, target_count=1, effects_on_next_ws=[target_becomes_dead, actor_loses_defeatinteraction_target_twoway], required_test_list=[actor_is_alive, target_is_alive, actor_is_not_unconscious, actor_and_target_shares_location, actor_has_defeatinteraction_target_twoway], suggested_test_list=[actor_has_killing_tool, actor_has_reason_to_kill_target])

# Scare (Makes a character leave home, works on children and adults, has a chance to cause adults to fight back instead (This is a Rule))

actor_has_reason_to_scare_target = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="ScareReason", object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True)

#Hey, maybe we should make becoming scared to be a thing on its own? A rule? Just a suggestion

actor_has_not_scared_target_check = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="HasScared", object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True, inverse=True)
actor_has_scared_target_change = RelChange(name="Actor has scared Target", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="HasScared", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.ADD)

scare_action = StoryNode(name="Actor Scares Target", tags={"Type":"Threaten"}, charcount=1, target_count=1, biasweight=200, required_test_list=[actor_has_reason_to_scare_target, actor_is_alive, actor_is_not_unconscious, target_is_not_unconscious, target_is_alive, actor_and_target_shares_location, actor_has_not_scared_target_check], effects_on_next_ws=[actor_has_scared_target_change])

# Defeat (A defeated character becomes unconscious)
# Unconscious characters cannot act, but they can wake up after a while. (With Patternless Rule)

target_becomes_unconscious = TagChange(name="Target Becomes Unconscious", object_node_name=GenericObjectNode.GENERIC_TARGET, tag="Unconscious", value=True, add_or_remove=ChangeAction.ADD)

actor_gain_defeatinteraction_target_twoway = RelChange(name="Actor Gains DefeatInteraction TwoWay", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="DefeatInteractionOccured", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.ADD, two_way=True)
actor_loses_attackinteraction_target_twoway = RelChange(name="Remove TwoWay AttackInteraction", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="AttackInteractionOccured", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.REMOVE, soft_equal=True, two_way=True)

actor_has_attackinteraction_target_check = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="AttackInteractionOccured", object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True, two_way=True)
actor_has_no_defeatinteraction_target_twoway = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="DefeatInteractionOccured", object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True, two_way=True, inverse=True)

defeat_action = StoryNode(name="Defeat", tags={"Type":"Fight"}, charcount=1, target_count=1, required_test_list=[actor_and_target_shares_location, actor_is_alive, target_is_alive, actor_is_not_unconscious, target_is_not_unconscious, actor_has_no_defeatinteraction_target_twoway, actor_has_attackinteraction_target_check], effects_on_next_ws=[target_becomes_unconscious, actor_gain_defeatinteraction_target_twoway, actor_loses_attackinteraction_target_twoway])

# Threaten (Can cause the target to either become scared or become defiant, either way this forms a new relationship between target and actor)
# Become Scared

target_has_scared_actor_check = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_TARGET, edge_name_test="HasScared", object_to_test=GenericObjectNode.GENERIC_ACTOR, soft_equal=True)
actor_becomes_scared_of_target = RelChange(name="Actor Fears Target", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="fears", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.ADD, value="Threatened")

actor_is_child = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Age", value="Child", score=10)
actor_is_not_child_gives_bad_score = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="Age", value="Child", inverse=True, score=-10)

actor_not_fear_target_check = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="fears", object_to_test=GenericObjectNode.GENERIC_TARGET, inverse=True, soft_equal=True)
actor_not_defy_target_check = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="defies", object_to_test=GenericObjectNode.GENERIC_TARGET, inverse=True, soft_equal=True)

actor_nothave_scare_resist = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="FearResist", object_to_test=GenericObjectNode.GENERIC_TARGET, inverse=True)
actor_scared_of_target = StoryNode(name="Actor becomes scared of Target", tags={"Type":"Fight"}, charcount=1, target_count=1, effects_on_next_ws=[actor_becomes_scared_of_target], suggested_test_list=[actor_is_child, actor_is_not_child_gives_bad_score], required_test_list=[actor_and_target_shares_location, actor_is_alive, target_is_alive, actor_is_not_unconscious, target_is_not_unconscious, actor_nothave_scare_resist, actor_not_fear_target_check, actor_not_defy_target_check, target_has_scared_actor_check])

# Become Defiant
actor_becomes_defiant_of_target = RelChange(name="Actor Defies Target", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="defies", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.ADD, value="Threatened")
actor_gain_attack_reason_defiant = RelChange(name="Actor Gains Attack Reason Defiant", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="has_attack_reason", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.ADD, value="defiant")
actor_defies_target = StoryNode(name="Actor becomes defiant of Target", tags={"Type":"Fight", "important_action":True}, charcount=1, target_count=1, effects_on_next_ws=[actor_becomes_defiant_of_target, actor_gain_attack_reason_defiant], required_test_list=[actor_is_alive, target_is_alive, actor_is_not_unconscious, target_is_not_unconscious, actor_and_target_shares_location, actor_not_fear_target_check, actor_not_defy_target_check, target_has_scared_actor_check])

# Attack (Can lead to a fight, killing, or can lead to the target escaping from the attacker)
# Someone would attack target if they have a reason to kill the other person, or if they are evil
actor_has_reason_to_attack_target_check = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="has_attack_reason", object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True)
actor_has_no_attack_interaction_target_twoway = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="AttackInteractionOccured", object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True, two_way=True, inverse=True)
actor_gains_attack_interaction_target_twoway = RelChange(name="Gain Twoway AttackInteraction", node_a=GenericObjectNode.GENERIC_ACTOR, node_b=GenericObjectNode.GENERIC_TARGET, edge_name="AttackInteractionOccured", add_or_remove=ChangeAction.ADD, two_way=True)
actor_has_less_than_minus_50_moralbias = InBiasRangeTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, bias_axis="moralbias", max_accept=-50, score=50)

actor_attacks_target = StoryNode(name="Actor Attacks Target", tags={"Type":"Fight"}, charcount=1, target_count=1, required_test_list=[actor_has_no_attack_interaction_target_twoway, actor_is_alive, target_is_alive, actor_is_not_unconscious, target_is_not_unconscious, actor_and_target_shares_location, actor_has_reason_to_attack_target_check], suggested_test_list=[actor_has_reason_to_kill_target, actor_has_killing_tool, actor_has_less_than_minus_50_moralbias], effects_on_next_ws=[actor_gains_attack_interaction_target_twoway])

# Escape from Attacker (This makes them scared of attacker, and thus more likely to run away)
# actor_escapes_from_attacking_target = StoryNode(name="Actor Flees Target", tags={"Type":"Fight"}, charcount=1, target_count=1, required_test_list=[actor_is_alive, target_is_alive, actor_is_not_unconscious, target_is_not_unconscious, actor_and_target_shares_location, actor_not_fear_target_check], effects_on_next_ws=[actor_becomes_scared_of_target])

actor_fears_wolf_check = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="fears", object_to_test=wolf)
# Destroy House (Owner must not be home. There must not be an active rod. This adds Home Destruction Tag to the actor. The tag goes away when the action is complete.)

actor_shares_location_with_someone = SameLocationTest(list_to_test=[GenericObjectNode.GENERIC_ACTOR, GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER])
actor_is_destroying_home_change = TagChange(name="Actor is Destroying Home", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="DestroyingHome", value=True, add_or_remove=ChangeAction.ADD)
actor_not_destroying_home_change = TagChange(name="Actor stops Destroying Home", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="DestroyingHome", value=True, add_or_remove=ChangeAction.REMOVE)
target_is_destroying_house_check = HasTagTest(object_to_test=GenericObjectNode.GENERIC_TARGET, tag="DestroyingHome", value=True)

# Attack Intruder (If sharing location with home destruction tag character)
actor_gain_attack_reason_homedestroy = RelChange(name="Actor Gains Attack Reason Defiant", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="has_attack_reason", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.ADD, value="anger_destroyhome")
killreason_homedestroyanger = RelChange(name="Gain Kill Reason HomeDestroy", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="KillReason", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.ADD, value="anger_destroyhome")
# attack_home_intruder = StoryNode(name="Attack Home Intruder", tags={"Type":"Fight", "important_action":True}, charcount=1, target_count=1, required_test_list=[actor_is_alive, target_is_alive, actor_is_not_unconscious, target_is_not_unconscious, actor_and_target_shares_location, target_is_destroying_house_check], effects_on_next_ws=[killreason_homedestroyanger])

# Rebuild House (House must have been destroyed)

def make_rebuild_home (homeowner_object, home_tag):
    homeowner_is_actor = ObjectEqualityTest(object_list=[GenericObjectNode.GENERIC_ACTOR, homeowner_object])
    house_is_destroyed_check = HasTagTest(object_to_test=GenericObjectNode.GENERIC_LOCATION, tag=home_tag, value=False)
    home_is_rebuilt_change = TagChange(name="Home is Rebuilt", object_node_name=GenericObjectNode.GENERIC_LOCATION, tag=home_tag, value=True, add_or_remove=ChangeAction.ADD)
    
    node_name = "Rebuild House (" + home_tag + ")"
    rebuild_house = StoryNode(name=node_name, tags={"Type":"Rebuilding"}, required_test_list=[actor_is_alive, actor_is_not_unconscious, homeowner_is_actor, house_is_destroyed_check], effects_on_next_ws=[home_is_rebuilt_change])

    return rebuild_house

pig_rebuild_home = make_rebuild_home(homeowner_object=brick_pig, home_tag="PigHomeStanding")
bear_rebuild_home = make_rebuild_home(homeowner_object=papabear, home_tag="BearHomeStanding")
witch_rebuild_home = make_rebuild_home(homeowner_object=witch, home_tag="WitchHomeStanding")

# Fight for Rod (if sharing location with someone else carrying rod and not scared of target, must be morally questionible)
# character_less_than_50_lawful_rewarded = InBiasRangeTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, bias_axis="moral", max_accept=-50, score=20)
target_holds_rod_check = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_TARGET, edge_name_test="holds", object_to_test=protection_pillar)

# fight_for_rod = StoryNode(name="Fight for Rod", tags={"Type":"Fight"}, charcount=1, target_count=1, required_test_list=[target_holds_rod_check, actor_is_alive, target_is_alive, actor_is_not_unconscious, target_is_not_unconscious], suggested_test_list=[character_less_than_50_lawful_rewarded])

# all_actors_hold_rod = HasEdgeTest(object_from_test=GenericObjectNode.ALL_ACTORS, edge_name_test="holds", object_to_test=protection_pillar)
# brawl_for_rod = StoryNode(name="Brawl for Rod", tags={"Type":"Fight"}, biasweight=100, charcount=-1, required_test_list=[all_actors_hold_rod, all_actors_alive, all_actors_not_unconscious])

# Defeat for Rod (follows up Fight for Rod if the character holding rod loses, follow up with normal defeat if character holding rod wins)
target_no_longer_holds_rod = RelChange(name="Target Stop Hold Rod", node_a=GenericObjectNode.GENERIC_TARGET, edge_name="holds", node_b=protection_pillar, soft_equal=True, add_or_remove=ChangeAction.REMOVE)
actor_holds_rod = RelChange(name="Actor Hold Rod", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="holds", node_b=protection_pillar, add_or_remove=ChangeAction.ADD)

actor_owns_forest_home = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="OwnsForestHome", value=True)
defeat_and_take_rod_target_unconscious = StoryNode(name="Defeat and Steal Rod", tags={"Type":"Fight"}, biasweight=100, charcount=1, target_count=-1, required_test_list=[actor_and_target_shares_location, actor_is_alive, target_is_alive, actor_is_not_unconscious, target_is_not_unconscious, target_holds_rod_check, actor_has_no_defeatinteraction_target_twoway,  actor_has_attackinteraction_target_check, actor_owns_forest_home], effects_on_next_ws=[target_becomes_unconscious, target_no_longer_holds_rod, actor_holds_rod, actor_loses_attackinteraction_target_twoway])
# actor_takes_rod_while_target_flees = StoryNode(name="Actor Takes Rod While Target Flees", tags={"Type":"Fight"}, charcount=1, target_count=1, required_test_list=[actor_is_alive, target_is_alive, actor_is_not_unconscious, target_is_not_unconscious, actor_and_target_shares_location, target_holds_rod_check], effects_on_next_ws=[actor_becomes_scared_of_target, target_no_longer_holds_rod, actor_holds_rod])

character_less_than_minus80_lawful_rewarded = InBiasRangeTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, bias_axis="moral", max_accept=-80, score=20)
character_more_than_minus80_lawful_punished = InBiasRangeTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, bias_axis="moral", min_accept=-80, score=-100)

kill_for_rod = StoryNode(name="Kill for Rod", tags={"Type":"Murder", "costly":True}, charcount=1, target_count=1, effects_on_next_ws=[target_becomes_dead, target_no_longer_holds_rod, actor_holds_rod, actor_loses_defeatinteraction_target_twoway, actor_owns_forest_home], required_test_list=[actor_is_alive, target_is_alive, actor_is_not_unconscious, actor_and_target_shares_location, target_holds_rod_check, actor_has_defeatinteraction_target_twoway], suggested_test_list=[actor_has_reason_to_kill_target, actor_has_killing_tool])

# Take Rod if rod is on ground (you can also take from other people's houses)
actor_shares_location_with_rod = SameLocationTest(list_to_test=[GenericObjectNode.GENERIC_ACTOR, protection_pillar])
location_no_longer_holds_rod = RelChange(name="Location Stop Hold Rod", node_a=GenericObjectNode.GENERIC_LOCATION, edge_name="holds", node_b=protection_pillar, soft_equal=True, add_or_remove=ChangeAction.REMOVE)

take_rod_from_location = StoryNode(name="Take Rod", tags={"Type":"Find Rod"}, charcount=1, actor=[GenericObjectNode.TASK_OWNER], location = magic_temple, target=[protection_pillar], required_test_list=[actor_is_alive, actor_is_not_unconscious, actor_shares_location_with_rod], effects_on_next_ws=[actor_holds_rod, location_no_longer_holds_rod])

# Tell Mom about Missing Grandma (Must have witnessed wolf in grandma's house)
# Gives Kill Reason towards Wolf, also gives CanKill to Red
actor_is_red = ObjectEqualityTest(object_list=[GenericObjectNode.GENERIC_ACTOR, red])
actor_seenwolf_change = TagChange(name="Seen the Wolf", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="SeenWolf", value=True, add_or_remove=ChangeAction.ADD)
actor_missingrandma_change = TagChange(name="Seen the Missing Grandma", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="SeenMissingGrandma", value=True, add_or_remove=ChangeAction.ADD)
target_is_actors_parent = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="child_of", object_to_test=GenericObjectNode.GENERIC_TARGET)

actor_not_know_missing_grandma_check = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="SeenMissingGrandma", value=True, inverse=True)
actor_knows_missing_grandma_check = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="SeenMissingGrandma", value=True)
actor_not_know_wolf_check = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="SeenWolf", value=True, inverse=True)
actor_knows_wolf_check = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="SeenWolf", value=True)

actor_gains_killing_tool = TagChange(name="Gain Killing Tool", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="CanKill", value="Knife", add_or_remove=ChangeAction.ADD)
actor_gains_kill_reason_to_wolf_for_grandma_endanger = RelChange(name="Wolf Kill Reason for Grandma Endanger", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="KillReason", value="GrandmaEndanger", node_b=wolf, add_or_remove=ChangeAction.ADD)

# This node should convince the Bear (who is now a normal character) to start hunting the wolf.
bear_gets_wolf_attack_reason = RelChange(name="Bear Has Kill Reason to attack Wolf", node_a=papabear, edge_name="has_attack_reason", node_b=wolf, add_or_remove=ChangeAction.ADD, value="kill_order")
bear_gets_kill_command = RelChange(name="Bear Has Kill Reason to Wolf", node_a=papabear, edge_name="KillReason", node_b=wolf, add_or_remove=ChangeAction.ADD, value="kill_order")

target_is_wolf = ObjectEqualityTest(object_list=[GenericObjectNode.GENERIC_TARGET, wolf])
witness_wolf = StoryNode(name="Witness Wolf", tags={"Type":"Witness"}, charcount=1, target_count=1, required_test_list=[actor_is_red, actor_is_alive, actor_is_not_unconscious, target_is_alive, target_is_not_unconscious, target_is_wolf, actor_not_know_wolf_check, actor_and_target_shares_location], effects_on_next_ws=[actor_seenwolf_change])

location_is_grandma_home = ObjectEqualityTest(object_list=[GenericObjectNode.GENERIC_LOCATION, forest_village])
location_not_hold_grandma = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_LOCATION, edge_name_test="holds", object_to_test=grandma, inverse=True)

notice_no_grandma = StoryNode(name="Notice Missing Grandma", tags={"Type":"Witness"}, charcount=1, required_test_list=[actor_is_red, actor_is_alive, actor_is_not_unconscious, location_is_grandma_home, location_not_hold_grandma, actor_knows_wolf_check, actor_not_know_missing_grandma_check], effects_on_next_ws=[actor_missingrandma_change])

# Witness House Destruction
actor_is_destroying_home_check = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="DestroyingHome", value=True)
witness_home_destruction = StoryNode(name="Witnessing Home Destruction", tags={"Type":"Fight", "important_action":True}, charcount=1, target_count=1, required_test_list=[actor_is_alive, target_is_alive, actor_is_not_unconscious, target_is_not_unconscious, actor_and_target_shares_location, actor_is_destroying_home_check], effects_on_next_ws=[killreason_homedestroyanger, actor_gain_attack_reason_homedestroy, actor_not_destroying_home_change])

# Kidnap (carries another unconscious character, holding them instead of the location. Characters can only hold one character at a time)

something_is_a_character = HasTagTest(object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, tag="Type", value="Character")
actor_grabs_something = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="grabs", object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, soft_equal=True)
actor_not_grab_character_test = SomethingPassesAllGivenTestsTest(list_of_tests_with_placeholder=[something_is_a_character, actor_grabs_something], inverse=True)

location_stops_holding_target = RelChange(name="Location Stops Holding Target", node_a=GenericObjectNode.GENERIC_LOCATION, edge_name="holds", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.REMOVE)
actor_starts_holding_target = RelChange(name="Actor Starts Holding Target", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="holds", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.ADD)
actor_starts_grabbing_target = RelChange(name="Actor Starts Holding Target", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="grabs", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.ADD)

gain_killreason_kidnapper = RelChange(name="Gain Kill Reason Kidnapper", node_a=GenericObjectNode.GENERIC_TARGET, edge_name="KillReason", node_b=GenericObjectNode.GENERIC_ACTOR, add_or_remove=ChangeAction.ADD, value="self_defense_kidnapper")

kidnap_target = StoryNode(name="Actor Kidnaps Target", tags={"Type":"Fight", "important_action":True}, charcount=1, target_count=1, required_test_list=[actor_is_alive, target_is_alive, actor_is_not_unconscious, target_is_unconscious, actor_and_target_shares_location, actor_not_grab_character_test, actor_has_defeatinteraction_target_twoway], effects_on_next_ws=[actor_starts_grabbing_target, actor_loses_defeatinteraction_target_twoway])

# Drop Character (places down an unconscious character you are currently holding)

actor_grab_character_test = SomethingPassesAllGivenTestsTest(list_of_tests_with_placeholder=[something_is_a_character, actor_grabs_something])

actor_grabs_target_check = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="grabs", object_to_test=GenericObjectNode.GENERIC_TARGET)
location_starts_holding_target = RelChange(name="Location Starts Holding Target", node_a=GenericObjectNode.GENERIC_LOCATION, edge_name="holds", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.ADD)
actor_stops_grabbing_target = RelChange(name="Actor Stops Grabbing Target", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="holds", node_b=GenericObjectNode.GENERIC_TARGET, add_or_remove=ChangeAction.REMOVE)

drop_other_actor = StoryNode(name="Actor Drops Target", tags={"Type":"Fight"}, charcount=1, target_count=1, required_test_list=[actor_is_alive, actor_is_not_unconscious, actor_grabs_target_check], effects_on_next_ws=[actor_stops_grabbing_target])

# Gain Consciousness (Unconscious characters wakes up. They must not currently be carried.)
actor_becomes_conscious = TagChange(name="Actor Becomes Conscious", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="Unconscious", value=True, add_or_remove=ChangeAction.REMOVE)
gain_consciousness = StoryNode(name="Gain Consciousness", tags={"Type":"Awaken"}, charcount=1, required_test_list=[actor_is_unconscious, actor_is_alive], effects_on_next_ws=[actor_becomes_conscious])

# Forgive (Removes memory of defeat interaction between two characters, so that the actor does not have to kill the target)
actor_has_pos_moral_bias_rewarded = InBiasRangeTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, bias_axis="moralbias", min_accept=0, score=50)
actor_has_no_reason_to_kill_target = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="KillReason", object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True, inverse=True)

forgive_action = StoryNode(name="Forgiveness", tags={"Type":"Fight", "important_action":True}, charcount=1, target_count=1, required_test_list=[actor_is_alive, actor_is_not_unconscious, target_is_alive, target_is_unconscious, actor_has_defeatinteraction_target_twoway, actor_has_no_reason_to_kill_target], effects_on_next_ws=[actor_loses_defeatinteraction_target_twoway], suggested_test_list=[actor_has_pos_moral_bias_rewarded])

# Rules
list_of_rules = []

# Rule: Defeat -> Kill
# defeat_into_kill = ContinuousJointRule(base_joint=defeat_action, joint_node=kill_another_actor, rule_name="Defeat Into Kill")
patternless_into_kill = JoiningJointRule(base_actions=[], joint_node=kill_another_actor, rule_name="Patternless into Kill")
list_of_rules.append(patternless_into_kill)

# Rule: Defeat -> Kill for Rod
# defeat_into_kill_rod = ContinuousJointRule(base_joint=defeat_action, joint_node=kill_for_rod, rule_name="Defeat into Kill For Rod")
patternless_into_killrod = JoiningJointRule(base_actions=[], joint_node=kill_for_rod, rule_name="Patternless into Kill for Rod")
list_of_rules.append(patternless_into_killrod)

# Rule: Defeat -> Eat
# defeat_into_eat = ContinuousJointRule(base_joint=defeat_action, joint_node=eat_and_kill, rule_name="Defeat Into Eat")
patternless_into_eat = JoiningJointRule(base_actions=[], joint_node=eat_and_kill, rule_name="Patternless into Eat and Kill")
list_of_rules.append(patternless_into_eat)

# Rule: Defeat -> Kidnap
# defeat_into_kidnap = ContinuousJointRule(base_joint=defeat_action, joint_node=kidnap_target, rule_name="Defeat Into Kidnap")
patternless_into_kidnap = JoiningJointRule(base_actions=[], joint_node=kidnap_target, rule_name="Patternless into Kidnap")
list_of_rules.append(patternless_into_kidnap)

# Rule: (Patternless) -> Scare
patternless_into_scare = JoiningJointRule(base_actions=None, joint_node=scare_action, rule_name="Patternless into Scare")
list_of_rules.append(patternless_into_scare)

# # Rule: Scare -> Fear Scarer (more likely for children) / Defy Scarer (more likely for adults)
# scare_into_fear = ContinuousJointRule(base_joint=scare, joint_node=actor_scared_of_target, rule_name="Scare Into Fear")
# scare_into_defy = ContinuousJointRule(base_joint=scare, joint_node=actor_defies_target, rule_name="Scare Into Defy")
# list_of_rules.append(scare_into_fear)
# list_of_rules.append(scare_into_defy)
patternless_into_fear = JoiningJointRule(base_actions=[], joint_node=actor_scared_of_target, rule_name="Patternless Into Fear")
patternless_into_defy = JoiningJointRule(base_actions=[], joint_node=actor_defies_target, rule_name="Patternless Into Defy")
list_of_rules.append(patternless_into_fear)
list_of_rules.append(patternless_into_defy)

# Rule: (Patternless) -> Stop Fearing (Only possible when not sharing location with someone target fears)
actor_fears_someone = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="fears", object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER)
actor_not_share_location_with_someone = SameLocationTest(list_to_test=[GenericObjectNode.GENERIC_ACTOR, GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER], inverse=True)

actor_stops_fearing_someone = RelChange(name="Stop Fear!", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="fears", node_b=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, add_or_remove=ChangeAction.REMOVE, soft_equal=True)
actor_resists_fear = RelChange(name="Resist Fear!", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="FearResist", node_b=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, add_or_remove=ChangeAction.ADD)
actor_gain_attack_reason_selfdefense = RelChange(name="Actor Gains Attack Reason SD", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="has_attack_reason", node_b=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, add_or_remove=ChangeAction.ADD, value="self_defense")

actor_stops_fearing_all_feared_characters = ConditionalChange(name="Actor Stops Fearing If Feared", list_of_condition_tests=[actor_fears_someone, actor_not_share_location_with_someone], list_of_changes=[actor_stops_fearing_someone, actor_resists_fear, actor_gain_attack_reason_selfdefense])

actor_not_share_location_with_feared_character = SomethingPassesAllGivenTestsTest(list_of_tests_with_placeholder=[actor_fears_someone, actor_shares_location_with_someone], inverse=True)

stop_fear = StoryNode(name="Stop Fearing Everything", effects_on_next_ws=[actor_stops_fearing_all_feared_characters], required_test_list=[actor_not_share_location_with_feared_character])

patternless_into_stop_fear = RewriteRule(story_condition=[], story_change=[stop_fear], name="Patternless into Stop Fear")
list_of_rules.append(patternless_into_stop_fear)

# Rule: (Patternless) -> Get task to find treasure / knowledge object
def make_find_item_rule(item_to_find, item_liking_tag, location_holding_item):
    
    current_location_has_item_check = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_LOCATION, edge_name_test="holds", object_to_test=item_to_find)

    take_quest_item = StoryNode(name="Take Quest Item ("+item_to_find.get_name()+")", tags={"Type":"Collect"}, actor=[GenericObjectNode.TASK_OWNER], target=[item_to_find], required_test_list=[actor_is_alive, actor_is_not_unconscious, current_location_has_item_check], effects_on_next_ws=[actor_starts_holding_target, location_stops_holding_target])

    location_no_longer_has_item_check = HasEdgeTest(object_from_test=location_holding_item, edge_name_test="holds", object_to_test=item_to_find, inverse=True)
    find_item_task = CharacterTask(task_name="Find Item Quest", task_actions=[take_quest_item], task_location_name=location_holding_item.get_name(), avoidance_state=[location_no_longer_has_item_check])

    location_has_item_check = HasEdgeTest(object_from_test=location_holding_item, edge_name_test="holds", object_to_test=item_to_find)
    
    memory_name = item_to_find.get_name() + "Memory"
    character_no_quest_memory_check = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag=memory_name, value=True, inverse=True)
    character_gains_quest_memory_change = TagChange(name="Gain Task Quest Memory", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag=memory_name, value=True, add_or_remove=ChangeAction.ADD)

    find_item_stack = TaskStack(stack_name="Find Item Stack ("+item_to_find.get_name()+")", task_stack=[find_item_task], task_stack_requirement=[])

    find_item_change = TaskChange(name="Find Item TaskChange", task_stack=find_item_stack, task_owner_name=GenericObjectNode.GENERIC_ACTOR, task_giver_name=GenericObjectNode.GENERIC_ACTOR)

    character_likes_item_type_check = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag=item_liking_tag, value=True)
    get_find_item_task_node = StoryNode(name="Gain Find Item Quest ("+item_to_find.get_name()+")", tags={"Type":"GetTask"}, effects_on_next_ws=[find_item_change, character_gains_quest_memory_change], required_test_list=[character_no_quest_memory_check, location_has_item_check, character_likes_item_type_check])
    
    patternless_into_find_item_node = RewriteRule(story_condition=[], story_change=[get_find_item_task_node], name="Patternless into Find Item Task Node")
    
    return patternless_into_find_item_node

patternless_get_find_harp_task = make_find_item_rule(item_to_find=singing_harp, item_liking_tag="LikesTreasure", location_holding_item=random_forest)
patternless_get_find_diary_task = make_find_item_rule(item_to_find=columbo_diary, item_liking_tag="LikesKnowledge", location_holding_item=random_forest)
patternless_get_find_goose_task = make_find_item_rule(item_to_find=golden_goose, item_liking_tag="LikesTreasure", location_holding_item=random_forest)

list_of_rules.append(patternless_get_find_harp_task)
list_of_rules.append(patternless_get_find_diary_task)
list_of_rules.append(patternless_get_find_goose_task)

# Rule: Patternless into Witness Home Destruction
destroy_home_into_witness_home_destruction = JoiningJointRule(base_actions=[], joint_node=witness_home_destruction, rule_name="Patternless Join Witness Home Destruction")
list_of_rules.append(destroy_home_into_witness_home_destruction)

# Rule: Witness Home Destruction into Attack
# witness_home_destruction_into_attack = ContinuousJointRule(base_joint=witness_home_destruction, joint_node=actor_attacks_target, rule_name="Witness Home Destruction Into Attack")
# list_of_rules.append(witness_home_destruction_into_attack)

# Rule: (Patternless) -> Attack
patternless_attack = JoiningJointRule(base_actions=[], joint_node=actor_attacks_target, rule_name="Patternless Attack Target")
list_of_rules.append(patternless_attack)

# Rule: Attack -> Attacker Defeated or Defender Defeated (No need to put this --- it will automatically pick a character to be defeated)

# attack_into_defeat = ContinuousJointRule(base_joint=actor_attacks_target, joint_node=defeat_action, rule_name="Attack into Defeat")
patternless_into_defeat = JoiningJointRule(base_actions=[], joint_node=defeat_action, rule_name="Patternless into Defeat")
list_of_rules.append(patternless_into_defeat)

# Rule: Attack -> Defeat and Take Rod (if the Attacker didn't have rod, but the Defender does)

# attack_into_defeatrod = ContinuousJointRule(base_joint=actor_attacks_target, joint_node=defeat_and_take_rod_target_unconscious, rule_name="Attack into Defeat (Rod)")
patternless_into_defeat_rod = JoiningJointRule(base_actions=[], joint_node=defeat_and_take_rod_target_unconscious, rule_name="Patternless into Defeat (Rod)")
list_of_rules.append(patternless_into_defeat_rod)

# Rule: Patternless -> Rebuild Home
patternless_into_rebuild_pig_home = RewriteRule(story_condition=[], story_change=[pig_rebuild_home], name="Patternless into Pig Rebuild Home")
patternless_into_rebuild_bear_home = RewriteRule(story_condition=[], story_change=[bear_rebuild_home], name="Patternless into Bear Rebuild Home")
patternless_into_rebuild_witch_home = RewriteRule(story_condition=[], story_change=[witch_rebuild_home], name="Patternless into Witch Rebuild Home")

list_of_rules.append(patternless_into_rebuild_pig_home)
list_of_rules.append(patternless_into_rebuild_bear_home)
list_of_rules.append(patternless_into_rebuild_witch_home)

# Rule: Patternless -> Witness Wolf
patternless_into_witness_wolf = JoiningJointRule(base_actions=[], joint_node=witness_wolf, rule_name="Patternless into Witness Wolf")
list_of_rules.append(patternless_into_witness_wolf)

# Rule: Patternless -> Notice No Grandma
patternless_into_notice_no_grandma = RewriteRule(story_condition=[], story_change=[notice_no_grandma], name="Patternless into Notice No Grandma")
list_of_rules.append(patternless_into_notice_no_grandma)

# Rule: Patternless -> Drop Actor
patternless_into_drop_other_actor = JoiningJointRule(base_actions=[], joint_node=drop_other_actor, rule_name="Patternless into Drop Character")
list_of_rules.append(patternless_into_drop_other_actor)

# Rule: Patternless -> Gain Consciousness
patternless_into_gain_consciousness = RewriteRule(name="Patternless into Gain Consciousness", story_condition=[], story_change=[gain_consciousness])
list_of_rules.append(patternless_into_gain_consciousness)

# Rule: Patternless -> Forgive
patternless_into_forgive = JoiningJointRule(base_actions=[], joint_node=forgive_action, rule_name="Patternless into Forgiveness")
list_of_rules.append(patternless_into_forgive)

# Generic Quests
# Find Rod Quest (We assume characters already know about the rod and will try to get there.)
# Steps: 
# Steal Rod (If Rod is found in someone else's house or on someone else's inventory, if rod is currently active need to deactivate rod to take it)
# Plant Rod (For the one holding an inactive rod: Installs the rod, if the rod is installed then it takes some effort to deactive or destroy)
#
# Failure condition: The rod is no longer in the Temple
# Requirement: Character must own a home, the rod must still be in the temple, 

def create_rod_task_node_for_homeowner(character_object):

    character_object_name = character_object.get_name()

    magical_temple_not_hold_rod = HasEdgeTest(object_from_test=magic_temple, edge_name_test="holds", object_to_test=protection_pillar, inverse=True)
    magical_temple_hold_rod = HasEdgeTest(object_from_test=magic_temple, edge_name_test="holds", object_to_test=protection_pillar)

    take_rod_from_temple_task = CharacterTask(task_name="Take Rod from Temple", task_actions=[take_rod_from_location], task_location_name="Magic Temple", avoidance_state=[magical_temple_not_hold_rod])
    
    take_rod_and_install_stack = TaskStack(stack_name="Rod Quest", task_stack=[take_rod_from_temple_task])

    take_rod_and_install_stackchange = TaskChange(name="Rod Quest Change", task_giver_name=GenericObjectNode.GENERIC_ACTOR, task_owner_name=GenericObjectNode.GENERIC_ACTOR, task_stack=take_rod_and_install_stack)

    actor_is_me_check = ObjectEqualityTest(object_list=[character_object, GenericObjectNode.GENERIC_ACTOR])

    actor_remembers_rod_quest_change = TagChange(name="Actor Knows Rod Quest", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="KnowsRodQuest", value=True, add_or_remove=ChangeAction.ADD)
    actor_not_remember_rod_quest_check = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="KnowsRodQuest", value=True, inverse=True)

    personal_rod_quest_name = "Get Rod Quest for " + character_object_name
    my_get_rod_quest_action = StoryNode(name=personal_rod_quest_name, tags={"Type":"GetTask"}, effects_on_next_ws=[take_rod_and_install_stackchange, actor_remembers_rod_quest_change], required_test_list=[actor_is_me_check, actor_not_remember_rod_quest_check, magical_temple_hold_rod, actor_is_alive])
    
    return my_get_rod_quest_action

brick_rod_quest_node = create_rod_task_node_for_homeowner(character_object=brick_pig)
papa_bear_rod_quest_node = create_rod_task_node_for_homeowner(character_object=papabear)
witch_rod_quest_node = create_rod_task_node_for_homeowner(character_object=witch)

def create_visit_place_storynode(task_owner, place_to_visit, additional_conditions_to_start_quest=[], additional_ws_change_in_visiting_node = [], additional_goal_state_check = []):

    place_to_visit_name = place_to_visit.get_name()

    visit_the_place = StoryNode(name="Visiting Place", tags={"Type":"Movement"}, actor=[GenericObjectNode.TASK_OWNER], effects_on_next_ws=additional_ws_change_in_visiting_node)

    visit_place_task = CharacterTask(task_name="Visiting Place Task", task_actions=[visit_the_place], task_location_name=place_to_visit_name, goal_state=additional_goal_state_check)

    visit_place_stack = TaskStack(stack_name="Visiting Place Stack", task_stack=[visit_place_task])    

    visit_place_taskchange = TaskChange(name="Visit Place Taskchange", task_giver_name=GenericObjectNode.GENERIC_ACTOR, task_owner_name=GenericObjectNode.GENERIC_ACTOR, task_stack=visit_place_stack)

    actor_is_me_check = ObjectEqualityTest(object_list=[task_owner, GenericObjectNode.GENERIC_ACTOR])

    required_tests = [actor_is_me_check, actor_is_alive]
    required_tests.extend(additional_conditions_to_start_quest)

    get_visit_place_stack_storynode = StoryNode(name="Get Visit Place Task for " + task_owner.get_name(), tags={"Type":"GetTask"}, effects_on_next_ws=[visit_place_taskchange], required_test_list=required_tests)
 
    return get_visit_place_stack_storynode

# #Red Visit Grandma Task Node. This one will be the first node for Red.
# # "So I visited my Grandma---"
# # "Bro visited her grandma"
# # :(???
red_get_visit_grandma_task_node = create_visit_place_storynode(task_owner=red, place_to_visit=forest_village)

actor_stops_fearing_wolf = RelChange(name="Actor Stops Fearing Wolf", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="fears", node_b=wolf, add_or_remove=ChangeAction.REMOVE, soft_equal=True)

taskowner_not_fear_wolf_check = HasEdgeTest(object_from_test=GenericObjectNode.TASK_OWNER, edge_name_test="fears", object_to_test=wolf, inverse=True)
brick_visit_wood_when_fearing_wolf = create_visit_place_storynode(task_owner=brick_pig, place_to_visit=plains_village, additional_conditions_to_start_quest=[actor_fears_wolf_check], additional_ws_change_in_visiting_node=[actor_stops_fearing_wolf], additional_goal_state_check=[taskowner_not_fear_wolf_check])

patternless_into_wood_visit = RewriteRule(story_condition=[], story_change=[brick_visit_wood_when_fearing_wolf], name="Patternless into Wood Pig Visitation")
list_of_rules.append(patternless_into_wood_visit)

# # Brick-Specific Quest
# # Run from Wolf to Wood House ()
# # Steps:
# # Talk to Wood Pig
# # Failure Condition: Wood Pig dies
# # Clear Condition: Wolf dies

# # Return Home (After completing the first quest)
# # Steps:
# # Go Home

# # Red-Specific Quest
# # Visit Grandma (First Actual Quest)
# # Steps:
# # Go to Grandma House
# # (might meet wolf on the way)

# # Tell Mom about Wolf (Second Quest, gain after witnessing Wolf, First witnessing the wolf gives her a kill reason)
# # Steps:
# # Go talk to Mom at Red House

# # Wolf-Specific Quest
# # TBH since we don't know these characters' locations they should be rules. Like if Wolf share a location with these guys he will try to scare them
# # We will define "These Guys" as ForestHomeowners.

# # Threaten Witch
# # Steps:

# # Threaten Brick
# # Steps: 

# # Threaten Bears
# # Steps:

# # And when he is done scaring them he will return to tell Grandma that he is done. For each character he scared he gets a token. There will be a jointless rule that says the wolf can report scaring all the people
# # Report All Residents Scared

# # Scheme Together (Characters must both have negative moral bias.)
target_gain_scarereason_witch_homeowner = RelChange(name="Scare Reason Gain", node_a=GenericObjectNode.GENERIC_TARGET, edge_name="ScareReason", value="ForestHomeowner", node_b=witch, add_or_remove=ChangeAction.ADD)
target_gain_scarereason_bear_homeowner = RelChange(name="Scare Reason Gain", node_a=GenericObjectNode.GENERIC_TARGET, edge_name="ScareReason", value="ForestHomeowner", node_b=papabear, add_or_remove=ChangeAction.ADD)
target_gain_scarereason_brick_homeowner = RelChange(name="Scare Reason Gain", node_a=GenericObjectNode.GENERIC_TARGET, edge_name="ScareReason", value="ForestHomeowner", node_b=brick_pig, add_or_remove=ChangeAction.ADD)
all_scare_reasons = [target_gain_scarereason_witch_homeowner, target_gain_scarereason_bear_homeowner, target_gain_scarereason_brick_homeowner]

scheme_leader_gives_task = StoryNode(name="Scheme Leader Gives Tasks", tags={"Type":"GiveTask"}, charcount=1, target_count=1, effects_on_next_ws=all_scare_reasons, required_test_list=[actor_is_alive, actor_is_not_unconscious, target_is_alive, target_is_not_unconscious])

# Once Wolf has scared all three ForestHomeowners, there will be an option to tell Grandma that he's done doing so, which will give Grandma the task to start destroying homes.
actor_has_scared_witch_check = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="HasScared", object_to_test=witch)
actor_has_scared_bear_check = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="HasScared", object_to_test=papabear)
actor_has_scared_brick_check = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="HasScared", object_to_test=brick_pig)

# #TODO: Home cannot be destroyed if the owner is holding the protection rod
def destroy_house_taskchanges(home_tag_name, homeowner_object):
    
    homeowner_not_holding_magical_rod_check = HasEdgeTest(object_from_test=homeowner_object, edge_name_test="holds", object_to_test=protection_pillar, soft_equal=True, inverse=True)

    home_tag_destroy_change = TagChange(name="Destroy Someone's Home", object_node_name=GenericObjectNode.GENERIC_LOCATION, tag=home_tag_name, value=False, add_or_remove=ChangeAction.ADD)
    home_tag_destroyed_check = HasTagTest(object_to_test=forest_village, tag=home_tag_name, value=False)

    node_name = "Actor Destroys House" + homeowner_object.get_name()
    actor_destroys_house = StoryNode(name=node_name, actor=[GenericObjectNode.TASK_OWNER], tags={"Type":"Destruction", "costly":True}, required_test_list=[actor_is_alive, actor_is_not_unconscious, homeowner_not_holding_magical_rod_check], effects_on_next_ws=[actor_is_destroying_home_change, home_tag_destroy_change])

    destroy_home_task = CharacterTask(task_name="Destroy Home Task", task_actions=[actor_destroys_house], task_location_name="Forest Village", goal_state=[home_tag_destroyed_check])

    stackname = "Destroy Home Stack (" + home_tag_name + ")"
    destroy_home_stack = TaskStack(stack_name=stackname, task_stack=[destroy_home_task])
    destroy_home_taskchange = TaskChange(name="Destroy Home TaskChange", task_giver_name=GenericObjectNode.GENERIC_TARGET, task_owner_name=GenericObjectNode.GENERIC_TARGET, task_stack=destroy_home_stack)

    return destroy_home_taskchange

destroy_witch_house_taskchange = destroy_house_taskchanges(home_tag_name="WitchHomeStanding", homeowner_object=witch)
destroy_brickhouse_taskchange = destroy_house_taskchanges(home_tag_name="PigHomeStanding", homeowner_object=brick_pig)
destroy_bearhouse_taskchange = destroy_house_taskchanges(home_tag_name="BearHomeStanding", homeowner_object=papabear)
report_scared_forest_memory_gain = TagChange(name="Report Scared Memory", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="ScaredForestReportMemory", value=True, add_or_remove=ChangeAction.ADD)

all_destroyhouse_taskchanges = [destroy_bearhouse_taskchange, destroy_brickhouse_taskchange, destroy_witch_house_taskchange, report_scared_forest_memory_gain]

actor_has_no_reportscare_memory_check = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="ScaredForestReportMemory", value=True, inverse=True)

target_is_grandma = ObjectEqualityTest(object_list=[grandma, GenericObjectNode.GENERIC_TARGET])
report_scared_forest = StoryNode(name="Report Scared Forest Village", tags={"Type":"GiveTask"}, charcount=1, target_count=1, effects_on_next_ws=all_destroyhouse_taskchanges, biasweight=50, required_test_list=[actor_is_alive, target_is_alive, actor_is_not_unconscious, target_is_not_unconscious, actor_has_scared_witch_check, actor_has_scared_bear_check, actor_has_scared_brick_check, actor_has_no_reportscare_memory_check, target_is_grandma])

patternless_into_report_scared_forest = JoiningJointRule(base_actions=None, joint_node=report_scared_forest, rule_name="Patternless into Report Scared Forest Village")
list_of_rules.append(patternless_into_report_scared_forest)

# #In hindsight, maybe these could have been quests (since Mom only exists in one place)
tell_mom_wolf_exists = StoryNode(name="Tell Mom Wolf Real", tags={"Type":"Conversation"}, actor=[GenericObjectNode.TASK_OWNER], target=[mom], charcount=1, required_test_list=[actor_is_alive, actor_is_not_unconscious, target_is_not_unconscious], effects_on_next_ws=[actor_gains_killing_tool])
tell_mom_wolf_task = CharacterTask(task_name="Tell Mom Wolf Task", task_actions=[tell_mom_wolf_exists], task_location_name="Plains Village")
tell_mom_wolf_stack = TaskStack(stack_name="Tell Mom Wolf Stack", task_stack=[tell_mom_wolf_task])
tell_mom_wolf_taskchange = TaskChange(name="Tell Mom Wolf TaskChange", task_giver_name=GenericObjectNode.GENERIC_ACTOR, task_owner_name=GenericObjectNode.GENERIC_ACTOR, task_stack=tell_mom_wolf_stack)
tell_mom_wolf_questmemory_not_exist_check = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="TellMomWolfQuestMemory", value=True, inverse=True)
tell_mom_wolf_questmemory_not_exist_change = TagChange(name="Tell Mom Wolf QuestMemory Change", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="TellMomWolfQuestMemory", value=True, add_or_remove=ChangeAction.ADD)
tell_mom_wolf_getquest = StoryNode(name="Get Tell Mom Wolf Quest", effects_on_next_ws=[tell_mom_wolf_taskchange, tell_mom_wolf_questmemory_not_exist_change], required_test_list=[tell_mom_wolf_questmemory_not_exist_check, actor_is_alive, actor_knows_wolf_check, actor_is_red, actor_is_not_unconscious])

tell_mom_missing_grandma = StoryNode(name="Tell Mom Missing Grandma", tags={"Type":"Conversation"}, actor=[GenericObjectNode.TASK_OWNER], target=[mom], charcount=1, required_test_list=[actor_is_alive, actor_is_not_unconscious, target_is_not_unconscious, actor_and_target_shares_location, target_is_actors_parent, actor_knows_missing_grandma_check], effects_on_next_ws=[bear_gets_kill_command, bear_gets_wolf_attack_reason])
tell_mom_grandma_task = CharacterTask(task_name="Tell Mom Missing Grandma Task", task_actions=[tell_mom_missing_grandma], task_location_name="Plains Village")
tell_mom_grandma_stack = TaskStack(stack_name="Tell Mom Missing Grandma Stack", task_stack=[tell_mom_grandma_task])
tell_mom_grandma_taskchange = TaskChange(name="Tell Mom Grandma TaskChange", task_giver_name=GenericObjectNode.GENERIC_ACTOR, task_owner_name=GenericObjectNode.GENERIC_ACTOR, task_stack=tell_mom_grandma_stack)
tell_mom_grandma_questmemory_not_exist_check = HasTagTest(object_to_test=GenericObjectNode.GENERIC_ACTOR, tag="TellMomGrandmaQuestMemory", value=True, inverse=True)
tell_mom_grandma_questmemory_not_exist_change = TagChange(name="Tell Mom Grandma QuestMemory Change", object_node_name=GenericObjectNode.GENERIC_ACTOR, tag="TellMomGrandmaQuestMemory", value=True, add_or_remove=ChangeAction.ADD)
tell_mom_grandma_getquest = StoryNode(name="Get Tell Mom Grandma Quest", effects_on_next_ws=[tell_mom_grandma_taskchange, tell_mom_grandma_questmemory_not_exist_change], required_test_list=[tell_mom_grandma_questmemory_not_exist_check, actor_is_alive, actor_is_not_unconscious, actor_knows_missing_grandma_check, actor_is_red])

patternless_into_tell_mom_wolf_real = RewriteRule(name="Patternless into Tell Mom Wolf Real Quest", story_condition=[], story_change=[tell_mom_wolf_getquest])
patternless_into_tell_mom_missing_grandma = RewriteRule(name="Patternless into Tell Mom Missing Grandma", story_condition=[], story_change=[tell_mom_grandma_getquest])

list_of_rules.append(patternless_into_tell_mom_wolf_real)
list_of_rules.append(patternless_into_tell_mom_missing_grandma)

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
# Brick, Bear, Witch: Wait
# Hunter: Wait
# Wolf: Get task to kick the bears, the pig, and the witch out from home

# TODO: Chases and runnning-aways aren't properly defined yet. What do we do with those?

DEFAULT_WAIT_NODE = StoryNode(name="Wait", biasweight=0, tags= {"Type":"Placeholder"}, charcount=1)

always_true_list = []

def make_only_one_holder_test(object_to_uniquely_be_held):
    return HasEdgeTest(object_from_test=None, edge_name_test="holds", object_to_test=object_to_uniquely_be_held, only_test_uniqueness=True, unique_incoming_test=True)

always_true_list.append(make_only_one_holder_test(protection_pillar))
always_true_list.append(make_only_one_holder_test(columbo_diary))
always_true_list.append(make_only_one_holder_test(golden_goose))
always_true_list.append(make_only_one_holder_test(singing_harp))

list_of_actors = [red, wolf, brick_pig, grandma, papabear, witch]

initial_graph = StoryGraph(name="Initial Story Graph", character_objects=list_of_actors, starting_ws=reds_world_state, always_true_tests=always_true_list)
initial_graph.add_story_part(part=red_get_visit_grandma_task_node, character=red, location=plains_village)
initial_graph.insert_joint_node(joint_node=scheme_leader_gives_task, main_actor=grandma, targets=[wolf], location=forest_village)
initial_graph.add_story_part(part=brick_rod_quest_node, character=brick_pig, location=forest_village)
initial_graph.add_story_part(part=papa_bear_rod_quest_node, character=papabear, location=forest_village)
initial_graph.add_story_part(part=witch_rod_quest_node, character=witch, location=forest_village)

# initial_graph.add_story_part(part=DEFAULT_WAIT_NODE, character=red, location=plains_village)
# initial_graph.add_story_part(part=DEFAULT_WAIT_NODE, character=wolf, location=forest_village)
# initial_graph.add_story_part(part=DEFAULT_WAIT_NODE, character=grandma, location=forest_village)
# initial_graph.add_story_part(part=DEFAULT_WAIT_NODE, character=brick_pig, location=forest_village)
# initial_graph.add_story_part(part=DEFAULT_WAIT_NODE, character=papabear, location=forest_village)
# initial_graph.add_story_part(part=DEFAULT_WAIT_NODE, character=witch, location=forest_village)

#TODO: Put the Metric Requirements in a list here, so that we can include it as an option when we want to generate with Metrics
metric_requirements = []

red_has_more_than_20_main = StoryMetric(metric_type=MetricType.PREFER, value=20, metric_mode=MetricMode.HIGHER, character_object=red)
brick_has_more_than_20_main = StoryMetric(metric_type=MetricType.PREFER, value=20, metric_mode=MetricMode.HIGHER, character_object=brick_pig)
wolf_has_more_than_20_main = StoryMetric(metric_type=MetricType.PREFER, value=20, metric_mode=MetricMode.HIGHER, character_object=wolf)

papa_has_less_than_20_main = StoryMetric(metric_type=MetricType.PREFER, value=20, metric_mode=MetricMode.LOWER, character_object=papabear)
witch_has_less_than_20_main = StoryMetric(metric_type=MetricType.PREFER, value=20, metric_mode=MetricMode.LOWER, character_object=witch)
grandma_has_less_than_20_main = StoryMetric(metric_type=MetricType.PREFER, value=20, metric_mode=MetricMode.LOWER, character_object=grandma)

brick_less_than_20_cost_metric = StoryMetric(metric_type=MetricType.COST, value=20, metric_mode=MetricMode.LOWER, character_object=brick_pig)
wolf_more_than_20_cost_metric = StoryMetric(metric_type=MetricType.COST, value=20, metric_mode=MetricMode.HIGHER, character_object=wolf)

red_has_more_than_40_uniqueness = StoryMetric(metric_type=MetricType.UNIQUE, value=40, metric_mode=MetricMode.HIGHER, character_object=red)
brickpig_has_more_than_40_uniqueness = StoryMetric(metric_type=MetricType.UNIQUE, value=40, metric_mode=MetricMode.HIGHER, character_object=brick_pig)
wolf_has_more_than_40_uniqueness = StoryMetric(metric_type=MetricType.UNIQUE, value=40, metric_mode=MetricMode.HIGHER, character_object=wolf)

grandma_has_more_than_20_joint = StoryMetric(metric_type=MetricType.JOINTS, value=20, metric_mode=MetricMode.HIGHER, character_object=grandma)

metric_requirements = [red_has_more_than_20_main, brick_has_more_than_20_main, wolf_has_more_than_20_main, brick_less_than_20_cost_metric, wolf_more_than_20_cost_metric, red_has_more_than_40_uniqueness, brickpig_has_more_than_40_uniqueness, wolf_has_more_than_40_uniqueness, grandma_has_more_than_20_joint, papa_has_less_than_20_main, witch_has_less_than_20_main, grandma_has_less_than_20_main]

#important_actions:
# Defying Target
# Attacking Home Intruder
# Witness Home Destruction
# Kidnap Target

#costly:
# Eat and Kill
# Kill Target
# Destroy Home
# Kill and Take Rod

movement_suggestion = []
current_location_holds_someone = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_LOCATION, edge_name_test="holds", object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER)
current_location_has_someone_actor_fears_penalty = SomethingPassesAllGivenTestsTest(list_of_tests_with_placeholder=[current_location_holds_someone, actor_fears_someone], score=-50)
movement_suggestion.append(current_location_has_someone_actor_fears_penalty)

target_holds_someone = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_TARGET, edge_name_test="holds", object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER)
target_location_has_someone_actor_fears_reward = SomethingPassesAllGivenTestsTest(list_of_tests_with_placeholder=[target_holds_someone, actor_fears_someone], score=50)
movement_suggestion.append(target_location_has_someone_actor_fears_reward)

someone_is_grandma = ObjectEqualityTest(object_list=[GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, grandma])
after_scaring_forest_resident_want_to_meet_grandma_reward = SomethingPassesAllGivenTestsTest(list_of_tests_with_placeholder=[actor_has_scared_bear_check, actor_has_scared_witch_check, actor_has_scared_witch_check, target_holds_someone, someone_is_grandma, actor_has_no_reportscare_memory_check], score=300)
movement_suggestion.append(after_scaring_forest_resident_want_to_meet_grandma_reward)

actor_is_wolf = ObjectEqualityTest(object_list=[GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, wolf])
def make_want_to_approach_forest_resident_test(forest_resident_object):
    someone_is_forest_resident = ObjectEqualityTest(object_list=[GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, forest_resident_object])
    actor_has_not_scared_forest_resident_check = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="HasScared", object_to_test=forest_resident_object, soft_equal=True, inverse=True)
    before_scaring_resident_want_to_meet_reward = SomethingPassesAllGivenTestsTest(list_of_tests_with_placeholder=[actor_is_wolf, someone_is_forest_resident, actor_has_not_scared_forest_resident_check], score=200)

    return before_scaring_resident_want_to_meet_reward

movement_suggestion.append(make_want_to_approach_forest_resident_test(papabear))
movement_suggestion.append(make_want_to_approach_forest_resident_test(witch))
movement_suggestion.append(make_want_to_approach_forest_resident_test(brick_pig))

# TODO: Generate graphs with these memories
# 1. No Metrics
# 2. x0 Metric Retention (Does not remember old graphs)
# 3. x0.5 Metric Retention (Each old graph's importance is multiplied by x0.5)
# 3. x1 Metric Retention (Always remembers old graphs)

# test_graph = StoryGraph(name="Test Graph", character_objects=list_of_actors, starting_ws=reds_world_state, always_true_tests=always_true_list)
# test_graph.insert_joint_node(joint_node=scheme_leader_gives_task, main_actor=grandma, targets=[wolf], location=forest_village, absolute_step=0)
# print(test_graph.calculate_score_from_rule_char_and_cont(actor=wolf, insert_index=1, rule=patternless_into_scare))

something_is_a_location = HasTagTest(object_to_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, tag="Type", value="Location")
something_holds_actor = HasEdgeTest(object_from_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name_test="holds", object_to_test=GenericObjectNode.GENERIC_ACTOR, soft_equal=True)

actor_is_held_by_location_check = SomethingPassesAllGivenTestsTest(list_of_tests_with_placeholder=[something_holds_actor, something_is_a_location])
movement_requirement = []
movement_requirement.append(actor_is_alive)
movement_requirement.append(actor_is_not_unconscious)
movement_requirement.append(actor_is_held_by_location_check)

extra_move_changes = []

something_new_location_change = RelChange(name="Go To Task Loc", node_a=GenericObjectNode.GENERIC_TARGET, edge_name=reds_world_state.DEFAULT_HOLD_EDGE_NAME, node_b=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, value=None, add_or_remove=ChangeAction.ADD)
something_leave_old_location_change = RelChange(name="Leave Current Loc", node_a=GenericObjectNode.GENERIC_LOCATION, edge_name=reds_world_state.DEFAULT_HOLD_EDGE_NAME, node_b=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, add_or_remove=ChangeAction.REMOVE, soft_equal=True, value=None)

if_actor_grabs_something_then_something_changes_location = ConditionalChange(name="If Grabbed Then Movealong", list_of_condition_tests=[actor_grabs_something], list_of_changes=[something_new_location_change, something_leave_old_location_change])
extra_move_changes.append(if_actor_grabs_something_then_something_changes_location)

start_gen_time = datetime.now()

# generated_graph = generate_story_from_starter_graph(init_storygraph=initial_graph, list_of_rules=list_of_rules, required_story_length=5, verbose=True, extra_attempts=-1)
#Uncomment each block for the desired result
#No Metrics
generated_graph_list = generate_multiple_graphs(initial_graph=initial_graph, list_of_rules=list_of_rules, required_story_length=25, max_storynodes_per_graph=5, verbose=True, extra_attempts=-1, suggested_movement_requirement_list=movement_suggestion, extra_movement_requirement_list=movement_requirement, task_movement_random=True, extra_move_changes=extra_move_changes)
base_folder_name = "no_metric_6"

# x0 Retention
# generated_graph_list = generate_multiple_graphs(initial_graph=initial_graph, list_of_rules=list_of_rules, required_story_length=25, max_storynodes_per_graph=5, verbose=True, extra_attempts=-1, suggested_movement_requirement_list=movement_suggestion, metric_requirements=metric_requirements, extra_movement_requirement_list=movement_requirement, metric_retention=0, extra_move_changes=extra_move_changes)
# base_folder_name = "x0_metric_3"

# x0.5 Retention
# generated_graph_list = generate_multiple_graphs(initial_graph=initial_graph, list_of_rules=list_of_rules, required_story_length=25, max_storynodes_per_graph=5, verbose=True, extra_attempts=-1, suggested_movement_requirement_list=movement_suggestion, metric_requirements=metric_requirements, extra_movement_requirement_list=movement_requirement, metric_retention=0.5, extra_move_changes=extra_move_changes)
# base_folder_name = "xhalf_metric_2"

# x1 Retention
# generated_graph_list = generate_multiple_graphs(initial_graph=initial_graph, list_of_rules=list_of_rules, required_story_length=25, max_storynodes_per_graph=5, verbose=True, extra_attempts=-1, suggested_movement_requirement_list=movement_suggestion, metric_requirements=metric_requirements, extra_movement_requirement_list=movement_requirement, metric_retention=1, extra_move_changes=extra_move_changes)
# base_folder_name = "x1_metric_2"

finish_gen_time = datetime.now()

print("xxx")
print("Generation Time:", str(finish_gen_time-start_gen_time))

base_directory = "application/tests/test_output/"

graphcounter = 1

for generated_graph in generated_graph_list:
    print("Cycle Number:", str(graphcounter))
    fullpath = base_directory + base_folder_name + "/" + str(graphcounter) + "/"
    if not os.path.exists(fullpath):
        os.makedirs(fullpath)

    generated_graph.print_graph_nodes_to_text_file(directory=fullpath, verbose=True)
    latest_ws = generated_graph.make_latest_state()
    latest_ws.print_wsedges_to_text_file(directory=fullpath, verbose=True)

    graphcounter += 1

print("Generation Complete! Yippee!!")

#TODO: Things to Consider:
# 1. Something is preventing Papa Bear from moving from the Mountain Valley to Forest Path. Check to see what it is.
# It might have to do with the attempt_move_towards_task_loc function
# It has to do with the task stacks that's for sure. I just don't know how they interact...
# It's very likely that the errors in moving around from location to location has to do with the task cancellation nodes. This problem is not replicated when no tasks are cancelled.

# Discussion:
# The metrics don't seem to do much in changing the generation. According to the generation logs, every single action passes the metric rules, even though we have tested that the metric rules can properly be measured in the stories.
# - There aren't enough nodes with the labels that count towards the metrics. This meant that:
#      - If a Metric is LOWER, then the metric is already satisfied (because the nodes that would increase the metrics don't get added often)
#      - If a Metric is HIGHER, then the metric would give a good score either if the new node is not less than the current value or if the new node stays within the higher range. Since the value is almost always 0, then all the actions will always be given a good score.
#      - STABLE has the same problem with HIGHER.
# - The stories should be the same, they're based on the same rules. We should expect the same parts to appear, but the order a bit different
#
# Despite there being rules that allow it, the characters don't end up using certain rules at all.
# - Some rules can only be applied if a pattern exists, and the patterns are not guaranteed to show up
#   - This meant that it's not possible for certain actions to be done if its prerequisites are not done.
#
# We must define more actions as costly / important actions, but which ones do we define?
#
# How to fix the Continuous Joint: Use Edges!
# AttackInteraction: This edge is given to characters who interacted with each other previously with an Attack node.
# Change Defeat into a patternless join with the condition that the actor and the target is doubleconnected by AttackInteraction. This removes the AttackInteraction.
# Defeat will now give DefeatInteraction
# Killing and Kidnapping now requires DefeatInteraction, and will remove it upon doing said action