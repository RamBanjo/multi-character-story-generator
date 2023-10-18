import tkinter as tk
import tkinter.ttk as ttk
from interface import ObjectFrame,OptionFrame,Menu

class App(tk.Tk):
    
    def __init__(self):
        super().__init__()
        
        self.resources = {
            'test': tk.Variable(value=["Alice", "Bob", "Charlie", "Dugson", "Edison", "Florence", "Giraffa", "Hector", "Ivan", "Jello"]),
            'optionNumber': tk.IntVar(value=-1),
            'btnLabels' : ["Objects","Actions","World State","Rules","Tasks","Initial Graph","Generate"]
        }

        self.title(" Multi-Character Story Generator")
        self.geometry("900x600")

        menu = Menu.Menu(self)
        self.config(menu=menu)

        self.resources['objectFrames'] = {
            9: ObjectFrame.InitialFrame(self)
        }
        self.objectFrame = self.resources['objectFrames'][9]
        self.resources['objectFrames'][0] = ObjectFrame.ObjectsTab(self.objectFrame)
        for i in range(1,7):
            self.resources['objectFrames'][i] = ObjectFrame.NumberedFrame(self.objectFrame,i)
        self.resources['objectFrames'][8] = ObjectFrame.PlaceholdingFrame(self.objectFrame)
        self.resources['objectFrames'][8].grid(column=0, row=1, padx=0, pady=0, sticky="nsew")

        self.optionFrame = OptionFrame.OptionFrame(self)
        self.optionFrame.pack(side='top',fill='x',padx=5,pady=2)
    
    def changeOptionNumber(self, i):
        self.resources['optionNumber'].set(i)
        self.objectFrame.label.config(text=self.resources['btnLabels'][i])
        self.resources['objectFrames'][i].tkraise()
