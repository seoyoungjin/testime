# vim:set et sts=4 sw=4:
import sys
from pprint import pprint

def read_xmodmap(filename):
    xmodmap = {}
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
        xmodmap[keycode] = keymap[0:4]
    return xmodmap

def gen_keyname_to_keycode(xmodmap):
    for key in xmodmap:
        val = xmodmap[key]
        if val and val[0]:
            if val[0].startswith('XF86') or val[0] in ['SunProps', 'SunFront']:
                continue
            print('    "%s" : %d,' % (val[0], key))

def gen_keycode_to_keysym(xmodmap):
    for key in xmodmap:
        val = xmodmap[key]
        if not val or not val[0]:
            continue
        if val[0].startswith('XF86') or val[0] in ['SunProps', 'SunFront', 'NoSymbol']:
            continue
        if val[0][0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            print('    %d : keysyms._%s,' % (key, val[0]))
        else:
            print('    %d : keysyms.%s,' % (key, val[0]))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("%s filename" % sys.argv[0])
        sys.exit(0)
    xmodmap = read_xmodmap(sys.argv[1])

    #pprint(xmodmap, indent = 4)
    #print("min = ", min(xmodmap.keys()))
    #print("max = ", max(xmodmap.keys()))
    #gen_keyname_to_keycode(xmodmap)
    gen_keycode_to_keysym(xmodmap)
