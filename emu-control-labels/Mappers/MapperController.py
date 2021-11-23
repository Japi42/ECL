'''
Created on Nov 22, 2021

@author: Japi42
'''

import threading
import time

from ECL_config import main_config

condition = threading.Condition()

def startup():
    ut = threading.Thread(name='UpdateMappersThread', target=updateMappersThread)
    ut.start()

def updateMappersThread():
    print("Start Mapper Thread")
    
    while True:
        
        with condition:
            for mapper_id in main_config.mappers:
                mapper = main_config.mappers[mapper_id]

                mapper.update()

        time.sleep(0.01)
    
