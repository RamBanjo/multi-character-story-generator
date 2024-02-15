from application.components.StoryObjects import *
from interface import Resources

def loadMockData() -> None:
    Resources._maxCharacters = 15
    print(Resources.getMaxCharacters())