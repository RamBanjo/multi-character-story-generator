import tkinter as tk
import tkinter.ttk as ttk

class OptionFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(master=container, borderwidth=1, relief="solid",height=66)
        ####loe
        self.btn = []
        for i in range(len(container.resources['btnLabels'])):
            self.btn.append(OptionButton(self, name=container.resources['btnLabels'][i],btnIdx=i))
            self.btn[i].grid(column=i,row=0,padx=1,pady=1,sticky="news")
            self.columnconfigure(i,weight=1)
        ####loe

class OptionButton(ttk.Button):
    def __init__(self, container, name, btnIdx):
        super().__init__(master=container, default='normal', text=name)
        def btnCmd():
            container.master.changeOptionNumber(btnIdx)
        self.config(command=btnCmd)