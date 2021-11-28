'''
Created on Nov 27, 2021

@author: Japi42
'''

import threading

from struct import pack

from Outputs.Output import Output

class HIDKeyboardUpdater(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.condition = threading.Condition()
        self.dirty = False
        self.devhandle = None
        self.held_keys = [ 0,0,0,0, 0,0,0,0 ]

    def run(self):
        self.initKeyboard()
    
        while True:
            with condition:
                condition.wait_for(checkControlsUpdate)
                report = self.buildHIDReport()
                dirty = False

# send the HID report outside of the lock
                
            self.devhandle.write(report)
            self.devhandle.flush()

    def buildHIDReport(self):
        report = pack('<BBBBBBBB',
                      0x00, 0x00,
                      self.held_keys[0],
                      self.held_keys[1],
                      self.held_keys[2],
                      self.held_keys[3],
                      self.held_keys[4],
                      self.held_keys[5])
        return report

    def pressKey(self, scancode):
        with self.condition:

# Check if the key is already pressed, this
# could confuse things

            for i in range(6):
                if self.held_keys[i] == scancode:
                    print("ERROR: Key pressed again?")
                    return

# Find an open slot for pressing the key
                
            for i in range(6):
                if self.held_keys[i] == 0x0:
                    self.held_keys[i] = scancode
                    self.dirty = True
                    self.condition.notifyAll()
                    return

            print("Max held keys")
                    
    def releaseKey(self, scancode):
        with condition:
            for i in range(6):
                if self.held_keys[i] == scancode:
                    self.held_keys[i] = 0x0
                    self.dirty = True
                    self.condition.notifyAll()
                    return

            print("Key not found while releasing")

    def releaseAllKeys(self):
        with condition:
            for i in range(6):
                self.held_keys[i] = 0x0

            self.dirty = True
            self.condition.notifyAll()
            
    def initKeyboard(self,devname="/dev/hidg1"):
        print("Initing keyboard")
        self.devhandle = open(devname, 'wb+')
        self.dirty = False
        print("Keyboard init done")
    
    def checkControlsUpdate(self):
        with self.condition:
            return self.dirty

keyboardThread = None
        
class KeyHIDOutput:

    def __init__(self, output_id, scancode):
        global keyboardThread
        
        Output.__init__(self)
        self.id = output_id
        self.scancode = scancode
        if keyboardThread is None:
            keyboardThread = HIDKeyboardUpdater()
            keyboardThread.start()
        
    def setState(self, state):
        with self.condition:
            self.state = state
            if state:
                pressKey(self.scancode)
            else:
                releaseKey(self.scancode)
                
            print(str(self.id) + " changed to " + str(state))

