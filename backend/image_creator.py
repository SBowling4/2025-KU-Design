from PIL import Image, ImageFont, ImageDraw

from frontend import resources

class ImageCreator:
    app = None
    entries = []

    def create_image(self):
        self.entries = self.app.get_entries()

        print("Creating image with:")
        print("Name: ", self.entries['name'])
        print("Date: ", self.entries['date'])
        print("Font: ", self.entries['font'])
        print("Frame: ", self.entries['frame'])
        print("Filter: ", self.entries['filter'], "\n\n")

        name = self.entries["name"]
        date = self.entries["date"]
        font = self.entries["font"]

        frame = self.entries["frame"]
        fil = self.entries["filter"]

        filter_image = None

        if fil == "filter_1":
            filter_image = resources.filter_1
        elif fil == "filter_2":
            filter_image = resources.filter_2
        elif fil == "filter_3":
            filter_image = resources.filter_3
        else:
            raise Exception("Unknown background image")

        frame_image = None

        if frame == "frame_1":
            frame_image = resources.frame_1
        elif frame == "frame_2":
            frame_image = resources.frame_2
        elif frame == "frame_3":
            frame_image = resources.frame_3
        else:
            raise Exception("Unknown frame image")

        font_obj = None

        if font == "Breaking Road":
            font_obj = resources.breaking_road
        elif font == "Fortalesia":
            font_obj = resources.fotalesia
        elif font == "Kitten Cafe":
            font_obj = resources.kitten_cafe
        else:
            raise Exception("Unknown font")

        current_image = resources.get_current_image().convert("RGBA")

        frame_image = frame_image.resize(current_image.size).convert("RGBA")

        filter_image = filter_image.resize(current_image.size).convert("RGBA")

        current_image_frame = Image.alpha_composite(current_image, frame_image)

        draw = ImageDraw.Draw(current_image_frame)

        name_position = (0,0)
        date_position = (0,0)

        match frame:
            case "frame_1":
                name_position = (0,0)
                date_position = (0,0)
            case "frame_2":
                name_position = (50, 290)
                date_position = (50, 340)
            case "frame_3":
                name_position = (100, 325)
                date_position = (100, 375)

        text_color = (255, 255, 255)

        draw.text(xy=name_position, text=name, font=font_obj, fill=text_color)
        draw.text(xy=date_position, text=date, font=font_obj, fill=text_color)


        final_image = Image.alpha_composite(current_image_frame, filter_image)

        brown_overlay = Image.new("RGBA", final_image.size, (181, 101, 29, 0))

        final_image = Image.blend(final_image, brown_overlay, 0.3)

        return final_image


