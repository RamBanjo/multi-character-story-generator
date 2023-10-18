import tkinter as tk
import tkinter.ttk as ttk

class PlaceholdingFrame(ttk.Frame):
    def __init__(self,container):
        super().__init__(master=container, borderwidth=1, relief="solid")
        self.label = ttk.Label(self, text=str("This frame is a placeholder for something."))
        self.label.pack(anchor="center", fill='x',padx=1,pady=1)