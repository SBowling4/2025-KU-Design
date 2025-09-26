from frontend import GUI
from backend import file_handling


class AppController:
    def __init__(self):
        self.file_handler = file_handling.FileHandler()
        self.app = GUI.App("azure", "dark")

        self.setup_component_connections()

        self.app.run()

    def setup_component_connections(self):
        print("Connections Setup")
        self.file_handler.app = self.app

        self.app.file_handler = self.file_handler

    def get_app(self):
        return self.app

    def get_file_handler(self):
        return self.file_handler