import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import json

from interface import SaveResourceVariable
from application.components import StoryObjects


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
    
    def reset(self) -> None:
        self.root.reset()
        print(self.root.resources['maxObjects'].get())

    def save_project_as(self):
        file = filedialog.asksaveasfile(title="Save As...", filetypes = [("JSON files","*.json")], defaultextension=[("JSON files","*.json")])
        self.projectFile = file
        
        saving_dict = self.dump_resources()
        file.write(json.dumps(saving_dict))

        print(file.name)
    
    def dump_resources(self) -> dict:
        res = self.root.resources
        saving_dict = {}
        for key in res:
            value = clean_to_value(res.get(key))
            saving_dict[key] = value
        return saving_dict
            
def clean_to_value(item):
    if(type(item) == int or
       type(item) == str or
       type(item) == float or
       type(item) == None or
       type(item) == bool):
        return item
    if(type(item) == SaveResourceVariable.Variable):
        return clean_to_value(item.get())
    if(type(item) == list):
        return_list = []
        for x in item:
            return_list.append(clean_to_value(x))
        return return_list
    if(type(item) == StoryObjects.ObjectNode or 
       type(item) == StoryObjects.CharacterNode or
       type(item) == StoryObjects.LocationNode):
        return item.export_object_as_dict()