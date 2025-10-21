# backend/file_handling.py
import glob
import os
import shutil
from tkinter import filedialog, messagebox
from PIL import Image
import datetime

class FileHandler:
    def __init__(self):
        self.file_path = ""
        self.has_image = False

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CURRENT_IMAGE_PATH = os.path.join(BASE_DIR, "resources", "current_image")
    EDITED_IMAGE_PATH = os.path.join(BASE_DIR, "resources", "edited_image")


    app = None

    def clear_images(self):
        for f in glob.glob(os.path.join(self.CURRENT_IMAGE_PATH, "current_image.*")):
            os.remove(f)

        for f in glob.glob(os.path.join(self.EDITED_IMAGE_PATH, "edited_image.png")):
            os.remove(f)

    def get_file_from_dialog(self):
        from tkinter import messagebox

        if self.has_image:
            response = messagebox.askyesno(
                title="Warning!",
                message="You already have an image. Are you sure you want to overwrite it?"
            )

            if not response:
                return

        self.file_path = filedialog.askopenfilename(
            parent=self.app.root,
            title="Select an Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif"), ("All files", "*.*")]
        )

        if not self.file_path:  # User cancelled
            return

        # Ensure destination folder exists
        os.makedirs(self.CURRENT_IMAGE_PATH, exist_ok=True)

        _, ext = os.path.splitext(self.file_path)
        dest_path = os.path.join(self.CURRENT_IMAGE_PATH, f"current_image{ext}")

        try:
            for f in glob.glob(os.path.join(self.CURRENT_IMAGE_PATH, "current_image.*")):
                os.remove(f)
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting previous image: {str(e)}")
            return

        try:
            # Copy file into folder, preserving filename
            shutil.copy(self.file_path, dest_path)
        except Exception as e:
            messagebox.showerror("Error", f"Error copying file: {e}")
            return

        self.has_image = True

    def save_edited_image(self, edited_image: Image):
        os.makedirs(self.EDITED_IMAGE_PATH, exist_ok=True)

        dest_path = os.path.join(self.EDITED_IMAGE_PATH, "edited_image.png")

        try:
            for f in glob.glob(os.path.join(self.EDITED_IMAGE_PATH, "edited_image.*")):
                os.remove(f)
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting edited image: {str(e)}")

        try :
            edited_image.save(dest_path, format="PNG")
        except Exception as e:
            messagebox.showerror("Error", f"Error copying edited image: {str(e)}")

    def save_image_to_desktop(self):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        file_name = "Wild_West_Poster_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
        save_path = os.path.join(desktop_path, file_name)

        # Get the edited image file path
        edited_image_files = glob.glob(os.path.join(self.EDITED_IMAGE_PATH, "edited_image.*"))

        if not edited_image_files:
            messagebox.showerror("Error", "No edited image to save. Please generate an image first.")
            return

        try:
            shutil.copy(edited_image_files[0], save_path)
            messagebox.showinfo("Success", f"Image saved to Desktop!")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving image: {str(e)}")


    def get_file_path(self):
        return self.file_path