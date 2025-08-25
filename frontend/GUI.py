from tkinter import *
from tkinter import ttk
from frontend import resource_images
from PIL import Image, ImageTk

root = Tk()

mainframe = ttk.Frame(root, padding="12 12 12 12")
root.title("Wild West Poster Generator")

mainframe.grid(column=0, row=0, sticky="N, W, E, S")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

name_var = StringVar()
date_var = StringVar()
font_var = StringVar()

button_images = {}

def setframecomponents():
    settitle()
    setinputs()
    setfontdropdown()
    setframesellectors()
    setbackgroundseelctors()
    setsavebutton()

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)


def settitle():
    ttk.Label(mainframe, text="Wild West Poster Generator").grid(column=0, row=0)


def setinputs():
    ttk.Button(mainframe, text="Upload Image").grid(column=1, row=0)

    name_entry = ttk.Entry(mainframe, width=20, textvariable=name_var)
    name_entry.grid(column=1, row=1)

    date_entry = ttk.Entry(mainframe, width=20, textvariable=date_var)
    date_entry.grid(column=2, row=1)



def setfontdropdown():
    optionlist = ('font1', 'font2')
    font_var.set(optionlist[0])

    font_entry = OptionMenu(mainframe, font_var, *optionlist)
    font_entry.grid(column=3, row=1)


def setframesellectors():
    frame_1_rgb = resource_images.frame_1.convert('RGB')
    frame_2_rgb = resource_images.frame_2.convert('RGB')
    frame_3_rgb = resource_images.frame_3.convert('RGB')

    frame_1_resized = frame_1_rgb.resize((100, 100), Image.Resampling.LANCZOS)
    frame_2_resized = frame_2_rgb.resize((100, 100), Image.Resampling.LANCZOS)
    frame_3_resized = frame_3_rgb.resize((100, 100), Image.Resampling.LANCZOS)

    button_images['frame_1'] = ImageTk.PhotoImage(frame_1_resized)
    button_images['frame_2'] = ImageTk.PhotoImage(frame_2_resized)
    button_images['frame_3'] = ImageTk.PhotoImage(frame_3_resized)

    Button(mainframe, image=button_images['frame_1']).grid(column=1, row=2)
    Button(mainframe, image=button_images['frame_2']).grid(column=2, row=2)
    Button(mainframe, image=button_images['frame_3']).grid(column=3, row=2)

def setbackgroundseelctors():
    bg_1_rgb = resource_images.bg_1.convert('RGB')
    bg_2_rgb = resource_images.bg_2.convert('RGB')
    bg_3_rgb = resource_images.bg_3.convert('RGB')

    bg_1_resized = bg_1_rgb.resize((100, 100), Image.Resampling.LANCZOS)
    bg_2_resized = bg_2_rgb.resize((100, 100), Image.Resampling.LANCZOS)
    bg_3_resized = bg_3_rgb.resize((100, 100), Image.Resampling.LANCZOS)

    button_images['bg_1'] = ImageTk.PhotoImage(bg_1_resized)
    button_images['bg_2'] = ImageTk.PhotoImage(bg_2_resized)
    button_images['bg_3'] = ImageTk.PhotoImage(bg_3_resized)

    Button(mainframe, image=button_images['bg_1']).grid(column=1, row=3)
    Button(mainframe, image=button_images['bg_2']).grid(column=2, row=3)
    Button(mainframe, image=button_images['bg_3']).grid(column=3, row=3)

def setsavebutton():
    ttk.Button(mainframe, text="Save Image").grid(column=1, row=4)



def getentries() -> dict[str, str]:
    entries = {
        "name": name_var.get(),
        "date": date_var.get(),
        "font": font_var.get(),
    }

    return entries

def start():
    setframecomponents()
    root.mainloop()