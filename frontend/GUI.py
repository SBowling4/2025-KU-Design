from tkinter import *
from PIL import Image, ImageTk
import TKinterModernThemes as TKMT
from frontend import resource_images


class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode):
        super().__init__("Wild West Poster Generator", theme, mode)

        # Tkinter variables (safe to create AFTER super().__init__)
        self.name_var = StringVar()
        self.date_var = StringVar()
        self.font_var = StringVar()
        self.frame_var = StringVar()
        self.bg_var = StringVar()

        # Store images so they aren’t garbage-collected
        self.images = {}

        # Build the UI
        self.set_frame_components()
        self.run()

    def set_frame_components(self):
        self.set_title()
        self.set_inputs()
        self.set_font_dropdown()
        self.set_frame_buttons()
        self.set_save_button()
        self.set_background_buttons()
        self.set_generate_button()

        for child in self.root.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def set_title(self):
        title_label = self.Label("Wild West Poster Generator")
        title_label.grid(column=0, row=0)

    def set_inputs(self):
        upload_button = self.Button(text="Upload Image", command=hi)
        upload_button.grid(column=1, row=0)

        name_entry = self.Entry(textvariable=self.name_var)
        name_entry.grid(column=1, row=1)

        date_entry = self.Entry(textvariable=self.date_var)
        date_entry.grid(column=2, row=1)

    def set_font_dropdown(self):
        font_option_list = ['font1', 'font2']
        self.font_var.set(font_option_list[0])

        font_entry = self.OptionMenu(font_option_list, self.font_var)
        font_entry.grid(column=3, row=1)

    def set_frame_buttons(self):
        frame_label = self.Label("Frames")

        frame_label.grid(column=1, row=2)

        frame_1_rgb = resource_images.frame_1.convert('RGB').resize((100, 100), Image.Resampling.LANCZOS)
        frame_2_rgb = resource_images.frame_2.convert('RGB').resize((100, 100), Image.Resampling.LANCZOS)
        frame_3_rgb = resource_images.frame_3.convert('RGB').resize((100, 100), Image.Resampling.LANCZOS)

        self.images['frame_1'] = ImageTk.PhotoImage(frame_1_rgb)
        self.images['frame_2'] = ImageTk.PhotoImage(frame_2_rgb)
        self.images['frame_3'] = ImageTk.PhotoImage(frame_3_rgb)

        frame_1_button = Button(self.root, command=hi, image=self.images['frame_1'])
        frame_2_button = Button(self.root, command=hi, image=self.images['frame_2'])
        frame_3_button = Button(self.root, command=hi, image=self.images['frame_3'])

        frame_1_button.grid(column=1, row=3)
        frame_2_button.grid(column=1, row=4)
        frame_3_button.grid(column=1, row=5)

    def set_background_buttons(self):
        bg_label = self.Label("Backgrounds")

        bg_label.grid(column=3, row=2)

        bg_1_rgb = resource_images.bg_1.convert('RGB').resize((100, 100))
        bg_2_rgb = resource_images.bg_2.convert('RGB').resize((100, 100))
        bg_3_rgb = resource_images.bg_3.convert('RGB').resize((100, 100))

        self.images['bg_1'] = ImageTk.PhotoImage(bg_1_rgb)
        self.images['bg_2'] = ImageTk.PhotoImage(bg_2_rgb)
        self.images['bg_3'] = ImageTk.PhotoImage(bg_3_rgb)

        bg_1_button = Button(self.root, command=hi, image=self.images['bg_1'])
        bg_2_button = Button(self.root, command=hi, image=self.images['bg_2'])
        bg_3_button = Button(self.root, command=hi,image=self.images['bg_3'])

        bg_1_button.grid(column=3, row=3)
        bg_2_button.grid(column=3, row=4)
        bg_3_button.grid(column=3, row=5)


    def set_save_button(self):
        save_button = self.Button(text="Save Image", command=hi)
        save_button.grid(column=3, row=6)

    def set_generate_button(self):
        generate_button = self.Button(text="Generate Image", command=hi)
        generate_button.grid(column=1, row=6)

    def get_entries(self) -> dict[str, str]:
        return {
            "name": self.name_var.get(),
            "date": self.date_var.get(),
            "font": self.font_var.get(),
        }


def hi():
    print("Button pressed")
