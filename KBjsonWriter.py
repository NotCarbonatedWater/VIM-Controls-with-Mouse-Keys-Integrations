import json

def write_to_json(filename, data):
    try:
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data successfully written to {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

def CAPS_SHIFT():
    return {"key_code": "caps_lock","modifiers": {"mandatory": ["shift"],"optional": ["any"]}}

def setMODES(VIM_MODE_BOOL, NORMAL_MODE_BOOL, MOUSE_MODE_BOOL):
    return [
        {"set_variable": {"name": "VIM_MODE","value": VIM_MODE_BOOL}},
        {"set_variable": {"name": "NORMAL_MODE","value": NORMAL_MODE_BOOL}},
        {"set_variable": {"name": "MOUSE_MODE","value": MOUSE_MODE_BOOL}}
    ]
def setExit(Key, VIM_MODE_BOOL, NORMAL_MODE_BOOL, MOUSE_MODE_BOOL):
    return [
        {"key_code": Key},
        {"set_variable": {"name": "VIM_MODE","value": VIM_MODE_BOOL}},
        {"set_variable": {"name": "NORMAL_MODE","value": NORMAL_MODE_BOOL}},
        {"set_variable": {"name": "MOUSE_MODE","value": MOUSE_MODE_BOOL}}
    ]

# checks if matches conditions 
def setCondition(VIM_MODE_BOOL):
    return [
        {"type": "variable_if","name": "VIM_MODE","value": VIM_MODE_BOOL}

    ]
def setConditions(VIM_MODE_BOOL, NORMAL_MODE_BOOL, MOUSE_MODE_BOOL):
    return [
        {"type": "variable_if","name": "VIM_MODE","value": VIM_MODE_BOOL},
        {"type": "variable_if","name": "NORMAL_MODE","value": NORMAL_MODE_BOOL},
        {"type": "variable_if","name": "MOUSE_MODE","value": MOUSE_MODE_BOOL}
    ]

def setDDConditions(VIM_MODE_BOOL, NORMAL_MODE_BOOL, MOUSE_MODE_BOOL, DD_KEY_COUNT):
    return [
        {"type": "variable_if","name": "VIM_MODE","value": VIM_MODE_BOOL},
        {"type": "variable_if","name": "NORMAL_MODE","value": NORMAL_MODE_BOOL},
        {"type": "variable_if","name": "MOUSE_MODE","value": MOUSE_MODE_BOOL},
        {"type": "variable_if","name": "DD_KEY_COUNT","value": DD_KEY_COUNT}
    ]

def toggleCapsVIM_MODE_ON():
    return {
        "type": "basic",
        "from": CAPS_SHIFT(),
        "to": setMODES(1, 1, 0),
        "conditions": setCondition(0)
    }

def toggleCapsVIM_MODE_OFF():
    return {
        "type": "basic",
        "from": CAPS_SHIFT(),
        "to": setMODES(0, 0, 0),
        "conditions": setCondition(1)
    }

def NORMAL_MODE(key, newKey):
    return {
        "type": "basic",
        "from": {"key_code": key,"modifiers": {"optional": ["any"]}},
        "to": [{"key_code": newKey}],
        "conditions": setConditions(1, 1, 0)
    }

def NORMAL_MODE_APPEND(key, newKey):
    return {
        "type": "basic",
        "from": {"key_code": key,"modifiers": {"optional": ["any"]}},
        "to": setExit(newKey, 0, 0, 0),
        "conditions": setConditions(1, 1, 0)
    }

def NORMAL_MODE_APPEND_W_MOD(key, newKey):
    return {
        "type": "basic",
        "from": {"key_code": key,"modifiers": {"mandatory": ["shift"], "optional": ["any"]}},
        "to": setExit(newKey, 0, 0, 0),
        "conditions": setConditions(1, 1, 0)
    }

def NORMAL_MODE_TOGGLE():
    return {
        "type": "basic",
        "from": {"key_code": "caps_lock","modifiers": {"optional": ["any"]}},
        "to": setMODES(1, 1, 0), 
        "conditions": setCondition(1) # potential bug
    }

def insert_MODE():
    return {
        "type": "basic",
        "from": {"key_code": "i","modifiers": {"optional": ["any"]}},
        "to": setMODES(0, 0, 0), 
        "conditions": setConditions(1, 1, 0)
    }

def MOUSE_MODE_TOGGLE_ON():
    return {
        "type": "basic",
        "from": {"key_code": "m","modifiers": {"optional": ["any"]}},
        "to": setMODES(1, 0, 1), 
        "conditions": setConditions(1, 1, 0) # potential bug
    }

def MOUSE_MODE_CLICK(key, buttonType):
    return {
        "type": "basic",
        "from": {"key_code": key,"modifiers": {"optional": ["any"]}},
        "to": [{ "pointing_button": buttonType}],
        "conditions": setConditions(1, 0, 1)
    }

def MOUSE_MODE(key, plane, dist):
    return {
        "type": "basic",
        "from": {"key_code": key,"modifiers": {"optional": ["any"]}},
        "to": [{ "mouse_key": { plane: dist } }],
        "conditions": setConditions(1, 0, 1)
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
                toggleCapsVIM_MODE_OFF(),
                toggleCapsVIM_MODE_ON(),
        
                # hjkl arrow keys
                NORMAL_MODE_TOGGLE(),
                NORMAL_MODE("j", "down_arrow"),
                NORMAL_MODE("k", "up_arrow"),
                NORMAL_MODE("h", "left_arrow"),
                NORMAL_MODE("l", "right_arrow"),
                NORMAL_MODE("x", "delete_forward"),
                NORMAL_MODE("d", ""),
                NORMAL_MODE_APPEND_W_MOD("a", "end"),
                NORMAL_MODE_APPEND("a", "right_arrow"),
                
                # insert mode 
                insert_MODE(),

                # mouse keys to turn off, set normal mode using caps-lock
                MOUSE_MODE_TOGGLE_ON(), 
                MOUSE_MODE("j", "y", 1000),
                MOUSE_MODE("k", "y", -1000),
                MOUSE_MODE("h", "x", -1000),
                MOUSE_MODE("l", "x", 1000),
                MOUSE_MODE_CLICK("spacebar", "button1"),
                MOUSE_MODE_CLICK("semicolon", "button2"),

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
            #default settings plus personal keyboard info
            "virtual_hid_keyboard": { "keyboard_type_v2": "ansi" },
            "devices": [
                {
                    "identifiers": {
                        "is_keyboard": True,
                        "is_pointing_device": True,
                        "product_id": 45915,
                        "vendor_id": 1133
                    },
                    "ignore": False
                }
            ],
        }
    ]
    }
    write_to_json("karabiner.json", data)    
