'''
Created on Nov 22, 2021

@author: Japi42
'''

import threading
import time

from Inputs.Input import Input

class TimerInput:

    def __init__(self, interval=5):
        Input.__init__(self)
        self.interval = interval
        self.state = False
        self.last_time = time.time()
 
    def getState(self):
        with self.condition:
            cur_time = time.time()
            diff = cur_time - self.last_time
            if diff >= self.interval:
                self.last_time = cur_time
                if self.state:
                    self.state = False
                else:
                    self.state = True

            return self.state
               
