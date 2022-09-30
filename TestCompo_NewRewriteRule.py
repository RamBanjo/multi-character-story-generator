#We want a rewrite rule half that checks conditions in the WorldState.
#For example, we want to check if the character is in a certain location in certain states.
#We can do this by drawing towards the world state, and check if the characters are in the proper places at that time.

#Then, when conditions are met, we can insert tag changes to the list of tag changes

# Story:
# 1 Bob goes to the Cave 
# 2 Bob collects the Treasure
# WS:
# 1 Home holds Bob, Cave holds Treasure
# 2 Cave holds Bob, Cave holds Treasure
#
# Rule: LHS: Go to Cave -> Collect Treasure (Bob must be in Cave in this step, and there must be a RelChange changing the ownership of the treasure)
# Replacement: RHS: Go to Cave -> Slay Dragon -> Collect Treasure (in the middle step where there is Slay Dragon action, there is a TagChange making the dragon Dead)

# The question here is how we're able to extract whether or not Bob is in the cave in the required steps? And how do we check for it?
# And how do we put this condition into the Rewrite Rule itself?
# This question is something that still has to be answered.

# We could fit these things into the StoryNode itself?
# Actor and Target Must Have Relationship
# Actor and Target Must Not Have Relationship
# Target and Actor Must Have Relationship
# Target and Actor Must Not Have Relationship
# If we're dealing with fixed object (For example, Characters having to know lore to do a ritual or needing to have a key to open a door)
# Then we need the rules to be customized for each specific context
# Actor and Fixed Object Must Have Relationship
# Actor and Fixed Object Must Not Have Relationship
# 
# Given the list of Must-Have and Must-Nots, we require the following:
# 1. With the list of world state changes, bring the world state up to the point where the replacement starts. Create a "Simulated World State" for the specific purpose of testing.
# 2. At that point, check if the character chosen satisfies the condition in that specific timestep.
# 3. Apply the changes, and then try again until all the states in the changes have been accounted for. Only return True if all of them satisfies the conditions.