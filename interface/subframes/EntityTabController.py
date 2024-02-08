from interface.subframes.ObjectsTab import EntityTab

currentTab = 0

class EntityTabController():
    def __init__(self, master):
        # note: this is not a Tk class, so it is not in the tree. It will still inherit some attributes, but it does not get gridded.
        self.root = master.root
        self.tabs = [None,None,None]
        self.tabs[0] = EntityTab(master, None, None, self)

    
    def tkraise(self):
        self.tabs[currentTab].tkraise()

    def changeEntityTab(self, i):
        currentTab = i
        self.tkraise()