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
