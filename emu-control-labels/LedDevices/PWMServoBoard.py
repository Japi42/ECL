'''

LED Driver for an Adafruit PCA9685 LED/Servo board.

Controls up to 16 LEDs via i2c.  Up to 62 boards are supported.  

Pins start at "0", like they are labeld on the board.

LEDs are powered from the 3.3V I2C voltage, which can make standard 5V 
arcade LEDs dim, especially when combined with the inline 220 Ohm resistors
on the PWM pins.

Created on Jan 19, 2021

@author: Japi42
'''

from board import SCL, SDA
import busio

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

from LedDevices.LedDevice import LedDevice, LedOutputState

class PWMServoBoard(LedDevice):

    def __init__(self, address=64):
        LedDevice.__init__(self)
        self.i2c_bus = busio.I2C(SCL, SDA)
        self.pca = PCA9685(self.i2c_bus, address=address)

# set the PWM frequency

        self.pca.frequency = 1000 

    def updateLEDs(self):
        with self.condition:
            for output in self.outputs:
                if output.state != LedOutputState.Off:
                     self.pca.channels[output.pin].duty_cycle = 0x0ffff
                else:
                     self.pca.channels[output.pin].duty_cycle = 0x0

