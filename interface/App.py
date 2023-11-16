import tkinter as tk
import tkinter.ttk as ttk
from interface import ObjectFrame,OptionFrame,Menu,ObjectsTab
from application.components import StoryObjects

class App(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.root = self

        self.resources = {
            'optionNumber': tk.IntVar(value=-1),
            'btnLabels' : ["Objects","Actions","World State","Rules","Tasks","Initial Graph","Generate"],
            'maxObjects': 10,
            'objects': [StoryObjects.ObjectNode("Iron Sword", tags={"Type": "Object", "Weapon": "Sword", "Material": "Iron"}, internal_id=1, description="A shoddy iron sword.")],
            'objectDetail': None
        }

        while(len(self.resources['objects']) < self.resources['maxObjects']):
            self.resources['objects'].append(StoryObjects.ObjectNode("", internal_id=len(self.resources['objects'])+1))

        self.title(" Multi-Character Story Generator")
        self.geometry("900x600")

        menu = Menu.Menu(self)
        self.config(menu=menu)

        self.resources['objectFrames'] = {
            9: ObjectFrame.InitialFrame(self)
        }
        self.objectFrame = self.resources['objectFrames'][9]
        self.resources['objectFrames'][0] = ObjectsTab.ObjectsTab(self.objectFrame)
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
