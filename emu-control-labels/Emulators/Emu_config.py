
import xml.etree.ElementTree as ET
from xml.dom import minidom
from ECL_config import main_config

class Emu_config:
    """Base class for a Emulator configuration"""
    
    def __init__(self):
        self.game_configs = {}
        self.control_mappings = {}
        self.emulator_id = 'base'
    
    def add_control_mapping(self, control_id, emu_control_id):
        self.control_mappings[control_id] = emu_control_id
    
    def lookup_control_mapping(self, game_id, control_id):
        """Lookup what the Emulator control ID is for a given ECL Control ID"""

        return self.control_mappings.get(control_id)
    
    def lookup_control_label(self, game_id, control_id):

        if control_id is None:
            return None

        game_config = self.load_game_config(game_id)
        if game_config is None:
            return None
        
        return game_config.lookup_label(control_id)
    
    def load_game_config(self, game_id):
        if game_id not in self.game_configs:
            self.game_configs[game_id] = Emu_game_config(game_id, self.emulator_id)

        return self.game_configs[game_id]
    
class Emu_game_config:
    """Configuration for a specific game"""
    
    def __init__(self, game_id, emulator_id):
        self.controls_label = {}
        self.misc_details = None
        self.emulator_id = emulator_id
        self.romname = game_id
        self.gamename = None
        self.num_players = None
        self.alternating = None
        self.font = None

        if game_id is not None:
            filename = self.get_config_filename(emulator_id, game_id)
            self.load_game_config(filename, game_id)

    def get_config_filename(self, emulator_id, game_id):
        return main_config.data_directory + "/configs/emulators/" + emulator_id + "/" + game_id + ".xml"
            
    def load_game_config(self, filename, game_id, clone=False):
        try:
            tree = ET.parse(filename)
            root = tree.getroot()

            game_root = root.find("./game[@romname='" + game_id + "']")
        
            if game_root is None:
                return

            gamename = game_root.attrib.get("gamename")
            num_players = game_root.attrib.get("numPlayers")
            alternating = game_root.attrib.get("alternating")
            clone_of = game_root.attrib.get("cloneof")

            if clone == False:
                self.gamename = gamename
                self.num_players = num_players
                self.alternating = alternating
                self.clone_of = clone_of
                
# If the game is a clone, load the parent config first (recursivly), then apply the
# clone-specifc stuff on top of it.

            if clone_of is not None:
                clone_filename = self.get_config_filename(self.emulator_id, clone_of)
                self.load_game_config(clone_filename, clone_of, clone=True)
       
            controls_elem = root.find("./game[@romname='" + game_id + "']/controls")

            default_color = None
            if controls_elem is not None:
                self.font = controls_elem.attrib.get("font")
                self.font_size = controls_elem.attrib.get("font_size")
                default_color = controls_elem.attrib.get("color")

            controls = root.findall("./game[@romname='" + game_id + "']/controls/control")
                
            for control in controls:
                if 'name' in control.attrib:
                    control_id = control.attrib['name']
                
                    default_text_id = control.attrib.get("default_text_id")

                    c_label = Control_label(default_text_id=default_text_id)

                    texts = control.findall("./text")
                    for text in texts:
                        label_text = text.text
                        width = text.attrib.get("width")
                        height = text.attrib.get("height")
                        lang = text.attrib.get("lang")
                        color = text.attrib.get("color")
                        font = text.attrib.get("font")
                        font_size = text.attrib.get("font_size")
                        text_id = text.attrib.get("id")

                        if font_size is None:
                            font_size = self.font_size
                        
                        if font is None:
                            font = self.font

                        if color is None:
                            color = default_color

                        c_label.set_text(text = label_text, width=width, height=height, lang=lang, color=color, 
                                         font=font, font_size=font_size, text_id=text_id)
                
                        self.controls_label[control_id] = c_label
        except Exception as e:
            print("Error loading config: " + filename)
            import traceback
            traceback.print_exc()
            print(e)
            pass
    
    def lookup_label(self, control_id):
        return self.controls_label.get(control_id)
    
    def save_config(self, filename):
        root = ET.Element('ecl')

        comment = ET.Comment('Generated by ECL')
        root.append(comment)
        
        game_root = ET.SubElement(root, 'game', {'romname':self.romname} )
        
        if self.gamename is not None:
            game_root.set('gamename', self.gamename)

        if self.num_players is not None:
            game_root.set('numPlayers', str(self.num_players))

        if self.alternating is not None:
            game_root.set('alternating', str(self.alternating))
            
        misc_details = ET.SubElement(game_root, 'miscDetails')
        
        if self.misc_details is not None:
            misc_details.text = self.misc_details

        controls_elem = ET.SubElement(game_root, 'controls')
        
        if self.font is not None:
            controls_elem.set('font', self.font)
        
        for control_id in sorted(self.controls_label):
            
            control_elem = ET.SubElement(controls_elem, 'control', {'name':control_id})
            control_text_elem = ET.SubElement(control_elem, 'text')
            
            for text_label_key in self.controls_label[control_id].text_labels:
                text_label = self.controls_label[control_id].text_labels[text_label_key]
                control_text_elem.text = text_label.text
                if text_label.color is not None:
                    control_text_elem.set('color',text_label.color )
                if text_label.lang is not None:
                    control_text_elem.set('lang',text_label.lang )
                if text_label.width is not None:
                    control_text_elem.set('width',text_label.width )
                if text_label.height is not None:
                    control_text_elem.set('height',text_label.height )
                if text_label.font is not None and text_label.font != self.font:
                    control_text_elem.set('font',text_label.font )
                if text_label.unverified is not None and text_label.unverified == 1:
                    control_text_elem.set('unverified', "1" )
        
        tree = ET.ElementTree(root)
        
        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
        with open(filename, "w") as f:
            f.write(xmlstr)
        
