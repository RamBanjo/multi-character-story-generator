import tkinter as tk
import tkinter.ttk as ttk

from interface.OptionButton import OptionButton

btnLabels = ["Objects","Actions","World State","Rules","Tasks","Initial Graph","Generate"]

class OptionFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(master=container, borderwidth=1, relief="solid")
        ####loe
        self.btn = []
        for i in range(len(btnLabels)):
            self.btn.append(OptionButton(self, name=btnLabels[i],btnIdx=i))
            self.btn[i].pack(side="left",padx=5,pady=1)
        ####loe