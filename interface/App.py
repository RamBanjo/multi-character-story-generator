import tkinter as tk
import tkinter.ttk as ttk
from interface import ObjectFrame,OptionFrame,Menu,UtilDefaults,UtilFunctions
from interface.subframes import ActionsTab,ObjectsTab
import interface.SaveResourceVariable as save
from application.components import StoryObjects,StoryNode

#tempload
from interface import TempObjectLoad as tol

class App(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.root = self

        self.btnLabels = ["Entities","Actions","World State","Rules","Tasks","Initial Graph","Generate"]
        self.optionNumber = save.Variable(value=-1)
        self.objectDetail = None

        self.resources = {
            'maxObjects': save.Variable(value=10),
            #'objects': [StoryObjects.ObjectNode("Iron Sword", tags={"Type": "Object", "Weapon": "Sword", "Material": "Iron"}, internal_id=1, description="A shoddy iron sword.")],
            'objects': tol.other_objects,
            'maxLocations': save.Variable(value=10),
            #'locations': [StoryObjects.LocationNode("Cathedral", tags={"Type": "Location", "Faith": "Feli"}, internal_id=1, description="A mysterious cathedral that resurrects the heroic.")],
            'locations': tol.all_locations,
            'maxCharacters': save.Variable(value=10),
            #'characters': [StoryObjects.CharacterNode("Harold", tags={"Type": "Character", "Class": "Hero", "Weapon": "Sword", "Attribute": "Holy"}, internal_id = 1, description="A man destined to be a hero.")],
            'characters': tol.all_characters,
            'maxActions': save.Variable(value=10),
            'actions': [StoryNode.StoryNode(name="Wait", biasweight=0, tags= {"Type":"Placeholder"}, charcount=1, internal_id=1)]
        }

        UtilFunctions.pad_or_truncate(self.resources['objects'], self.resources['maxObjects'].get(), UtilDefaults.DEFAULT_OBJECT_NODE)
        UtilFunctions.pad_or_truncate(self.resources['locations'], self.resources['maxLocations'].get(), UtilDefaults.DEFAULT_LOCATION_NODE)
        UtilFunctions.pad_or_truncate(self.resources['characters'], self.resources['maxCharacters'].get(), UtilDefaults.DEFAULT_CHARACTER_NODE)
        UtilFunctions.pad_or_truncate(self.resources['actions'], self.resources['maxActions'].get(), UtilDefaults.DEFAULT_STORYNODE)

        self.title(" Multi-Character Story Generator")
        self.geometry("1000x600")

        self.mainmenu = Menu.Menu(self)
        self.config(menu=self.mainmenu)

        self.subframes = {
            9: ObjectFrame.InitialFrame(self)
        }
        self.objectFrame = self.subframes[9]
        self.subframes[0] = ObjectsTab.EntityTabController(self.objectFrame)
        self.subframes[1] = ActionsTab.ActionsTab(self.objectFrame)
        for i in range(2,7):
            self.subframes[i] = ObjectFrame.NumberedFrame(self.objectFrame,i)
        self.subframes[8] = ObjectFrame.PlaceholdingFrame(self.objectFrame)
        self.subframes[8].grid(column=0, row=1, padx=0, pady=0, sticky="nsew")

        self.optionFrame = OptionFrame.OptionFrame(self)
        self.optionFrame.pack(side='top',fill='x',padx=5,pady=2)
    
    def changeOptionNumber(self, i) -> None:
        self.optionNumber.set(i)
        if(i == 8):
            self.objectFrame.label.config(text="Welcome!")
        else:
            self.objectFrame.label.config(text=self.btnLabels[i])
        self.subframes[i].tkraise()
    
    def reset(self) -> None:
        self.resources['maxObjects'].set(10)
        self.resources['maxLocations'].set(10)
        self.resources['maxCharacters'].set(10)
        self.resources['maxActions'].set(10)

        self.resources['objects'].clear()
        self.resources['objects'].append(StoryObjects.ObjectNode("Iron Sword", tags={"Type": "Object", "Weapon": "Sword", "Material": "Iron"}, internal_id=1, description="A shoddy iron sword."))
        self.resources['locations'].clear()
        self.resources['locations'].append(StoryObjects.LocationNode("Cathedral", tags={"Type": "Location", "Faith": "Feli"}, internal_id=1, description="A mysterious cathedral that resurrects the heroic."))
        self.resources['characters'].clear()
        self.resources['characters'].append(StoryObjects.CharacterNode("Harold", tags={"Type": "Character", "Class": "Hero", "Weapon": "Sword", "Attribute": "Holy"}, internal_id = 1, description="A man destined to be a hero."))
        self.resources['actions'].clear()
        self.resources['actions'].append(StoryNode.StoryNode(name="Wait", biasweight=0, tags= {"Type":"Placeholder"}, charcount=1, internal_id=1))
        
        UtilFunctions.pad_or_truncate(self.resources['objects'], self.resources['maxObjects'].get(), UtilDefaults.DEFAULT_OBJECT_NODE)
        UtilFunctions.pad_or_truncate(self.resources['locations'], self.resources['maxLocations'].get(), UtilDefaults.DEFAULT_LOCATION_NODE)
        UtilFunctions.pad_or_truncate(self.resources['characters'], self.resources['maxCharacters'].get(), UtilDefaults.DEFAULT_CHARACTER_NODE)
        UtilFunctions.pad_or_truncate(self.resources['actions'], self.resources['maxActions'].get(), UtilDefaults.DEFAULT_STORYNODE)
        
        self.subframes[0].reset()
        self.root.changeOptionNumber(8)
    
    def destroy(self) -> None:
        super().destroy()