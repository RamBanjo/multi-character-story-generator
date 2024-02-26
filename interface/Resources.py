

class Resources():
    def __new__(cls):
        if not hasattr(cls,'instance'):
            cls.instance = super(Resources, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        self._objects = [
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
        ]
        self._locations = [
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
        ]
        self._characters = [
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

    def getObjects(self) -> dict:
        return self._objects

    def getLocations(self) -> dict:
        return self._locations

    def getCharacters(self) -> dict:
        return self._characters

