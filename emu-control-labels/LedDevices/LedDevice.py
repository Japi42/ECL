'''
Created on Jan 19, 2021

@author: Japi42
'''

from enum import Enum, unique

import threading

@unique
class LedOutputState(Enum):
    Off = 0
    On = 1
    AlwaysOn = 2

class LedDevice:

    def __init__(self):
        self.condition = threading.Condition()
        self.outputs = []
        self.control_mappings = {}

    def hardResetLEDs(self):
        with self.condition:
            for output_id in self.control_mappings:
                output = self.control_mappings[output_id]
                output.disableLED()

    def resetLEDs(self):
        with self.condition:
            for output_id in self.control_mappings:
                output = self.control_mappings[output_id]
                if output.state != LedOutputState.AlwaysOn:
                    output.disableLED()
        
    def addLED(self, control_id, pin):
        with self.condition:
            output = LedOutput(device=self, control_id=control_id, pin=pin)
            self.control_mappings[control_id] = output
            self.outputs.append(output)
            print("Added LED " + control_id + " (" + str(pin) + ")")
            return output
        
    def getLED(self, control_id):
        with self.condition:
            return self.control_mappings[control_id]
        
    def enableLED(self, control_id):
        with self.condition:
            if control_id in self.control_mappings:
                self.control_mappings[control_id].enableLED()
            
    def disableLED(self, control_id):
        with self.condition:
            if control_id in self.control_mappings:
                self.control_mappings[control_id].disableLED()

    def setAlwaysOn(self, control_id):
        with self.condition:
            if control_id in self.control_mappings:
                self.control_mappings[control_id].setAlwaysOn()

class LedOutput:

    def __init__(self, device=None, control_id=None, pin=None):
        self.control_id = control_id
        self.pin = pin
        self.state = LedOutputState.Off
        self.device = device
        
    def enableLED(self):
        if self.state != LedOutputState.AlwaysOn:
            self.state = LedOutputState.On
        
    def disableLED(self):
        if self.state != LedOutputState.AlwaysOn:
            self.state = LedOutputState.Off

    def setAlwaysOn(self):
        self.state = LedOutputState.AlwaysOn        

