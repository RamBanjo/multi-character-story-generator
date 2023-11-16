import tkinter as tk
import tkinter.ttk as ttk

class OptionFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(master=container, borderwidth=1, relief="solid",height=66)
        self.root = self.master.root
        self.btn = []
        for i in range(len(self.root.resources['btnLabels'])):
            self.btn.append(OptionButton(self, name=self.root.resources['btnLabels'][i],btnIdx=i))
            self.btn[i].grid(column=i,row=0,padx=1,pady=1,sticky="news")
            self.columnconfigure(i,weight=1)


class OptionButton(ttk.Button):
    def __init__(self, container, name, btnIdx):
        super().__init__(master=container, default='normal', text=name)
        self.root = self.master.root
        def btnCmd():
            self.root.changeOptionNumber(btnIdx)
        self.config(command=btnCmd)