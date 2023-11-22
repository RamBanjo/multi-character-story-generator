import tkinter as tk
import tkinter.ttk as ttk
from interface import ObjectFrame,OptionFrame,Menu,ObjectsTab
from application.components import StoryObjects

#tempload
from interface import TempObjectLoad as tol

class App(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.root = self

        self.resources = {
            'optionNumber': tk.IntVar(value=-1),
            'btnLabels' : ["Entities","Actions","World State","Rules","Tasks","Initial Graph","Generate"],
            'maxObjects': tk.IntVar(value=10),
            #'objects': [StoryObjects.ObjectNode("Iron Sword", tags={"Type": "Object", "Weapon": "Sword", "Material": "Iron"}, internal_id=1, description="A shoddy iron sword.")],
            'objects': tol.other_objects,
            'maxLocations': tk.IntVar(value=10),
            #'locations': [StoryObjects.LocationNode("Cathedral", tags={"Type": "Location", "Faith": "Feli"}, internal_id=1, description="A mysterious cathedral that resurrects the heroic.")],
            'locations': tol.all_locations,
            'maxCharacters': tk.IntVar(value=10),
            #'characters': [StoryObjects.CharacterNode("Harold", tags={"Type": "Character", "Class": "Hero", "Weapon": "Sword", "Attribute": "Holy"}, internal_id = 1, description="A man destined to be a hero.")],
            'characters': tol.all_characters,
            'objectDetail': None
        }

        while(len(self.resources['objects']) < self.resources['maxObjects'].get()):
            self.resources['objects'].append(StoryObjects.ObjectNode("", internal_id=len(self.resources['objects'])+1))
        while(len(self.resources['locations']) < self.resources['maxLocations'].get()):
            self.resources['locations'].append(StoryObjects.LocationNode("", internal_id=len(self.resources['locations']) + 1))
        while(len(self.resources['characters']) < self.resources['maxCharacters'].get()):
            self.resources['characters'].append(StoryObjects.CharacterNode("", internal_id=len(self.resources['characters']) + 1))

        self.title(" Multi-Character Story Generator")
        self.geometry("1000x600")

        self.mainmenu = Menu.Menu(self)
        self.config(menu=self.mainmenu)

        self.resources['objectFrames'] = {
            9: ObjectFrame.InitialFrame(self)
        }
        self.objectFrame = self.resources['objectFrames'][9]
        self.resources['objectFrames'][0] = ObjectsTab.EntityTabController(self.objectFrame)
        for i in range(1,7):
            self.resources['objectFrames'][i] = ObjectFrame.NumberedFrame(self.objectFrame,i)
        self.resources['objectFrames'][8] = ObjectFrame.PlaceholdingFrame(self.objectFrame)
        self.resources['objectFrames'][8].grid(column=0, row=1, padx=0, pady=0, sticky="nsew")

        self.optionFrame = OptionFrame.OptionFrame(self)
        self.optionFrame.pack(side='top',fill='x',padx=5,pady=2)
    
    def changeOptionNumber(self, i):
        self.resources['optionNumber'].set(i)
        if(i == 8):
            self.objectFrame.label.config(text="Welcome!")
        else:
            self.objectFrame.label.config(text=self.resources['btnLabels'][i])
        self.resources['objectFrames'][i].tkraise()
    
    def reset(self):
        self.resources['maxObjects'].set(10)
        self.resources['objects'].clear()
        self.resources['objects'].append(StoryObjects.ObjectNode("Iron Sword", tags={"Type": "Object", "Weapon": "Sword", "Material": "Iron"}, internal_id=1, description="A shoddy iron sword."))
        self.resources['maxLocations'].set(10)
        self.resources['maxCharacters'].set(10)
        self.resources['locations'].clear()
        self.resources['locations'].append(StoryObjects.LocationNode("Cathedral", tags={"Type": "Location", "Faith": "Feli"}, internal_id=1, description="A mysterious cathedral that resurrects the heroic."))
        self.resources['characters'].clear()
        self.resources['characters'].append(StoryObjects.CharacterNode("Harold", tags={"Type": "Character", "Class": "Hero", "Weapon": "Sword", "Attribute": "Holy"}, internal_id = 1, description="A man destined to be a hero."))
        while(len(self.resources['objects']) < self.resources['maxObjects'].get()):
            self.resources['objects'].append(StoryObjects.ObjectNode("", internal_id=len(self.resources['objects'])+1))
        while(len(self.resources['locations']) < self.resources['maxLocations'].get()):
            self.resources['locations'].append(StoryObjects.LocationNode("", internal_id=len(self.resources['locations']) + 1))
        while(len(self.resources['characters']) < self.resources['maxCharacters'].get()):
            self.resources['characters'].append(StoryObjects.CharacterNode("", internal_id=len(self.resources['characters']) + 1))
        self.resources['objectFrames'][0].reset()
        self.root.changeOptionNumber(8)