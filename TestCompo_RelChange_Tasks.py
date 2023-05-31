# Testing TaskChange Objects
# How will we be able to retain Task information?
#
# A Task Database for all possible tasks (Hey, ReGEN did have something similar as a list of rules)
# Something to assign slots to the task once it's added to the story? (Stuff like placeholder objects as well as owner name / giver name)
# Leaning towards assigning slots outside of the Worldstate and SG2WS because honestly it feels like a lot of trouble fixing this from the inside

from components.RelChange import TaskChange

#TaskChange objects will now only have the actor name AKA the task's owner
taskchange = TaskChange("Test Task Change", actor_name="Alice")