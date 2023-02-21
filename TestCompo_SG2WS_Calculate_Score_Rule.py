#We will make a few storygraphs to test the function where we calculate the score from the rules.
#Character for all cases: Alice
#Case 1: Normal rule, no purging (A(BC)D -> A(BCEF)D (If BC then append EF))
#Case 2: Normal rule with purging (A(BC)D -> A(EF)D (If BC then purge and append EF))

#For these cases, we will introduce Bob, who is going to be waiting and will perform C at the same step where Alice is.
#Case 3: JoiningJointRule (AB(C) -> AB(CX) (If there is someone doing C, then all of them can do X))
#Case 4: ContJointRule (ABC(X) -> ABC(XY), (Cont X with XY))
#Case 5: SplitJointRule (ABCX(Y) -> ABCX(YG, YH) (Cont Y with G and H, for two different characters. Value for Alice is max between G and H.))

from components.StoryObjects import LocationNode, CharacterNode
from components.StoryNode import StoryNode
from components.WorldState import WorldState
from components.StoryGraphTwoWS import StoryGraph
from components.RewriteRuleWithWorldState import *

alice = CharacterNode("Alice", biases={"lawbias": 20, "moralbias":50}, tags={"Type":"Character", "Job":"Swordmaster", "Wealth":"Average"})

#These nodes are for testing all cases. They are one character nodes.
DEFAULT_WAIT_NODE = StoryNode(name="Wait", biasweight=0, tags= {"Type":"Placeholder"}, charcount=1)
node_a = StoryNode(name="Node A", biasweight=1, tags= {"Type":"Placeholder"}, charcount=1)
node_b = StoryNode(name="Node B", biasweight=1, tags= {"Type":"Placeholder"}, charcount=1)
node_c = StoryNode(name="Node C", biasweight=1, tags= {"Type":"Placeholder"}, charcount=1)
node_d = StoryNode(name="Node D", biasweight=1, tags= {"Type":"Placeholder"}, charcount=1)
node_e = StoryNode(name="Node E", biasweight=3, tags= {"Type":"Placeholder"}, charcount=1) 
node_f = StoryNode(name="Node F", biasweight=1, tags= {"Type":"Placeholder"}, charcount=1, suggested_included_tags=[("Job","Swordmaster")], suggested_excluded_tags=[("Wanted","Theft")], suggested_bias_range={"lawbias":(0,100), "moralbias":(30,100)})

#Alice should be able to proc up all the checks in the suggested includes in Node F, which means Node E will add 3 to the score and Node F will add 5 to the score. For both Case 1 and Case 2, Max Mode should return 5, and Avg Mode should return 4.

#The following nodes are going to be used in Joint Rules, because they may allow more than one characters to partake.
node_x = StoryNode(name="Node X", biasweight=1, tags={"Type":"Placeholder"}, charcount=2, suggested_included_tags=[("Job","Swordmaster"), ("Job","Warrior"), ("Job","Fighter")])
node_y = StoryNode(name="Node Y", biasweight=1, tags={"Type":"Placeholder"}, charcount=2, suggested_included_tags=[("Wealth","Average"), ("Living",True), ("Job","Fighter")])

#These two are for splits. Max between these should be 3. Average between these should be 2.5.
node_g = StoryNode(name="Node G", biasweight=1, tags={"Type":"Placeholder"}, charcount=1, suggested_included_tags=[("Job","Swordmaster")])
node_h = StoryNode(name="Node H", biasweight=1, tags={"Type":"Placeholder"}, charcount=3, suggested_included_tags=[("Job","Cook")])

#Okay, here are rules.
rule_1 = RewriteRule(story_condition=[node_b, node_c], story_change=[node_e, node_f], remove_before_insert=False)
rule_2 = RewriteRule(story_condition=[node_b, node_c], story_change=[node_e, node_f], remove_before_insert=True)

#TODO: Merge Count isn't needed since we can take the limit from the node's charcount itself?
rule_3 = JoiningJointRule(base_actions=[node_c], joint_node=node_x)
rule_4 = ContinuousJointRule
rule_5 = SplittingJointRule