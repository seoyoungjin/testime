# vim:set et sts=4 sw=4:
import re
from testime.keyboard import KeynameToKeycode

all_modifiers = {'alt', 'ctrl', 'shift', 'windows'}

_is_str = lambda x: isinstance(x, str)
_is_number = lambda x: isinstance(x, int)
_is_list = lambda x: isinstance(x, (list, tuple))

def key_to_scan_codes(key):
   print(key)
   keycode = KeynameToKeycode[key]
   print(key, keycode)
   return key

def normalize_name(name):
    """
    Given a key name (e.g. "LEFT CONTROL"), clean up the string and convert to
    the canonical representation (e.g. "left ctrl") if one is known.
    """
    if not name or not isinstance(name, basestring):
        raise ValueError('Can only normalize non-empty string names. Unexpected '+ repr(name))

    if len(name) > 1:
        name = name.lower()
    if name != '_' and '_' in name:
        name = name.replace('_', ' ')

    return canonical_names.get(name, name)

def parse_hotkey(hotkey):
    """
    Example:
        parse_hotkey("alt+shift+a, alt+b, c")
        #    Keys:    ^~^ ^~~~^ ^  ^~^ ^  ^
        #    Steps:   ^~~~~~~~~~^  ^~~~^  ^
        # ((alt_codes, shift_codes, a_codes), (alt_codes, b_codes), (c_codes,))
    """
    if _is_number(hotkey) or len(hotkey) == 1:
        scan_codes = key_to_scan_codes(hotkey)
        step = (scan_codes,)
        steps = (step,)
        return steps
    elif _is_list(hotkey):
        if not any(map(_is_list, hotkey)):
            step = tuple(key_to_scan_codes(k) for k in hotkey)
            steps = (step,)
            return steps
        return hotkey

    steps = []
    for step in re.split(r',\s?', hotkey):
        keys = re.split(r'\s?\+\s?', step)
        steps.append(tuple(key_to_scan_codes(key) for key in keys))
    return tuple(steps)


if __name__ == '__main__':
    a = parse_hotkey("alt+shift+a, alt+b, c")
    print(a)
    a = parse_hotkey("ctrl+space, c")
    print(a)
