'''
Created on Nov 22, 2021

@author: Japi42
'''

import threading

class Output:

    def __init__(self):
        self.condition = threading.Condition()
        self.state = None

    def setState(self, state):
        with self.condition:
            self.state = state

