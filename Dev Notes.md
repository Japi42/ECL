
The class structure:

Emu_config::Emu_config
 Definition for an emulator, holds emulator-specific configuration.  
 Emulators typically implement a class that inherits from this, named like "MAME_config".
 Includes a dictionary for configs for all the games for the emulator
 
Emu_config::Emu_game_config
 Class for a single game, includes a dictionary of all the control labels
 
Emu_config::Control_label
 Class for a label for a control
 
Emu_config::Text_label
 Class for a control label that is a text string.    
 
Emu_config::Image_label
 Class for a control label that is an image.  

