# Default Adjacent Locations - Connects
# Default Holding Item - Holds

import tkinter as tk
import tkinter.ttk as ttk
from interface.Resources import Resources

class Linkbox(ttk.Frame):
    def __init__(self, container):
        super().__init__(master=container, borderwidth=1, relief="solid")
        self.root = self.master.root 
        self.grid(column=0,row=1,padx=5, pady=5,sticky="news")

        self.rowconfigure(0,minsize=5,weight=1)
        self.rowconfigure(1,weight=700)

        self.boxLabel = tk.Label(self, text="Relations", font='Helvetica 9 bold')
        self.boxLabel.grid(column=0,row=0,sticky="ws")

        self.tagTable = ttk.Treeview(self)
        self.tagTable['columns'] = ('from','dir','to','name')

        self.tagTable.column("#0", width=0,  stretch=tk.NO)
        self.tagTable.column("from", width=150)
        self.tagTable.column("dir", anchor=tk.CENTER, width=50)
        self.tagTable.column("to", width=150)
        self.tagTable.column("name",width=150)

        self.tagTable.heading("#0",text="",anchor=tk.CENTER)
        self.tagTable.heading("from",text="Entity",anchor=tk.CENTER)
        self.tagTable.heading("dir",text="",anchor=tk.CENTER)
        self.tagTable.heading("to",text="Entity",anchor=tk.CENTER)
        self.tagTable.heading("name",text="Relation",anchor=tk.CENTER)

        self.tagTable.grid(column=0,row=1,padx=5,pady=5,sticky="nsew")
    
    def fetch(self, object):
        if object is None:
            return
        for item in self.tagTable.get_children():
            self.tagTable.delete(item)
        res: Resources = self.root.resources
        relations = res.getRelations()
        for rel in relations:
            relFromEntity = res.getEntityFromId(rel.get("fromEntityId"))
            relToEntity = res.getEntityFromId(rel.get("toEntityId"))
            if(relFromEntity != object and relToEntity != object):
                continue
            relConnection = res.getConnectionFromId(rel["connectionId"])
            if(relConnection["is2way"]):
                arrow = "<--->"
            else:
                arrow = "---->"
            self.tagTable.insert(parent='', index='end', values=(relFromEntity["name"], arrow, relToEntity["name"], relConnection["name"]))
        self.tagTable.insert(parent='',index='end',values=('','','',''))