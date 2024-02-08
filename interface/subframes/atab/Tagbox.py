import tkinter as tk
import tkinter.ttk as ttk

from application.components import StoryObjects

class Tagbox(ttk.Frame):
    def __init__(self, container):
        super().__init__(master=container, borderwidth=1, relief="solid")
        self.root = self.master.root
        self.grid(column=1,row=0,rowspan=2,padx=5, pady=5,sticky="news")

        self.rowconfigure(0,minsize=5,weight=1)
        self.rowconfigure(1,weight=700)

        self.boxLabel = tk.Label(self, text="Traits", font='Helvetica 9 bold')
        self.boxLabel.grid(column=0,row=0,sticky="ws")

        self.tagTable = ttk.Treeview(self)
        self.tagTable['columns'] = ('type', 'content')

        self.tagTable.column("#0", width=0,  stretch=tk.NO)
        self.tagTable.column("type", anchor=tk.CENTER, width=100)
        self.tagTable.column("content", anchor=tk.CENTER, width=200)

        self.tagTable.heading("#0",text="",anchor=tk.CENTER)
        self.tagTable.heading("type",text="Tag",anchor=tk.CENTER)
        self.tagTable.heading("content",text="Content",anchor=tk.CENTER)

        self.tagTable.bind("<Double-1>", self.onDoubleClick)
        self.tagTable.bind("<Delete>", self.onDelete)
        self.tagTable.grid(column=0,row=1,padx=5,pady=5,sticky="nsew")
    
    def fetch(self):
        # first clear tagTable
        for i in self.tagTable.get_children():
            self.tagTable.delete(i)
        # add new tags of current object
        object = self.root.objectDetail
        if object != None:
            # TODO: add law/moral bias for character nodes
            if isinstance(object,StoryObjects.CharacterNode):
                self.tagTable.insert(parent='', index='end', values=("Law Bias", object.biases["lawbias"]))
                self.tagTable.insert(parent='', index='end', values=("Moral Bias", object.biases["moralbias"]))
            for key, value in object.tags.items():
                if key != 'Type':
                    self.tagTable.insert(parent='', index='end', values=(key, value))
            self.tagTable.insert(parent='',index='end',values=('',''))
    
    def onDoubleClick(self, event):
        self.tag = self.tagTable.item(self.tagTable.selection()[0],'values')
        if(self.tag[0] != "Law Bias" and self.tag[0] != "Moral Bias"):
            self.openChangeTagWindow()
    
    def openChangeTagWindow(self):
        self.changeTags = tk.Toplevel(self)
        self.changeTags.minsize(400,50)
        self.changeTags.columnconfigure(0,minsize=200,weight=0)
        self.changeTags.columnconfigure([1,2],weight=100)
        self.changeTags.resizable(False,False)

        self.changeTagnameLabel = ttk.Label(self.changeTags, text="Tag")
        self.changeTagnameLabel.grid(column=0,row=0,padx=5,pady=5,sticky="nsew")
        self.changeTagnameEntry = ttk.Entry(self.changeTags)
        self.changeTagnameEntry.grid(column=0,row=1,padx=5,pady=5,sticky="nsew")
        self.changeTagnameEntry.insert(0,str(self.tag[0]))

        self.changeTagvalueLabel = ttk.Label(self.changeTags, text="Value")
        self.changeTagvalueLabel.grid(column=1,row=0,padx=5,pady=5,sticky="nsew")
        self.changeTagvalueEntry = ttk.Entry(self.changeTags)
        self.changeTagvalueEntry.grid(column=1,row=1,padx=5,pady=5,sticky="nsew")
        self.changeTagvalueEntry.insert(0,str(self.tag[1]))

        self.cancelChangeMax = ttk.Button(self.changeTags, text="Cancel", command=self.changeTags.destroy)
        self.cancelChangeMax.grid(column=1,row=2,sticky="nsew")
        self.okChangeMax = ttk.Button(self.changeTags, text="Submit", command=self.change_tags)
        self.okChangeMax.grid(column=2,row=2,sticky="nsew")
    
    def change_tags(self):
        newTagName = self.changeTagnameEntry.get()
        newTagValue = self.changeTagvalueEntry.get()
        object = self.root.objectDetail
        if(newTagName == '' and self.tag[0] == ''): #nothing lost, nothing gained
            self.changeTags.destroy()
        elif(newTagName == "Type"):
            ttk.Label(self.changeTags,text="Cannot change Type attribute.").grid(column=0,row=2,sticky="nsew")
        elif(self.tag[0] == newTagName): #change only the value
            object.tags[newTagName] = newTagValue
            self.fetch()
            self.changeTags.destroy()
        else: #remove the old tag, create the new tag
            if(self.tag[0] != ''): #THERE IS AN OLD TAG
                del object.tags[self.tag[0]]
            if(newTagName != ''): #THERE IS A NEW TAG
                object.tags[newTagName] = newTagValue
                print("Add tag",newTagName,"to",object)
            self.fetch()
            self.changeTags.destroy()

    def onDelete(self, event):
        self.tag = self.tagTable.item(self.tagTable.selection()[0],'values')
        self.delete_tag()

    def delete_tag(self):
        object = self.root.objectDetail
        del object.tags[self.tag[0]]
        self.fetch()
    
    def reset(self):
        for i in self.tagTable.get_children():
            self.tagTable.delete(i)