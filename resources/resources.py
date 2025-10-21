import glob
from PIL import Image, ImageFont
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FOLDER_PATH = os.path.join(BASE_DIR, "resources")

FRAMES_DIR = os.path.join(FOLDER_PATH, "frames")
BACKGROUND_DIR = os.path.join(FOLDER_PATH, "filters")
CURRENT_IMAGE_DIR = os.path.join(FOLDER_PATH, "current_image")
EDITED_IMAGE_DIR = os.path.join(FOLDER_PATH, "edited_image")
FONTS_DIR = os.path.join(FOLDER_PATH, "fonts")
FILTER_DISPLAYS_DIR = os.path.join(FOLDER_PATH, "filter_displays")
TEMP_IMAGE_DIR = os.path.join(FOLDER_PATH, "temp_image", "temp_image.jpg")

# Frames
frame_1 = Image.open(os.path.join(FRAMES_DIR, "Frame_1.png"))
frame_2 = Image.open(os.path.join(FRAMES_DIR, "Frame_2.png"))
frame_3 = Image.open(os.path.join(FRAMES_DIR, "Frame_3.png"))

# Filters
filter_1 = Image.open(os.path.join(BACKGROUND_DIR, "Filter_1.png"))
filter_2 = Image.open(os.path.join(BACKGROUND_DIR, "Filter_2.png"))
filter_3 = Image.open(os.path.join(BACKGROUND_DIR, "Filter_3.png"))

# Filter displays for GUI
filter_display_1 = Image.open(os.path.join(FILTER_DISPLAYS_DIR, "Filter_display_1.png"))
filter_display_2 = Image.open(os.path.join(FILTER_DISPLAYS_DIR, "Filter_display_2.png"))
filter_display_3 = Image.open(os.path.join(FILTER_DISPLAYS_DIR, "Filter_display_3.png"))

# Temp fallback image
temp_image = Image.open(TEMP_IMAGE_DIR).resize((500, 500))

# Fonts
breaking_road = ImageFont.truetype(os.path.join(FONTS_DIR, "breaking_road.ttf"), 30)
perfecto = ImageFont.truetype(os.path.join(FONTS_DIR, "perfecto.ttf"), 30)
priestacy = ImageFont.truetype(os.path.join(FONTS_DIR, "priestacy.otf"), 30)


def get_current_image():
    current_image_files = glob.glob(os.path.join(CURRENT_IMAGE_DIR, "current_image.*"))
    if not current_image_files:
        raise FileNotFoundError("No current image found")
    return Image.open(current_image_files[0]).resize((500, 500)).convert('RGB')


def get_edited_image():
    edited_image_files = glob.glob(os.path.join(EDITED_IMAGE_DIR, "edited_image.*"))
    if not edited_image_files:
        raise FileNotFoundError("No edited image found")
    return Image.open(edited_image_files[0])
