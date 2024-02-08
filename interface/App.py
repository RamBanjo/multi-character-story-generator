import tkinter as tk
import tkinter.ttk as ttk
from interface import ObjectFrame,OptionFrame,Menu,UtilDefaults,UtilFunctions,Mock
from interface.subframes import ActionsTab,WorldStateTab,ObjectsTab,EntityTabController
from application.components import StoryObjects,StoryNode, WorldState

pageNumber = 9

class App(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.root = self

        self.btnLabels = ["Entities","World State","Rules","Actions","Tasks","Initial Graph","Generate"]
        self.optionNumber = -1
        self.objectDetail = None

        self.title(" Multi-Character Story Generator")
        self.geometry("1000x600")

        self.subframes = {}
        self.subframes[9] = ObjectFrame.InitialFrame(self)
        self.objectFrame = self.subframes[9]
        self.subframes[0] = EntityTabController.EntityTabController(self.objectFrame)
        self.subframes[1] = WorldStateTab.WorldStateTab(self.objectFrame)
        self.subframes[2] = ObjectFrame.NumberedFrame(self.objectFrame,2)
        self.subframes[3] = ActionsTab.ActionsTab(self.objectFrame)
        self.subframes[4] = ObjectFrame.NumberedFrame(self.objectFrame,4)
        self.subframes[5] = ObjectFrame.NumberedFrame(self.objectFrame,5)
        self.subframes[6] = ObjectFrame.NumberedFrame(self.objectFrame,6)
        self.subframes[7] = ObjectFrame.NumberedFrame(self.objectFrame,7)
        self.subframes[8] = ObjectFrame.PlaceholdingFrame(self.objectFrame)
        self.subframes[8].grid(column=0, row=1, padx=0, pady=0, sticky="nsew")

        self.optionFrame = OptionFrame.OptionFrame(self)
        self.optionFrame.pack(side='top',fill='x',padx=5,pady=2)
    
    def changeOptionNumber(self, i) -> None:
        
        self.optionNumber = i
        self.subframes[i].tkraise()
        return
    
    def destroy(self) -> None:
        super().destroy()