import tkinter as tk
import tkinter.ttk as ttk
from interface.subframes.wstab.RelInfobox import RelInfobox
from interface.subframes.wstab.GeneralSettingsBox import GeneralSettingsBox
from interface.subframes.wstab.Linkbox import Linkbox

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
        self.linkbox = Linkbox(self)
        self.relinfobox = RelInfobox(self)

    def fetch(self, objectDetail):
        self.generalsettings.fetch(objectDetail)
        self.linkbox.fetch(objectDetail)
    
    def reset(self):
        self.generalsettings.reset()
