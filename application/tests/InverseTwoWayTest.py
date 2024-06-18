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

print(reds_world_state.test_story_compatibility_with_conditiontest(test=HasEdgeTest(object_from_test=red, edge_name_test="AttackInteractionOccured", object_to_test=wolf, soft_equal=True, two_way=True, inverse=True)))

reds_world_state.apply_relationship_change(relchange_object=RelChange(name="AttackInteraction RedWolf", node_a=red, edge_name="AttackInteractionOccured", node_b=wolf, add_or_remove=ChangeAction.ADD, two_way=True))

testchange = RelChange(name="Gain Twoway AttackInteraction", node_a=red, node_b=wolf, edge_name="AttackInteractionOccured", add_or_remove=ChangeAction.ADD, two_way=True)

reds_world_state.apply_relationship_change(testchange)