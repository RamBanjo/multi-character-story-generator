import tkinter as tk

import tkinter.ttk as ttk
from application.components import StoryObjects

class ObjectsTab(ttk.Frame):
    def __init__(self,container):
        super().__init__(master=container, borderwidth=1, relief="solid")
        self.root = self.master.root
        self.grid(column=0, row=1, padx=0, pady=0, sticky="nsew")

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=30)
        self.rowconfigure(2,weight=1)
        self.columnconfigure(0,minsize=150,weight=1)
        self.columnconfigure(1,minsize=700,weight=50)

        self.label = ttk.Label(self, text=str("Select an Object."))
        self.label.grid(column=0, row=0, padx=0, pady=0, sticky="nsew")

        self.changeMaxBtn = ttk.Button(self,text=str("Change Maximum..."), command=self.openChangeMaximumWindow)
        self.changeMaxBtn.grid(column=0,row=2,padx=0,pady=0,sticky="nsew")

        self.listvar = []
        self.tklistvar = None
        self.listbox = None
        self.generate_listbox()

        self.descbox = Descbox(container=self)
    
    def items_selected(self, event):
        if(len(self.listbox.curselection()) > 0):
            # get all selected indices
            selected_indices = self.listbox.curselection()[0]
            # get selected items
            self.root.resources['objectDetail'] = self.root.resources['objects'][selected_indices]
            self.descbox.fetch()
    
    def clear_selected(self, event):
        if(len(self.listbox.curselection()) > 0):
            # get all selected indices
            selected_indices = self.listbox.curselection()[0]
            # get selected items (and clear it)
            self.root.resources['objects'][selected_indices].name = ""
            self.root.resources['objects'][selected_indices].tags = {'Type': 'Object'}
            self.root.resources['objects'][selected_indices].description = ""
            self.root.resources['objectDetail'] = self.root.resources['objects'][selected_indices]
            self.descbox.fetch()
    
    def generate_listbox(self):
        self.listvar.clear()
        objectList = self.root.resources['objects']
        for i in range(len(objectList)):
            self.listvar.append(str(objectList[i].internal_id)+': '+objectList[i].get_name())
        if(self.listbox != None):
            self.listbox.destroy()
        self.tklistvar = tk.Variable(value=self.listvar)
        self.listbox = tk.Listbox(self, relief="solid", listvariable=self.tklistvar)
        self.listbox.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")
        self.listbox.bind('<<ListboxSelect>>', self.items_selected)
        self.listbox.bind('')
    
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
        self.changeMaxEntry.insert(0,str(self.root.resources['maxObjects']))

        self.cancelChangeMax = ttk.Button(self.changeMaxLevel, text="Cancel", command=self.changeMaxLevel.destroy)
        self.cancelChangeMax.grid(column=1,row=2,sticky="nsew")
        self.okChangeMax = ttk.Button(self.changeMaxLevel, text="Submit", command=self.change_maximum)
        self.okChangeMax.grid(column=2,row=2,sticky="nsew")
    
    def change_maximum(self):
        val = self.changeMaxEntry.get()
        if(not val.isdigit()):
            ttk.Label(self.changeMaxLevel,text="Not a positive number.").grid(column=0,row=2,sticky="nsew")
        else:
            val = int(val)
            if(val < self.root.resources['maxObjects']):
                self.root.resources['objects'] = self.root.resources['objects'][0:val]
            else:
                while len(self.root.resources['objects']) < val:
                    self.root.resources['objects'].append(StoryObjects.ObjectNode(name="", internal_id=self.root.resources['maxObjects']+1))
                    self.root.resources['maxObjects'] = self.root.resources['maxObjects']+1
            self.generate_listbox()
            self.changeMaxLevel.destroy()

