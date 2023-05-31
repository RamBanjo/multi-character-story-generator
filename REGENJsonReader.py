#Here is where I would put the ReGEN World State and Rules, if I had any
#I should have done this instead of fucking around with the JSONReader (The rules reader could have waited until later!!!)

from JSONReader import *

regen_story_nodes = read_list_of_objects_from_json(json_file_name="json/ReGEN_Examples/REGENObjects.json", verbose=True)
regen_ws = make_world_state_from_extracted_list_of_objects("Regen WS", regen_story_nodes)
make_connection_from_json(json_file_name="json/ReGEN_Examples/ReGEN_Relations.json", verbose=True, world_state=regen_ws)

#TODO (Important): Make Story Parts

story_part_list = []

hates_target = HasEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="hates", object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True)
actor_target_shareloc = SameLocationTest(list_to_test=[GenericObjectNode.GENERIC_ACTOR, GenericObjectNode.GENERIC_TARGET])

attack_by_npc = StoryNode(name="Attack Target", biasweight=0, tags={"NodeType":"Attack"}, charcount=1, target_count=1, required_tags_list=[("type","NPC"), ("alive",True)], required_tags_list_target=[("alive",True)], condition_tests=[hates_target, actor_target_shareloc])

#Oh shoot---we don't have a way to ensure that the attacker is the same person who kills the target. Is the actor/target always going to be random? Maybe make players dying unwanted?
#Or maybe this:
#First story node assigns the murderer with a temporary tag, second story node uses that tag to force the murderer into the actor spot, then removes the temporary tag
#I'm a genius!
#To have random outcome, simply don't have these tags. We want random outcomes for most cases anyways
#
#EDIT: This is now handled by Tasks.
target_unalives = TagChange("Target Dies", GenericObjectNode.GENERIC_TARGET, "alive", True, ChangeAction.REMOVE)
target_dies = TagChange("Target Dies", GenericObjectNode.GENERIC_TARGET, "alive", False, ChangeAction.ADD)

# Oh shoot again---okay so. What if C hates A and B but then A kills B, would C instantly like A?
# Intensity of reason? Values? This isn't how ReGEN works though??? Maybe we can chalk it up as ReGEN characters not being very logical? Who knows?
#
# EDIT: This is covered by multiple sets of condition change

placeholder_share_loc_actor = SameLocationTest(list_to_test=[GenericObjectNode.GENERIC_ACTOR, GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER])
placeholder_friends_target = HasEdgeTest(object_from_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name_test="friends", object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True)
placeholder_hate_actor = RelChange("Placeholder Hates Actor", node_a=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name="hates", node_b=GenericObjectNode.GENERIC_ACTOR, add_or_remove=ChangeAction.ADD, value="murder_of_friend")
witnesses_hate_killer_because_friend = ConditionalChange(name="Hate Killer Because Friend", list_of_test_object_names=regen_story_nodes, list_of_condition_tests=[placeholder_friends_target, placeholder_share_loc_actor], list_of_changes=[placeholder_hate_actor])

placeholder_loves_target = HasEdgeTest(object_from_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name_test="loves", object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True)
witnesses_hate_killer_because_lover = ConditionalChange(name ="Hate Killer Because Lover", list_of_test_object_names=regen_story_nodes, list_of_condition_tests=[placeholder_loves_target, placeholder_share_loc_actor], list_of_changes=[placeholder_hate_actor])

placeholder_hates_target = HasEdgeTest(object_from_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name_test="hates", object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True)
placeholder_friends_actor = RelChange("Placeholder Hates Actor", node_a=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name="friend", node_b=GenericObjectNode.GENERIC_ACTOR, add_or_remove=ChangeAction.ADD, value="murder_of_disliked")
witnesses_friends_killer_because_hate = ConditionalChange(name = "Friend Killer Because Hate", list_of_condition_tests=[placeholder_hates_target, placeholder_share_loc_actor], list_of_test_object_names=regen_story_nodes, list_of_changes=[placeholder_friends_actor])

placeholder_dislikes_target = HasEdgeTest(object_from_test=GenericObjectNode.CONDITION_TESTOBJECT_PLACEHOLDER, edge_name_test="dislike", object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True)
witnesses_friends_killer_because_dislike = ConditionalChange(name = "Friend Killer Because Hate", list_of_condition_tests=[placeholder_dislikes_target, placeholder_share_loc_actor], list_of_test_object_names=regen_story_nodes, list_of_changes=[placeholder_friends_actor])

