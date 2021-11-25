
class Display:

    font_cache = {}

    def __init__(self):
        self.width = 0
        self.height = 0
        self.colors = 0

    def init_draw_context(self):
        from PIL import Image, ImageDraw, ImageFont

        # Get an image for drawing on, and a drawing context

        self.image = Image.new("RGB", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)

    def display_text(self, text, font_name=None, font_size=None, color="#ffffff"):
        if font_size is None:
            font_size = 24

        font = self.get_font(font_name, font_size)

        self.draw.rectangle((0, 0, self.width-1, self.height-1), outline="#000000", fill="#000000")
        
        (text_width, text_height) = self.draw.textsize(text, font) 

        x = (self.width / 2) - (text_width / 2)
        y = (self.height / 2) - (text_height / 2)
        
        self.draw.multiline_text((x, y), text, font=font, fill=color, align="center")

        self.output_image(self.image)

    def calc_max_font_size(self, text, font_name=None):

        for font_size in range(80, 1, -1):
            font = self.get_font(font_name, font_size)

            (text_width, text_height) = self.draw.textsize(text, font) 

            if text_width <= self.width and text_height <= self.height:
                print("Font size: " + str(font_size))
                return font_size

        return None


    def get_font(self, font_name=None, font_size=None):
        from ECL_config import main_config
        
        if font_name is None:
            font_name = main_config.default_font
            
        if font_size is None:
            font_size = 24

        font_size = int(font_size)

        key = font_name + "-" + str(font_size)
        
        font = Display.font_cache.get(key)
        if font is None:
            from PIL import Image, ImageDraw, ImageFont
            try:
                font = ImageFont.truetype(main_config.font_path + font_name, font_size)
            except Exception as e:
                font = ImageFont.truetype(main_config.font_path + main_config.default_font, font_size)
                pass
    
            Display.font_cache[key] = font
            
        return font
            
