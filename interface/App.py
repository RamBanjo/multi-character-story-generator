import tkinter as tk
import tkinter.ttk as ttk
from interface import ObjectFrame,OptionFrame,PlaceholdingFrame

class App(tk.Tk):
    
    def __init__(self):
        super().__init__()
        
        self.resources = {
            'test': tk.IntVar(value=0),
            'optionNumber': tk.IntVar(value=-1),
            'btnLabels' : ["Objects","Actions","World State","Rules","Tasks","Initial Graph","Generate"]
        }

        self.title(" Multi-Character Story Generator")
        self.geometry("900x600")

        menu = tk.Menu(self, tearoff=0)
        filemenu = tk.Menu(menu,tearoff=0)
        filemenu.add_command(label="New")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menu.add_cascade(label="File",menu=filemenu)
        self.config(menu=menu)

        self.resources['objectFrames'] = {
            9: ObjectFrame.InitialFrame(self)
        }

        self.objectFrame = self.resources['objectFrames'][9]
        for i in range(7):
            self.resources['objectFrames'][i] = ObjectFrame.NumberedFrame(self.objectFrame,i)

        self.optionFrame = OptionFrame.OptionFrame(self)
        self.optionFrame.pack(side='top',fill='x',padx=5,pady=2)
    
    def increment(self, event=None):
        old_value = int(self.resources['test'].get())
        result = old_value + 1
        self.resources['test'].set(result)
        self.objectFrame.label.config(text=str(result))
    
    def changeOptionNumber(self, i):
        self.resources['optionNumber'].set(i)
        self.objectFrame.label.config(text="Button: "+str(i))
        self.resources['objectFrames'][i].tkraise()
