import tkinter as tk
import tkinter.ttk as ttk
from interface.subframes.wstab.Descbox import Descbox

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
        return
    
    def items_selected(self, event):
        return