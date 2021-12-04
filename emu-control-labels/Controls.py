'''
Created on Nov 26, 2021

@author: Japi42
'''

from ECL_config import main_config
from ECL_core import updateControls
from ECL_core import sleepDisplays,wakeDisplays

import threading
import time

class ControlsController(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.condition = threading.Condition()
        self.current_game = {}
        self.multitext_ids = {}
        self.next_game = {}
        self.next_wake = False
        self.last_update = time.time()
        self.next_control_ids = []
        self.clearControlsQueue()
        self.setDaemon(True)

    def wakeControls(self):
        with self.condition:
            self.next_wake = True
            self.last_update = time.time()
            self.condition.notifyAll()
        
    def clearControlsQueue(self):
        with self.condition:
            self.next_game['game'] = None
            self.next_game['emulator'] = None
            self.next_game['mappings'] = None
            self.next_control_ids = []
            self.condition.notifyAll()
            
    def checkControlsUpdate(self):
        with self.condition:
            if self.next_game['game'] is not None:
                return True
            if self.next_game['emulator'] is not None:
                return True
            if self.next_game['mappings'] is not None:
                return True
            if len(self.next_control_ids) > 0:
                return True
            if self.next_wake:
                return True

            current_time = time.time()
            if current_time > (self.last_update + main_config.burn_in_time):
                return True
            
        return False
    
    def run(self):
    
        while True:
            game = None
            emulator = None
            mappings = None
            updateAll = False
            sleep = False
            wake = False
            
            with self.condition:
                self.condition.wait_for(self.checkControlsUpdate,timeout=1)
                game = self.next_game['game']
                emulator = self.next_game['emulator']
                mappings = self.next_game['mappings']
                if game is not None:
                    self.current_game = self.next_game.copy()
                    updateAll = True
                else:
                    game = self.current_game.get('game')
                    emulator = self.current_game.get('emulator')
                    mappings = self.current_game.get('mappings')
                    next_control_ids = self.next_control_ids.copy()
                    updateAll = False

                multitext_ids = self.multitext_ids.copy()

                if self.next_wake:
                    wake = True
                    self.next_wake = False
                
                if time.time() > (self.last_update + main_config.burn_in_time):
                    sleep = True
                    self.last_update = time.time()
                    
                self.clearControlsQueue()

            if updateAll:
                updateControls(game, emulator, mappings, multitext_ids=multitext_ids)
            elif game is not None and len(next_control_ids) > 0:
                for control_id in next_control_ids:
                    updateControls(game, emulator, mappings, multitext_ids=multitext_ids, update_display_id=control_id)
            else:
                if sleep:
                    sleepDisplays()
                elif wake:
                    wakeDisplays()

    def queueUpdateControls(self, game, emulator, mappings):
        
        with self.condition:
            self.next_game['game'] = game
            self.next_game['emulator'] = emulator
            self.next_game['mappings'] = mappings
            self.multitext_ids = {}
            self.next_control_ids = []

            self.last_update = time.time()

            self.condition.notifyAll()
    
    def queueUpdateMultiText(self, control_id, text_id):

        with self.condition:
            print("Queue " + control_id + " update to " + text_id)
            self.multitext_ids[control_id] = text_id

# Only add to the to-be-updated list if not already in the list

            existing = False
            for s_c in self.next_control_ids:
                if s_c == control_id:
                    existing = True

            if not existing:
                self.next_control_ids.append(control_id)

            self.last_update = time.time()
            
            self.condition.notifyAll()

main_controller = ControlsController()
