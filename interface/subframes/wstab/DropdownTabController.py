import tkinter as tk
import tkinter.ttk as ttk
from interface.subframes.wstab.DropdownTab import DropdownTab

class DropdownTabController():
    def __init__(self, master, root):
        # note: this is not a Tk class, so it is not in the tree. It will still inherit some attributes, but it does not get gridded.
        self.root = root

        self.tabs = [self.objectTab,self.locationTab,self.characterTab]
        self.currentTab = 0
        self.tkraise()
    
    def tkraise(self):
        self.tabs[self.currentTab].tkraise()

    def reset(self):
        self.currentTab = 0
        self.objectTab.reset()
        self.locationTab.reset()
        self.characterTab.reset()
        self.tkraise() 