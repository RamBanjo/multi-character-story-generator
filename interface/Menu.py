import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import json

from application.components import StoryObjects,StoryNode


class Menu(tk.Menu):
    def __init__(self, container):
        super().__init__(master=container, tearoff=0)
        self.root = self.master.root
        self.filemenu = tk.Menu(self,tearoff=0)
        self.add_cascade(label="File",menu=self.filemenu)
        
        self.filemenu.add_command(label="New", command=self.reset)
        self.filemenu.add_command(label="Open")
        self.filemenu.add_command(label="Save")
        self.filemenu.add_command(label="Save As...")
        self.filemenu.add_command(label="Export As...")
        self.filemenu.add_command(label="Quit", command=container.quit)

        self.projectFile = None
    
    def reset(self) -> None:
        self.root.reset()
