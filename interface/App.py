import tkinter as tk
import tkinter.ttk as ttk
from interface import OptionFrame,ObjectFrame

class App(tk.Tk):
    
    def __init__(self):
        super().__init__()
        
        self.title(" Multi-Character Story Generator")
        self.geometry("900x600")

        optionFrame = OptionFrame.OptionFrame(self)
        optionFrame.pack(side='top',fill='x',padx=5,pady=2)

        objectFrame = ObjectFrame.ObjectFrame(self)
        objectFrame.pack(side='bottom',fill='both',expand=True,padx=5,pady=2)
    