from copy import deepcopy
from turtle import st

from numpy import place
from components.RewriteRules import RewriteRule
from components.StoryObjects import *
from components.WorldState import *
from components.StoryGraph import *

'''
Starting Point: 

A->B->C

where A, B are in TS 1 and C is in TS 2

If we apply the rule that replaces A->B with A->D->B then it should work and D would be in TS 1

but if we apply the rule that replaces B->C with B->E->C it would not work because B and C are in different timesteps

Here we go, Good luck, Ram!
'''