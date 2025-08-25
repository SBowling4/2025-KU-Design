import TKinterModernThemes as TKMT

class ImageButton(TKMT.ThemedTKinterFrame.Button):
    def __init__(self, *args, image=None, **kwargs):
        super().__init__(*args, **kwargs)
        if image is not None:
            self.config(image=image)
