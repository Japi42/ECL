'''
Created on Jan 7, 2021

@author: Japi42
'''

from flask import Flask, jsonify, request, json
from ECL_core import updateControls
import subprocess
from ECL_config import main_config
import threading
import time

condition = threading.Condition()
next_game = {}

def startup():
    clearControlsQueue()
    ut = threading.Thread(name='UpdateControlsThread', target=updateControlsThread)
    ut.start()
    app.run(debug=True, threaded=False, use_reloader=False, host='0.0.0.0')

app = Flask(__name__)

def clearControlsQueue():
    with condition:
        next_game['game'] = None
        next_game['emulator'] = None
        next_game['mappings'] = None
        condition.notifyAll()
        
def checkControlsUpdate():
    with condition:
        if next_game['game'] is not None:
            return True
        if next_game['emulator'] is not None:
            return True
        if next_game['mappings'] is not None:
            return True
        
    return False

def updateControlsThread():

    while True:
        game = None
        emulator = None
        mappings = None
        
        with condition:
            condition.wait_for(checkControlsUpdate)
            game = next_game['game']
            emulator = next_game['emulator']
            mappings = next_game['mappings']
            clearControlsQueue()

        if game is not None:
            updateControls(game, emulator, mappings)
            
def queueUpdateControls(game, emulator, mappings):
    
    with condition:
        next_game['game'] = game
        next_game['emulator'] = emulator
        next_game['mappings'] = mappings

        condition.notifyAll()
        
#@app.route('/ecl/api/v1.0/game', methods=['GET'])
#def get_tasks():
#    return jsonify({'tasks': tasks})
    
# This only works if we have the button mappings local    

@app.route('/ecl/api/v1.0/game', methods=['PUT'])
def put_game():
    content = request.json
    
    print("Inbound game: " + content['game'])
    
    game = content['game']
    emulator = content['emulator']
    
    mappings = content.get('controls')
    
    queueUpdateControls(game, emulator, mappings)
    return jsonify({'status': 'Good'})
    
# Shutdown the system (used for clean rpi shutdown)

@app.route('/ecl/api/v1.0/shutdown', methods=['PUT'])
def shutdown():
    content = request.json
    
    confirm = content['confirm']
    if confirm == "YES":
        args = ["/sbin/shutdown", 'now']
        subprocess.call(args)
    
    return jsonify({'status': 'Good'})
    
# Re-init the system

@app.route('/ecl/api/v1.0/reinit', methods=['PUT'])
def reinit():
    content = request.json
    
    confirm = content['confirm']
    if confirm == "YES":
        main_config.load_xml_config(configfile = options.configfile)
    
    return jsonify({'status': 'Good'})
