import tkinter as tk

import tkinter.ttk as ttk
from application.components import StoryObjects
from interface import UtilDefaults,UtilFunctions
from interface.subframes.etab.Descbox import Descbox
from interface.subframes.etab.EntityTabButtonPanel import EntityTabButtonPanel


class EntityTab(ttk.Frame):
    def __init__(self,container,entityResource,maxEntityResource, controller):
        super().__init__(master=container)
        self.root = self.master.root
        self.grid(column=0, row=1, padx=0, pady=0, sticky="nsew")
        self.entityResource = entityResource
        self.maxEntityResource = maxEntityResource
        self.controller = controller

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=30)
        self.rowconfigure(2,weight=1)
        self.columnconfigure(0,minsize=150,weight=1)
        self.columnconfigure(1,minsize=700,weight=50)

        self.label = EntityTabButtonPanel(self, self.controller)
        self.label.grid(column=0, row=0, padx=0, pady=0, sticky="nsew")

        self.changeMaxBtn = ttk.Button(self,text=str("Change Maximum..."), command=self.openChangeMaximumWindow)
        self.changeMaxBtn.grid(column=0,row=2,padx=0,pady=0,sticky="nsew")

        self.descbox = Descbox(container=self)
    
    def items_selected(self, event):
        if(len(self.listbox.curselection()) > 0):
            # get all selected indices
            selected_indices = self.listbox.curselection()[0]
            # get selected items
            self.root.objectDetail = self.entityResource[selected_indices]
            self.descbox.fetch()
    
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
        val = self.changeMaxEntry.get()
        if(not val.isdigit()):
            ttk.Label(self.changeMaxLevel,text="Not a positive number.").grid(column=0,row=2,sticky="nsew")
        else:
            val = int(val)
            if(val == 0 or val >= 1000000):
                return
            else:
                self.maxEntityResource.set(val)
                UtilFunctions.pad_or_truncate(self.entityResource,self.maxEntityResource.get(),UtilDefaults.DEFAULT_OF_OBJECT(self.entityResource[0]))
            self.generate_listbox()
            self.changeMaxLevel.destroy()

    def reset(self):
        self.generate_listbox()
        self.descbox.reset()
