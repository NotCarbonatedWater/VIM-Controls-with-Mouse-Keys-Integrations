import json


def write_to_json(filename, data):
    try:
        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data successfully written to {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")


def PRESSKEY(KEY):
    return {"key_code": KEY}


def PRESSKEY_W_MOD(KEY, MOD):
    return {"key_code": KEY, "modifiers": {"mandatory": [MOD], "optional": ["any"]}}


def GETKEY(KEY):
    return {"key_code": KEY, "modifiers": {"optional": ["any"]}}


def CAPS_SHIFT():
    return PRESSKEY_W_MOD("caps_lock", "shift")

def CTRL_CLOSEBRACKET():
    return PRESSKEY_W_MOD("close_bracket", "control")

def ESCAPE():
    return PRESSKEY("escape")


def SET_VAR(NAME, VAL):
    return {"set_variable": {"name": NAME, "value": VAL}}


def SET_VIM_ON():
    return SET_VAR("VIM_STATE", 1)


def SET_VIM_OFF():
    return SET_VAR("VIM_STATE", 0)


def SET_NORMAL_MODE_ON():
    return SET_VAR("NORMAL_MODE", 1)


def SET_NORMAL_MODE_OFF():
    return SET_VAR("NORMAL_MODE", 0)


def SET_MOUSE_MODE_ON():
    return SET_VAR("MOUSE_MODE", 1)


def SET_MOUSE_MODE_OFF():
    return SET_VAR("MOUSE_MODE", 0)


def START_VIM():
    return [SET_VIM_ON(), SET_NORMAL_MODE_ON(), SET_MOUSE_MODE_OFF()]


def START_NORMAL_MODE():
    return [SET_VIM_ON(), SET_NORMAL_MODE_ON(), SET_MOUSE_MODE_OFF()]


def START_MOUSE_MODE():
    return [SET_VIM_ON(), SET_NORMAL_MODE_OFF(), SET_MOUSE_MODE_ON()]


def RESET_EXIT():
    return [
        SET_VIM_OFF(),
        SET_NORMAL_MODE_OFF(),
        SET_MOUSE_MODE_OFF(),
    ]


def PLACE_RESET_EXIT(KEY):
    return [SET_VIM_OFF(), SET_NORMAL_MODE_OFF(), SET_MOUSE_MODE_OFF(), PRESSKEY(KEY)]


def VAR_EQUALS_VALUE(NAME, VAL):
    return {"type": "variable_if", "name": NAME, "value": VAL}


def IF_VIM_ON():
    return VAR_EQUALS_VALUE("VIM_STATE", 1)


def IF_VIM_OFF():
    return VAR_EQUALS_VALUE("VIM_STATE", 0)


def IF_NORMAL_ON():
    return VAR_EQUALS_VALUE("NORMAL_MODE", 1)


def IF_NORMAL_OFF():
    return VAR_EQUALS_VALUE("NORMAL_MODE", 0)


def IF_MOUSE_ON():
    return VAR_EQUALS_VALUE("MOUSE_MODE", 1)


def IF_MOUSE_OFF():
    return VAR_EQUALS_VALUE("MOUSE_MODE", 0)


def IF_NORMAL_MODE_ON():
    return [IF_VIM_ON(), IF_NORMAL_ON(), IF_MOUSE_OFF()]


def IF_MOUSE_MODE_ON():
    return [IF_VIM_ON(), IF_NORMAL_OFF(), IF_MOUSE_ON()]


def toggleVIM_STATE_ON(KEYS):
    return {
        "type": "basic",
        "from": KEYS,
        "to": START_VIM(),
        "conditions": [IF_VIM_OFF()],
    }


def toggleVIM_STATE_OFF(KEYS):
    return {
        "type": "basic",
        "from": KEYS,
        "to": RESET_EXIT(),
        "conditions": [IF_VIM_ON()],
    }


def NORMAL_MODE(KEY, NEWKEY):
    return {
        "type": "basic",
        "from": GETKEY(KEY),
        "to": PRESSKEY(NEWKEY),
        "conditions": IF_NORMAL_MODE_ON(),
    }


def NORMAL_MODE_APPEND(KEY, NEWKEY):
    return {
        "type": "basic",
        "from": GETKEY(KEY),
        "to": PLACE_RESET_EXIT(NEWKEY),
        "conditions": IF_NORMAL_MODE_ON(),
    }


def NORMAL_MODE_APPEND_W_MOD(KEY, NEWKEY):
    return {
        "type": "basic",
        "from": PRESSKEY_W_MOD(KEY, "shift"),
        "to": PLACE_RESET_EXIT(NEWKEY),
        "conditions": IF_NORMAL_MODE_ON(),
    }


def NORMAL_MODE_TOGGLE():
    return {
        "type": "basic",
        "from": PRESSKEY("caps_lock"),
        "to": SET_NORMAL_MODE_ON(),
        "conditions": [IF_VIM_ON()],
    }


def insert_MODE():
    return {
        "type": "basic",
        "from": GETKEY("i"),
        "to": RESET_EXIT(),
        "conditions": IF_NORMAL_MODE_ON(),
    }


def MOUSE_MODE_TOGGLE_ON():
    return {
        "type": "basic",
        "from": GETKEY("m"),
        "to": START_MOUSE_MODE(),
        "conditions": [IF_VIM_ON()],
    }


def MOUSE_MODE_CLICK(KEY, buttonType):
    return {
        "type": "basic",
        "from": GETKEY(KEY),
        "to": [{"pointing_button": buttonType}],
        "conditions": IF_MOUSE_MODE_ON(),
    }


def MOUSE_MODE(KEY, plane, dist):
    return {
        "type": "basic",
        "from": GETKEY(KEY),
        "to": [{"mouse_key": {plane: dist}}],
        "conditions": IF_MOUSE_MODE_ON(),
    }


def setComplexMods():
    return {
        "rules": [
            {
                "description": "Arrow keypad Mode [Capslock as trigger KEY]",
                "manipulators": [
                    # toggles VIM MODE
                    toggleVIM_STATE_OFF(ESCAPE()),
                    toggleVIM_STATE_OFF(CAPS_SHIFT()),
                    toggleVIM_STATE_OFF(CTRL_CLOSEBRACKET()),
                    toggleVIM_STATE_ON(CAPS_SHIFT()),
                    toggleVIM_STATE_ON(CTRL_CLOSEBRACKET()),


                    # hjkl arrow KEYs
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
                    # mouse KEYs to turn off, set normal mode using caps-lock
                    MOUSE_MODE_TOGGLE_ON(),
                    MOUSE_MODE("j", "y", 1000),
                    MOUSE_MODE("k", "y", -1000),
                    MOUSE_MODE("h", "x", -1000),
                    MOUSE_MODE("l", "x", 1000),
                    MOUSE_MODE_CLICK("spacebar", "button1"),
                    MOUSE_MODE_CLICK("semicolon", "button2"),
                ],
            }
        ]
    }


if __name__ == "__main__":
    data = {
        "profiles": [
            {
                # set MODS
                "complex_modifications": setComplexMods(),
                # default settings plus personal KEYboard info
                "virtual_hid_keyboard": {"keyboard_type_v2": "ansi"},
                "devices": [
                    {
                        "identifiers": {
                            "is_KEYboard": True,
                            "is_pointing_device": True,
                            "product_id": 45915,
                            "vendor_id": 1133,
                        },
                        "ignore": False,
                    }
                ],
            }
        ]
    }
    write_to_json("karabiner.json", data)
