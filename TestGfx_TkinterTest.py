from tkinter import *
import tkinter.ttk as ttk

# define window
window = Tk()
window.title(" Multi-Character Story Generator")
window.geometry("900x720")

#define menu gridding
window.grid_columnconfigure(0,weight=1)

#define style
style = ttk.Style(window)
style.configure('OptionFrame.TFrame', background='white')

# define menu
menu = Menu(window)
window.config(menu = menu)
filemainmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=filemainmenu)
filemainmenu.add_command(label="Exit", command=window.destroy)

# define body
frm = ttk.Frame(window, padding=10, style="OptionFrame.TFrame")
frm.grid(column=0,row=0,sticky="new")
frm.grid_columnconfigure((0,1,2,3,4,5,6),weight=1)

buttons = [
    ttk.Button(frm,text="Objects").grid(column=0,row=0, sticky="news"),
    ttk.Button(frm,text="Actions").grid(column=1,row=0, sticky="news"),
    ttk.Button(frm,text="World State").grid(column=2,row=0, sticky="news"),
    ttk.Button(frm,text="Rules").grid(column=3,row=0, sticky="news"),
    ttk.Button(frm,text="Tasks").grid(column=4,row=0, sticky="news"),
    ttk.Button(frm,text="Initial Graph").grid(column=5,row=0, sticky="news"),
    ttk.Button(frm,text="Generate").grid(column=6,row=0, sticky="news"),
]

# mainloop
window.mainloop()