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

        self.projectFilepath = None
    
    def reset(self):
        self.root.resources['maxObjects'] = 10
        self.root.resources['objects'] = [StoryObjects.ObjectNode("Iron Sword", tags={"Type": "Object", "Weapon": "Sword", "Material": "Iron"}, internal_id=1, description="A shoddy iron sword.")]
        self.root.resources['objectDetail'] = None
        while(len(self.root.resources['objects']) < self.root.resources['maxObjects']):
            self.root.resources['objects'].append(StoryObjects.ObjectNode("", internal_id=len(self.root.resources['objects'])+1))
        
        self.root.changeOptionNumber(8)
        self.root.resources['objectFrames'][0].generate_listbox()
        self.root.resources['objectFrames'][0].descbox.fetch()

    def save_project_as(self):
        filename = filedialog.asksaveasfile(initialdir="/",title="Save As...",filetypes=(("JSON files", "*.json")))
        self.projectFilepath = filename
        print(filename)