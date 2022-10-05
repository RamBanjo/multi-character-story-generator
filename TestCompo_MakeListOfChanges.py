from components.StoryGraphTwoWS import StoryGraph

# We're making a basic storyline with no complex changes yet
# WS0: Home holds Bob. Home holds Key. Home holds Door. Door has the tag {LockState: Locked}
# SG0: Bob takes Key. (rem currentloc holds target, add actor holds target)
# WS1: Home holds Bob. Bob holds Key.
# SG1: Bob unlocks Door. (Requirement: Bob has Key) (add target {LockState: Unlocked})
# WS2: Home holds Bob. Bob holds Key. Home holds Door. Door has the tag {LockState: Unlocked}

# Aha! I got it. Generic WS Changes is where we're heading. If we generalize the RelChange objects and make them take in
# roles instead of actual objects, we should be able to enforce these changes.

# For now though, here are the objects.