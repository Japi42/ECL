'''
Created on Sep 15, 2020

@author: Japi42
'''

from Emulators.Emu_config import Emu_config, Emu_game_config, Control_label

class Generic_Config(Emu_config):
    
    def __init__(self):
        super().__init__()
        self.emulator_id = 'supermodel'
    
