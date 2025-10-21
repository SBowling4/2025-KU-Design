import glob
import os
import shutil
from tkinter import filedialog, messagebox
from PIL import Image, PngImagePlugin
import datetime


class FileHandler:
    def __init__(self):
        self.file_path = ""
        self.has_image = False
        self.response_2 = None
        self.app = None

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CURRENT_IMAGE_PATH = os.path.join(BASE_DIR, "resources", "current_image")
    EDITED_IMAGE_PATH = os.path.join(BASE_DIR, "resources", "edited_image")

    def clear_images(self):
        for f in glob.glob(os.path.join(self.CURRENT_IMAGE_PATH, "current_image.*")):
            os.remove(f)
        for f in glob.glob(os.path.join(self.EDITED_IMAGE_PATH, "edited_image.png")):
            os.remove(f)

    def get_file_from_dialog(self):
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

        # --- Check for embedded metadata if it's a PNG ---
        base_image_path = None
        image_found_at_base = True
        if self.file_path.lower().endswith(".png"):
            try:
                img = Image.open(self.file_path)
                base_image_path = img.info.get("BaseImagePath")

                if not os.path.exists(base_image_path):
                    messagebox.showwarning(
                        "Base Image Missing",
                        f"The original base image at:\n{base_image_path}\nwas not found.\n"
                        "You can still continue, but the poster will start from this uploaded image."
                    )
                    image_found_at_base = False

                img.close()
            except Exception as e:
                print(f"Metadata check failed: {e}")


        # --- If metadata found, ask user what to do ---
        if base_image_path and image_found_at_base:
            response_2 = messagebox.askyesno(
                title="Poster Detected",
                message=f"This image appears to be a previously generated poster.\n\n"
                        f"Original base image:\n{base_image_path}\n\n"
                        f"Do you want to continue editing this poster?"
            )
            if response_2:
                os.makedirs(self.CURRENT_IMAGE_PATH, exist_ok=True)
                dest_path = os.path.join(self.CURRENT_IMAGE_PATH, "current_image.png")
                try:
                    for f in glob.glob(os.path.join(self.CURRENT_IMAGE_PATH, "current_image.*")):
                        os.remove(f)
                    shutil.copy(base_image_path, dest_path)
                except Exception as e:
                    messagebox.showerror("Error", f"Error copying file: {e}")
                    return
                self.has_image = True
                self.response_2 = True
                self.save_edited_image(Image.open(self.file_path))
                self.app.update_edited_image(upload=True)
                return
            else:
                self.response_2 = False

        # --- Regular base image load ---
        os.makedirs(self.CURRENT_IMAGE_PATH, exist_ok=True)
        _, ext = os.path.splitext(self.file_path)
        dest_path = os.path.join(self.CURRENT_IMAGE_PATH, f"current_image{ext}")

        try:
            for f in glob.glob(os.path.join(self.CURRENT_IMAGE_PATH, "current_image.*")):
                os.remove(f)
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

        try:
            meta = PngImagePlugin.PngInfo()
            if self.file_path:
                meta.add_text("BaseImagePath", self.file_path)
            edited_image.save(dest_path, format="PNG", pnginfo=meta)
        except Exception as e:
            messagebox.showerror("Error", f"Error saving edited image: {str(e)}")

    def save_image_to_desktop(self):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        file_name = "Wild_West_Poster_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
        save_path = os.path.join(desktop_path, file_name)
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