class Descbox(ttk.Frame):
    def __init__(self, container):
        super().__init__(master=container, borderwidth=1, relief="solid")
        self.root = self.master.root
        self.grid(column=1, row=0, rowspan=3, padx=5, pady=5, sticky="nsew")

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=20)
        self.columnconfigure(0,minsize=400,weight=60)
        self.columnconfigure(1,minsize=300,weight=1)

        self.generalsettings = GeneralSettingsBox(self)
        self.notes = NoteBox(self)
        self.taglist = Tagbox(self)
    
    def fetch(self):
        self.taglist.fetch()
        self.generalsettings.fetch()
        self.notes.fetch()

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

        self.tagTable.grid(column=0,row=1,padx=5,pady=5,sticky="nsew")
    
    def fetch(self):
        # first clear tagTable
        for i in self.tagTable.get_children():
            self.tagTable.delete(i)
        # add new tags of current object
        object = self.root.resources['objectDetail']
        if object != None:
            for key, value in object.tags.items():
                #if key != 'Type':
                    self.tagTable.insert(parent='', index='end', values=(key, value))

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
        self.typeLabel = tk.Label(self,text = "Type")
        self.typeLabel.grid(column=0,row=2,padx=5,pady=5,sticky="e")

        self.typeFlag = tk.StringVar(self, "1")
        self.itemButton = ttk.Radiobutton(self, text="Item",variable=self.typeFlag, value="1", command = lambda : self.update(None))
        self.itemButton.grid(column=1,row=2,padx=0,pady=5,sticky="nsew")
        self.locaButton = ttk.Radiobutton(self, text="Location",variable=self.typeFlag, value="2", command = lambda : self.update(None))
        self.locaButton.grid(column=2,row=2,padx=0,pady=5,sticky="nsew")
        self.charButton = ttk.Radiobutton(self, text="Character",variable=self.typeFlag, value="3", command = lambda : self.update(None))
        self.charButton.grid(column=3,row=2,padx=0,pady=5,sticky="nsew")

        self.nameVariable = tk.StringVar(self,"")
        self.nameEntry = tk.Entry(self,textvariable=self.nameVariable,width=47)
        self.nameEntry.grid(column=1,columnspan=3,row=1,sticky="ws")
        self.nameEntry.bind('<KeyRelease>', self.update)
    
    def fetch(self):
        object = self.root.resources['objectDetail']
        if object != None:
            self.nameVariable.set(object.name)
            if(object.tags["Type"] == "Object"):
                self.typeFlag.set("1")
            elif(object.tags["Type"] == "Location"):
                self.typeFlag.set("2")
            elif(object.tags["Type"] == "Character"):
                self.typeFlag.set("3")
        else:
            self.nameVariable.set("")
    
    def update(self, event):
        object = self.root.resources['objectDetail']
        object.set_name(self.nameVariable.get())
        if(self.typeFlag.get() == "1"):
            object.tags["Type"] = "Object"
        elif(self.typeFlag.get() == "2"):
            object.tags["Type"] = "Location"
        elif(self.typeFlag.get() == "3"):
            object.tags["Type"] = "Character"
        # TODO: convert object to the given StoryObject type
        # i.e. convert from an ObjectNode to a CharacterNode

        newObject = None
        if(self.typeFlag.get() == "1"):
            newObject = StoryObjects.ObjectNode(name=object.name, tags=object.tags, internal_id=object.internal_id, description=object.description)
        elif(self.typeFlag.get() == "2"):
            newObject = StoryObjects.LocationNode(name=object.name, tags=object.tags, internal_id=object.internal_id, description=object.description)
        elif(self.typeFlag.get() == "3"):
            newObject = StoryObjects.CharacterNode(name=object.name, tags=object.tags, internal_id=object.internal_id, description=object.description)
        self.root.resources['objectDetail'] = newObject
        self.master.master.generate_listbox()
        self.master.fetch()

class NoteBox(ttk.Frame):
    def __init__(self, container):
        super().__init__(master=container, borderwidth=1, relief="solid")
        self.root = self.master.root
        self.grid(column=0,row=1,padx=5, pady=5,sticky="news")

        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=100)

        self.noteLabel = tk.Label(self, text="Notes", font='Helvetica 9 bold', anchor='w')
        self.noteLabel.grid(column=0,row=0,padx=5,pady=5,sticky="sw")

        self.noteVariable = tk.StringVar(self,"")
        self.noteEntry = tk.Text(self, font='Helvetica 9')
        self.noteEntry.grid(column=0,row=1,padx=5,pady=5,sticky='nwse')
    
    def fetch(self):
        self.noteEntry.delete('1.0','end')
        object = self.root.resources['objectDetail']
        if object != None:
            self.noteEntry.insert('end',object.description)
    
    def update(self, event):
        object = self.root.resources['objectDetail']
        object.description = self.noteEntry.get('1.0','end')