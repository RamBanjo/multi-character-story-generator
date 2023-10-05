import tkinter as tk
import tkinter.ttk as ttk

class OptionButton(ttk.Button):
    def __init__(self, container, name, cmd = None):
        super().__init__(master=container, default='normal', text=name, command=cmd)