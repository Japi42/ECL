# ECL - Emulator Control Labels

A python script for driving OLED displays labeling the controls on an arcade cabinet control panel.

The script is fed in the emulator and game name (either via the command line, or a web service), and updates the OLED displays to display the appropriate label for each control.  For MAME, the script parses the MAME configuration file for each game and maps physical buttons to label correctly (so if you use physical button 3 for MAME button 1, it will display the label on physical button 3).

## Demostration

[![ECL](http://img.youtube.com/vi/qXnlxxjjD2I/0.jpg)](https://youtu.be/qXnlxxjjD2I "ECL")

## Pre-requisites (blinka):

    sudo apt-get install python3-pil python3-pip
    pip3 install adafruit-circuitpython-rgb-display

## Compatiable hardware:

It has only been tested with SSD1331 displays, driven by either a raspberry pi, or an adafruit FT232H USB-to-SPI adapter.  In theory it should work with any SPI or I2C display with some minor changes.  

## Warnings:

OLED displays are prone to burn in.  Anti-burnin protection has not been developed yet.  Don't leave displays displaying the same label for hours on end, or you will have burn-in.  

This script has not been heavily tested.  It works well enough on my cabinet, but it will almost certainly take a bit of work to get it working on anything else.  Documentation is lacking.  Code needs more comments and cleanup.  