#TODO (Extra Features): BLAAGH MAKING ALL THESE FOR ALL THE CONDITIONS IS TEDIOUS IS THERE ANOTHER WAY AROUND THIS
# I might just have to suck it up and accept this as the reality at this moment, but that might change once I talk to professor or Ami, they might be able to suggest a faster way to do this

attacker_wins = StoryNode(name="Attacker Wins and Kills Target", biasweight=0, tags={"NodeType":"Murder"}, charcount=1, target_count=1, effects_on_next_ws=[target_dies, target_unalives, witnesses_hate_killer_because_friend, witnesses_friends_killer_because_dislike, witnesses_friends_killer_because_hate, witnesses_hate_killer_because_lover])

#Okay, so I know this was originally an NPC asking the player to break an allyship for them, but I'm taking creative decision to not have the players involved.
#Okay something's up here. There's absolutely no reason for someone to break an allyship, the request to break/the breaking of allyship just happens randomly as a quest. What???

actor_allied_target_test = HasDoubleEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="allies", object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True)
actor_target_break_ally = RelChange("Actor Target Unfriend", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="allies", node_b=GenericObjectNode.GENERIC_TARGET, value=None, add_or_remove=ChangeAction.REMOVE, soft_equal=True, two_way=True)
actor_target_become_enemies = RelChange("Actor Target Enemies", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="enemies", node_b=GenericObjectNode.GENERIC_TARGET, value="broken_ally", add_or_remove=ChangeAction.REMOVE, two_way=True)

break_friendship = StoryNode(name = "Break Ally", biasweight=0, charcount=1, target_count=1, condition_tests=[actor_target_shareloc, actor_allied_target_test], effects_on_next_ws=[actor_target_break_ally, actor_target_become_enemies])

#Fight her! I hardly knew her!
#How to assign what monster to fight? It just says there is at least one thing tagged as enemy in the world, but how do we make sure of the type of monster being fought?
#And how do we even facilitate the movement of characters towards the monsters' location?

#Information regarding Monster Location
#Information regarding Current Location
#Information regarding path from current location to monster location

#Pathfinding. We need Pathfinding

#Let's say that characters have knowledge of the world state. Then they would be able to properly travel to their destination.
#God this is Graph Theory all over again which I will need to implement. Haha Ram.

#This feels very confusing I hope I figure something out :(

get_kill_monster_quest = TagChange(name="Get Kill Monster Quest", object_node_name=GenericObjectNode.GENERIC_TARGET, tag="kill_monster_quest_active", value=True)
actor_request_fight_monster_quest = StoryNode(name="Actor Request Fight Quest", biasweight=0,charcount=1, target_count=1)

#Forge Allies is the same as break ally, but in the reverse. Still, there's no reason for someone to suddenly forge ally other than graph conditioning.

actor_enemies_target_test = HasDoubleEdgeTest(object_from_test=GenericObjectNode.GENERIC_ACTOR, edge_name_test="enemies", object_to_test=GenericObjectNode.GENERIC_TARGET, soft_equal=True)
actor_target_break_enemies = RelChange("Actor Target Unenemies", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="enemies", node_b=GenericObjectNode.GENERIC_TARGET, value=None, add_or_remove=ChangeAction.REMOVE, soft_equal=True, two_way=True)
actor_target_become_allies = RelChange("Actor Target Allies", node_a=GenericObjectNode.GENERIC_ACTOR, edge_name="enemies", node_b=GenericObjectNode.GENERIC_TARGET, value="broken_ally", add_or_remove=ChangeAction.REMOVE, two_way=True)

forge_allyship = StoryNode(name = "Forge Ally", biasweight=0, charcount=1, target_count=1, condition_tests=[actor_target_shareloc, actor_enemies_target_test], effects_on_next_ws=[actor_target_break_enemies, actor_target_become_allies])

#Give Blackmail Letter works on the same logic as Fight Monster: We need knowledge of the world's path and the current location of the target to resolve quest. Unless the characters are already in the same location?
#I'm skipping anything that requires the world path and knowledge of target's location for now.

#Holy shit most of these quests require those knowledge. I'm in trouble haha

