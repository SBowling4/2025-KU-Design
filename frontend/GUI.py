from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import TKinterModernThemes as TKMT

from resources import resources


class App(TKMT.ThemedTKinterFrame):

    file_handler = None
    image_creator = None

    messagebox = messagebox

    def __init__(self, theme, mode):
        super().__init__("Wild West Poster Generator", theme, mode)

        # Tkinter variables
        self.name_var = StringVar()
        self.loc_var = StringVar()
        self.font_var = StringVar()
        self.frame_var = StringVar()
        self.filter_var = StringVar()
        self.text_color_var = StringVar()


        # Store images
        self.images = {}

        # Build the UI
        self.set_frame_components()


    def set_frame_components(self):
        self.set_title()
        self.set_inputs()
        self.set_font_dropdown()
        self.set_frame_buttons()
        self.set_save_button()
        self.set_filter_buttons()
        self.set_generate_button()
        self.set_font_color_dropdown()
        self.set_current_image(False)

        for child in self.root.winfo_children():
            if child.winfo_name().__contains__("label"):
                child.grid_configure(sticky="s")

    def set_title(self):
        title_label = self.Label("Wild West Poster Generator")
        title_label.grid(column=1, row=0)

    def set_inputs(self):
        upload_button = self.Button(text="Upload Image", command=lambda: self.upload_image())
        upload_button.grid(column=2, row=0)

        name_label = self.Label("Name")
        name_label.grid(column=2, row=1)

        name_entry = self.Entry(textvariable=self.name_var)
        name_entry.grid(column=2, row=2)

        loc_label = self.Label("Location")
        loc_label.grid(column=3, row=1)

        loc_entry = self.Entry(textvariable=self.loc_var)
        loc_entry.grid(column=3, row=2)

    def set_font_dropdown(self):
        font_label = self.Label("Font")
        font_label.grid(column=4, row=1)

        font_option_list = ['Breaking Road', 'Perfecto', 'Priestacy']
        self.font_var.set(font_option_list[0])

        font_entry = self.OptionMenu(font_option_list, self.font_var)
        font_entry.grid(column=4, row=2)

    def set_frame_buttons(self):
        frame_label = self.Label("Frames")

        frame_label.grid(column=2, row=3)

        frame_1_rgb = resources.frame_1.convert('RGBA').resize((100, 100), Image.Resampling.LANCZOS)
        frame_2_rgb = resources.frame_2.convert('RGBA').resize((100, 100), Image.Resampling.LANCZOS)
        frame_3_rgb = resources.frame_3.convert('RGBA').resize((100, 100), Image.Resampling.LANCZOS)

        self.images['frame_1'] = ImageTk.PhotoImage(frame_1_rgb)
        self.images['frame_2'] = ImageTk.PhotoImage(frame_2_rgb)
        self.images['frame_3'] = ImageTk.PhotoImage(frame_3_rgb)

        frame_1_button = Button(self.root, command=lambda: self.update_frame("frame_1"), image=self.images['frame_1'])
        frame_2_button = Button(self.root, command=lambda: self.update_frame("frame_2"), image=self.images['frame_2'])
        frame_3_button = Button(self.root, command=lambda: self.update_frame("frame_3"), image=self.images['frame_3'])

        frame_1_button.grid(column=2, row=4)
        frame_2_button.grid(column=2, row=5)
        frame_3_button.grid(column=2, row=6)

    def set_filter_buttons(self):
        filter_label = self.Label("Filters")

        filter_label.grid(column=4, row=3)

        filter_1_rgb = resources.filter_display_1.convert('RGB').resize((100, 100))
        filter_2_rgb = resources.filter_display_2.convert('RGB').resize((100, 100))
        filter_3_rgb = resources.filter_display_3.convert('RGB').resize((100, 100))

        self.images['filter_1'] = ImageTk.PhotoImage(filter_1_rgb)
        self.images['filter_2'] = ImageTk.PhotoImage(filter_2_rgb)
        self.images['filter_3'] = ImageTk.PhotoImage(filter_3_rgb)

        bg_1_button = Button(self.root, command=lambda: self.update_filter("filter_1"), image=self.images['filter_1'])
        bg_2_button = Button(self.root, command=lambda: self.update_filter("filter_2"), image=self.images['filter_2'])
        bg_3_button = Button(self.root, command=lambda: self.update_filter("filter_3"), image=self.images['filter_3'])

        bg_1_button.grid(column=4, row=4)
        bg_2_button.grid(column=4, row=5)
        bg_3_button.grid(column=4, row=6)


    def set_save_button(self):
        save_button = self.Button(text="Save Image", command=lambda: self.file_handler.save_image_to_desktop())
        save_button.grid(column=4, row=7)

    def set_generate_button(self):
        generate_button = self.Button(text="Generate Image", command=self.update_edited_image)
        generate_button.grid(column=2, row=7)

    def set_font_color_dropdown(self):
        font_color_label = self.Label("Font Color")
        font_color_label.grid(column=5, row=1)

        text_color_option_list = ['Black', 'White']
        self.text_color_var.set(text_color_option_list[0])

        text_color_dropdown = self.OptionMenu(text_color_option_list, self.text_color_var)
        text_color_dropdown.grid(column=5, row=2)

    def set_current_image(self, edit):
        if not edit:
            try:
                current_image = resources.get_current_image().convert('RGB').resize((500, 500))
            except FileNotFoundError:
                current_image = resources.temp_image

            self.images['current_image'] = ImageTk.PhotoImage(current_image)

        current_image_label = Label(self.root, image=self.images['current_image'])

        current_image_label.grid(column=0, row=1, rowspan=6, columnspan=2)

    def update_edited_image(self):
        if not self.get_entries()['frame']:
            messagebox.showerror("Error", "No frame selected")
            return

        if not self.get_entries()['filter']:
            messagebox.showerror("Error", "No filter selected")
            return

        try:
            edited_image = self.image_creator.create_image()
        except FileNotFoundError:
            messagebox.showerror("Error", "No image found")
            self.images['current_image'] = resources.temp_image
            edited_image = self.images['current_image']
            self.set_current_image(False)

        self.file_handler.save_edited_image(edited_image)

        self.images['current_image'] = ImageTk.PhotoImage(edited_image)

        self.set_current_image(True)


    def upload_image(self):
        self.file_handler.get_file_from_dialog()


        try:
            resources.get_edited_image()
        except FileNotFoundError:
            self.set_current_image(False)

        self.set_current_image(True)

    def update_frame(self, frame):
        self.frame_var.set(frame)

    def update_filter(self, fil):
        self.filter_var.set(fil)

    def get_entries(self) -> dict[str, str]:
        return {
            "name": self.name_var.get(),
            "location": self.loc_var.get(),
            "font": self.font_var.get(),
            "frame": self.frame_var.get(),
            "filter": self.filter_var.get(),
            "text_color": self.text_color_var.get()
        }
