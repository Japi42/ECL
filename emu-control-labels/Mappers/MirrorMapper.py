'''
Created on Jan 19, 2021

@author: Japi42
'''

import threading

from Mappers.Mapper import Mapper

class MirrorMapper:

    def __init__(self, id, input, output):
        Mapper.__init__(self)
        self.id = id
        self.input = input
        self.output = output
        self.last_state = None
        
    def update(self):
        with self.condition:
            state = self.input.getState()
            if state != self.last_state:
                self.last_state = state
                self.output.setState(state)
                
