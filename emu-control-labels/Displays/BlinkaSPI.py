
from Displays.Display import Display
import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ssd1331 as ssd1331  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1351 as ssd1351  # pylint: disable=unused-import

class BlinkaSPI(Display):

    # Shared SPI bus
    shared_spi = board.SPI()

    def __init__(self, spi=None, cs="C0", dc="C1", rst=None, rotation=0, baudrate=16000000, driver_chip=None):
        self.width = 128
        self.height = 128
        self.colors = 65536
        self.rotation = rotation
        self.baudrate = baudrate
        
        self.cs_pin = self.create_pin(cs)
        self.dc_pin = self.create_pin(dc)
        self.reset_pin = self.create_pin(rst)
        if spi is None:
            self.spi = self.shared_spi
        else:
            self.spi = spi

# Create the display object

        if driver_chip == "ssd1351":
            self.width = 128
            self.height = 128
            self.disp = ssd1351.SSD1351(self.spi,
                               rotation=self.rotation,
                               cs=self.cs_pin,
                               dc=self.dc_pin,
                               rst=self.reset_pin,
                               baudrate=self.baudrate,
                               )
        else:
            self.width = 96
            self.height = 64
            self.disp = ssd1331.SSD1331(self.spi,
                               rotation=self.rotation,
                               cs=self.cs_pin,
                               dc=self.dc_pin,
                               rst=self.reset_pin,
                               baudrate=self.baudrate,
                               )

        self.disp.fill(0)

# init the draw context

        self.init_draw_context()
    
# Helper function to create a pin from a text string.  
# Uses eval - not exactly safe.  Need to update to either validate or restrict what
# can be used.
    
    def create_pin(self, pin):
        if pin is None:
            return None
        board_pin = eval("board." + pin)
        pin_obj = digitalio.DigitalInOut(board_pin)
        return pin_obj
    
    def output_image(self, image):
        self.disp.image(image)

