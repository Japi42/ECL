'''
Created on Nov 22, 2021

@author: Japi42
'''

import threading

class Input:

    def __init__(self):
        self.condition = threading.Condition()
        self.state = None

    def getState(self):
        with self.condition:
            return self.state

