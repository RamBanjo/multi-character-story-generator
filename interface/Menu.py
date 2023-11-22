import tkinter as tk
import tkinter.ttk as ttk
from application.components import StoryObjects
from tkinter import filedialog
import json

class Menu(tk.Menu):
    def __init__(self, container):
        super().__init__(master=container, tearoff=0)
        self.root = self.master.root
        self.filemenu = tk.Menu(self,tearoff=0)
        self.add_cascade(label="File",menu=self.filemenu)
        
        self.filemenu.add_command(label="New", command=self.reset)
        self.filemenu.add_command(label="Open")
        self.filemenu.add_command(label="Save")
        self.filemenu.add_command(label="Save As...", command=self.save_project_as)
        self.filemenu.add_command(label="Export As...")
        self.filemenu.add_command(label="Quit", command=container.quit)

        self.projectFile = None
    
    def reset(self):
        self.root.reset()
        print(self.root.resources['maxObjects'].get())

    def save_project_as(self):
        file = filedialog.asksaveasfile(title="Save As...", filetypes = [("JSON files","*.json")], defaultextension=[("JSON files","*.json")])
        self.projectFile = file
        file.write("balls")
        print(file.name)
