'''
Created on Nov 22, 2021

@author: Japi42
'''

import threading

class Mapper:

    def __init__(self):
        self.condition = threading.Condition()

    def update(self):
        with self.condition:
            pass
    
