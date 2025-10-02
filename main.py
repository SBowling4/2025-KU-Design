from frontend import GUI
from backend import file_handling


file_handler = file_handling.FileHandler()
app = GUI.App("azure", "dark")

file_handler.app = app
app.file_handler = file_handler

app.run()

