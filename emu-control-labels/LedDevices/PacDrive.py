'''
Created on Jan 19, 2021

@author: Japi42
'''

import json
import sys
import subprocess
from LedDevices.LedDevice import LedDevice, LedOutputState

class PacDrive(LedDevice):

    def __init__(self, board=1, umtool=None):
        LedDevice.__init__(self)
        self.board = board
        if umtool is not None:
            self.umtool = umtool
        else:
            self.umtool = "/usr/local/bin/umtool"

    def updateLEDs(self):
        with self.condition:
            self.run_umtool()
    
    def build_led_list(self):
        leds = []
        
        for output in self.outputs:
            print("Found output " + str(output.pin))
            if output.state != LedOutputState.Off:
                leds.append(output.pin)
        
        return leds
        
    def run_umtool(self):
        output = {}
        output.update({"version":1 })
        output.update({"product": "pacdrive"})
        output.update({"board id": self.board})
        leds = self.build_led_list()
        output.update({"led": leds})
        f = open("/tmp/pacdrive.json", "w")
        f.write(json.dumps(output))
        f.close()
        args = [self.umtool, '/tmp/pacdrive.json']
        subprocess.call(args)

        
