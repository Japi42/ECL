'''
Created on Jan 7, 2021

@author: Japi42
'''

import requests
import json
from ECL_core import lookupControls

def updateLabels(game, emulator, remote='localhost'):
    url = 'http://' + remote + ':5000/ecl/api/v1.0/game'

    mappings = lookupControls(game, emulator)

    response = requests.put(url, json={"game": game, "emulator": emulator, "controls": mappings})

    print(str(response))
    print('')
    print(json.dumps(response.json(), indent=4))
    
