import tkinter as tk
import tkinter.ttk as ttk
from interface import OptionFrame,ObjectFrame

class App(tk.Tk):
    
    def __init__(self):
        super().__init__()
        
        self.resources = {
            'test': tk.IntVar(value=0),
            'optionNumber': tk.IntVar(value=-1)
        }

        self.title(" Multi-Character Story Generator")
        self.geometry("900x600")

        self.objectFrame = ObjectFrame.ObjectFrame(self)
        self.objectFrame.pack(side='bottom',fill='both',expand=True,padx=5,pady=2)

        self.optionFrame = OptionFrame.OptionFrame(self)
        self.optionFrame.pack(side='top',fill='x',padx=5,pady=2)
    
    def increment(self, event=None):
        old_value = int(self.resources['test'].get())
        result = old_value + 1
        self.resources['test'].set(result)
        self.objectFrame.label.config(text=str(result))
    
    def changeOptionNumber(self, i):
        self.resources['optionNumber'].set(i)
        self.objectFrame.label.config(text="Button: "+str(i+1))