'''
Created on Jan 19, 2021

@author: Japi42
'''

class LedDevice:

    def __init__(self):
        self.outputs = []
        self.control_mappings = {}

    def resetLEDs(self):
        for output_id in self.control_mappings:
            output = self.control_mappings[output_id]
            output.disableLED()
        
    def addLED(self, control_id, pin):
        output = LedOutput(device=self, control_id=control_id, pin=pin)
        self.control_mappings[control_id] = output
        self.outputs.append(output)
        print("Added LED " + control_id + " (" + str(pin) + ")")
        return output
        
    def getLED(self, control_id):
        return self.control_mappings[control_id]
        
    def enableLED(self, control_id):

        if control_id in self.control_mappings:
            self.control_mappings[control_id].enableLED()
            
    def disableLED(self, control_id):
        if control_id in self.control_mappings:
            self.control_mappings[control_id].disableLED()
    
class LedOutput:

    def __init__(self, device=None, control_id=None, pin=None):
        self.control_id = control_id
        self.pin = pin
        self.state = 0
        self.device = device
        
    def enableLED(self):
        self.state = 1
        
    def disableLED(self):
        self.state = 0        
        
