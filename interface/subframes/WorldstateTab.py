import tkinter as tk

import tkinter.ttk as ttk
from interface import UtilDefaults,UtilFunctions
from application.components import WorldState, StoryNode, StoryObjects
from interface.subframes.wstab.ButtonTray import ButtonTray
from interface.subframes.wstab.WorldStateCanvas import WorldStateCanvas
from interface.subframes.wstab.Descbox import Descbox

'''
WORLD STATE
A canvas that is composed of the following:
- All of the Entities that is meant to exist in this story.
- All of the connections between said Entities, either uni- or bidirectional.
- Uhh... I think that's it?

The following functions will be implemented:
- The ability to add and delete StoryObjects (with a button)
- The ability to add and delete connections between StoryObjects
- The ability to modify properties of connections (name and direction)
- The ability to display all of these in a single canvas.
...Sort of terrifying, but I have to do this in order to have any chance of passing.
'''

class WorldstateTab(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.root = self.master.root
        self.grid(column=0, row=1, padx=0, pady=0, sticky="nsew")

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=30)
        self.rowconfigure(2,weight=1)
        self.columnconfigure(0,minsize=150,weight=1)
        self.columnconfigure(1,minsize=700,weight=50)

        self.entityLabel = ttk.Label(self, text="Entities")
        self.entityLabel.grid(column=0,row=0)

        self.listvar = []
        self.tklistvar = None
        self.listbox = None
        self.descbox = Descbox(self)
        self.generate_listbox() #instantiates the listbox, of course.
    
    def generate_listbox(self):
        return
    
    def items_selected(self, event):
        return
    
    def reset(self):
        print("Uhhh reset?")