# Testing Worldstate Change where tags are added to or removed from objects

# WS1: Alice (Feeling: Happy)
# WS2: Alice (Health: Sick, Feeling: Happy), Alice becomes sick
# WS3: Alice (Health: Sick), Alice is no longer happy

from components.StoryObjects import CharacterNode
from components.WorldState import WorldState
from components.RelChange import TagChange

alice = CharacterNode("Alice", tags = {"Type": "Character", "Feeling": "Happy", "Job": "Swordmaster"})

init_state = WorldState("Init State", [alice])

alice_becomes_sick = TagChange("alice_sick_add", "Alice", "Health", "Sick", "add")
alice_not_happy = TagChange("alice_happy_rem", "Alice", "Feeling", "Happy", "remove")

alice.print_all_tags()

init_state.apply_some_change(alice_becomes_sick)
init_state.apply_some_change(alice_not_happy)

print()
print("Alice becomes sick, is no longer happy.")
print()

alice.print_all_tags()