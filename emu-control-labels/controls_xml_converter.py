#!/usr/bin/python3

from Emulators import Emu_config
from Emulators.MAME import MAME_game_config
from Emulators.Emu_config import Emu_config, Emu_game_config, Control_label
import xml.etree.ElementTree as ET
import time
import re
import argparse
import sys

def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Parses command.")
    parser.add_argument("-g", "--game", required=False, help="Game to convert.")
    parser.add_argument("-c", "--controlsfile", required=True, help="Controls.xml file.")
    parser.add_argument("-x", "--mamexmlfile", required=False, help="Mame.xml file.")
    parser.add_argument("-o", "--outputdir", required=True, help="Output directory.")
    parser.add_argument("-f", "--romlistfile", required=False, help="ROM list file.")
    parser.add_argument("-v", "--verbose",dest='verbose',action='store_true', help="Verbose mode.")
    options = parser.parse_args(args)
    return options

def convertConfig(controls_file, game_id, output_dir, mame_xml=None):
    print("Converting '" + game_id + "'")
    config = MAME_game_config_conv(None)
    config.load_controls_xml_config(controls_file, game_id)

    if mame_xml is not None:
        config.load_mame_xml_config(mame_xml, game_id)

    if config.gamename is not None:
        config.save_config(output_dir + "/" + game_id + ".xml")
    else:
        print("Config file for game '" + game_id + "' could not be converted")

def loadRomList(filename):
    text_file = open(filename, "r")
    rom_list = text_file.read().splitlines()
    text_file.close()
    
    return rom_list

# MAME_game_config class with added functions for conversion

class MAME_game_config_conv(MAME_game_config):
    
    mame_xml_tree = None
    
    def renumber_button(self, control_id, player_num):
        control_id = re.sub(r'^P1_',"P" + str(player_num) + "_", control_id)
        return control_id
    
    def load_controls_xml_config(self, filename, game_id):
        tree = ET.parse(filename)
        root = tree.getroot()

        self.romname = game_id
    
        game_root = root.find("./game[@romname='" + game_id + "']")
        
        if game_root is None:
            print("Unable to find game '" + game_id + "' in controls.xml")
            return
        
        self.gamename = game_root.attrib.get("gamename")
        
        self.num_players = game_root.attrib.get("numPlayers")
        if self.num_players is not None:
            self.num_players = int(self.num_players)
        else:
            self.num_players = 1
            
        self.alternating = int(game_root.attrib.get("alternating"))
        
        mirrored = int(game_root.attrib.get("mirrored"))
        
        misc_details = game_root.find("./miscDetails")
        if misc_details is not None:
            self.misc_details = misc_details.text

# Add all the START buttons
            
        c_label = Control_label()
        c_label.set_text(text = 'Start')

        for player_num in range(1, self.num_players + 1):
            control_id = "P" + str(player_num) + "_START"
            self.controls_label[control_id] = c_label

# Add other button labels
        
        player_root = game_root.find("./player")

        labels = player_root.findall("./labels/label")
        for label in labels:
            if 'name' in label.attrib:
                control_id = label.attrib['name']
                label_text = label.attrib['value']
            
                c_label = Control_label()
                c_label.set_text(text = label_text)
                self.controls_label[control_id] = c_label
                if mirrored == 1 and self.alternating == 0:
                    for alt_player_num in range(2, self.num_players + 1):
                        alt_control_id = self.renumber_button(control_id, alt_player_num)
                        self.controls_label[alt_control_id] = c_label


    def add_buttons(self, player_num=1, num_buttons=1, subsystem=None):

        # Don't add buttons if they already exist (from controls.xml)

        control_id = "P" + str(player_num) + "_BUTTON1"
        if self.controls_label.get(control_id) is not None:
            return

        if subsystem == "neogeo":
            control_id = "P" + str(player_num) + "_BUTTON"

            if self.controls_label.get(control_id + "1") is None:
                self.controls_label[control_id +"1"] = Control_label(text = str("A"), unverified=1)
            if self.controls_label.get(control_id + "2") is None:
                self.controls_label[control_id +"2"] = Control_label(text = str("B"), unverified=1)
            if self.controls_label.get(control_id + "3") is None:
                self.controls_label[control_id +"3"] = Control_label(text = str("C"), unverified=1)
            if self.controls_label.get(control_id + "4") is None:
                self.controls_label[control_id +"4"] = Control_label(text = str("D"), unverified=1)

        elif subsystem == "vsnes":
            control_id = "P" + str(player_num) + "_BUTTON"
            if self.controls_label.get(control_id + "1") is None:
                self.controls_label[control_id +"1"] = Control_label(text = str("B"), unverified=1)
            if self.controls_label.get(control_id + "2") is None:
                self.controls_label[control_id +"2"] = Control_label(text = str("A"), unverified=1)
        
        else:    
            for button_num in range(1, num_buttons + 1):
                control_id = "P" + str(player_num) + "_BUTTON" + str(button_num)
                if self.controls_label.get(control_id) is None:
                    self.controls_label[control_id] = Control_label(text = str(button_num), unverified=1)
                
    def add_control(self, player_num, type):
        control_id = "P" + str(player_num) + "_" + type
        if self.controls_label.get(control_id) is None:
            self.controls_label[control_id] = Control_label(text = "")
                        
    def load_mame_xml_config(self, filename, game_id):
        
        if MAME_game_config_conv.mame_xml_tree is None:
            MAME_game_config_conv.mame_xml_tree = ET.parse(filename)
        
        root = MAME_game_config_conv.mame_xml_tree.getroot()

        self.romname = game_id
    
        game_root = root.find("./machine[@name='" + game_id + "']")
        
        if game_root is None:
            print("Unable to find game '" + game_id + "' in mame.xml")
            return
        
        # game description (name, for example "Tempest (rev 3, Revised Hardware)")

        description_tag = game_root.find("./description")
        if description_tag is not None and self.gamename is None:
            self.gamename = description_tag.text

