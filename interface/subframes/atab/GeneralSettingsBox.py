import tkinter as tk
import tkinter.ttk as ttk

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
