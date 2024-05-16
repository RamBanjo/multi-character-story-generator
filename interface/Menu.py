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
        
        self.filemenu.add_command(label="New", command=self.new)
        self.filemenu.add_command(label="Import", command=self.importResource)
        self.filemenu.add_command(label="Export", command=self.exportResource)
        self.filemenu.add_command(label="Quit", command=container.quit)
    
    def new(self) -> None:
        self.root.clear()
    
    def exportResource(self) -> None:
        fileFormat = [('JSON Object', '*.json')]
        filename = filedialog.asksaveasfilename(filetypes=fileFormat, defaultextension=fileFormat)

        if(not filename):
            return
        file = open(filename,mode="w")
        file.write(json.dumps(self.root.resources.getResourceDict(), ensure_ascii=False, indent=2))
        
        file.close()

    def importResource(self) -> None:
        fileFormat = [('JSON Object', '*.json')]
        filename = filedialog.askopenfilename(filetypes=fileFormat, defaultextension=fileFormat)

        if(not filename):
            return
        
        file = open(filename,mode="r")
        self.root.resources.setResourceDict(json.loads(file.read()))
        file.close()
        self.root.changeOptionNumber(0)