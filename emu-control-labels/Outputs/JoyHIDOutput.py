'''
Created on Nov 22, 2021

@author: Japi42
'''

import threading

from struct import pack

from Outputs.Output import Output

condition = threading.Condition()
inited = False
x_axis = 0
y_axis = 0
my_buttons = 0
dirty = False
devhandle = None

# Need a thread for working
# Need a condition for thread safety
# Need an array of states for output

def startup():
    global inited
    
    if not inited:
        print("Starting up Update Joystick Thread")
        ut = threading.Thread(name='UpdateJoystickThread', target=updateJoystickThread)
        ut.start()
        inited = True

def setButton(button, state):
    global my_buttons
    global condition
    global dirty

    with condition:
        if state:
            my_buttons |= (1<<button)
        else:
            my_buttons &= ~(1<<button)

        dirty = True
        condition.notifyAll()

        
def initJoystick(devname="/dev/hidg0"):
    global devhandle
    global dirty
    
    print("Initing joystick")
    devhandle = open(devname, 'wb+')
    x_axis = 0
    y_axis = 0
    my_buttons = 0
    dirty = False
    report = buildHIDReport()
    writeHIDReport(report)
    print("Init done")
    
def writeHIDReport(report):
    global devhandle

    print("Writing HID report")
    
    devhandle.write(report)
    devhandle.flush()

    print("Done writing HID report")

    
def buildHIDReport():
    report = pack('<bbH', x_axis, y_axis, my_buttons)
    return report
    
def updateJoystickThread():

    global condition
    global dirty
    
    initJoystick()
    
    while True:
        with condition:
            condition.wait_for(checkControlsUpdate)
            report = pack('<bbH', x_axis, y_axis, my_buttons)
            dirty = False

        writeHIDReport(report)

def checkControlsUpdate():
    global condition
    global dirty

    with condition:
        return dirty

class JoyHIDOutput:

    def __init__(self, output_id, button_num):
        Output.__init__(self)
        self.id = output_id
        self.button_num = button_num
        startup()

    def setState(self, state):
        with self.condition:
            self.state = state
            setButton(self.button_num, state)
            print(str(self.id) + " changed to " + str(state))

