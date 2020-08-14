from .import keysyms
from .import modifier

from PySide2.QtCore import *

def ModConv(mod):
    state = 0
    if Qt.ShiftModifier & mod:
        state |= modifier.SHIFT_MASK
    if Qt.ControlModifier & mod:
        state |= modifier.CONTROL_MASK
    if Qt.AltModifier & mod:
        state |= modifier.ALT_MASK
    if Qt.MetaModifier & mod:
        state |= modifier.META_MASK
    return state

def KeysymConv(keysym):
    # TBD
    return keysym

 
def test():
    assert(ModConv(Qt.ShiftModifier) == modifier.SHIFT_MASK)
    assert(ModConv(Qt.ControlModifier) == modifier.CONTROL_MASK)
    assert(ModConv(Qt.AltModifier) == modifier.ALT_MASK)
    assert(ModConv(Qt.MetaModifier) == modifier.META_MASK)

    assert(KeysymConv(Qt.Key_Space) == keysyms.space)
    assert(KeysymConv(Qt.Key_0) == keysyms._0)
    assert(KeysymConv(Qt.Key_A) == keysyms.A)


if __name__ == "__main__":
        test()
