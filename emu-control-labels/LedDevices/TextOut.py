'''
Created on Jan 19, 2021

@author: Japi42
'''

from LedDevices.LedDevice import LedDevice

class TextOut(LedDevice):

    def __init__(self):
        LedDevice.__init__(self)

    def updateLEDs(self):
        for output in self.outputs:
            if output.state == 1:
                print("LED " + str(output.pin) + " enabled")
