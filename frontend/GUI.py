from tkinter import *
from tkinter import ttk
from frontend import resource_images
from PIL import Image, ImageTk
import TKinterModernThemes as TKMT
from frontend import ImageButton

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

class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode):
        super().__init__("Wild West Poster Generator", theme, mode)

        self.setframecomponents()

        self.run()

    def setframecomponents(self):
        self.settitle()
        self.setinputs()
        self.setfontdropdown()
        self.setframesellectors()
        self.setbackgroundseelctors()
        self.setsavebutton()

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)


    def settitle(self):
        title_label = self.Label("Wild West Poster Generator")
        title_label.grid(column=0, row=0)


    def setinputs(self):
        upload_button = self.Button(text="Upload Image", command=hi)
        upload_button.grid(column=1, row=0)

        name_entry = self.Entry(textvariable=name_var)
        name_entry.grid(column=1, row=1)

        date_entry = self.Entry(textvariable=date_var)
        date_entry.grid(column=2, row=1)



    def setfontdropdown(self):
        optionlist = ['font1', 'font2']
        font_var.set(optionlist[0])

        font_entry = self.OptionMenu(optionlist, font_var)
        font_entry.grid(column=3, row=1)

    def setframesellectors(self):
        frame_1_rgb = resource_images.frame_1.convert('RGB')
        frame_2_rgb = resource_images.frame_2.convert('RGB')
        frame_3_rgb = resource_images.frame_3.convert('RGB')

        frame_1_resized = frame_1_rgb.resize((100, 100), Image.Resampling.LANCZOS)
        frame_2_resized = frame_2_rgb.resize((100, 100), Image.Resampling.LANCZOS)
        frame_3_resized = frame_3_rgb.resize((100, 100), Image.Resampling.LANCZOS)

        button_images['frame_1'] = ImageTk.PhotoImage(frame_1_resized)
        button_images['frame_2'] = ImageTk.PhotoImage(frame_2_resized)
        button_images['frame_3'] = ImageTk.PhotoImage(frame_3_resized)

        ImageButton(self, image=button_images['frame_1'], command=hi).grid(column=1, row=2)
        ImageButton(self, image=button_images['frame_2'], command=hi).grid(column=2, row=2)
        ImageButton(self, image=button_images['frame_3'], command=hi).grid(column=3, row=2)

        # self.Button(command=hi, **{"image": button_images['frame_1']}).grid(column=1, row=2)
        # self.Button(command=hi, **{"image": button_images['frame_2']}).grid(column=2, row=2)
        # self.Button(command=hi, **{"image": button_images['frame_3']}).grid(column=3, row=2)

    def setbackgroundseelctors(self):
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

    def setsavebutton(self):
        ttk.Button(mainframe, text="Save Image").grid(column=1, row=4)



    def getentries(self) -> dict[str, str]:
        entries = {
            "name": name_var.get(),
            "date": date_var.get(),
            "font": font_var.get,
        }
        return entries

def hi():
    print("Button pressed")