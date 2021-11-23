'''

Led Driver for a Adafruit AW9523 GPIO Expander/LED driver board

Supports up to 16 LEDs, using i2c.  Up to four boards can be connected.

Pins start at "0", to match the labels on the board.  

Created on Nov 12, 2021

@author: Japi42
'''

import busio
import board
import adafruit_aw9523

from LedDevices.LedDevice import LedDevice, LedOutputState

class LedAW9523(LedDevice):

    def __init__(self, address=88):
        LedDevice.__init__(self)
        self.i2c_bus = busio.I2C(board.SCL, board.SDA)
        self.aw = adafruit_aw9523.AW9523(self.i2c_bus, address=address)

# set all pins to outputs, LED constant current mode

        self.aw.LED_modes = 0x0FFFF 
        self.aw.directions = 0x0FFFF 

    def updateLEDs(self):
        with self.condition:
            for output in self.outputs:
                if output.state != LedOutputState.Off:
                     self.aw.set_constant_current(output.pin, 0x0ff)
                else:
                     self.aw.set_constant_current(output.pin, 0x000)

