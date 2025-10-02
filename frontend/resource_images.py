import glob

from PIL import Image
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FOLDER_PATH = os.path.join(BASE_DIR, "resources")

FRAMES_DIR = os.path.join(FOLDER_PATH, "frames")
BACKGROUND_DIR = os.path.join(FOLDER_PATH, "backgrounds")
CURRENT_IMAGE_DIR = os.path.join(FOLDER_PATH, "current_image")
TEMP_IMAGE_DIR = os.path.join(FOLDER_PATH, "temp_image")

frame_1 = Image.open(os.path.join(FRAMES_DIR, "Frame_1.png"))
frame_2 = Image.open(os.path.join(FRAMES_DIR, "Frame_2.png"))
frame_3 = Image.open(os.path.join(FRAMES_DIR, "Frame_3.png"))

bg_1 = Image.open(os.path.join(BACKGROUND_DIR, "Background_1.png"))
bg_2 = Image.open(os.path.join(BACKGROUND_DIR, "Background_2.png"))
bg_3 = Image.open(os.path.join(BACKGROUND_DIR, "Background_3.png"))

temp_image = Image.open(os.path.join(TEMP_IMAGE_DIR, "temp_image.png"))


def get_current_image():
    current_image_files = glob.glob(os.path.join(CURRENT_IMAGE_DIR, "current_image.*"))

    if not current_image_files:
        raise FileNotFoundError("No current image found")

    return Image.open(current_image_files[0])





