from PIL import Image, ImageDraw

from resources import resources


class ImageCreator:
    app = None
    entries = []

    def create_image(self):
        self.entries = self.app.get_entries()

        print("Creating image with:")
        print("Name: ", self.entries['name'])
        print("Location: ", self.entries['location'])
        print("Font: ", self.entries['font'])
        print("Frame: ", self.entries['frame'])
        print("Filter: ", self.entries['filter'])
        print("Text Color: ", self.entries['text_color'])

        name = self.entries["name"]
        location = self.entries["location"]
        font = self.entries["font"]
        color = self.entries["text_color"]

        frame = self.entries["frame"]
        fil = self.entries["filter"]

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
            raise Exception("Unknown background image")

        if frame == "frame_1":
            frame_image = resources.frame_1
            name_position = (50, 340)
            date_position = (50, 390)
        elif frame == "frame_2":
            frame_image = resources.frame_2
            name_position = (50, 290)
            date_position = (50, 340)
        elif frame == "frame_3":
            frame_image = resources.frame_3
            name_position = (100, 325)
            date_position = (100, 375)
        else:
            raise Exception("Unknown frame image")

        if font == "Breaking Road":
            font_obj = resources.breaking_road
        elif font == "Perfecto":
            font_obj = resources.perfecto
        elif font == "Priestacy":
            font_obj = resources.priestacy
        else:
            raise Exception("Unknown font")

        if color == "White":
            text_color = (255,255,255)
        elif color == "Black":
            text_color = (0,0,0)
        else:
            text_color = (255,255,255)

        current_image = resources.get_current_image().convert("RGBA")

        frame_image = frame_image.resize(current_image.size).convert("RGBA")

        filter_image = filter_image.resize(current_image.size).convert("RGBA")


        current_image_frame = Image.alpha_composite(current_image, frame_image)

        draw = ImageDraw.Draw(current_image_frame)

        draw.text(xy=name_position, text=name, font=font_obj, fill=text_color)
        draw.text(xy=date_position, text=location, font=font_obj, fill=text_color)

        final_image = Image.alpha_composite(current_image_frame, filter_image)

        brown_overlay = Image.new("RGBA", final_image.size, filter_color)

        final_image = Image.blend(final_image, brown_overlay, 0.4)

        return final_image


