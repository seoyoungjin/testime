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

from tools.xmodmap_read import read_xmodmap
from testime import keysyms

KEYNAMES = './data/keynames.txt'
XMODMAP_PKE = './data/xmodmap.dump'


def read_keynames(filename):
    keynames = []
    with open(filename) as f:
        lines = f.readlines()
    for line in lines:
        keycode, keyname = line.split(' ')
        keynames.append([keycode.strip(), keyname.strip()])
    return keynames

def print_unknown_keyname(keynames, xmodmap):
    kn_set = set(map(lambda x : x[1], keynames))
    xm_set = set()
    for v in xmodmap.values():
        xm_set |= set(v)
    for key in xm_set:
        if key not in kn_set:
            print(key)


if __name__ == "__main__":
    keynames = read_keynames(KEYNAMES)
    xmodmap = read_xmodmap(XMODMAP_PKE)

    #pprint(keynames, indent = 4)
    #print_unknown_keyname(keynames, xmodmap)
    for kn in keynames:
        if kn[1][0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            print('    "%s" : keysyms._%s,' % (kn[1], kn[1]))
            continue
        try:
            eval( "keysyms." + kn[1])
            print('    "%s" : keysyms.%s,' % (kn[1], kn[1]))
        except:
            print('    "%s" : %s,' % (kn[1], kn[0]))
            pass
