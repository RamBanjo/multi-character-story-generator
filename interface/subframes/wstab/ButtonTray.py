import tkinter as tk
import tkinter.ttk as ttk
from interface.subframes.wstab.DetailedViewTopLevel import DetailedViewTopLevel

class ButtonTray(ttk.Frame):
    def __init__(self, container, targetCanvas):
        super().__init__(master=container, borderwidth=1, padding=1)
        self.pack(side='top', expand=False, fill='x')
        self.root = self.master.root
        self.addObjectBtn = ttk.Button(self, text="Add Entity", command= lambda: self.onClickAddEntity())
        self.addObjectBtn.grid(row=0,column=0,padx=1,pady=0)
        self.detailedBtn = ttk.Button(self, text="Detailed View", command= lambda: self.onClickDetailedView())
        self.detailedBtn.grid(row=0,column=1, padx=1,pady=0)
        self.targetCanvas = targetCanvas
    
    def onClickAddEntity(self):
        self.topLevel = tk.Toplevel(self)
    
    def onClickDetailedView(self):
        self.topLevel = DetailedViewTopLevel(self)