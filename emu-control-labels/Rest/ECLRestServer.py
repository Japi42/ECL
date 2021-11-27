'''
Created on Jan 7, 2021

@author: Japi42
'''

from flask import Flask, jsonify, request, json
import subprocess
from ECL_config import main_config
import time
from Controls import main_controller

def startup():
    main_controller.clearControlsQueue()
    app.run(debug=True, threaded=False, use_reloader=False, host='0.0.0.0', port='5000')

app = Flask(__name__)

# Change the control labels to a new game    

@app.route('/ecl/api/v1.0/game', methods=['PUT'])
def put_game():
    content = request.json
    
    print("Inbound game: " + content['game'])
    
    game = content['game']
    emulator = content['emulator']
   
    print(str(content)) 
    mappings = content.get('controls')
    
    main_controller.queueUpdateControls(game, emulator, mappings)
    return jsonify({'status': 'Good'})

# Change a multi-text control label to a different text

@app.route('/ecl/api/v1.0/control/<id>', methods=['PUT'])
def put_control_id(id):
    content = request.json
 
    print("Inbound control change: " + id)
    
    text_id = content['text_id']
    
#    queueUpdateControls(game, emulator, mappings)
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
