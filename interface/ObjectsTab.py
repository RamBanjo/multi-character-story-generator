import tkinter as tk
import tkinter.ttk as ttk
from application.components import StoryObjects

class ObjectsTab(ttk.Frame):
    def __init__(self,container):
        super().__init__(master=container, borderwidth=1, relief="solid")
        self.grid(column=0, row=1, padx=0, pady=0, sticky="nsew")

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=30)
        self.columnconfigure(0,minsize=150,weight=1)
        self.columnconfigure(1,minsize=700,weight=50)

        self.label = ttk.Label(self, text=str("Select an Object."))
        self.label.grid(column=0, row=0, padx=0, pady=0, sticky="nsew")

        self.listvar = []
        self.tklistvar = None
        self.listbox = None
        self.generate_listbox()

        self.descbox = Descbox(container=self)
    
    def items_selected(self, event):
        # get all selected indices
        selected_indices = self.listbox.curselection()[0]
        # get selected items
        if(selected_indices < len(self.master.master.resources['objects'])):
            self.master.master.resources['objectDetail'] = self.master.master.resources['objects'][selected_indices]
        else:
            self.add_item()
    
    def generate_listbox(self):
        self.listvar.clear()
        objectList = self.master.master.resources['objects']
        for i in range(len(objectList)):
            self.listvar.append(str(i)+': '+objectList[i].get_name())
        self.listvar.append("-- Add New --")
        if(self.listbox != None):
            self.listbox.destroy()
        self.tklistvar = tk.Variable(value=self.listvar)
        self.listbox = tk.Listbox(self, borderwidth=1, relief="solid", listvariable=self.tklistvar)
        self.listbox.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")
        self.listbox.bind('<<ListboxSelect>>', self.items_selected)
    
    def add_item(self): #triggered through selecting "-- Add New --"
        objectList = self.master.master.resources['objects']
        objectList.append(StoryObjects.ObjectNode(name=""))
        self.generate_listbox()

class Descbox(ttk.Frame):
    def __init__(self, container):
        super().__init__(master=container, borderwidth=1, relief="solid")
        self.grid(column=1, row=0, rowspan=2, padx=5, pady=5, sticky="nsew")

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=20)
        self.columnconfigure(0,minsize=400,weight=60)
        self.columnconfigure(1,minsize=300,weight=1)

        self.generalsettings = GeneralSettingsBox(self)

        self.objsettings = tk.Frame(self, borderwidth=1, relief="solid")
        self.objsettings.grid(column=0,row=1,padx=5, pady=5,sticky="news")

        self.taglist = Tagbox(self)

class Tagbox(ttk.Frame):
    def __init__(self, container):
        super().__init__(master=container, borderwidth=1, relief="solid")
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

        self.tagTable.insert(parent='',index='end',values=("Type","Object"))
        self.tagTable.grid(column=0,row=1,padx=5,pady=5,sticky="nsew")

class GeneralSettingsBox(ttk.Frame):
    def __init__(self, container):
        super().__init__(master=container, borderwidth=1, relief="solid")
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
        self.itemButton = ttk.Radiobutton(self, text="Item",variable=self.typeFlag, value="1")
        self.itemButton.grid(column=1,row=2,padx=0,pady=5,sticky="nsew")
        self.locaButton = ttk.Radiobutton(self, text="Location",variable=self.typeFlag, value="2")
        self.locaButton.grid(column=2,row=2,padx=0,pady=5,sticky="nsew")
        self.charButton = ttk.Radiobutton(self, text="Character",variable=self.typeFlag, value="3")
        self.charButton.grid(column=3,row=2,padx=0,pady=5,sticky="nsew")

        self.nameVariable = tk.StringVar(self,"")
        self.nameEntry = tk.Entry(self,textvariable=self.nameVariable,width=47)
        self.nameEntry.grid(column=1,columnspan=3,row=1,sticky="ws")