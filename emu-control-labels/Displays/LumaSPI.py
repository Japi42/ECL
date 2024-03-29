'''
Created on Sep 18, 2020

@author: Japi42
'''

from Displays.Display import Display
from luma.core.interface.serial import gpio_cs_spi
from luma.core.render import canvas
from luma.oled.device import ssd1331
from luma.oled.device import ssd1351
import time

class LumaSPI(Display):

    def __init__(self, device=0, port=0, cs=8, dc=24, rst=None, rotation=0, baudrate=4000000, subtype="SSD1331"):


        if subtype == "SSD1331":
            self.width = 96
            self.height = 64
            self.colors = 65536
        elif subtype == "SSD1351":
            self.width = 128
            self.height = 128
            self.colors = 65536
        else:
            print("Unknown Luma SPI display type " + subtype) 
            sys.exit(1)

        self.rotation = rotation
        self.baudrate = baudrate

        if self.baudrate is None:
            self.baudrate = 4000000

        print("Bus speed: " + str(self.baudrate))

# Convert rotation degrees into Luma rotation values

        luma_rot = 0
        if self.rotation == 90:
            luma_rot = 1
        elif self.rotation == 180:
            luma_rot = 2
        elif self.rotation == 270:
            luma_rot = 3

        self.serial = gpio_cs_spi(device=device, port=port, gpio_CS=cs, gpio_RST=rst, reset_hold_time=0.2, reset_release_time=0.15, bus_speed_hz=self.baudrate)
 
        if subtype == "SSD1331":
            self.device = ssd1331(self.serial, rotate=luma_rot)
        elif subtype == "SSD1351":       
            self.device = ssd1351(self.serial, rotate=luma_rot)
        time.sleep(0.1)

# init the draw context

        self.init_draw_context()
    
    def output_image(self, image):
        self.awaken()
        self.device.display(image.convert(self.device.mode))

    def sleep(self):
        self.device.hide()
        pass

    def awaken(self):
        self.device.show()
        pass
