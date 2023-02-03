
from Displays.Display import Display

class TextOut(Display):

    def __init__(self, id=''):
        super().__init__()
        self.id = id
        self.width = 96
        self.height = 64
        self.colors = 65536

    def display_text(self, text, font_name=None, font_size=None, color=None):
        self.awaken()
        if self.id is not None and text is not None:
            print(self.id + ":" + text)
        else:
            print("ID None? text: " + text)

    def display_image(self, image):
        pass

    def calc_max_font_size(self, text, font_name=None, size_hint=None):
        return None
    
    def sleep(self):
        print(self.id + " went to sleep")
        pass

    def awaken(self):
        if self.id is not None:
           print(self.id + " woke up")
        pass
