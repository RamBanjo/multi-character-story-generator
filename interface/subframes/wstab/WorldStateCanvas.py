import tkinter as tk

class WorldStateCanvas(tk.Canvas):
    def __init__(self, container):
        super().__init__(master=container, width=600, height=400, bg='white')
        self.root = self.master.root
        self.pack(side='bottom', expand=True, fill="both")