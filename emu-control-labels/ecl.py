#!/usr/bin/python3

from ECL_config import ECL_config
from ECL_config import main_config
from ECL_core import updateControls
from Controls import main_controller
import time
import argparse
import sys

def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="ECL - Emulator Controls Label.  \n Version 0.1.")
    parser.add_argument("-g", "--game", help="Game to display.")
    parser.add_argument("-e", "--emulator", help="Emulator.")
    parser.add_argument("-c", "--configfile", required=True, help="Configuration file.")
    parser.add_argument("-r", "--remote", help="Address for remote connection.")
    parser.add_argument("-l", "--listen", dest='listen',action='store_true', help="Listen mode.")
    parser.add_argument("-v", "--verbose",dest='verbose',action='store_true', help="Verbose mode.")
    options = parser.parse_args(args)
    return options

# Parse command line options

options = getOptions(sys.argv[1:])

# Load the main configuration file

main_config.load_xml_config(configfile = options.configfile)

# Start the main controller thread

main_controller.start()

# Start the Flask server, if we are listening for updates

if options.listen:
    from Mappers import MapperController
    MapperController.startup()

    from Rest import ECLRestServer
    ECLRestServer.startup()

# Update a remote instance

elif options.remote:
    from Rest import ECLRestClient
    ECLRestClient.updateLabels(options.game, options.emulator, remote=options.remote)

# Update local displays

else:
    updateControls(options.game, options.emulator)

