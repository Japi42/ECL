'''
Created on Nov 22, 2021

@author: Japi42
'''

import threading
import time

from Inputs.Input import Input

class TimerInput:

    def __init__(self, interval=5, hold=0.1):
        Input.__init__(self)
        self.interval = interval
        self.state = False
        self.last_time = time.time()
        self.hold_time = hold
        self.next_time = self.last_time + self.interval
 
    def getState(self):
        with self.condition:
            cur_time = time.time()
            if cur_time >= self.next_time:
                if self.state:
                    self.next_time = cur_time + self.interval
                    self.state = False
                else:
                    self.next_time = cur_time + self.hold_time
                    self.state = True

            return self.state
               
