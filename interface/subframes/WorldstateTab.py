import tkinter as tk

import tkinter.ttk as ttk
from interface import UtilDefaults,UtilFunctions
from application.components import WorldState, StoryNode, StoryObjects

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

class WorldStateTab(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.root = self.master.root
        self.grid(column=0, row=1, padx=0, pady=0, sticky="nsew")

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=30)

        self.canvas = WorldStateCanvas(self) #note: packed geometry, cannot grid shit
        self.buttons = ButtonTray(self, self.canvas)
        self.ws = self.root.resources['worldState'].get()

class WorldStateCanvas(tk.Canvas):
    def __init__(self, container):
        super().__init__(master=container, width=600, height=400, bg='white')
        self.root = self.master.root
        self.pack(side='bottom', expand=True, fill="both")
        self.create_text((300,100), text=self.root.resources['worldState'].get().name, fill="orange", font='tkDefaeultFont 24')

class DropdownTabController():
    def __init__(self, master, root):
        # note: this is not a Tk class, so it is not in the tree. It will still inherit some attributes, but it does not get gridded.
        self.root = root
        self.objectTab = DropdownTab(master,self.root.resources['objects'], "Add Object", self)
        self.locationTab = DropdownTab(master,self.root.resources['locations'], "Add Location", self)
        self.characterTab = DropdownTab(master,self.root.resources['characters'], "Add Character", self)

        self.tabs = [self.objectTab,self.locationTab,self.characterTab]
        self.currentTab = 0
        self.tkraise()
    
    def tkraise(self):
        self.tabs[self.currentTab].tkraise()

    def reset(self):
        self.currentTab = 0
        self.objectTab.reset()
        self.locationTab.reset()
        self.characterTab.reset()
        self.tkraise() 

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

class ButtonTray(ttk.Frame):
    def __init__(self, container, targetCanvas):
        super().__init__(master=container, borderwidth=1, padding=1)
        self.pack(side='top', expand=False, fill='x')
        self.root = self.master.root
        self.addObjectBtn = ttk.Button(self, text="Add Entity", command= lambda: self.onClickAddEntity())
        self.addObjectBtn.grid(row=0,column=0,padx=1,pady=0)
        self.detailedBtn = ttk.Button(self, text="Detailed View", command= lambda: self.onClickDetailedView())
        self.detailedBtn.grid(row=0,column=1, padx=1,pady=0)
        self.targetCanvas = targetCanvas
    
    def onClickAddEntity(self):
        self.topLevel = tk.Toplevel(self)
        self.dropdowntab = DropdownTabController(self.topLevel, self.root)
    
    def onClickDetailedView(self):
        self.topLevel = DetailedViewTopLevel(self)

class DetailedViewTopLevel(tk.Toplevel):
    def __init__(self, container):
        super().__init__(container)
        self.root = self.master.root

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=30)
        self.rowconfigure(2,weight=1)
        self.columnconfigure(0,minsize=150,weight=1)
        self.columnconfigure(1,minsize=700,weight=50)

        self.entityLabel = ttk.Label(self, text="Entities")
        self.entityLabel.grid(column=0,row=0)

        self.listvar = []
        self.tklistvar = None
        self.listbox = None
        self.descbox = Descbox(self)
        self.generate_listbox() #instantiates the listbox, of course.
    
    def generate_listbox(self):
        # 1. fetch all entities (IN WS) and put them in a list.
        # 3. bind the list with item_selected()
        self.listvar.clear()
        for entity in self.root.resources['worldState'].get().objectnodes:
            self.listvar.append(entity.name)
        # 2. create a listbox with that list and grid it.
        self.tklistvar = tk.Variable(value=self.listvar)
        self.listbox = tk.Listbox(self, relief="solid", listvariable=self.tklistvar)
        self.listbox.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")
        self.listbox.bind('<<ListboxSelect>>', self.items_selected)
    
    def items_selected(self, event):
        if(len(self.listbox.curselection()) > 0):
            # get all selected indices
            selected_indices = self.listbox.curselection()[0]
            # get selected item
            name = self.listbox.get(selected_indices,selected_indices)
            self.root.objectDetail = self.root.resources['worldState'].get().node_dict[name[0]]
            self.descbox.fetch()

