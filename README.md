# ECL - Emulator Control Labels

A python script for driving OLED displays labeling the controls on an arcade cabinet control panel.

The script is fed in the emulator and game name (either via the command line, or a web service), and updates the OLED displays to display the appropriate label for each control.  For MAME, the script parses the MAME configuration file for each game and maps physical buttons to label correctly (so if you use physical button 3 for MAME button 1, it will display the label on physical button 3).

## Demostration

[![ECL](http://img.youtube.com/vi/qXnlxxjjD2I/0.jpg)](https://youtu.be/qXnlxxjjD2I "ECL")

## Pre-requisites (blinka):

    sudo apt-get install python3-pil python3-pip
    pip3 install adafruit-circuitpython-rgb-display

## Pre-requisites (luma):

    sudo apt-get install python3-pil python3-pip
    pip3 install luma

## Compatiable hardware:

It has only been tested with SSD1331 displays, driven by either a raspberry pi or an adafruit FT232H USB-to-SPI adapter.  In theory it should work with any SPI or I2C display with some minor changes.  

## Fonts

Fonts are not distributed, due to licensing complexities.  All of the fonts referenced in the configuration files are free for personal use, they just need to be downloaded and placed in the appropriate directory (as referenced in the font_path in the config file).  The currently used fonts are:

Jellee-Roman.ttf (Default font): <https://www.1001fonts.com/jellee-font.html>
BravoRG.otf (SF2, etc): <https://www.1001fonts.com/bravo-font.html>
Eurostile-Bol.otf (Asteroids):
Goudy Medieval Alternate.ttf (D&D, Joust): <https://www.1001fonts.com/goudy-font.html>
MumboSSK Bold.ttf (Asteriods Deluxe): <https://ufonts.com/fonts/mumbossk-bold.html> (Needs to be renamed)
computerfont.ttf (Defender): <https://www.dafont.com/computerfont.font>

## Warnings:

OLED displays are prone to burn in.  Anti-burnin protection has not been developed yet.  Don't leave displays displaying the same label for hours on end, or you will have burn-in.  

This script has not been heavily tested.  It works well enough on my cabinet, but it will almost certainly take a bit of work to get it working on anything else.  Documentation is lacking.  Code needs more comments and cleanup.  



