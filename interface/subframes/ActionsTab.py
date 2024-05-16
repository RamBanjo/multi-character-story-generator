import tkinter as tk

import tkinter.ttk as ttk
from interface import UtilFunctions
from application.components import StoryObjects,StoryNode
from interface.subframes.atab.Descbox import Descbox

# Note: abandoned for World State instead.
'''
As a reminder to self:
The Actions Tab is a location to store various StoryNodes with the ability to edit, create, and destroy them at will.
Each StoryNode has the following components, which must have their respective interfaces.
- General Settings
    Name, str: The name of the StoryNode. Edited in this tab.
    Bias Weight, int: No fucking idea what this does. Apparently goes up to atleast 200. Wut.
    Tags, dict: Just steal the taglist. Probably used to determine what actions can be used in a WS.
    Actor: 
     - charcount, int: The number of CharacterNodes who's doing the action.
     - #actor: The set of CharacterNodes actually doing the action. (No Interface)
    Target:
     - target_count, int: The number of CharacterNodes who is NOT DOING THE ACTION but is affected by it (and is thus involved)
     - #target: The set of CharacterNodes affected by the action. (No Interface)
    #Location = None: Where this StoryNode happens. (No Interface)
    #timestep: When this StoryNode happens in timestep notation. (No Interface)
    effects_on_next_ws, list(RelChange): What happens to the World after this StoryNode happens.
    #abs_step = 0: Joint Rules, apparently. I haven't looked into it yet. (No Interface)
    Required Test List, list(ConditionTest): The conditions required to perform this StoryNode.
    Suggested Test List, list(ConditionTest): The conditions recommended to prioritize this StoryNode.
'''

class ActionsTab(ttk.Frame):
    def __init__(self,container):
        super().__init__(master=container)
        self.root = self.master.root
        self.grid(column=0, row=1, padx=0, pady=0, sticky="nsew")

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=30)
        self.rowconfigure(2,weight=1)
        self.columnconfigure(0,minsize=150,weight=1)
        self.columnconfigure(1,minsize=700,weight=50)

        self.changeMaxBtn = ttk.Button(self,text=str("Change Maximum..."), command=self.openChangeMaximumWindow)
        self.changeMaxBtn.grid(column=0,row=2,padx=0,pady=0,sticky="nsew")

        self.listvar = []
        self.tklistvar = None
        self.listbox = None
        self.generate_listbox()

        self.descbox = Descbox(container=self)
    
    def items_selected(self, event):
        return
    
    def generate_listbox(self):
        return
    
    def openChangeMaximumWindow(self): 
        self.changeMaxLevel = tk.Toplevel(self)
        self.changeMaxLevel.minsize(400,50)
        self.changeMaxLevel.columnconfigure(0,minsize=200,weight=0)
        self.changeMaxLevel.columnconfigure([1,2],weight=100)
        self.changeMaxLevel.resizable(False,False)

        self.changeMaxLabel = ttk.Label(self.changeMaxLevel, text="Enter new maximum object number")
        self.changeMaxLabel.grid(column=0,row=0,columnspan=3,padx=5,pady=5,sticky="nsew")
        self.changeMaxEntry = ttk.Entry(self.changeMaxLevel)
        self.changeMaxEntry.grid(column=0,row=1,columnspan=3,padx=5,pady=5,sticky="nsew")
        self.changeMaxEntry.insert(0,str(self.maxEntityResource.get()))

        self.cancelChangeMax = ttk.Button(self.changeMaxLevel, text="Cancel", command=self.changeMaxLevel.destroy)
        self.cancelChangeMax.grid(column=1,row=2,sticky="nsew")
        self.okChangeMax = ttk.Button(self.changeMaxLevel, text="Submit", command=lambda: self.change_maximum())
        self.okChangeMax.grid(column=2,row=2,sticky="nsew")
    
    def change_maximum(self):
        return

