# backend/file_handling.py
import os
import shutil
from tkinter import filedialog



class FileHandler():
    def __init__(self):
        self.file_path = ""

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FOLDER_PATH = os.path.join(BASE_DIR, "resources", "current_image")

    app = None

    def get_file_from_dialog(self):
        from tkinter import messagebox
        import os

        self.file_path = filedialog.askopenfilename(
            parent=self.app.root,
            title="Select an Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif"), ("All files", "*.*")]
        )

        if not self.file_path:  # User cancelled
            return

        # Ensure destination folder exists
        os.makedirs(self.FOLDER_PATH, exist_ok=True)

        try:
            # Copy file into folder, preserving filename
            dest_path = os.path.join(self.FOLDER_PATH, os.path.basename(self.file_path))
            shutil.copy(self.file_path, dest_path)
        except Exception as e:
            messagebox.showerror("Error", f"Error copying file: {e}")

    def get_file_path(self):
        return self.file_path