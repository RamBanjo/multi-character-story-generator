import tkinter as tk
import tkinter.ttk as ttk
from interface.subframes.wstab.DropdownTabButtonPanel import DropdownTabButtonPanel

class DropdownTab(ttk.Frame):
    def __init__(self,container,entityResource,labelText, controller):
        super().__init__(master=container)
        self.grid(column=0, row=1, padx=0, pady=0, sticky="nsew")
        self.entityResource = entityResource
        self.labelText = labelText
        self.controller = controller

        self.dropdownVar = tk.StringVar()
        self.dropdownOptions = []
        
        for entity in self.entityResource:
            if entity.name != "":
                self.dropdownOptions.append(entity.name)
        self.dropdown = tk.OptionMenu(self, self.dropdownVar, *self.dropdownOptions)
        self.dropdown.grid(column=0, row=2, padx=0, pady=0, sticky="nsew")

        self.label = DropdownTabButtonPanel(self, self.controller)
        self.label.grid(column=0, row=0, padx=0, pady=0, sticky="nsew")

        self.addX = ttk.Label(self, text=self.labelText)
        self.addX.grid(column=0,row=1,padx=2,pady=2,sticky="nsew")

        self.yesnoframe = ttk.Frame(self)
        self.yesButton = ttk.Button(self.yesnoframe, text="OK", command = lambda: self.submitAddEntity())
        self.yesButton.grid(column=0,row=0,sticky="nsew")
        self.noButton = ttk.Button(self.yesnoframe, text="Cancel", command=self.master.destroy)
        self.noButton.grid(column=1,row=0,sticky="nsew")
        self.yesnoframe.grid(column=0,row=3,sticky="nsew")
    
    def submitAddEntity(self):
        name_of_entity = self.dropdownVar.get()
        targetEntity = None
        for entity in self.entityResource:
            if(entity.name == name_of_entity):
                targetEntity = entity
                break
        self.master.master.master.ws.add_node(targetEntity)
        self.master.destroy()