# system type (neogeo, vsnes)

        sourcefile = game_root.get("sourcefile")
        if sourcefile == "vsnes.cpp":
            subsystem = "vsnes"
        elif sourcefile == "neogeo.cpp":
            subsystem = "neogeo"
        else:
            subsystem = None

# number of players

        input_tag = game_root.find("./input")
        if input_tag is not None:
            num_players = input_tag.attrib['players']
            if self.num_players is None:
                if num_players is not None:
                    self.num_players = int(num_players)
                else:
                    self.num_players = 2
                    
# Add all the START buttons
            
                c_label = Control_label()
                c_label.set_text(text = 'Start')

                for player_num in range(1, self.num_players + 1):
                    control_id = "P" + str(player_num) + "_START"
                    self.controls_label[control_id] = c_label

# coin controls

            coin_label = Control_label()
            coin_label.set_text(text = 'Coin')
                
            num_coins = input_tag.attrib.get('coins')
            if num_coins is not None:
                num_coins = int(num_coins)
            else:
                num_coins = 0
            
            for coin_num in range(1, num_coins + 1):
                control_id = "COIN" + str(coin_num)
                self.controls_label[control_id] = coin_label

# controls        

            controls = input_tag.findall("./control")
            for control_tag in controls:
                c_type = control_tag.attrib["type"]
                
                num_buttons = control_tag.attrib.get("buttons")
                if num_buttons is None:
                    num_buttons = 0
                else:
                    num_buttons = int(num_buttons)
                    
                player_num = control_tag.attrib.get("player")
                if player_num is None:
                    player_num = 1
                else:
                    player_num = int(player_num)

                # If alternating controls (from controls.xml), then only
                # output controls for player 1
                    
                if self.alternating == 1 and player_num > 1:
                    continue
                
                if player_num > self.num_players:
                    continue
                    
                if c_type == "dial":
                    self.add_control(player_num, "DIAL")
                    self.add_buttons(player_num, num_buttons)
                elif c_type == "doublejoy":
                    self.add_control(player_num, "JOYSTICKLEFT")
                    self.add_control(player_num, "JOYSTICKRIGHT")
                    self.add_buttons(player_num, num_buttons)
                elif c_type == "joy":
                    self.add_control(player_num, "JOYSTICK")
                    self.add_buttons(player_num, num_buttons, subsystem=subsystem)
                elif c_type == "keypad":
                    self.add_buttons(player_num, num_buttons)
                elif c_type == "lightgun":
                    self.add_control(player_num, "LIGHTGUN")
                    self.add_buttons(player_num, num_buttons)
                elif c_type == "mouse":
                    self.add_control(player_num, "MOUSE")
                    self.add_buttons(player_num, num_buttons)
                elif c_type == "only_buttons":
                    self.add_buttons(player_num, num_buttons)
                elif c_type == "paddle":
                    self.add_control(player_num, "PADDLE")
                    self.add_buttons(player_num, num_buttons)
                elif c_type == "pedal":
                    self.add_control(player_num, "PEDAL")
                    self.add_buttons(player_num, num_buttons)
                elif c_type == "positional":
                    self.add_control(player_num, "DIAL")
                    self.add_buttons(player_num, num_buttons)
                elif c_type == "stick":
                    self.add_control(player_num, "STICK")
                    self.add_buttons(player_num, num_buttons)
                elif c_type == "trackball":
                    self.add_control(player_num, "TRACKBALL")
                    self.add_buttons(player_num, num_buttons)
                else:
                    print("Unknown input type " + c_type)

# Entry point
                                
options = getOptions(sys.argv[1:])

if options.romlistfile is not None:
    rom_list = loadRomList(options.romlistfile)
    for game_id in rom_list:
        convertConfig(options.controlsfile, game_id, options.outputdir, mame_xml=options.mamexmlfile)
elif options.game is not None:
        convertConfig(options.controlsfile, options.game, options.outputdir)
else:
    print("No game specified")
