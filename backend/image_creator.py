from PIL import Image, ImageDraw
from resources import resources


class ImageCreator:
    app = None

    def __init__(self):
        self.entries = []

    def create_image(self):
        self.entries = self.app.get_entries()

        name = self.entries["name"]
        location = self.entries["location"]
        font = self.entries["font"]
        color = self.entries["text_color"]
        frame = self.entries["frame"]
        fil = self.entries["filter"]

        if len(name) >= 50:
            self.app.messagebox.showerror("Error", "Name too long")
            return resources.get_current_image()

        if len(location) >= 50:
            self.app.messagebox.showerror("Error", "Location too long")
            return resources.get_current_image()

        # Select filter image and overlay color
        if fil == "filter_1":
            filter_image = resources.filter_1
            filter_color = (181, 101, 29, 255)
        elif fil == "filter_2":
            filter_image = resources.filter_2
            filter_color = (135, 98, 21, 255)
        elif fil == "filter_3":
            filter_image = resources.filter_3
            filter_color = (117, 73, 11, 255)
        else:
            filter_image = None

        # Select frame and text positions
        if frame == "frame_1":
            frame_image = resources.frame_1
            name_position = (50, 340)
            location_position = (50, 390)
        elif frame == "frame_2":
            frame_image = resources.frame_2
            name_position = (50, 290)
            location_position = (50, 340)
        elif frame == "frame_3":
            frame_image = resources.frame_3
            name_position = (100, 325)
            location_position = (100, 375)
        else:
            frame_image = None
            name_position = (100,400)
            location_position = (100,450)

        # Select font
        if font == "Breaking Road":
            font_obj = resources.breaking_road
        elif font == "Perfecto":
            font_obj = resources.perfecto
        elif font == "Priestacy":
            font_obj = resources.priestacy
        else:
            raise Exception("Unknown font")

        # Text color
        if color == "White":
            text_color = (255, 255, 255)
        else:
            text_color = (0, 0, 0)

        # Load current image
        current_image = resources.get_current_image().convert("RGBA")

        # Resize frame and filter

        if frame_image:
            frame_image = frame_image.resize(current_image.size).convert("RGBA")

        if filter_image:
            filter_image = filter_image.resize(current_image.size).convert("RGBA")

        current_image_frame = current_image

        if  frame_image:
            current_image_frame = Image.alpha_composite(current_image, frame_image)

        # Draw text
        draw = ImageDraw.Draw(current_image_frame)
        draw.text(xy=name_position, text=name, font=font_obj, fill=text_color)
        draw.text(xy=location_position, text=location, font=font_obj, fill=text_color)

        # Apply filter overlay
        final_image = current_image_frame

        if filter_image:
            final_image = Image.alpha_composite(current_image_frame, filter_image)
            brown_overlay = Image.new("RGBA", final_image.size, filter_color)
            final_image = Image.blend(final_image, brown_overlay, 0.4)



        return final_image
