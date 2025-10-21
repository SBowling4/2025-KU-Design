from frontend import GUI
from backend import file_handling
from backend import image_creator

file_handler = file_handling.FileHandler()
file_handler.clear_images()

app = GUI.App("azure", "dark")
image = image_creator.ImageCreator()


file_handler.app = app
image.app = app

app.file_handler = file_handler
app.image_creator = image


app.run()

