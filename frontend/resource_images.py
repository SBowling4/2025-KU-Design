from PIL import Image
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

FRAMES_DIR = os.path.join(BASE_DIR, "resources", "frames")
BACKGROUND_DIR = os.path.join(BASE_DIR, "resources", "backgrounds")

frame_1 = Image.open(os.path.join(FRAMES_DIR, "Frame_1.png"))
frame_2 = Image.open(os.path.join(FRAMES_DIR, "Frame_2.png"))
frame_3 = Image.open(os.path.join(FRAMES_DIR, "Frame_3.png"))

bg_1 = Image.open(os.path.join(BACKGROUND_DIR, "Background_1.png"))
bg_2 = Image.open(os.path.join(BACKGROUND_DIR, "Background_2.png"))
bg_3 = Image.open(os.path.join(BACKGROUND_DIR, "Background_3.png"))




