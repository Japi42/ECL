
from Displays.Display import Display

class TextOut(Display):

    def __init__(self, id=''):
        super().__init__()
        self.id = id
        self.width = 96
        self.height = 64
        self.colors = 65536
        self.init_draw_context()

    def display_text(self, text, font_name=None, font_size=None, color=None):
        print(self.id + ":" + text)

    def display_image(self, image):
        pass

