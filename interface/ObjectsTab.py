import tkinter as tk

import tkinter.ttk as ttk
from application.components import StoryObjects

class EntityTabController():
    def __init__(self, master):
        # note: this is not a Tk class, so it is not in the tree. It will still inherit some attributes, but it does not get gridded.
        self.root = master.root
        self.objectTab = EntityTab(master,self.root.resources['objects'], self.root.resources['maxObjects'], self)
        self.locationTab = EntityTab(master,self.root.resources['locations'], self.root.resources['maxLocations'], self)
        self.characterTab = EntityTab(master,self.root.resources['characters'], self.root.resources['maxCharacters'], self)

        self.tabs = [self.objectTab,self.locationTab,self.characterTab]
        self.currentTab = 0
    
    def tkraise(self):
        self.tabs[self.currentTab].tkraise()

    def reset(self):
        self.currentTab = 0
        self.objectTab.reset()
        self.locationTab.reset()
        self.characterTab.reset()
        self.tkraise() 

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
        self.controller.currentTab = tabNumber
        self.controller.tkraise()

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
            self.root.resources['objectDetail'] = self.entityResource[selected_indices]
            self.descbox.fetch()
    
    def clear_selected(self, event):
        if(len(self.listbox.curselection()) > 0):
            # get all selected indices
            selected_indices = self.listbox.curselection()[0]
            # get selected items (and clear it)
            self.entityResource[selected_indices].name = ""
            self.entityResource[selected_indices].tags = {'Type': 'Object'}
            self.entityResource[selected_indices].description = ""
            self.root.resources['objectDetail'] = self.entityResource[selected_indices]
            self.descbox.fetch()
    
    def generate_listbox(self):
        self.listvar.clear()
        objectList = self.entityResource
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
            if(val < self.maxEntityResource.get()):
                self.entityResource = self.entityResource[0:val]
            else:
                while len(self.entityResource) < val:
                    self.entityResource.append(StoryObjects.ObjectNode(name="", internal_id=self.maxEntityResource.get()+1))
                    self.maxEntityResource.set(self.maxEntityResource.get()+1)
            self.generate_listbox()
            self.changeMaxLevel.destroy()

    def reset(self):
        self.generate_listbox()
        print(len(self.entityResource))
        print(self.maxEntityResource.get())
        self.descbox.reset()

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
        self.notes = NoteBox(self)
        self.taglist = Tagbox(self)
    
    def fetch(self):
        self.taglist.fetch()
        self.generalsettings.fetch()
        self.notes.fetch()
    
    def reset(self):
        self.taglist.reset()
        self.generalsettings.reset()
        self.notes.reset()

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
        object = self.root.resources['objectDetail']
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
        object = self.root.resources['objectDetail']
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
            self.fetch()
            self.changeTags.destroy()

    def onDelete(self, event):
        self.tag = self.tagTable.item(self.tagTable.selection()[0],'values')
        self.delete_tag()

    def delete_tag(self):
        object = self.root.resources['objectDetail']
        del object.tags[self.tag[0]]
        self.fetch()
    
    def reset(self):
        for i in self.tagTable.get_children():
            self.tagTable.delete(i)

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
        object = self.root.resources['objectDetail']
        if object != None:
            self.nameVariable.set(object.name)
        else:
            self.nameVariable.set("")
    
    def update(self, event):
        object = self.root.resources['objectDetail']
        if object != None:
            object.set_name(self.nameVariable.get())
        # TODO: convert object to the given StoryObject type
        # i.e. convert from an ObjectNode to a CharacterNode

        self.master.master.generate_listbox()
        self.master.fetch()
    
    def reset(self):
        self.nameVariable.set("")

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
    
    def reset(self):
        self.noteEntry.delete('1.0','end')