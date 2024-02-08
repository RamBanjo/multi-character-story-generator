import tkinter as tk
from tkinter import ttk

class EntityTabButtonPanel(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(master=container)
        self.rowconfigure(0,weight=1)
        self.columnconfigure([0,1,2],weight=1)
        self.controller = controller

        self.objectButton = ttk.Button(self, text="Object", command = lambda: self.changeEntityTab(0))
        self.locationButton = ttk.Button(self, text="Location", command = lambda: self.changeEntityTab(1))
        self.characterButton = ttk.Button(self, text="Character", command = lambda: self.changeEntityTab(2))

        self.objectButton.grid(column=0,row=0)
        self.locationButton.grid(column=1,row=0)
        self.characterButton.grid(column=2,row=0)
    
    def changeEntityTab(self, tabNumber):
        self.controller.changeEntityTab(tabNumber)