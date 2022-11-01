from components.Edge import Edge
from components.RelChange import ChangeAction, GenericObjectNode, RelChange, TagChange
from components.StoryGraphTwoWS import StoryGraph
from components.StoryNode import StoryNode
from components.StoryObjects import CharacterNode, LocationNode, ObjectNode
from components.WorldState import WorldState

# We're making a basic storyline with no complex changes yet
# WS0: Home holds Bob. Home holds Key. Home holds Door. Door has the tag {LockState: Locked}
# SG0: Bob takes Key. (rem currentloc holds target, add actor holds target)
# WS1: Home holds Bob. Bob holds Key.
# SG1: Bob unlocks Door. (Requirement: Bob has Key) (add target {LockState: Unlocked})
# WS2: Home holds Bob. Bob holds Key. Home holds Door. Door has the tag {LockState: Unlocked}

# Aha! I got it. Generic WS Changes is where we're heading. If we generalize the RelChange objects and make them take in
# roles instead of actual objects, we should be able to enforce these changes.

# For now though, here are the objects.

bob = CharacterNode("Bob")
key = ObjectNode("Key", tags={"Type": "Object", "Unlocks":"BobHomeDoor"})
home = LocationNode("Home")
door = ObjectNode("Door", tags={"Type": "Object", "UnlockGroup":"BobHomeDoor", "LockState":"Locked"})

# Init Worldstate
bws = WorldState("Base Worldstate", [bob, key, home, door])
bws.connect(home, "holds", key)
bws.connect(home, "holds", bob)
bws.connect(home, "holds", door)

home_has_key = Edge("holds", GenericObjectNode.GENERIC_LOCATION, GenericObjectNode.GENERIC_TARGET)
bob_has_key = Edge("holds", GenericObjectNode.GENERIC_ACTOR, GenericObjectNode.GENERIC_TARGET)

#And here are the nodes.
take_key_effects = [RelChange("generic_pickup_loc", GenericObjectNode.GENERIC_LOCATION, home_has_key, GenericObjectNode.GENERIC_TARGET, ChangeAction.REMOVE), RelChange("generic_pickup_actor", GenericObjectNode.GENERIC_ACTOR, bob_has_key, GenericObjectNode.GENERIC_TARGET, ChangeAction.ADD)]
take_key = StoryNode("take_key", None, None, None, 1, 0, effects_on_next_ws=take_key_effects)

door_unlock_effects = [TagChange("door unlock", GenericObjectNode.GENERIC_TARGET, "LockState", "Unlocked", ChangeAction.ADD)]
unlock_door = StoryNode("unlock_door", None, None, None, 1, 0, effects_on_next_ws=door_unlock_effects)

#This Story Node will contain these story parts.
mygraph = StoryGraph("My Graph", [bob], [home], bws, [])

mygraph.add_story_part(take_key, bob, home, 0, copy=True, targets=[key])
mygraph.add_story_part(unlock_door, bob, home, 0, copy=True, targets=[door])

mygraph.update_list_of_changes()
latest_state = mygraph.make_latest_state()

#If this is right, the door should be open and Bob should have the key.
latest_state.print_all_edges()
latest_state.node_dict["Door"].print_all_tags()