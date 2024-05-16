import tkinter as tk
import tkinter.ttk as ttk
from interface.subframes.wstab.DropdownTabButtonPanel import DropdownTabButtonPanel

class CreateRelationFrame(ttk.Frame):
    def __init__(self,container):
        super().__init__(master=container, width=450,height=300)
        self.root = self.master.master.root
        self.grid(column=0, row=1, padx=0, pady=0, sticky="nsew")

        self.instructionLabel = tk.Label(self, text="--- Add new relation between entities ---", font="Helvetica 9 bold")
        self.instructionLabel.grid(column=0,row=0,columnspan=3,padx=5,pady=0,sticky="new")

        self.relNameLabel = tk.Label(self, text="Name")
        self.relNameLabel.grid(column=0,row=1,columnspan=2,sticky="new")
        self.relNameVar = tk.StringVar(self)
        self.relNameEntry = tk.Entry(self, textvariable=self.relNameVar,justify="left")
        self.relNameEntry.grid(column=0,row=2,columnspan=2,padx=5,pady=5,sticky="new")

        self.relParamsLabel = tk.Label(self, text="Params")
        self.relParamsLabel.grid(column=2,row=1,sticky="new")
        self.relParamsVar = tk.StringVar(self)
        self.relParamsEntry = tk.Entry(self, textvariable=self.relParamsVar,justify="left")
        self.relParamsEntry.grid(column=2,row=2,padx=5,pady=5,sticky="new")

        self.entityOptions = []
        self.generateListboxStringVar()
        self.arrowOptions = ["---->","<--->"]
        self.fromEntityVar = tk.StringVar(self)
        self.toEntityVar = tk.StringVar(self)
        self.arrowVariable = tk.StringVar(self)
        self.fromEntityMenu = tk.OptionMenu(self, self.fromEntityVar,*self.entityOptions)
        self.arrowMenu = tk.OptionMenu(self, self.arrowVariable,*self.arrowOptions)
        self.toEntityMenu = tk.OptionMenu(self, self.toEntityVar,*self.entityOptions)
        self.fromEntityLabel = tk.Label(self, text="From",width=20)
        self.fromArrowLabel = tk.Label(self, text="---",width=15)
        self.toEntityLabel = tk.Label(self, text="To",width=20)
        
        self.fromEntityLabel.grid(column=0,row=3,padx=5,pady=0,sticky="new")
        self.fromArrowLabel.grid(column=1,row=3,padx=5,pady=0,sticky="new")
        self.toEntityLabel.grid(column=2,row=3,padx=5,pady=0,sticky="new")
        self.fromEntityMenu.grid(column=0,row=4,padx=5,pady=0,sticky="new")
        self.arrowMenu.grid(column=1,row=4,padx=5,pady=0,sticky="new")
        self.toEntityMenu.grid(column=2,row=4,padx=5,pady=0,sticky="new")

        self.cancelButton = tk.Button(self,text="Cancel",command=self.master.destroy)
        self.cancelButton.grid(column=0,row=5,padx=5,pady=10,sticky="nesw")

        self.submitButton = tk.Button(self,text="Submit",command=self.onSubmit)
        self.submitButton.grid(column=2,row=5,padx=5,pady=10,sticky="nesw")

    def generateListboxStringVar(self) -> None:
        resource = self.root.resources.getEntities()
        # parse the resource
        self.entityOptions.clear()
        self.entityOptions.append("-- Objects --")
        for i in range(len(resource.get("objects"))):
            self.entityOptions.append("["+str(i)+"O] "+resource.get("objects")[i].get("name"))
        self.entityOptions.append("-- Locations --")
        for i in range(len(resource.get("locations"))):
            self.entityOptions.append("["+str(i)+"L] "+resource.get("locations")[i].get("name"))
        self.entityOptions.append("-- Characters --")
        for i in range(len(resource.get("characters"))):
            self.entityOptions.append("["+str(i)+"C] "+resource.get("characters")[i].get("name"))
    
    def onSubmit(self) -> None:
        # data verification
        fromEntityTag = self.fromEntityVar.get()
        if(not fromEntityTag.startswith("[")):
            print("trip condition 1")
            return
        toEntityTag = self.toEntityVar.get()
        if(not toEntityTag.startswith("[")):
            print("trip condition 2")
            return
        arrowTag = self.arrowVariable.get()
        if(not arrowTag.endswith(">")):
            print("trip condition 3")
            return
        relName = self.relNameVar.get()
        if(len(relName) == 0):
            print("trip condition 4")
            return

        # extract data
        fromEntityTag = fromEntityTag.split("]")[0][1:]
        toEntityTag = toEntityTag.split("]")[0][1:]
        arrowTag = arrowTag.startswith("<")
        relParams = self.relParamsVar.get()
        print(fromEntityTag, toEntityTag, str(arrowTag), relName, relParams)
        
        # create relation
        newRel = {
            "fromEntityId": {},
            "toEntityId": {},
            "connection": {
                "name": relName,
                "params": relParams,
                "is2way": arrowTag
            }
        }

        if(fromEntityTag.endswith("O")):
            newRel["fromEntityId"]["entityType"] = "objects"
        elif(fromEntityTag.endswith("L")):
            newRel["fromEntityId"]["entityType"] = "locations"
        else:
            newRel["fromEntityId"]["entityType"] = "characters"
        newRel["fromEntityId"]["entityId"] = int(fromEntityTag[:-1])

        if(toEntityTag.endswith("O")):
            newRel["toEntityId"]["entityType"] = "objects"
        elif(fromEntityTag.endswith("L")):
            newRel["toEntityId"]["entityType"] = "locations"
        else:
            newRel["toEntityId"]["entityType"] = "characters"
        newRel["toEntityId"]["entityId"] = int(toEntityTag[:-1])
        
        self.root.resources.addRelation(newRel)
        self.master.master.master.master.fetch()
        self.master.destroy()
        return
