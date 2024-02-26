import tkinter as tk
from tkinter import ttk

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
        self.noteEntry.bind('<KeyRelease>', self.update)
    
    def fetch(self):
        self.noteEntry.delete('1.0','end')
        object = self.master.master.objectDetail
        if object.get("notes") != None:
            self.noteEntry.insert('end',object.get("notes"))
    
    def update(self, event):
        if(self.master.master.objectDetail.get("notes") != None):
            self.master.master.objectDetail["notes"] = self.noteEntry.get('1.0','end')
    
    def reset(self):
        self.noteEntry.delete('1.0','end')