'''
Created on Sep 15, 2020

@author: Japi42
'''

from Emulators.Emu_config import Emu_config, Emu_game_config, Control_label
import xml.etree.ElementTree as ET
import re
import os.path
from os import path
import copy

class MAME_Config(Emu_config):
    
    def __init__(self, config_path="~/.mame/cfg/"):
        super().__init__()
        self.config_path = config_path
        if self.config_path.endswith("/") is False:
            self.config_path = self.config_path + "/"
        self.default_cfg = MAME_ctrlr_config()
        self.default_cfg.set_defaults()
        self.default_cfg.load_from_xml(self.config_path + "default.cfg", 'default')
        self.emulator_id = 'mame'
    
    def load_game_config(self, game_id):
        if game_id not in self.game_configs:
            self.game_configs[game_id] = MAME_game_config(game_id, self.config_path, self.default_cfg)

        return self.game_configs[game_id]
    
    def lookup_control_mapping(self, game_id, control_id):

# control_id is the physical control id, from the ecl-config.xml file
        
        self.load_game_config(game_id)

# Apply emulator specific mapping (physical control to key code) 
# key code (emu_control_id) is something like "JOYCODE_1_BUTTON1"
       
        emu_control_id = self.control_mappings.get(control_id)
        if emu_control_id is None:
            emu_control_id = control_id

# Apply game specific mapping (keycode to MAME control)
        
        mame_game_cfg = self.game_configs[game_id]
        if mame_game_cfg != None:
            mame_ctrlr_cfg = mame_game_cfg.game_ctrlr_config
        
        # check game specific MAME config file
        # if no game specific MAME config file exists, this will use the 
        # default mappings
        # "control" will be the id of the control (eg P1_BUTTON1)
        
        if mame_ctrlr_cfg != None:
            control = mame_ctrlr_cfg.control_mappings.get(emu_control_id)
            if control != None:
                return control

        return emu_control_id
        
class MAME_game_config(Emu_game_config):
    
    def __init__(self, game_id, config_path, default_config=None):

        self.config_path = config_path
        super().__init__(game_id, 'mame')
        if game_id is not None:
            if default_config is not None:
               self.game_ctrlr_config = copy.deepcopy(default_config)
               self.game_ctrlr_config.load_from_xml(self.config_path + game_id + ".cfg", game_id)
            else:
               self.game_ctrlr_config = MAME_ctrlr_config(self.config_path + game_id + ".cfg", game_id)

class MAME_ctrlr_config:
    
    def __init__(self, filename=None, romname = "default"):

#        print("Loading MAME config for " + romname)
        self.control_mappings = {}
        if filename == None or path.exists(filename) == False:
            self.set_defaults()
        else:
            self.load_from_xml(filename, romname)
    
    def load_from_xml(self, filename, romname):

        if filename == None:
            return
        if path.exists(filename) == False:
            print("Failed to load file " + filename)
            return

        tree = ET.parse(filename)
        root = tree.getroot()
        
        ports = root.findall("./system[@name='" + romname + "']/input/port")
        for port in ports:

            # "type" is something like "P1_BUTTON4" - what is used in the ECL game config

            if 'type' in port.attrib:
                type = port.attrib['type']
            
                seqs = port.findall("./newseq[@type='standard']")
                for seq in seqs:
                    keystr = seq.text
                    self.parse_keyseq(type, keystr)

    def remove_mapping_by_target(self, target):

        for key, value in dict(self.control_mappings).items():
            if self.control_mappings[key] == target:
                print("Removing key " + key)
                self.control_mappings.pop(key)
                    
    def parse_keyseq(self, type, all_seqs):

# Clear out the default, if it exists
        
        self.remove_mapping_by_target(type)
        
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
        self.control_mappings['ECL_P1_SHIFT_UP'] = "ECL_P1_SHIFT_UP"
        self.control_mappings['ECL_P1_SHIFT_DOWN'] = "ECL_P1_SHIFT_DOWN"
        self.control_mappings['ECL_P1_GEAR'] = "ECL_P1_GEAR"
        

