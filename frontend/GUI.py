from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import TKinterModernThemes as TKMT
from resources import resources


class App(TKMT.ThemedTKinterFrame):
    file_handler = None
    image_creator = None

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

        # Start the UI state update loop
        self._update_ui_state()

    def set_frame_components(self):
        self.set_title()
        self.set_inputs()
        self.set_font_dropdown()
        self.set_frame_buttons()
        self.set_save_button()
        self.set_filter_buttons()
        self.set_generate_button()
        self.set_font_color_dropdown()
        self.set_current_image(edit=False)

        for child in self.root.winfo_children():
            if "label" in child.winfo_name():
                child.grid_configure(sticky="s")

    def set_title(self):
        title_label = self.Label("Wild West Poster Generator")
        title_label.grid(column=1, row=0)

    def set_inputs(self):
        upload_button = self.Button(text="Upload Image", command=self.upload_image)
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

        frames = {
            "frame_1": resources.frame_1,
            "frame_2": resources.frame_2,
            "frame_3": resources.frame_3
        }

        self.frame_buttons = {}
        for i, (key, img) in enumerate(frames.items(), start=4):
            resized = img.convert('RGBA').resize((100, 100), Image.Resampling.LANCZOS)
            self.images[key] = ImageTk.PhotoImage(resized)

            border = Frame(self.root, background="gray", padx=2, pady=2)
            border.grid(column=2, row=i)

            btn = Button(border, image=self.images[key], command=lambda k=key: self.update_frame(k))
            btn.pack()
            self.frame_buttons[key] = (border, btn)

    def set_filter_buttons(self):
        filter_label = self.Label("Filters")
        filter_label.grid(column=4, row=3)

        filters = {
            "filter_1": resources.filter_display_1,
            "filter_2": resources.filter_display_2,
            "filter_3": resources.filter_display_3
        }

        self.filter_buttons = {}
        for i, (key, img) in enumerate(filters.items(), start=4):
            resized = img.convert('RGB').resize((100, 100))
            self.images[key] = ImageTk.PhotoImage(resized)

            border = Frame(self.root, background="gray", padx=2, pady=2)
            border.grid(column=4, row=i)

            btn = Button(border, image=self.images[key], command=lambda k=key: self.update_filter(k))
            btn.pack()
            self.filter_buttons[key] = (border, btn)

    def set_save_button(self):
        save_button = self.Button(text="Save Image", command=self.save_to_desktop)
        save_button.grid(column=4, row=7)

    def set_generate_button(self):
        generate_button = self.Button(text="Generate Image", command=self.generate_poster)
        generate_button.grid(column=2, row=7)

    def set_font_color_dropdown(self):
        font_color_label = self.Label("Font Color")
        font_color_label.grid(column=5, row=1)

        text_color_option_list = ['Black', 'White']
        self.text_color_var.set(text_color_option_list[0])

        text_color_dropdown = self.OptionMenu(text_color_option_list, self.text_color_var)
        text_color_dropdown.grid(column=5, row=2)

    def set_current_image(self, edit=False):
        """
        Display current image. edit=True shows edited image if exists.
        """
        try:
            if edit:
                img = resources.get_edited_image().convert('RGB').resize((500, 500))
            else:
                img = resources.get_current_image().convert('RGB').resize((500, 500))
        except FileNotFoundError:
            # If the image doesn't exist, show temp image
            img = resources.temp_image

        self.images['current_image'] = ImageTk.PhotoImage(img)

        if hasattr(self, 'current_image_label'):
            self.current_image_label.config(image=self.images['current_image'])
            self.current_image_label.image = self.images['current_image']
        else:
            self.current_image_label = Label(self.root, image=self.images['current_image'])
            self.current_image_label.grid(column=0, row=1, rowspan=6, columnspan=2)

    def upload_image(self):
        """Handle image upload with poster detection"""
        # Check if overwriting
        if self.file_handler.has_image:
            if not messagebox.askyesno(
                    "Warning!",
                    "You already have an image. Are you sure you want to overwrite it?"
            ):
                return
            # Clear both current and edited images when starting fresh
            self.file_handler.clear_current_image()
            self.file_handler.clear_edited_image()

        # Get file from user
        file_path = filedialog.askopenfilename(
            parent=self.root,
            title="Select an Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif"), ("All files", "*.*")]
        )

        if not file_path:  # User cancelled
            return

        # Check for poster metadata
        base_image_path, base_exists = self.file_handler.check_for_poster_metadata(file_path)

        # Handle poster detection
        if base_image_path:
            if not base_exists:
                # Base image missing - warn user
                messagebox.showwarning(
                    "Base Image Missing",
                    "This image appears to be a previously generated poster.\n\n"
                    f"The original base image at:\n{base_image_path}\nwas not found.\n"
                    "You can still continue, but the poster will start from this uploaded image."
                )
                # Treat as regular image
                self._load_regular_image(file_path)
            else:
                # Base exists - ask if user wants to continue editing
                if messagebox.askyesno(
                        "Poster Detected",
                        f"This image appears to be a previously generated poster.\n\n"
                        f"Original base image:\n{base_image_path}\n\n"
                        f"Do you want to continue editing this poster?"
                ):
                    # Load for editing
                    if self.file_handler.load_poster_for_editing(file_path, base_image_path):
                        self.set_current_image(edit=True)
                    else:
                        messagebox.showerror("Error", "Failed to load poster for editing")
                else:
                    # Use poster as new base image
                    self._load_regular_image(file_path)
        else:
            # No metadata - regular image
            self._load_regular_image(file_path)

    def _load_regular_image(self, file_path: str):
        """Load a regular image as base image"""
        # Clear edited image from disk when loading new base
        self.file_handler.clear_edited_image()

        if self.file_handler.load_base_image(file_path):
            # Show the new base image (not edited)
            self.set_current_image(edit=False)
        else:
            messagebox.showerror("Error", "Failed to load image")

    def update_edited_image(self, upload=False):
        """
        Update the edited image display (used for backward compatibility).
        """
        if upload:
            self.set_current_image(edit=True)

    def generate_poster(self):
        """Generate the poster with current settings"""
        # Validate frame and filter selection
        entries = self.get_entries()

        if not entries['frame']:
            if not messagebox.askyesno("No Frame", "No frame selected, would you like to continue?"):
                return

        if not entries['filter']:
            if not messagebox.askyesno("No Filter", "No filter selected, would you like to continue?"):
                return

        # Generate image
        try:
            edited_image = self.image_creator.create_image()
        except FileNotFoundError:
            messagebox.showerror("Error", "No base image found. Please upload an image first.")
            return
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate poster: {str(e)}")
            return

        # Save and display
        if self.file_handler.save_edited_image(edited_image):
            self.set_current_image(edit=True)
        else:
            messagebox.showerror("Error", "Failed to save edited image")

    def save_to_desktop(self):
        """Save the current edited image to desktop"""
        success, message = self.file_handler.save_image_to_desktop()

        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    def update_frame(self, frame):
        self.frame_var.set(frame)

    def update_filter(self, fil):
        self.filter_var.set(fil)

    def _update_ui_state(self):
        """Periodically update UI elements to reflect current state"""
        # Update frame borders
        current_frame = self.frame_var.get()
        for key, (border, _) in self.frame_buttons.items():
            border.config(background="blue" if key == current_frame else "gray")

        # Update filter borders
        current_filter = self.filter_var.get()
        for key, (border, _) in self.filter_buttons.items():
            border.config(background="blue" if key == current_filter else "gray")

        # Schedule next update (every 100ms)
        self.root.after(100, self._update_ui_state)

    def get_entries(self) -> dict[str, str]:
        return {
            "name": self.name_var.get(),
            "location": self.loc_var.get(),
            "font": self.font_var.get(),
            "frame": self.frame_var.get(),
            "filter": self.filter_var.get(),
            "text_color": self.text_color_var.get()
        }