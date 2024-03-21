import itertools

class Resources():
    def __new__(cls):
        if not hasattr(cls,'instance'):
            cls.instance = super(Resources, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):

        self._entities = {
            "objects": [
                {
                    "name": "Apple",
                    "notes": "",
                    "tags": {
                        
                    }
                },
                {
                    "name": "Banana",
                    "notes": "",
                    "tags": {
                        
                    }
                }
            ],
            "locations": [
                {
                    "name": "Apothecary",
                    "notes": "",
                    "tags": {
                        
                    }
                },
                {
                    "name": "Building",
                    "notes": "",
                    "tags": {
                        
                    }
                }
            ],
            "characters": [
                {
                    "name": "Alice",
                    "notes": "",
                    "biases": [0,0],
                    "tags": {
                        "gender": "F"
                    }
                },
                {
                    "name": "Bob",
                    "notes": "",
                    "biases": [0,0],
                    "tags": {
                        "gender": "M"
                    }
                }
            ]
        }
        self._objects = self._entities.get("objects")
        self._locations = self._entities.get("locations")
        self._characters = self._entities.get("characters")

    def getObjects(self) -> list:
        return self._objects

    def getLocations(self) -> list:
        return self._locations

    def getCharacters(self) -> list:
        return self._characters

    def getEntities(self) -> dict:
        return self._entities