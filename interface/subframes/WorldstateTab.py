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
    def __init__(self, container, getResourceMethod):
        super().__init__(container)
        self.root = self.master.root
        self.grid(column=0, row=1, padx=0, pady=0, sticky="nsew")
        self.getResourceMethod = getResourceMethod

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=30)
        self.rowconfigure(2,weight=1)
        self.columnconfigure(0,minsize=150,weight=1)
        self.columnconfigure(1,minsize=700,weight=50)

        self.entityLabel = ttk.Label(self, text="Entities")
        self.entityLabel.grid(column=0,row=0)

        self.val = []
        self.listboxVar = tk.StringVar(value="")
        self.generateListboxStringVar()

        self.listbox = tk.Listbox(self, listvariable=self.listboxVar)
        self.listbox.grid(column=0, row=1, padx=0, pady=0, sticky="nsew")
        self.listbox.bind('<<ListboxSelect>>', self.items_selected)

        self.descbox = Descbox(self)
    
    def generateListboxStringVar(self) -> None:
        resource = self.getResourceMethod()
        print(id(resource))
        # parse the resource
        self.val.clear()
        self.val.append("-- Objects --")
        for item in resource.get("objects"):
            self.val.append(item.get("name"))
        self.val.append("-- Locations --")
        for item in resource.get("locations"):
            self.val.append(item.get("name"))
        self.val.append("-- Characters --")
        for item in resource.get("characters"):
            self.val.append(item.get("name"))
        print(" ".join(self.val))
        self.listboxVar.set(self.val)
    
    def items_selected(self, event):
        if(len(self.listbox.curselection()) > 0):
            # get all selected indices
            resource = self.getResourceMethod()
            selected_indices = self.listbox.curselection()[0]
            if self.listbox.get(selected_indices) == "-- Objects --" or self.listbox.get(selected_indices) == "-- Locations --" or self.listbox.get(selected_indices) == "-- Characters --":
                return
            # get selected items
            print(self.val[selected_indices]) #unused variable, needs to link later.
            if selected_indices < len(resource.get("objects")):
                self.objectDetail = resource.get("objects")[selected_indices - 1]
            elif selected_indices < len(resource.get("objects")) + len(resource.get("locations")):
                self.objectDetail = resource.get("locations")[selected_indices - len(resource.get("objects")) - 2]
            else:
                self.objectDetail = resource.get("characters")[selected_indices - len(resource.get("objects")) - len(resource.get("locations")) - 3]
            
            self.descbox.fetch()
    
    def reset(self):
        print("Uhhh reset?")