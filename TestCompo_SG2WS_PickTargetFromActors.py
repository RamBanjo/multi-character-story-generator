#The goal here is to be able to determine who should be the target, given the previous absolute step's condition.
#For example, in ReGEN's example, if we put the three villagers and the king together, what requirements do you use to determine who gets to be revolted against, given that we only need one target?

from components.StoryObjects import CharacterNode, LocationNode
from components.RewriteRuleWithWorldState import *
from components.StoryNode import StoryNode

alice = CharacterNode(name = "Alice", biases={"lawbias":-30, "moralbias":50}, tags={"Type":"Character","Job":"Peasant"})
bob = CharacterNode(name = "Bob", biases={"lawbias":-50, "moralbias":10}, tags={"Type":"Character","Job":"Peasant"})
charlie = CharacterNode(name = "Charlie", biases={"lawbias":-20, "moralbias":0}, tags={"Type":"Character","Job":"Peasant"})

tyrant = CharacterNode(name = "Tyrant", biases={"lawbias":60, "moralbias":-100}, tags={"Type":"Character","Job":"King"})

revolt = StoryNode(name = "Revolt", biasweight=-20, tags={"Type":"Revolution"}, charcount=-1, bias_range={"lawbias":(-100, -20)}, bias_range_target={"moralbias":(-100, -20)})

basews = WorldState("BaseWS", [alice, bob, charlie, tyrant])
somewhere = LocationNode("Somewhere")
waiting = StoryNode("Waiting", biasweight=0, tags={"Type":"Waiting"})

basesg = StoryGraph("Base Story Graph", [alice, bob, charlie, tyrant], [somewhere], basews)

#We want 1 target for this thing, and only the tyrant qualifies as the target.