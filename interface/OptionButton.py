import tkinter as tk
import tkinter.ttk as ttk

class OptionButton(ttk.Button):
    def __init__(self, container, name, btnIdx):
        super().__init__(master=container, default='normal', text=name)
        def btnCmd():
            container.master.changeOptionNumber(btnIdx)
        self.config(command=btnCmd)