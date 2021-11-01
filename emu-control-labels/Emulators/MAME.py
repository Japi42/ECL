'''
Created on Sep 15, 2020

@author: Japi42
'''

from Emulators.Emu_config import Emu_config, Emu_game_config, Control_label
import xml.etree.ElementTree as ET
import re
import os.path
from os import path

class MAME_Config(Emu_config):
    
    def __init__(self, config_path="~/.mame/cfg/"):
        super().__init__()
        self.config_path = config_path
        if self.config_path.endswith("/") is False:
            self.config_path = self.config_path + "/"
        self.empty_cfg = MAME_ctrlr_config()
        self.empty_cfg.set_defaults()
        self.default_cfg = MAME_ctrlr_config(self.config_path + "default.cfg")
        self.emulator_id = 'mame'
    
    def load_game_config(self, game_id):
        if game_id not in self.game_configs:
            self.game_configs[game_id] = MAME_game_config(game_id, self.config_path)

        return self.game_configs[game_id]
    
    def lookup_control_mapping(self, game_id, control_id):
        
        self.load_game_config(game_id)

# Apply emulator specific mapping (control to key code) 
        
        emu_control_id = self.control_mappings.get(control_id)
        if emu_control_id is None:
            emu_control_id = control_id

# Apply game specific mapping (keycode to control)
        
        mame_game_cfg = self.game_configs[game_id]
        if mame_game_cfg != None:
            mame_ctrlr_cfg = mame_game_cfg.game_ctrlr_config
        
        # check game specific config file
        
        if mame_ctrlr_cfg != None:
            control = mame_ctrlr_cfg.control_mappings.get(emu_control_id)
            if control != None:
                return control
        
        # check default config

        if self.default_cfg != None:
            control = self.default_cfg.control_mappings.get(emu_control_id)
            if control != None:
                return control
        
        # check hard coded defaults
        
        control = self.empty_cfg.control_mappings.get(emu_control_id)
        if control != None:
            return control
        
        return control_id
        
class MAME_game_config(Emu_game_config):
    
    def __init__(self, game_id, config_path):
        self.config_path = config_path
        super().__init__(game_id, 'mame')
        if game_id is not None:
            self.game_ctrlr_config = MAME_ctrlr_config(self.config_path + game_id + ".cfg", game_id)

class MAME_ctrlr_config:
    
    def __init__(self, filename=None, romname = "default"):

        print("Loading MAME config for " + romname)
        self.control_mappings = {}
        if filename == None or path.exists(filename) == False:
            self.set_defaults()
        else:
            self.load_from_xml(filename, romname)
    
    def load_from_xml(self, filename, romname):
        tree = ET.parse(filename)
        root = tree.getroot()
        
        ports = root.findall("./system[@name='" + romname + "']/input/port")
        for port in ports:
            if 'type' in port.attrib:
                type = port.attrib['type']
            
                seqs = port.findall("./newseq[@type='standard']")
                for seq in seqs:
                    keystr = seq.text
                    self.parse_keyseq(type, keystr)
        
    def parse_keyseq(self, type, all_seqs):
        
        seqs = all_seqs.split("OR")
        for seq in seqs:
            raw_seq = seq.strip()
            
            # Don't allow chorded controls
            
            if raw_seq.find(" ") == -1:
                self.control_mappings[raw_seq] = type
    
    def set_defaults(self):
        self.control_mappings['JOYCODE_1_BUTTON1'] = "P1_BUTTON1"
        self.control_mappings['JOYCODE_1_BUTTON2'] = "P1_BUTTON2"
        self.control_mappings['JOYCODE_1_BUTTON3'] = "P1_BUTTON3"
        self.control_mappings['JOYCODE_1_BUTTON4'] = "P1_BUTTON4"
        self.control_mappings['JOYCODE_1_BUTTON5'] = "P1_BUTTON5"
        self.control_mappings['JOYCODE_1_BUTTON6'] = "P1_BUTTON6"
        self.control_mappings['JOYCODE_1_BUTTON7'] = "P1_BUTTON7"
        self.control_mappings['JOYCODE_1_BUTTON8'] = "P1_BUTTON8"
        self.control_mappings['JOYCODE_2_BUTTON1'] = "P2_BUTTON1"
        self.control_mappings['JOYCODE_2_BUTTON2'] = "P2_BUTTON2"
        self.control_mappings['JOYCODE_2_BUTTON3'] = "P2_BUTTON3"
        self.control_mappings['JOYCODE_2_BUTTON4'] = "P2_BUTTON4"
        self.control_mappings['JOYCODE_2_BUTTON5'] = "P2_BUTTON5"
        self.control_mappings['JOYCODE_2_BUTTON6'] = "P2_BUTTON6"
        self.control_mappings['JOYCODE_2_BUTTON7'] = "P2_BUTTON7"
        self.control_mappings['JOYCODE_2_BUTTON8'] = "P2_BUTTON8"
        

