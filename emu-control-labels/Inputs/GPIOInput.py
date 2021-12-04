'''
Created on Nov 22, 2021

@author: Japi42
'''

import board
from digitalio import DigitalInOut, Direction, Pull

from Controls import main_controller

import threading

from Inputs.Input import Input

class GPIOInput:

    def __init__(self, pin=None):
        Input.__init__(self)
        self.pin = pin
        self.button =  DigitalInOut(self.pinMapper(pin))
        self.button.direction = Direction.INPUT
        self.button.pull = Pull.UP

    def getState(self):
        with self.condition:
            if self.button.value:
                self.state = False
            else:
                self.state = True

            if self.state != self.last_state:
                self.last_state = self.state
                main_controller.wakeControls()
            
            return self.state

    def pinMapper(self, pin):
        if pin == "D4":
            return board.D4
        elif pin == "D5":
            return board.D5
        elif pin == "D6":
            return board.D6
        elif pin == "D12":
            return board.D12
        elif pin == "D13":
            return board.D13
        elif pin == "D17":
            return board.D17
        elif pin == "D18":
            return board.D18
        elif pin == "D22":
            return board.D22
        elif pin == "D23":
            return board.D23
        elif pin == "D27":
            return board.D27
        else:
            return None

