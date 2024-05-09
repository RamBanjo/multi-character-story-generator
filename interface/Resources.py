import itertools

class Resources():
    def __new__(cls):
        if not hasattr(cls,'instance'):
            cls.instance = super(Resources, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        #ObjectsTab
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

        #WorldstateTab
        self._relations = [
            {
                # Alice and Bob are in love.
                "fromEntityId": {
                    "entityType": "characters",
                    "entityId": 0
                },
                "toEntityId": {
                    "entityType": "characters",
                    "entityId": 1
                },
                "connection": {
                    "name": "Lovers",
                    "params": "Childhood Friends",
                    "is2way": True
                }
            },
            {
                # Alice holds an apple.
                "fromEntityId": {
                    "entityType": "characters",
                    "entityId": 0
                },
                "toEntityId": {
                    "entityType": "objects",
                    "entityId": 0
                },
                "connection": {
                    "name": "Holds",
                    "params": "Right Hand",
                    "is2way": False
                }
            },
            {
                # Apothecary and Building are adjacent.
                "fromEntityId": {
                    "entityType": "locations",
                    "entityId": 0
                },
                "toEntityId": {
                    "entityType": "locations",
                    "entityId": 1
                },
                "connection": {
                    "name": "Connects",
                    "params": "On Land",
                    "is2way": True
                }
            }
        ]

    def getObjects(self) -> list:
        return self._objects

    def getObjectFromId(self, objectId: int) -> dict:
        return self._objects[objectId]

    def getLocations(self) -> list:
        return self._locations
    
    def getLocationFromId(self, locationId: int) -> dict:
        return self._locations[locationId]

    def getCharacters(self) -> list:
        return self._characters
    
    def getCharacterFromId(self, characterId: int) -> dict:
        return self._characters[characterId]

    def getEntities(self) -> dict:
        return self._entities
    
    def getEntityFromId(self, entityId: dict) -> dict:
        if(entityId.get("entityType") == "characters"):
            return self.getCharacterFromId(entityId.get("entityId"))
        elif(entityId.get("entityType") == "locations"):
            return self.getLocationFromId(entityId.get("entityId"))
        else:
            return self.getObjectFromId(entityId.get("entityId"))

    def getRelations(self) -> list:
        return self._relations

    def getRelationFromId(self, relationId: int) -> dict:
        return self._relations[relationId]
    
    def addRelation(self, newRel: dict) -> None:
        self._relations.append(newRel)