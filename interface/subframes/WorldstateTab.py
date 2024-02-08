import tkinter as tk

import tkinter.ttk as ttk
from interface import UtilDefaults,UtilFunctions
from application.components import WorldState, StoryNode, StoryObjects
from interface.subframes.wstab.ButtonTray import ButtonTray
from interface.subframes.wstab.WorldStateCanvas import WorldStateCanvas


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

class WorldStateTab(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.root = self.master.root
        self.grid(column=0, row=1, padx=0, pady=0, sticky="nsew")

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=30)

        self.canvas = WorldStateCanvas(self) #note: packed geometry, cannot grid shit
        self.buttons = ButtonTray(self, self.canvas)
    
    def reset(self):
        print("Uhhh reset?")