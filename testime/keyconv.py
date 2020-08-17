from . import keysyms
from . import modifier

from PySide2.QtCore import *

def ModConv(mod):
    state = 0
    if Qt.ShiftModifier & mod:
        state |= modifier.SHIFT_MASK
    # no capslock in Qt.modifers, we have to check keyboad status
    # nativeModifiers
    # if ...:
    #    state |= modifier.LOCK_MASK
    if Qt.ControlModifier & mod:
        state |= modifier.CONTROL_MASK
    if Qt.AltModifier & mod:
        state |= modifier.ALT_MASK
    if Qt.KeypadModifier & mod:
        state |= modifier.MOD2_MASK
    if Qt.AltModifier & mod:
        state |= modifier.ALT_MASK
    # super state |= modifier.SUPER_MASK
    if Qt.MetaModifier & mod:
        state |= modifier.META_MASK
    return state

def KeysymConv(ksym, mod):
    # TODO
    if ksym >= keysyms.A and ksym <= keysyms.Z:
        if not mod & modifier.SHIFT_MASK:
            ksym = ksym - keysyms.A + keysyms.a
    return ksym

 
def test():
    assert(ModConv(Qt.ShiftModifier) == modifier.SHIFT_MASK)
    assert(ModConv(Qt.ControlModifier) == modifier.CONTROL_MASK)
    assert(ModConv(Qt.AltModifier) == modifier.ALT_MASK)
    assert(ModConv(Qt.MetaModifier) == modifier.META_MASK)

    assert(KeysymConv(Qt.Key_Space, 0) == keysyms.space)
    assert(KeysymConv(Qt.Key_0, 0) == keysyms._0)
    assert(KeysymConv(Qt.Key_A, 0) == keysyms.a)
    assert(KeysymConv(Qt.Key_A, modifier.SHIFT_MASK) == keysyms.A)


if __name__ == "__main__":
        test()
