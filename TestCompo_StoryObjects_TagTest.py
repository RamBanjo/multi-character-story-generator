from components.ConditionTest import ConditionTest, HasEdgeTest
from components.StoryObjects import *
from components.Edge import Edge
from components.WorldState import WorldState

alice = CharacterNode("Alice", tags={"Type":"Character", "Status":"Alive", "Job":"Swordmaster", "Wanted":None, "Cursed":"AncientCurse"})

print("Alice has Type: Character (Expect True):", alice.check_if_this_item_has_tag("Type", "Character"))
print("Alice has Status: Dead (Expect False):", alice.check_if_this_item_has_tag("Status", "Dead"))
print("Alice is Wanted (Expect True):", alice.check_if_this_item_has_tag("Wanted", None))
print("Alice is Cursed (Expect True):", alice.check_if_this_item_has_tag("Cursed", None))
print("Alice is Drunk (Expect False):", alice.check_if_this_item_has_tag("Drunk", None))

bob = CharacterNode("Bob")

testws = WorldState("TestWS", [alice, bob])

testws.doubleconnect(alice, "likes", bob)
testws.disconnect(alice, "likes", bob)

#Expect this to print only Bob likes Alice
testws.print_all_edges()

edge_a = Edge("loves", alice, bob, "personality")
edge_b = Edge("loves", alice, bob, "looks")
edge_c = Edge("loves", alice, bob, "personality")
edge_d = Edge("owes", alice, bob, "money")
not_edge = "I like Cream Cheese Sandwiches"

print("Edge A equals to Edge C (Expected True):", edge_a == edge_c)
print("Edge A equals to Edge B (Expected False):", edge_a == edge_b)
print("Edge A equals to Edge D (Expected False):", edge_a == edge_d)
print("Edge A soft equals to Edge B (Expected True)", edge_a.soft_equal(edge_b))
print("Edge A equals to not_edge (Expected False):", edge_a == not_edge)
print("Edge A soft equals to not_edge (Expected False):", edge_a.soft_equal(not_edge))

testws.disconnect(bob, "likes", alice)
testws.connect(alice, "loves", bob, "looks")
testws.connect(bob, "loves", alice, "looks")

charlie = CharacterNode("Charlie")
dan = CharacterNode("Dan")
testws.add_nodes([charlie, dan])

testws.connect(charlie, "dislikes", dan, "personality")
testws.connect(dan, "dislikes", charlie, "profession")

test_a = HasEdgeTest(charlie, "dislikes", dan, None, soft_equal=True)
test_b = HasEdgeTest(dan, "dislikes", charlie, None, soft_equal=True)
test_c = HasEdgeTest(charlie, "dislikes", alice, None, soft_equal=True)
test_d = HasEdgeTest(charlie, "dislikes", dan, "personality", soft_equal=False)
test_e = HasEdgeTest(dan, "dislikes", charlie, "personality", soft_equal=False)
test_f = HasEdgeTest(charlie, "dislikes", alice, "personality", soft_equal=False)

print("Test A (Expect True):", testws.test_story_compatibility_with_conditiontest(test_a))
print("Test B (Expect True):", testws.test_story_compatibility_with_conditiontest(test_b))
print("Test C (Expect False):", testws.test_story_compatibility_with_conditiontest(test_c))
print("Test D (Expect True):", testws.test_story_compatibility_with_conditiontest(test_d))
print("Test E (Expect False):", testws.test_story_compatibility_with_conditiontest(test_e))
print("Test F (Expect False):", testws.test_story_compatibility_with_conditiontest(test_f))