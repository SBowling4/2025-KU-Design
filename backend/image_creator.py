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
        filter = self.entries["bg"]

        filter_image = None

        if filter == "bg_1":
            filter_image = resource_images.filter_1
        elif filter == "bg_2":
            filter_image = resource_images.filter_2
        elif filter == "bg_3":
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

        frame_image.resize(current_image.size)
        filter_image.resize(current_image.size)

        current_image_frame = Image.alpha_composite(frame_image, current_image)

        final_image = Image.alpha_composite(current_image_frame, filter_image)

        return final_image


