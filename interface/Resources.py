

class Resources():
    def __new__(cls):
        if not hasattr(cls,'instance'):
            cls.instance = super(Resources, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        self._maxObjects = 10
        self._objects = {}
        self._maxLocations = 10
        self._locations = {}
        self._maxCharacters = 10
        self._characters = {}

    def getMaxObjects(self) -> int:
        return self._maxObjects

    def getObjects(self) -> dict:
        return self._objects

    def getMaxLocations(self) -> int:
        return self._locations

    def getLocations(self) -> dict:
        return self._locations

    def getMaxCharacters(self) -> int:
        return self._maxCharacters

    def getCharacters(self) -> dict:
        return self._characters

if __name__ == "__main__":
    r = Resources()
    print(r.getCharacters())