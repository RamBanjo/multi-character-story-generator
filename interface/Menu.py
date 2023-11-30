import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import json

from interface import SaveResourceVariable
from application.components import StoryObjects,StoryNode


class Menu(tk.Menu):
    def __init__(self, container):
        super().__init__(master=container, tearoff=0)
        self.root = self.master.root
        self.filemenu = tk.Menu(self,tearoff=0)
        self.add_cascade(label="File",menu=self.filemenu)
        
        self.filemenu.add_command(label="New", command=self.reset)
        self.filemenu.add_command(label="Open", command=self.open_project)
        self.filemenu.add_command(label="Save", command=self.save_project)
        self.filemenu.add_command(label="Save As...", command=self.save_project_as)
        self.filemenu.add_command(label="Export As...")
        self.filemenu.add_command(label="Quit", command=container.quit)

        self.projectFile = None
    
    def reset(self) -> None:
        self.root.reset()
    
    def open_project(self):
        with filedialog.askopenfile(title="Open Project...", filetypes = [("JSON files","*.json")], defaultextension=[("JSON files","*.json")]) as file:
            self.projectFile = file.name
            data = json.loads(file.read())
            
            self.root.resources['maxObjects'].set(data['maxObjects'])
            self.root.resources['maxLocations'].set(data['maxLocations'])
            self.root.resources['maxCharacters'].set(data['maxCharacters'])
            self.root.resources['maxActions'].set(data['maxActions'])
            self.resources['objects'].clear()
            self.resources['locations'].clear()
            self.resources['characters'].clear()
            self.resources['actions'].clear()
            # replace the current data with the loaded data, as needed.
            for item in data['objects']:
                self.resources['objects'].append(StoryObjects.ObjectNode(name = item['name'],tags = item['tags'],internal_id = item['internal_id'],display_name = item['display_name'],description = item['description']))
            for item in data['locations']:
                self.resources['locations'].append(StoryObjects.LocationNode(name = item['name'],tags = item['tags'],internal_id = item['internal_id'],display_name = item['display_name'],description = item['description']))
            for item in data['characters']:
                self.resources['characters'].append(StoryObjects.CharacterNode(name = item['name'],biases = item['biases'], tags = item['tags'],start_timestep = item['start_timestep'],internal_id = item['internal_id'],display_name = item['display_name'],description = item['description']))
            for item in data['actions']:
                # incomplete, cannot transfer over effects_on_next_ws, required_test_list, and suggested_test_list
                self.resources['actions'].append(StoryNode.StoryNode(name = item['name'], biasweight=item['biasweight'], tags=item['tags'], charcount=item['charcount'], target_count=item['target_count'], timestep=item['timestep'], actor=item['actor'], target=item['target'], internal_id=item['internal_id']))
    
    def save_project(self):
        if(self.projectFile == None):
            self.save_project_as()
        else:
            with open(self.projectFile, mode="w") as file:
                saving_dict = self.dump_resources()
                file.write(json.dumps(saving_dict))

            print(file.name)

    def save_project_as(self):
        with filedialog.asksaveasfile(title="Save As...", filetypes = [("JSON files","*.json")], defaultextension=[("JSON files","*.json")]) as file:
            self.projectFile = file.name
            
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
       type(item) == StoryObjects.LocationNode or
       type(item) == StoryNode.StoryNode):
        return item.export_object_as_dict()