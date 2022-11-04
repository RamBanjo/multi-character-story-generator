#The Situation:
#The story is the same story from SG2WS_FillLocationSelf
#However, we would like to fill in a step where Bob goes to another place, talks to Charlie, before heading to Alice's house.
#The following must be true:
#   
#   On the step where Bob leaves the Shop:
#       - The Park (Charlie's Location) must be adjacent to the Shop (HasDoubleEdge)
#   On the step where Bob Talks to Charlie about the present:
#       - Bob must not hate Charlie (Reverse of HasEdge, not implemented?)
#       - Bob must have the birthday present (HeldItem: Present)
#       - Bob and Charlie must be in the same location (The Park) (SameLocation)
#   On the step where Bob leaves the Park to go to Alice House:
#       - The House must be adjacent to The Park (HasDoubleEdge)
#   
#   Additionally, at Alice's House, we would like Bob to give the present to Alice, this continues from the step where Bob goes to the house.
#   On the step where Bob gives the present to Alice:
#       - Bob must have the birthday present (HasEdge)
#       - Bob must like Alice (like)
#       - Bob and Alice must be in the same location (SameLocation)