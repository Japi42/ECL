'''
Created on Jan 19, 2021

@author: Japi42
'''

import threading

from Outputs.Output import Output

class TextOutput:

    def __init__(self, output_id):
        Output.__init__(self)
        self.id = output_id

    def setState(self, state):
        with self.condition:
            self.state = state
            print(str(self.id) + " changed to " + str(state))

