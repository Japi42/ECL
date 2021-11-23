'''
Created on Sep 14, 2020

@author: Japi42
'''
from Displays.TextOut import TextOut
import time
import os
import xml.etree.ElementTree as ET
import pathlib


class ECL_config:
    """Main configuration class for ECL"""
    
    def __init__(self):
        self.led_devices = {}
        self.controls = {}
        self.emulators = {}
        
        my_path = pathlib.Path(__file__).parent.absolute()
        self.data_directory = str(my_path.parent) + "/data"
        self.default_font = "Jellee-Roman.ttf"
        self.font_path = "~/fonts/"
    
    def load_xml_config(self, configfile):
        tree = ET.parse(configfile)
        root = tree.getroot()
       
        # Font path

        font_paths = root.findall("./font_paths/path")
        for path in font_paths:
            fpath = path.attrib["path"]
            if fpath.endswith("/") is False:
                fpath = fpath + "/"
            self.font_path = fpath

        # Mapped fonts

 
        # Create all the led controller devices
                
        led_devices = root.findall("./ledDevices/ledDevice")
        for led_dev in led_devices:
            dev = self.leddevice_factory(led_dev.attrib)
            
            if dev is not None:
                id = led_dev.attrib["id"]
                self.led_devices[id] = dev

        # Create all the physical controls (with displays and LEDs)
        
        control_tags = root.findall("./controls/control")
        for control_tag in control_tags:
            id = control_tag.attrib["id"]
            
            control = ECL_control(id)
            
            # Process the display

            display_tags = control_tag.findall("./display")
            for display_tag in display_tags:
                control.display = self.display_factory(display_tag.attrib) 
                
            # Process the LED

            led_tags = control_tag.findall("./led")
            for led_tag in led_tags:
                led_device_id = led_tag.attrib["device_id"]
                pin = int(led_tag.attrib["pin"])
                led = self.led_devices[led_device_id].addLED(id, pin)

                alwayson = led_tag.attrib.get("alwayson")
                if alwayson == "1":
                    led.setAlwaysOn()

                control.led = led
                
            print("Adding control " + id)

            self.controls[id] = control
                
# Create all the emulators

        emus = root.findall("./emulators/emulator")
        for emu in emus:
            emu_type = emu.attrib.get("type")
            emu_id = emu.attrib.get("id")
            ec = None
            
            if emu_type == "MAME":
                cp_elem = emu.find("./config_dir")
                config_path = cp_elem.attrib["path"]
                from Emulators.MAME import MAME_Config
                ec = MAME_Config(config_path=config_path)

            if ec is not None: 
                disps = emu.findall("./controls/control")
                for disp in disps:
                    controlid = disp.attrib["controlid"]
                    emu_control_id = disp.attrib["emu_control"]
                    ec.add_control_mapping(controlid, emu_control_id)
                    print("ECL Control " + controlid + " is " + emu_type + " button " + emu_control_id)
                
                self.emulators[emu_id] = ec
                print("Added emulator " + emu_id + "of type " + emu_type)

    def display_factory(self, options):
        """Create a Display object"""
        driver_type = options.get("type")
        driver_subtype = options.get("subtype")
            
        if driver_type == "BlinkaSPI":
            print("Adding BlinkaSPI display")
            spi_adaptor = options.get("spi_adaptor")
            if spi_adaptor == "FT232H":
                os.environ["BLINKA_FT232H"] = "1"

            cs_pin = options.get("cs_pin")
            dc_pin = options.get("dc_pin")
            rotation = int(options.get("rotation"))
            driver_chip = options.get("driver_chip")
                     
            from Displays.BlinkaSPI import BlinkaSPI
            return BlinkaSPI(cs=cs_pin, dc=dc_pin, rotation=rotation, driver_chip=driver_chip)

        if driver_type == "LumaSPI":
            print("Adding LumaSPI display")
            cs_pin = int(options.get("cs_pin"))
#            dc_pin = int(options.get("dc_pin"))

            rst_pin = options.get("rst_pin")
            if rst_pin is not None:
                rst_pin = int(rst_pin)

            rotation = options.get("rotation")
            if rotation is not None:
                rotation = int(rotation)

            subtype = options.get("subtype")
                     
            from Displays.LumaSPI import LumaSPI
            return LumaSPI(cs=cs_pin, rst=rst_pin, rotation=rotation, subtype=subtype)

        if driver_type == "TextOut":
            from Displays.TextOut import TextOut
            
            id = options.get("id")
            
            return TextOut(id=id)
        
        return None
    
    def leddevice_factory(self, options):
        """Create a LED control device"""
        driver_type = options.get("type")
        
        if driver_type == "pacdrive":
            from LedDevices.PacDrive import PacDrive

            board = int(options.get("board"))
            umtool = options.get("umtool")
            
            return PacDrive(board=board, umtool=umtool)
        elif driver_type == "PWMServoBoard":
            from LedDevices.PWMServoBoard import PWMServoBoard

            address = int(options.get("address"))
            
            return PWMServoBoard(address=address)
        elif driver_type == "LedAW9523":
            from LedDevices.LedAW9523 import LedAW9523

            address = int(options.get("address"))
            
            return LedAW9523(address=address)
        elif driver_type == "textout":
            from LedDevices.TextOut import TextOut
            
            return TextOut()
        
        return None

class ECL_config_display:
    
    def __init__(self, control_id, display_in):
        self.control_id = control_id
        self.display = display_in

class ECL_control:
    
    def __init__(self, control_id):
        self.control_id = control_id
        self.display = None
        self.led = None

main_config = ECL_config()

