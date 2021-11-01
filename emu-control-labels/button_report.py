#!/usr/bin/python3

from ECL_config import ECL_config
from ECL_config import main_config
from Emulators.Emu_config import Emu_game_config
from Emulators.Emu_config import Emu_config
import time
import argparse
import sys
import os
import re

def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Parses command.")
    parser.add_argument("-g", "--game", required=False, help="Game to display.")
    parser.add_argument("-e", "--emulator", required=True, help="Emulator.")
    parser.add_argument("-f", "--romlistfile", required=False, help="ROM list file.")
    parser.add_argument("-v", "--verbose",dest='verbose',action='store_true', help="Verbose mode.")
    options = parser.parse_args(args)
    return options

def outputGame(game_id, emulator):
    ec = Emu_config()
    config = Emu_game_config(game_id, emulator)
    if config.gamename is not None:
        print(config.romname + "\t" + config.gamename + "\t", end='')
        for button_id in ['P1_BUTTON1','P1_BUTTON2','P1_BUTTON3','P1_BUTTON4','P1_BUTTON5','P1_BUTTON6']:
            label = ec.lookup_control_label(game_id, button_id)
            if label is not None and label.get_text_label().text is not None:
                print(label.get_text_label().text + "\t", end='')
        print("")
        
    else:
        print(game_id + "\t")
        
def loadRomList(filename):
    text_file = open(filename, "r")
    rom_list = text_file.read().splitlines()
    text_file.close()
    
    return rom_list

def directoryRomList(cfg_directory):
    rom_list = []
    for file in sorted(os.listdir(cfg_directory)):
        game_id = re.sub("\.xml$","", file)
        rom_list.append(game_id)

    return rom_list

options = getOptions(sys.argv[1:])

main_config.data_directory = "/tmp/data"

if options.romlistfile is not None:
    rom_list = loadRomList(options.romlistfile)
    for game_id in rom_list:
        outputGame(game_id,options.emulator)
elif options.game is not None:
    outputGame(options.game, options.emulator)
else:
    rom_list = directoryRomList(main_config.data_directory + "/configs/emulators/" + options.emulator)
    for game_id in rom_list:
        outputGame(game_id, options.emulator)
    
