from PIL import Image

from frontend import resource_images

class ImageCreator:
    app = None
    entries = []

    def create_image(self):
        self.entries = self.app.get_entries()

        name = self.entries["name"]
        date = self.entries["date"]
        font = self.entries["font"]

        frame = self.entries["frame"]
        filter = self.entries["filter"]

        filter_image = None

        if filter == "filter_1":
            filter_image = resource_images.filter_1
        elif filter == "filter_2":
            filter_image = resource_images.filter_2
        elif filter == "filter_3":
            filter_image = resource_images.filter_3
        else:
            raise Exception("Unknown background image")

        frame_image = None

        if frame == "frame_1":
            frame_image = resource_images.frame_1
        elif frame == "frame_2":
            frame_image = resource_images.frame_2
        elif frame == "frame_3":
            frame_image = resource_images.frame_3
        else:
            raise Exception("Unknown frame image")

        current_image = resource_images.get_current_image()
        current_image = current_image.convert("RGBA")

        frame_image.resize(current_image.size)
        frame_image = frame_image.convert('RGBA')

        # filter_image.resize(current_image.size)

        current_image_frame = Image.alpha_composite(current_image, frame_image)

        # final_image = Image.alpha_composite(current_image_frame, filter_image)

        return current_image_frame


