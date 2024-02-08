import tkinter as tk
import tkinter.ttk as ttk

class DropdownTabButtonPanel(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(master=container)
        self.rowconfigure(0,weight=1)
        self.columnconfigure([0,1,2],weight=1)
        self.controller = controller

        self.objectButton = ttk.Button(self, text="Object", command = lambda: self.changeDropdownTab(0))
        self.locationButton = ttk.Button(self, text="Location", command = lambda: self.changeDropdownTab(1))
        self.characterButton = ttk.Button(self, text="Character", command = lambda: self.changeDropdownTab(2))

        self.objectButton.grid(column=0,row=0)
        self.locationButton.grid(column=1,row=0)
        self.characterButton.grid(column=2,row=0)
    
    def changeDropdownTab(self, tabNumber):
        self.controller.currentTab = tabNumber
        self.controller.tkraise()