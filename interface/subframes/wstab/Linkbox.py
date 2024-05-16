# Default Adjacent Locations - Connects
# Default Holding Item - Holds

import tkinter as tk
import tkinter.ttk as ttk
from interface.Resources import Resources
from interface.subframes.wstab.CreateRelationFrame import CreateRelationFrame

class Linkbox(ttk.Frame):
    def __init__(self, container):
        super().__init__(master=container, borderwidth=1, relief="solid")
        self.root = self.master.root 
        self.grid(column=0,row=1,padx=5, pady=5,sticky="news")

        self.rowconfigure(0,minsize=5,weight=1)
        self.rowconfigure(1,weight=700)

        self.boxLabel = tk.Label(self, text="Relations", font='Helvetica 9 bold')
        self.boxLabel.grid(column=0,row=0,sticky="ws")

        self.addRelBtn = tk.Button(self, text="Add New", font="Helvetica 9 bold", command= self.onBtn)
        self.addRelBtn.grid(column=1,row=0,sticky="es")

        self.tagTable = ttk.Treeview(self)
        self.tagTable['columns'] = ('num','from','dir','to','name')

        self.tagTable.column("#0", width=0,  stretch=tk.NO)
        self.tagTable.column("num",width=0,  stretch=tk.NO)
        self.tagTable.column("from", width=150)
        self.tagTable.column("dir", anchor=tk.CENTER, width=50)
        self.tagTable.column("to", width=150)
        self.tagTable.column("name",width=150)

        self.tagTable.heading("#0",text="",anchor=tk.CENTER)
        self.tagTable.heading("num",text="",anchor=tk.CENTER)
        self.tagTable.heading("from",text="Entity",anchor=tk.CENTER)
        self.tagTable.heading("dir",text="",anchor=tk.CENTER)
        self.tagTable.heading("to",text="Entity",anchor=tk.CENTER)
        self.tagTable.heading("name",text="Relation",anchor=tk.CENTER)

        self.tagTable.bind("<ButtonRelease-1>", self.onClick)
        self.tagTable.bind("<Delete>", self.onDelete)
        self.tagTable.grid(column=0,row=1,columnspan=2,padx=5,pady=5,sticky="nsew")
    
    def fetch(self, object):
        if object is None:
            return
        self.root.objectDetail = object
        for item in self.tagTable.get_children():
            self.tagTable.delete(item)
        res: Resources = self.root.resources
        relations = res.getRelations()
        for i in range(len(relations)):
            rel = relations[i]
            relFromEntity = res.getEntityFromId(rel.get("fromEntityId"))
            relToEntity = res.getEntityFromId(rel.get("toEntityId"))
            if(relFromEntity != object and relToEntity != object):
                continue
            relConnection = rel.get("connection")
            if(relConnection["is2way"]):
                arrow = "<--->"
            else:
                arrow = "---->"
            self.tagTable.insert(parent='', index='end', values=(i, relFromEntity["name"], arrow, relToEntity["name"], relConnection["name"]))
    
    def onClick(self, event):
        if(len(self.tagTable.selection()) == 0):
            return
        tag = self.tagTable.item(self.tagTable.selection()[0],'values')
        print(tag)
        self.master.relinfobox.fetch(tag)
        return

    def onDelete(self, event):
        tag = self.tagTable.item(self.tagTable.selection()[0],'values')
        del self.root.resources.getRelations()[int(tag[0])]
        self.fetch(self.root.objectDetail)

    def onBtn(self):
        self.topLevel = tk.Toplevel(self)
        self.createRelFrame = CreateRelationFrame(self.topLevel)