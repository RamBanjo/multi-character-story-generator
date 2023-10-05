import tkinter as tk
import tkinter.ttk as ttk

class ObjectFrame(ttk.Frame):
    def __init__(self,container):
        super().__init__(master=container, borderwidth=1, relief="solid")
        self.label = ttk.Label(self, text="0")
        self.label.pack(anchor="center", fill='x',padx=1,pady=1)