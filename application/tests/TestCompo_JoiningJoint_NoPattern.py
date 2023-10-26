import sys

sys.path.insert(0,'')

from application.components.StoryObjects import CharacterNode, LocationNode, ObjectNode
from application.components.WorldState import WorldState
from application.components.StoryNode import StoryNode
from application.components.RewriteRuleWithWorldState import JoiningJointRule

jointrule = JoiningJointRule(base_actions=[])