class Descbox(ttk.Frame):
    def __init__(self, container):
        super().__init__(master=container)
        self.root = self.master.root
        self.grid(column=1, row=0, rowspan=3, padx=5, pady=5, sticky="nsew")

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=20)
        self.columnconfigure(0,minsize=400,weight=60)
        self.columnconfigure(1,minsize=300,weight=1)

        self.generalsettings = GeneralSettingsBox(self)
        self.taglist = Tagbox(self)

    def fetch(self):
        self.taglist.fetch()
        self.generalsettings.fetch()
    
    def reset(self):
        self.taglist.reset()
        self.generalsettings.reset()

class GeneralSettingsBox(ttk.Frame):
    def __init__(self, container):
        super().__init__(master=container, borderwidth=1, relief="solid")
        self.root = self.master.root
        self.grid(column=0,row=0,padx=5, pady=5,sticky="news")

        self.columnconfigure([0,1,2,3],weight=1)
        self.rowconfigure([0,1],minsize=5,weight=1)
        self.rowconfigure(2,weight=30)

        self.boxLabel = tk.Label(self, text="General Settings", font='Helvetica 9 bold')
        self.boxLabel.grid(column=0,columnspan=4,row=0,sticky="ws")
        self.nameLabel = tk.Label(self, text="Name")
        self.nameLabel.grid(column=0,row=1,sticky="es")

        self.nameVariable = tk.StringVar(self,"")
        self.nameEntry = tk.Entry(self,textvariable=self.nameVariable,width=47)
        self.nameEntry.grid(column=1,columnspan=3,row=1,sticky="ws")
        self.nameEntry.bind('<KeyRelease>', self.update)
    
    def fetch(self):
        object = self.root.objectDetail
        if object != None:
            self.nameVariable.set(object.name)
        else:
            self.nameVariable.set("")
    
    def update(self, event):
        object = self.root.objectDetail
        if object != None:
            object.set_name(self.nameVariable.get())
        # TODO: convert object to the given StoryObject type
        # i.e. convert from an ObjectNode to a CharacterNode

        self.master.master.generate_listbox()
        self.master.fetch()
    
    def reset(self):
        self.nameVariable.set("")