#        tree.write(open(filename, 'wb'), encoding='UTF-8', method='xml', xml_declaration=True)
    
class Control_label:
    
    def __init__(self, text=None, unverified=None,default_text_id=None):
        self.text_labels = {}
        self.image_labels = {}
        self.default_text_id = default_text_id
        if text is not None:
            self.set_text(text=text, unverified=unverified)
        
    def get_text_label(self, width=None, height=None, lang="en_us", text_id=None):
        key = self.get_text_key(width=width, height=height, lang=lang, text_id=text_id)

        if key is not None:
            return self.text_labels[key]

        return None

    def get_text_key(self, width=None, height=None, lang="en_us", text_id=None):

        if text_id is None:
            w_text_id = self.default_text_id
        else:
            w_text_id = text_id

# Check for the specific text_id, with dimensions
            
        key = self.build_key(width, height, lang, w_text_id)
        if key in self.text_labels:
            return key

# Check for the specific text_id, without dimensions
       
        key = self.build_key(lang=lang, text_id=w_text_id)
        if key in self.text_labels:
            return key
        
        return None

    def get_default_text_id(self):
        return self.default_text_id
    
    def get_text_ids(self):
        text_ids = {}

        for key in self.text_labels:
            k_parts = self.split_key(key)
            k_width = k_parts[0]
            k_height = k_parts[1]
            k_lang = k_parts[2]
            k_text_id = k_parts[3]

            if k_text_id not in text_ids:
                text_ids[k_text_id] = k_text_id
            
        return text_ids
    
    def get_default_key(self, width=None, height=None, lang="en_us"):
        key = self.build_key(width, height, lang)
        if key in self.text_labels:
            return key

        key = self.build_key(lang=lang)
        if key in self.text_labels:
            return key

        return None
    
    def get_image(self, width=None, height=None, lang="en_us"):
        return None
    
    def set_text(self, text=None, width=None, height=None, lang="en_us", color=None, font=None, font_size=None, unverified=None, text_id=None):
        key = self.build_key(width, height, lang, text_id)
        print("Adding key " + str(key))
        text_label = Text_label(text=text, width=width, height=height, lang=lang, color=color, font=font, font_size=font_size, unverified=unverified)
        self.text_labels[key] = text_label
            
    def build_key(self, width=None, height=None, lang="en_us", text_id=None):
        key = ""
        if width is None:
            key = "None"
        else:
            key = str(width)
        
        if height is None:
            key = key + "|None"
        else:
            key = key + "|" + str(height)
        
        if lang is None:
            key = key + "|None"
        else:
            key = key + "|" + str(lang)

        if text_id is None:
            key = key + "|None"
        else:
            key = key + "|" + str(text_id)

        return key

    def split_key(self, key):
        parts = key.split("|")

        return parts
    
class Text_label:
    
    def __init__(self, text="", font=None, font_size=None, color=None, lang=None, width=None, height=None, unverified=None):
        self.text = text
        self.font = font
        self.font_size = font_size
        self.font_size_calced = False 
        self.color = color
        self.lang = lang
        self.width = width
        self.height = height
        self.unverified = unverified
    
class Image_label:
    
    def __init__(self):
        self.lang = None
        self.width = None
        self.height = None
        self.filename = None
    
    
