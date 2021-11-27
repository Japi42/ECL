'''
Created on Nov 26, 2021

@author: Japi42
'''

from ECL_config import ECL_config
from ECL_config import main_config
from LedDevices.PacDrive import PacDrive
from ECL_core import updateControls

import threading

class ControlsController(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.condition = threading.Condition()
        self.next_game = {}
        self.next_control_id = {}
        self.clearControlsQueue()
        self.setDaemon(True)
        
    def clearControlsQueue(self):
        with self.condition:
            self.next_game['game'] = None
            self.next_game['emulator'] = None
            self.next_game['mappings'] = None
            self.condition.notifyAll()
            
    def checkControlsUpdate(self):
        with self.condition:
            if self.next_game['game'] is not None:
                return True
            if self.next_game['emulator'] is not None:
                return True
            if self.next_game['mappings'] is not None:
                return True
            
        return False
    
    def run(self):
    
        while True:
            game = None
            emulator = None
            mappings = None
            
            with self.condition:
                self.condition.wait_for(self.checkControlsUpdate)
                game = self.next_game['game']
                emulator = self.next_game['emulator']
                mappings = self.next_game['mappings']
                self.clearControlsQueue()

            if game is not None:
                updateControls(game, emulator, mappings)
                
    def queueUpdateControls(self,game, emulator, mappings):
        
        with self.condition:
            self.next_game['game'] = game
            self.next_game['emulator'] = emulator
            self.next_game['mappings'] = mappings
    
            self.condition.notifyAll()

            
main_controller = ControlsController()
