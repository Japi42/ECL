'''
Created on Jan 19, 2021

@author: Japi42
'''

import threading

from Mappers.Mapper import Mapper
from ECL_config import main_config

class ShifterMapper:

    def __init__(self, config_elem=None):
        Mapper.__init__(self)
        self.shiftup = None
        self.shiftdown = None
        self.shiftup_ls = None
        self.shiftdown_ls = None
        self.num_gears = None
        self.current_gear = None
        self.gearoutputs = []
        self.parse_config(config_elem)
        self.update_outputs()

    def parse_config(self, config_elem):

        self.gearoutputs = []
        self.num_gears = 5
        self.current_gear = 1

        input_id = config_elem.attrib.get("shiftup")
        self.shiftup = main_config.inputs[input_id]

        input_id = config_elem.attrib.get("shiftdown")
        self.shiftdown = main_config.inputs[input_id]
        
        outputs = config_elem.findall("./output")
        for output_elem in outputs:
            output_id = output_elem.attrib.get("outputid")
            output = main_config.outputs[output_id]
            
            self.gearoutputs.append(output)
            print("Adding gear " + str(output_id))
        
    def update_outputs(self):

        index = 1
        for gear_output in self.gearoutputs:
            if self.current_gear == index:
                gear_output.setState(True)
            else:
                gear_output.setState(False)

            index += 1

    def shift_up(self):
        print("Starting gear is " + str(self.current_gear))
        if self.current_gear < self.num_gears:
            self.current_gear += 1
            print("New gear is " + str(self.current_gear))
            self.update_outputs()

    def shift_down(self):
        print("Starting gear is " + str(self.current_gear))
        if self.current_gear > 1:
            self.current_gear -= 1
            print("New gear is " + str(self.current_gear))
            self.update_outputs()

    def update(self):
        with self.condition:
            state = self.shiftup.getState()

            if state != self.shiftup_ls:
                print("Shift up: "+ str(state))
                self.shiftup_ls = state
                if state:
                    self.shift_up()

            state = self.shiftdown.getState()

            if state != self.shiftdown_ls:
                print("Shift down: " + str(state))
                self.shiftdown_ls = state
                if state:
                    self.shift_down()

                
