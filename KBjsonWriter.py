import json

def write_to_json(filename, data):
    try:
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data successfully written to {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

def toggleCapsVIM_MODE_ON():
    return {
        "type": "basic",
        "from": {"key_code": "caps_lock","modifiers": {"mandatory": ["shift"],"optional": ["any"]}},
        "to": [{"set_variable": {"name": "VIM_MODE","value": 1}}],
        "conditions": [{"type": "variable_if","name": "VIM_MODE","value": 0}]
    }

def new_line():
    return{
        "type": "basic",
        "from": {"key_code": "o", "modifiers": {"optional": ["any"]}},
        "to": [
            {"key_code": "end"}, #go to the end of the line
            {"key_code": "return_or_enter"}, #create the new line
            {"set_variable": {"name": "VIM_MODE", "value": 0}}  #insert mode
        ],
        "conditions": [{"type": "variable_if", "name": "VIM_MODE", "value": 1}]
    }

def new_line_above():
    return{
        "type": "basic",
        "from": {"key_code": "o", "modifiers": {"mandatory": ["shift"], "optional": ["any"]}},
        "to": [
            {"key_code": "home"}, #go to the beginning of the line
            {"key_code": "return_or_enter"}, #create the new line (pushes current line down)
            {"key_code": "up_arrow"}, #go up to the new empty line
            {"set_variable": {"name": "VIM_MODE", "value": 0}}  #insert mode
        ],
        "conditions": [{"type": "variable_if", "name": "VIM_MODE", "value": 1}]
    }

def toggleCapsVIM_MODE_OFF():
    return {
        "type": "basic",
        "from": {"key_code": "caps_lock","modifiers": {"mandatory": ["shift"],"optional": ["any"]}},
        "to": [{"set_variable": {"name": "VIM_MODE","value": 0}}],
        "conditions": [{"type": "variable_if","name": "VIM_MODE","value": 1}]
    }

def normal_MODE(key, newKey):
    return {
        "type": "basic",
        "from": {"key_code": key,"modifiers": {"optional": ["any"]}},
        "to": [{"key_code": newKey}],
        "conditions": [{"type": "variable_if","name": "VIM_MODE","value": 1}]
    }

def insert_MODE():
    return {
        "type": "basic",
        "from": {"key_code": "i","modifiers": {"optional": ["any"]}},
        "to": [{"set_variable": {"name": "VIM_MODE","value": 0}}],
        "conditions": [{"type": "variable_if","name": "VIM_MODE","value": 1}]
    }

def setComplexMods(): 
    return {
    "rules": 
    [
        {
            "description": "Arrow Keypad Mode [Capslock as trigger key]",
            "manipulators": 
            [
                # toggles VIM MODE
                toggleCapsVIM_MODE_ON(),
                toggleCapsVIM_MODE_OFF(),
                # hjkl arrow keys
                normal_MODE("j", "down_arrow"),
                normal_MODE("k", "up_arrow"),
                normal_MODE("h", "left_arrow"),
                normal_MODE("l", "right_arrow"),
                
                # new line
                new_line(),
                new_line_above(),
                # insert mode 
                insert_MODE()
            ]
        }
    ]
    }

if __name__ == "__main__":
    data = {
    "profiles": 
    [
        {
            #set MODS
            "complex_modifications": setComplexMods(),
            #default settings 
            "virtual_hid_keyboard": { "keyboard_type_v2": "ansi" }
        }
    ]
    }
    write_to_json("karabiner.json", data)    
