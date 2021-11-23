'''
Created on Jan 19, 2021

@author: Japi42
'''

from LedDevices.LedDevice import LedDevice, LedOutputState

class TextOut(LedDevice):

    def __init__(self):
        LedDevice.__init__(self)

    def updateLEDs(self):
        with self.condition:
            print("LED Status:")
            for output in self.outputs:
                if output.state != LedOutputState.Off:
                    print("LED " + str(output.pin) + " enabled")
