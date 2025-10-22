import glob
import os
import shutil
from PIL import Image, PngImagePlugin
import datetime
import json


class PosterMetadata:
    """Handle poster metadata operations"""

    @staticmethod
    def extract_base_image_path(file_path: str) -> tuple[str | None, bool]:
        """
        Extract base image path from PNG metadata if it exists.
        Returns: (base_image_path, base_exists)
        """
        if not file_path.lower().endswith(".png"):
            return None, False

        try:
            img = Image.open(file_path)
            # Access metadata
            base_image_path = img.info.get("BaseImagePath")
            img.close()

            if base_image_path:
                base_exists = os.path.exists(base_image_path)
                return base_image_path, base_exists
            return None, False
        except Exception as e:
            print(f"Metadata check failed: {e}")
            return None, False

    @staticmethod
    def create_metadata(base_image_path: str) -> PngImagePlugin.PngInfo:
        """Create PNG metadata with base image path"""
        meta = PngImagePlugin.PngInfo()
        if base_image_path:
            # Add file path to metadata
            meta.add_text("BaseImagePath", base_image_path)
        return meta


class FileHandler:
    '''Class for handling file operations'''
    def __init__(self):
        self.file_path = ""
        self.has_image = False
        self.app = None

    # Create file paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CURRENT_IMAGE_PATH = os.path.join(BASE_DIR, "resources", "current_image")
    EDITED_IMAGE_PATH = os.path.join(BASE_DIR, "resources", "edited_image")

    def clear_current_image(self):
        """Clear all current images"""
        for f in glob.glob(os.path.join(self.CURRENT_IMAGE_PATH, "current_image.*")):
            try:
                os.remove(f)
            except Exception as e:
                print(f"Error removing current image: {e}")

    def clear_edited_image(self):
        """Clear all edited images"""
        for f in glob.glob(os.path.join(self.EDITED_IMAGE_PATH, "edited_image.*")):
            try:
                os.remove(f)
            except Exception as e:
                print(f"Error removing edited image: {e}")

    def check_for_poster_metadata(self, file_path: str) -> tuple[str | None, bool]:
        """
        Check if file is a poster with metadata.
        Returns: (base_image_path, base_exists)
        """
        return PosterMetadata.extract_base_image_path(file_path)

    def load_base_image(self, file_path: str) -> bool:
        """
        Load a new base image into current_image directory.
        Returns: True on success, False on failure
        """
        os.makedirs(self.CURRENT_IMAGE_PATH, exist_ok=True) # Checks to see path exists
        _, ext = os.path.splitext(file_path) # Gets the extension
        dest_path = os.path.join(self.CURRENT_IMAGE_PATH, f"current_image{ext}") # Creates destination path, saves extension

        try:
            shutil.copy(file_path, dest_path) # Saves image
            self.file_path = file_path
            self.has_image = True
            return True
        except Exception as e:
            print(f"Error loading base image: {e}")
            return False

    def load_poster_for_editing(self, poster_path: str, base_image_path: str) -> bool:
        """
        Load a poster and its base image for continued editing.
        Returns: True on success, False on failure
        """
        os.makedirs(self.CURRENT_IMAGE_PATH, exist_ok=True) # Verifies 
        dest_path = os.path.join(self.CURRENT_IMAGE_PATH, "current_image.png")

        try:
            # Copy base image to current_image
            shutil.copy(base_image_path, dest_path)

            # Save the poster as edited_image
            poster_img = Image.open(poster_path)
            self.file_path = base_image_path
            self.save_edited_image(poster_img)
            poster_img.close()

            self.has_image = True
            return True
        except Exception as e:
            print(f"Error loading poster for editing: {e}")
            return False
        
    

    def save_edited_image(self, edited_image: Image) -> bool:
        """
        Save the edited image with metadata.
        Returns: True on success, False on failure
        """
        self.clear_edited_image()

        os.makedirs(self.EDITED_IMAGE_PATH, exist_ok=True) # Verifies
        dest_path = os.path.join(self.EDITED_IMAGE_PATH, "edited_image.png")

        try:
            meta = PosterMetadata.create_metadata(self.file_path) # Sets image metadata
            edited_image.save(dest_path, format="PNG", pnginfo=meta) # Saves
            return True
        except Exception as e:
            print(f"Error saving edited image: {e}")
            return False

    def save_image_to_desktop(self) -> tuple[bool, str]:
        """
        Save edited image to desktop.
        Returns: (success, message) tuple
        """
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop") # Finds path to desktop
        file_name = "Wild_West_Poster_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".png" # Name for saved image
        save_path = os.path.join(desktop_path, file_name)
        edited_image_files = glob.glob(os.path.join(self.EDITED_IMAGE_PATH, "edited_image.*"))

        if not edited_image_files:
            return False, "No edited image to save. Please generate an image first."

        try:
            shutil.copy(edited_image_files[0], save_path) # Saves image to desktop
            return True, f"Image saved to Desktop as {file_name}!"
        except Exception as e:
            return False, f"Error saving image: {str(e)}"

    def get_file_path(self) -> str:
        """Get the current base image file path"""
        return self.file_path