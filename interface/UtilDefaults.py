from application.components import StoryNode,StoryObjects
from copy import deepcopy
#this file holds all default objects to be copied from via shenanigans when the time arises.

DEFAULT_OBJECT_NODE = StoryObjects.ObjectNode(name="", display_name="")
DEFAULT_LOCATION_NODE = StoryObjects.LocationNode(name="")
DEFAULT_CHARACTER_NODE = StoryObjects.CharacterNode(name="")
DEFAULT_STORYNODE = StoryNode.StoryNode(name="")

def DEFAULT_OF_OBJECT(obj):
    if(type(obj) == StoryObjects.ObjectNode):
        return DEFAULT_OBJECT_NODE
    elif(type(obj) == StoryObjects.LocationNode):
        return DEFAULT_LOCATION_NODE
    elif(type(obj) == StoryObjects.CharacterNode):
        return DEFAULT_CHARACTER_NODE
    elif(type(obj) == StoryNode.StoryNode):
        return DEFAULT_STORYNODE