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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("%s filename" % sys.argv[0])
        sys.exit(0)
    xmodmap = read_xmodmap(sys.argv[1])

    pprint(xmodmap, indent = 4)
    print("min = ", min(xmodmap.keys()))
    print("max = ", max(xmodmap.keys()))