class Tagbox(ttk.Frame):
    def __init__(self, container):
        super().__init__(master=container, borderwidth=1, relief="solid")
        self.root = self.master.root
        self.grid(column=1,row=0,rowspan=2,padx=5, pady=5,sticky="news")

        self.rowconfigure(0,minsize=5,weight=1)
        self.rowconfigure(1,weight=700)

        self.boxLabel = tk.Label(self, text="Traits", font='Helvetica 9 bold')
        self.boxLabel.grid(column=0,row=0,sticky="ws")

        self.tagTable = ttk.Treeview(self)
        self.tagTable['columns'] = ('type', 'content')

        self.tagTable.column("#0", width=0,  stretch=tk.NO)
        self.tagTable.column("type", anchor=tk.CENTER, width=100)
        self.tagTable.column("content", anchor=tk.CENTER, width=200)

        self.tagTable.heading("#0",text="",anchor=tk.CENTER)
        self.tagTable.heading("type",text="Tag",anchor=tk.CENTER)
        self.tagTable.heading("content",text="Content",anchor=tk.CENTER)

        self.tagTable.bind("<Double-1>", self.onDoubleClick)
        self.tagTable.bind("<Delete>", self.onDelete)
        self.tagTable.grid(column=0,row=1,padx=5,pady=5,sticky="nsew")
    
    def fetch(self):
        # first clear tagTable
        for i in self.tagTable.get_children():
            self.tagTable.delete(i)
        # add new tags of current object
        object = self.root.objectDetail
        if object != None:
            # TODO: add law/moral bias for character nodes
            if isinstance(object,StoryObjects.CharacterNode):
                self.tagTable.insert(parent='', index='end', values=("Law Bias", object.biases["lawbias"]))
                self.tagTable.insert(parent='', index='end', values=("Moral Bias", object.biases["moralbias"]))
            for key, value in object.tags.items():
                if key != 'Type':
                    self.tagTable.insert(parent='', index='end', values=(key, value))
            self.tagTable.insert(parent='',index='end',values=('',''))
    
    def onDoubleClick(self, event):
        self.tag = self.tagTable.item(self.tagTable.selection()[0],'values')
        if(self.tag[0] != "Law Bias" and self.tag[0] != "Moral Bias"):
            self.openChangeTagWindow()
    
    def openChangeTagWindow(self):
        self.changeTags = tk.Toplevel(self)
        self.changeTags.minsize(400,50)
        self.changeTags.columnconfigure(0,minsize=200,weight=0)
        self.changeTags.columnconfigure([1,2],weight=100)
        self.changeTags.resizable(False,False)

        self.changeTagnameLabel = ttk.Label(self.changeTags, text="Tag")
        self.changeTagnameLabel.grid(column=0,row=0,padx=5,pady=5,sticky="nsew")
        self.changeTagnameEntry = ttk.Entry(self.changeTags)
        self.changeTagnameEntry.grid(column=0,row=1,padx=5,pady=5,sticky="nsew")
        self.changeTagnameEntry.insert(0,str(self.tag[0]))

        self.changeTagvalueLabel = ttk.Label(self.changeTags, text="Value")
        self.changeTagvalueLabel.grid(column=1,row=0,padx=5,pady=5,sticky="nsew")
        self.changeTagvalueEntry = ttk.Entry(self.changeTags)
        self.changeTagvalueEntry.grid(column=1,row=1,padx=5,pady=5,sticky="nsew")
        self.changeTagvalueEntry.insert(0,str(self.tag[1]))

        self.cancelChangeMax = ttk.Button(self.changeTags, text="Cancel", command=self.changeTags.destroy)
        self.cancelChangeMax.grid(column=1,row=2,sticky="nsew")
        self.okChangeMax = ttk.Button(self.changeTags, text="Submit", command=self.change_tags)
        self.okChangeMax.grid(column=2,row=2,sticky="nsew")
    
    def change_tags(self):
        newTagName = self.changeTagnameEntry.get()
        newTagValue = self.changeTagvalueEntry.get()
        object = self.root.objectDetail
        if(newTagName == '' and self.tag[0] == ''): #nothing lost, nothing gained
            self.changeTags.destroy()
        elif(newTagName == "Type"):
            ttk.Label(self.changeTags,text="Cannot change Type attribute.").grid(column=0,row=2,sticky="nsew")
        elif(self.tag[0] == newTagName): #change only the value
            object.tags[newTagName] = newTagValue
            self.fetch()
            self.changeTags.destroy()
        else: #remove the old tag, create the new tag
            if(self.tag[0] != ''): #THERE IS AN OLD TAG
                del object.tags[self.tag[0]]
            if(newTagName != ''): #THERE IS A NEW TAG
                object.tags[newTagName] = newTagValue
                print("Add tag",newTagName,"to",object)
            self.fetch()
            self.changeTags.destroy()

    def onDelete(self, event):
        self.tag = self.tagTable.item(self.tagTable.selection()[0],'values')
        self.delete_tag()

    def delete_tag(self):
        object = self.root.objectDetail
        del object.tags[self.tag[0]]
        self.fetch()
    
    def reset(self):
        for i in self.tagTable.get_children():
            self.tagTable.delete(i)