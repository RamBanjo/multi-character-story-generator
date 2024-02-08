import tkinter as tk
from tkinter import ttk

from interface.subframes.etab.GeneralSettingsBox import GeneralSettingsBox
from interface.subframes.etab.Notebox import NoteBox
from interface.subframes.etab.Tagbox import Tagbox

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