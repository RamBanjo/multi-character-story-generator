import tkinter as tk
import tkinter.ttk as ttk

class OptionFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(master=container, borderwidth=1, relief="solid")
        label = ttk.Label(self, text="This is the label which indicates where the Option Frame is.")
        label.pack(anchor="center", fill='x',padx=5,pady=5)