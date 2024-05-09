import tkinter as tk
import tkinter.ttk as ttk
from interface.Resources import Resources

class RelInfobox(ttk.Frame):
    def __init__(self, container):
        super().__init__(master=container, borderwidth=1, relief="solid")
        self.root = self.master.root 
        self.grid(column=1,row=0,rowspan=2,padx=5, pady=5,sticky="news")

        self.boxLabel = tk.Label(self, text="Connection Info", font='Helvetica 9 bold')
        self.boxLabel.grid(column=0,row=0, columnspan=2,sticky="ws")
        
        self.nameLabel = tk.Label(self, text="Name")
        self.nameLabel.grid(column=0,row=1,sticky="es")
        self.nameVariable = tk.StringVar(self)
        self.nameEntry = tk.Entry(self, textvariable=self.nameVariable)
        self.nameEntry.grid(column=1,columnspan=3,row=1,sticky="new")

        self.paramsLabel = tk.Label(self,text="Params")
        self.paramsLabel.grid(column=0,row=2,sticky="es")
        self.paramsVariable = tk.StringVar(self)
        self.paramsEntry = tk.Entry(self, textvariable=self.paramsVariable)
        self.paramsEntry.grid(column=1,columnspan=3,row=2,sticky="new")

        self.arrowLabel = tk.Label(self, text="Direction")
        self.arrowLabel.grid(column=0,row=3,sticky="es")
        self.arrowOptions = ["---->","<--->"]
        self.arrowVariable = tk.StringVar(self)
        self.arrowMenu = tk.OptionMenu(self, self.arrowVariable,*self.arrowOptions)
        self.arrowMenu.grid(column=1,row=3, sticky="ne")

        self.nameEntry.bind('<KeyRelease>', self.update)
        self.paramsEntry.bind('<KeyRelease>', self.update)
        self.arrowVariable.trace_add("write", lambda a,b,c:self.update(None))

    def fetch(self, tag):
        self.relDetail = self.root.resources.getRelationFromId(int(tag[0]))
        con = self.relDetail.get("connection")
        self.nameVariable.set(con.get("name"))
        self.paramsVariable.set(con.get("params"))
        self.arrowVariable.set(tag[2])
    
    def update(self, event):
        
        if self.relDetail.get("connection") != None:
            self.relDetail["connection"]["name"] = self.nameVariable.get()
            self.relDetail["connection"]["params"] = self.paramsVariable.get()
            self.relDetail["connection"]["is2way"] = self.arrowVariable.get().startswith("<")

        
        self.master.master.fetch()
        self.master.fetch(self.master.master.objectDetail)