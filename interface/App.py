import tkinter as tk
import tkinter.ttk as ttk
from interface import OptionFrame,ObjectFrame

class App(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.test = tk.IntVar()
        self.test.set(0)
        self.title(" Multi-Character Story Generator")
        self.geometry("900x600")

        self.optionFrame = OptionFrame.OptionFrame(self)
        self.optionFrame.pack(side='top',fill='x',padx=5,pady=2)

        self.objectFrame = ObjectFrame.ObjectFrame(self)
        self.objectFrame.pack(side='bottom',fill='both',expand=True,padx=5,pady=2)
    
    