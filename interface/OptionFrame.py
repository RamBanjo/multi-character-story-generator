import tkinter as tk
import tkinter.ttk as ttk

from interface.OptionButton import OptionButton

btnLabels = ["Objects","Actions","World State","Rules","Tasks","Initial Graph","Generate"]

class OptionFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(master=container, borderwidth=1, relief="solid")
        for label in btnLabels:
            btn = OptionButton(container=self, name=label)
            btn.pack(side="left",padx=1,pady=1)
        