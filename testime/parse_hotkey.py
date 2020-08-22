# vim:set et sts=4 sw=4:
import re
from testime import modifier
from testime.keyboard import KeynameToKeycode

def parse_hotkey(exp):
    "Helper function to specify keymap"
    modifier_strs = []
    while True:
        m = re.match(r"\A(LC|LCtrl|RC|RCtrl|C|Ctrl|LM|LAlt|RM|RAlt|M|Alt|LShift|RShift|Shift|LSuper|LWin|RSuper|RWin|Super|Win)-", exp)
        if m is None:
            break
        modifier = m.group(1)
        modifier_strs.append(modifier)
        exp = re.sub(r"\A{}-".format(modifier), "", exp)
    key_str = exp
    key = KeynameToKeycode[key_str]
    return KeySequence(modmask_from_strings(modifier_strs), key)

def modmask_from_strings(modifier_strs):
    mask = 0
    for mod in modifier_strs:
        if mod in ('LShift', 'RShift', 'Shift'):
            mask |= modifier.SHIFT_MASK
        elif mod in ('LC', 'LCtrl', 'RC', 'RCtrl', 'C', 'Ctrl'):
            mask |= modifier.CONTROL_MASK
        elif mod in ('LM', 'LAlt', 'RM', 'RAlt', 'M', 'Alt'):
            mask |= modifier.ALT_MASK
        elif mod in ('LSuper', 'LWin', 'RSuper', 'RWin', 'Super', 'Win'):
            mask |= modifier.SUPER_MASK
    return mask

class KeySequence:
    def __init__(self, modifier, keycode):
        self.modifier = modifier
        self.keycode = keycode

    def __eq__(self, other):
        if isinstance(other, KeySequence):
            return self.modifier == other.modifier and self.keycode == other.keycode
        return NotImplemented

    def __hash__(self):
        return hash((frozenset(self.modifier), self.keycode))

    def __str__(self):
        return format("modifier(%04x) keycode(%d)" % (self.modifier, self.keycode))

    def with_modifier(self, modifier):
        return KeySequence(self.modifier | modifier, self.keycode)

if __name__ == '__main__':
    a = parse_hotkey("Ctrl-Shift-c")
    print(a)
    '''
    a = parse_hotkey("Alt+Shift-a, Alt-b, c")
    print(a)
    a = parse_hotkey("ctrl-space, c")
    print(a)
    '''
