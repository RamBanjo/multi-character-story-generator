import tkinter as tk
import tkinter.ttk as ttk

from interface.OptionButton import OptionButton

btnLabels = ["Objects","Actions","World State","Rules","Tasks","Initial Graph","Generate"]

class OptionFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(master=container, borderwidth=1, relief="solid")
        self.btn = OptionButton(self, "Test Button", cmd=self.increment)
        self.btn.pack(side="left",padx=5,pady=1)
    
    def increment(self):
        try:
            old_value = int(self.master.test.get())
            result = old_value + 1
            self.master.test.set(result)
            self.master.objectFrame.label.config(text=str(result))
        except ValueError:
            print("How.")