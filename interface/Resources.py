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

        self._connections = [
            {
                "name": "Connects",
                "fromEntityType": "locations",
                "toEntityType": "locations",
                "is2way": True
            },
            {
                "name": "Holds",
                "fromEntityType": "any",
                "toEntityType": "objects",
                "is2way": False
            },
            {
                "name": "Lovers",
                "fromEntityType": "characters",
                "toEntityType": "characters",
                "is2way": True
            }
        ]

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
                "connectionId": 2
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
                "connectionId": 1
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

    def getConnections(self) -> list:
        return self._connections
    
    def getConnectionFromId(self, connectionId: int) -> dict:
        return self._connections[connectionId]

    def getRelations(self) -> list:
        return self._relations