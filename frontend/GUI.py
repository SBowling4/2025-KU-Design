from tkinter import *
from tkinter import ttk

root = Tk()

def initalizeframe():
    global mainframe
    mainframe = ttk.Frame(root, padding="12 12 12 12")
    root.title("Wild West Poster Generator")

    mainframe.grid(column=0, row=0, sticky="N, W, E, S")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

def setframecomponents():
    settitle()
    setinputs()
    setfontdropdown()

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

def settitle():
    ttk.Label(mainframe, text="Wild West Poster Generator").grid(column=0, row=0)


def setinputs():
    ttk.Button(mainframe, text="Upload Image").grid(column=1, row=0)

    name_var = StringVar()
    name_entry = ttk.Entry(mainframe, width=20, textvariable=name_var)
    name_entry.grid(column=1, row=1)

    date_var = StringVar()
    date_entry = ttk.Entry(mainframe, width=20, textvariable=date_var)
    date_entry.grid(column=2, row=1)


def setfontdropdown():
    optionlist = ('font1', 'font2')

    v = StringVar()
    v.set(optionlist[0])

    font_entry = OptionMenu(mainframe, v, *optionlist)
    font_entry.grid(column=3, row=1)


def startloop():
    root.mainloop()

