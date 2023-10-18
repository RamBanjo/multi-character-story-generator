import tkinter as tk
import tkinter.ttk as ttk

class InitialFrame(ttk.Frame):
    def __init__(self,container):
        super().__init__(master=container, relief="solid")
        self.label = ttk.Label(self, text=str("Click a button to get started!"))
        self.label.grid(column=0, row=0, padx=0, pady=0, sticky="nsew")
        self.pack(side='bottom',fill='both',expand=True,padx=5,pady=2)
        self.rowconfigure(0,minsize=10,weight=1)
        self.rowconfigure(1,weight=30)
        self.columnconfigure(0,weight=1)

class NumberedFrame(ttk.Frame):
    def __init__(self,container,i):
        super().__init__(master=container, borderwidth=1, relief="solid")
        self.label = ttk.Label(self, text=str("Numbered Frame: "+str(i)))
        self.label.pack(anchor="center", fill='x',padx=1,pady=1)
        self.grid(column=0, row=1, padx=0, pady=0, sticky="nsew")

class PlaceholdingFrame(ttk.Frame):
    def __init__(self,container):
        super().__init__(master=container, borderwidth=1, relief="solid")
        self.label = ttk.Label(self, text=str("This frame is a placeholder for something."))
        self.label.pack(anchor="center", fill='x',padx=1,pady=1)

class ObjectsTab(ttk.Frame):
    def __init__(self,container):
        super().__init__(master=container, borderwidth=1, relief="solid")
        self.grid(column=0, row=1, padx=0, pady=0, sticky="nsew")

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=30)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=5)

        self.label = ttk.Label(self, text=str("This is the Objects Tab!"))
        self.label.grid(column=0, row=0, padx=0, pady=0, sticky="nsew")

        self.listbox = tk.Listbox(self, borderwidth=1, relief="solid", listvariable=container.master.resources['test'])
        self.listbox.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")
        self.descbox = tk.Frame(self, borderwidth=1, relief="solid")
        self.descbox.grid(column=1, row=0, rowspan=2, padx=5, pady=5, sticky="nsew")
