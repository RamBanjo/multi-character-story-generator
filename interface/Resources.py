
class Resources():
    def __new__(cls):
        if not hasattr(cls,'instance'):
            cls.instance = super(Resources, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):

        self._resources = {
            "entities": {
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
        },
            "relations": [
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
        }

    def getResourceDict(self) -> dict:
        return self._resources
    
    def setResourceDict(self, res) -> None:
        self._resources = res
    
    def getEntities(self) -> dict:
        return self.getResourceDict().get("entities")

    def getObjects(self) -> list:
        return self.getEntities().get("objects")

    def getObjectFromId(self, objectId: int) -> dict:
        return self.getObjects()[objectId]

    def getLocations(self) -> list:
        return self.getEntities().get("locations")
    
    def getLocationFromId(self, locationId: int) -> dict:
        return self.getLocations()[locationId]

    def getCharacters(self) -> list:
        return self.getEntities().get("characters")
    
    def getCharacterFromId(self, characterId: int) -> dict:
        return self.getCharacters()[characterId]
    
    def getEntityFromId(self, entityId: dict) -> dict:
        if(entityId.get("entityType") == "characters"):
            return self.getCharacterFromId(entityId.get("entityId"))
        elif(entityId.get("entityType") == "locations"):
            return self.getLocationFromId(entityId.get("entityId"))
        else:
            return self.getObjectFromId(entityId.get("entityId"))

    def getRelations(self) -> list:
        return self.getResourceDict().get("relations")

    def getRelationFromId(self, relationId: int) -> dict:
        return self.getRelations()[relationId]
    
    def addRelation(self, newRel: dict) -> None:
        self.getRelations().append(newRel)

    def refreshRelations(self) -> None:
        # remove relations which specifies entities that do not currently exist
        self.getRelations()[:] = [element for element in self.getRelations()
                              if len(self.getEntities()[element["fromEntityId"]["entityType"]]) > element["fromEntityId"]["entityId"]
                              and len(self.getEntities()[element["toEntityId"]["entityType"]]) > element["toEntityId"]["entityId"]]
        
    
    
    def clear(self) -> None:
        self.getObjects().clear()
        self.getCharacters().clear()
        self.getLocations().clear()
        self.getRelations().clear()