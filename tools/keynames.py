# vim:set et sts=4 sw=4:
#
# check keysym name in xmodmap exist in keynames.txt

'''
$ python keynames.py | grep -v XF86
NoSymbol
SunProps
SunFront
'''

import sys
from pprint import pprint

KEYNAMES = '../data/keynames.txt'
XMODMAP_PKE = '../data/xmodmap.dump'

def read_keynames(filename):
    keynames = set()
    with open(filename) as f:
        lines = f.readlines()
    for line in lines:
        keycode, keyname = line.split(' ')
        keyname = keyname.strip()
        keynames.add(keyname)
    return keynames

def read_xmodmap(filename):
    xmodmap = set()
    with open(filename, 'r') as f:
        lines = f.readlines()
    for line in lines:
        keycode, keymap = line.split('=')
        keycode = int(keycode[8:].strip())
        keymap = keymap.strip()
        if keymap:
            keymap = keymap.strip().split(' ')
        else:
            keymap = []
        xmodmap |= set(keymap[0:4])
    return xmodmap


if __name__ == "__main__":
    keynames = read_keynames(KEYNAMES)
    xmodmap = read_xmodmap(XMODMAP_PKE)

    #pprint(keynames, indent = 4)
    #pprint(xmodmap, indent = 4)
    for key in xmodmap:
        if key not in keynames:
            print(key)
