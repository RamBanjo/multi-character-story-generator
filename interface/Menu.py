import tkinter as tk
import tkinter.ttk as ttk

class Menu(tk.Menu):
    def __init__(self, container):
        super().__init__(master=container, tearoff=0)
        self.filemenu = tk.Menu(self,tearoff=0)
        self.add_cascade(label="File",menu=self.filemenu)
        
        self.filemenu.add_command(label="New")
        self.filemenu.add_command(label="Open")
        self.filemenu.add_command(label="Save")
        self.filemenu.add_command(label="Save As...")
        self.filemenu.add_command(label="Export As...")
        self.filemenu.add_command(label="Quit", command=container.quit)

