from interface.Resources import Resources
from interface.subframes.ObjectsTab import EntityTab

class EntityTabController():
    def __init__(self, master):
        # note: this is not a Tk class, so it is not in the tree. It will still inherit some attributes, but it does not get gridded.
        self.root = master.root
        self.tabs = [None,None,None]
        self.currentTab = 0
        self.tabs[0] = EntityTab(master, "objects",self)
        self.tabs[1] = EntityTab(master, "locations",self)
        self.tabs[2] = EntityTab(master, "characters", self)
    
    def tkraise(self):
        self.tabs[self.currentTab].tkraise()
    
    def fetch(self):
        self.tabs[0].fetch()
        self.tabs[1].fetch()
        self.tabs[2].fetch()

    def changeEntityTab(self, i):
        self.currentTab = i
        self.tkraise()