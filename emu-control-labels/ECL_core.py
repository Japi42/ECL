'''
Created on Jan 7, 2021

@author: Japi42
'''

from ECL_config import ECL_config
from ECL_config import main_config
from LedDevices.PacDrive import PacDrive

def lookupControls(game, emulator):

    controlMappings = {}

# Get the config for the requested emulator

    emu_conf = main_config.emulators[emulator]

# Loop through all the controls, updating labels
    
    for control_id in main_config.controls:
        control = main_config.controls[control_id]
        
        emu_control_id = emu_conf.lookup_control_mapping(game, control_id)
        
        controlMappings[control_id] = emu_control_id
        if emu_control_id is not None:
            print(game + " " + control_id + " is emulator control " + emu_control_id)
        else:
            print(game + " " + control_id + " is emulator control None")
        
    return controlMappings

def updateDisplays(game, emulator, mappings):
# Get the config for the requested emulator

    emu_conf = main_config.emulators[emulator]

    calced_font_size = calcFontSize(game, emulator, mappings)    

# Loop through all the controls, updating labels
    
    for control_id in main_config.controls:
        control = main_config.controls[control_id]
        display = control.display
        if display is None:
            continue
        
        emu_control_id = mappings.get(control_id)
        
        label = emu_conf.lookup_control_label(game, emu_control_id)
        if label is not None:
            text_label = label.get_text_label(width=display.width, height=display.height)
            text = text_label.text
            color = text_label.color
            font = text_label.font
            font_size = text_label.font_size
            if color is None:
                color = "#ff0000"
        
            if font_size is None:
                font_size = calced_font_size
                
            display.display_text(text, color=color, font_name=font, font_size=font_size)
        else:
            display.display_text("", color="#000000")

def calcFontSize(game, emulator, mappings):
# Get the config for the requested emulator

    emu_conf = main_config.emulators[emulator]

    max_font_size = None

# Loop through all the controls, updating labels
    
    for control_id in main_config.controls:
        control = main_config.controls[control_id]
        display = control.display
        if display is None:
            continue
        
        emu_control_id = mappings.get(control_id)
        
        label = emu_conf.lookup_control_label(game, emu_control_id)
        if label is not None:
            text_label = label.get_text_label(width=display.width, height=display.height)
            text = text_label.text
            font = text_label.font
            font_size = display.calc_max_font_size(text, font_name=font)
            if font_size is not None:
                if max_font_size is None or font_size < max_font_size:
                    max_font_size = font_size

    print("Calculated font size of " + str(max_font_size))
                
    return max_font_size

def updateLEDs(game, emulator, mappings):

# Get the config for the requested emulator

    emu_conf = main_config.emulators[emulator]

# reset the LED devices 

    for led_dev_id in main_config.led_devices:
        led_dev = main_config.led_devices[led_dev_id]
        led_dev.resetLEDs()

# Loop through each control, checking if there is a emulator control label for it

    for control_id in main_config.controls:
        control = main_config.controls[control_id]
        led_output = control.led
        if led_output is None:
            continue

        emu_control_id = mappings.get(control_id)
        
        if emu_control_id is not None:
            label = emu_conf.lookup_control_label(game, emu_control_id)
            if label is not None:
                led_output.enableLED()

# run updates on all the output devices
    
    for led_dev_id in main_config.led_devices:
        led_dev = main_config.led_devices[led_dev_id]
        led_dev.updateLEDs()

def updateControls(game, emulator, mappings=None):
    
    if mappings is None:
        mappings = lookupControls(game, emulator)
        
    updateLEDs(game, emulator, mappings)
    
    updateDisplays(game, emulator, mappings)