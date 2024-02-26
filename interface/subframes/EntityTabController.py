from interface.Resources import Resources
from interface.subframes.ObjectsTab import EntityTab

class EntityTabController():
    def __init__(self, master):
        # note: this is not a Tk class, so it is not in the tree. It will still inherit some attributes, but it does not get gridded.
        self.root = master.root
        self.tabs = [None,None,None]
        r = Resources()
        self.currentTab = 0
        self.tabs[0] = EntityTab(master, r.getObjects,self)
        self.tabs[1] = EntityTab(master, r.getLocations,self)
        self.tabs[2] = EntityTab(master, r.getCharacters, self)
    
    def tkraise(self):
        self.tabs[self.currentTab].tkraise()

    def changeEntityTab(self, i):
        self.currentTab = i
        self.tkraise()