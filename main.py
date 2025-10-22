from backend.ai_image_editing import AIHandling
from frontend import GUI
from backend import file_handling
from backend import image_creator

file_handler = file_handling.FileHandler()
file_handler.clear_edited_image()
file_handler.clear_current_image()

app = GUI.App("azure", "dark")
image = image_creator.ImageCreator()
ai = AIHandling()

file_handler.app = app

image.app = app

app.file_handler = file_handler
app.image_creator = image
app.ai_handler = ai

ai.file_handler = file_handler

app.run()

