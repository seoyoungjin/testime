# https://unicode.org/charts/nameslist/n_1100.html#1100
from enum import IntEnum

# chosung
class Chosung(IntEnum):
    G       = 0x1100,
    GG      = 0x1101,
    N       = 0x1102,
    D       = 0x1103,
    DD      = 0x1104,
    R       = 0x1105,
    M       = 0x1106,
    B       = 0x1107,
    BB      = 0x1108,
    S       = 0x1109,
    SS      = 0x110A,
    NG      = 0x110B,
    J       = 0x110C,
    JJ      = 0x110D,
    C       = 0x110E,
    K       = 0x110F,
    T       = 0x1110,
    P       = 0x1111,
    H       = 0x1112

# jungsung
class Jungsung(IntEnum):
    A       = 0x1161,
    AE      = 0x1162,
    YA      = 0x1163,
    YAE     = 0x1164,
    EO      = 0x1165,
    E       = 0x1166,
    YEO     = 0x1167,
    YE      = 0x1168,
    O       = 0x1169,
    WA      = 0x116A,
    WAE     = 0x116B,
    OE      = 0x116C,
    YO      = 0x116D,
    U       = 0x116E,
    WEO     = 0x116F,
    WE      = 0x1170,
    WI      = 0x1171,
    YU      = 0x1172,
    EU      = 0x1173,
    YI      = 0x1174,
    I       = 0x1175

# jongsung
class Jongsung(IntEnum):
    FILLER	= 0x11A7,
    G		= 0x11A8,
    GG		= 0x11A9,
    GS		= 0x11AA,
    N		= 0x11AB,
    NJ		= 0x11AC,
    NH		= 0x11AD,
    D		= 0x11AE,
    L		= 0x11AF,
    LG		= 0x11B0,
    LM		= 0x11B1,
    LB		= 0x11B2,
    LS		= 0x11B3,
    LT		= 0x11B4,
    LP		= 0x11B5,
    LH		= 0x11B6,
    M		= 0x11B7,
    B		= 0x11B8,
    BS		= 0x11B9,
    S		= 0x11BA,
    SS		= 0x11BB,
    NG		= 0x11BC,
    J		= 0x11BD,
    C		= 0x11BE,
    K		= 0x11BF,
    T		= 0x11C0,
    P		= 0x11C1,
    H		= 0x11C2

# 2bulsik keyboad
dubulsik_keyboard = {
    Chosung.G       : ['r'],
    Chosung.GG      : ['Shift-r'],
    Chosung.N       : ['s'],
    Chosung.D       : ['e'],
    Chosung.DD      : ['Shift-e'],
    Chosung.R       : ['f'],
    Chosung.M       : ['a'],
    Chosung.B       : ['q'],
    Chosung.BB      : ['Shift-q'],
    Chosung.S       : ['t'],
    Chosung.SS      : ['Shift-t'],
    Chosung.NG      : ['d'],
    Chosung.J       : ['w'],
    Chosung.JJ      : ['Shift-w'],
    Chosung.C       : ['c'],
    Chosung.K       : ['z'],
    Chosung.T       : ['x'],
    Chosung.P       : ['v'],
    Chosung.H       : ['g'],

    Jungsung.A      : ['k'],
    Jungsung.AE     : ['o'],
    Jungsung.YA     : ['i'],
    Jungsung.YAE    : ['Shift-o'],
    Jungsung.EO     : ['j'],
    Jungsung.E      : ['p'],
    Jungsung.YEO    : ['u'],
    Jungsung.YE     : ['Shift-p'],
    Jungsung.O      : ['h'],
    Jungsung.WA     : ['h', 'k'],
    Jungsung.WAE    : ['h', 'o'],
    Jungsung.OE     : ['h', 'l'],
    Jungsung.YO     : ['y'],
    Jungsung.U      : ['n'],
    Jungsung.WEO    : ['n', 'j'],
    Jungsung.WE     : ['n', 'p'],
    Jungsung.WI     : ['n', 'l'],
    Jungsung.YU     : ['b'],
    Jungsung.EU     : ['m'],
    Jungsung.YI     : ['m', 'l'],
    Jungsung.I      : ['l'],

    Jongsung.FILLER	: [],
    Jongsung.G		: ['r'],
    Jongsung.GG		: ['Shift-r'],
    Jongsung.GS		: ['r', 't'],
    Jongsung.N		: ['s'],
    Jongsung.NJ		: ['s', 'w'],
    Jongsung.NH		: ['s', 'g'],
    Jongsung.D		: ['e'],
    Jongsung.L		: ['f'],
    Jongsung.LG		: ['f', 'r'],
    Jongsung.LM		: ['f', 'a'],
    Jongsung.LB		: ['f', 'q'],
    Jongsung.LS		: ['f', 't'],
    Jongsung.LT		: ['f', 'x'],
    Jongsung.LP		: ['f', 'v'],
    Jongsung.LH		: ['f', 'g'],
    Jongsung.M		: ['a'],
    Jongsung.B		: ['q'],
    Jongsung.BS		: ['q', 't'],
    Jongsung.S		: ['t'],
    Jongsung.SS		: ['Shift-t'],
    Jongsung.NG		: ['d'],
    Jongsung.J		: ['w'],
    Jongsung.C		: ['c'],
    Jongsung.K		: ['z'],
    Jongsung.T		: ['x'],
    Jongsung.P		: ['v'],
    Jongsung.H		: ['g']
}

# 3bulsik keyboard
sebulsik_keyboard = {
    Chosung.G       : ['k'],
    Chosung.GG      : ['k', 'k'],
    Chosung.N       : ['h'],
    Chosung.D       : ['u'],
    Chosung.DD      : ['u', 'u'],
    Chosung.R       : ['y'],
    Chosung.M       : ['i'],
    Chosung.B       : ['semicolon'],
    Chosung.BB      : ['semicolon', 'semicolon'],
    Chosung.S       : ['n'],
    Chosung.SS      : ['n', 'n'],
    Chosung.NG      : ['j'],
    Chosung.J       : ['l'],
    Chosung.JJ      : ['l', 'l'],
    Chosung.C       : ['o'],
    Chosung.K       : ['0'],
    Chosung.T       : ['apostrophe'],
    Chosung.P       : ['p'],
    Chosung.H       : ['m'],

    Jungsung.A      : ['f'],
    Jungsung.AE     : ['r'],
    Jungsung.YA     : ['6'],
    Jungsung.YAE    : ['Shift-r'],
    Jungsung.EO     : ['t'],
    Jungsung.E      : ['c'],
    Jungsung.YEO    : ['e'],
    Jungsung.YE     : ['7'],
    Jungsung.O      : ['v'],            # LATER : /
    Jungsung.WA     : ['v', 'f'],
    Jungsung.WAE    : ['v', 'r'],
    Jungsung.OE     : ['v', 'd'],
    Jungsung.YO     : ['4'],
    Jungsung.U      : ['b'],            # LATER : 9
    Jungsung.WEO    : ['b', 't'],
    Jungsung.WE     : ['b', 'c'],
    Jungsung.WI     : ['b', 'd'],
    Jungsung.YU     : ['5'],
    Jungsung.EU     : ['g'],
    Jungsung.YI     : ['8'],            # LATER : g, d
    Jungsung.I      : ['d'],

    Jongsung.FILLER	: [],
    Jongsung.G		: ['x'],
    Jongsung.GG		: ['Shift-f'],      # LATER : x, x
    Jongsung.GS		: ['x', 'q'],
    Jongsung.N		: ['s'],
    Jongsung.NJ		: ['s', 'Shift-1'],
    Jongsung.NH		: ['Shift-s'],      # LATER : 's', '1'
    Jongsung.D		: ['Shift-a'],
    Jongsung.L		: ['w'],
    Jongsung.LG		: ['Shift-d'],      # LATER : w, x
    Jongsung.LM		: ['Shift-c'],      # LATER : w, z
    Jongsung.LB		: ['w', '3'],
    Jongsung.LS		: ['w', 'q'],
    Jongsung.LT		: ['w', 'Shift-w'],
    Jongsung.LP		: ['w', 'Shift-q'],
    Jongsung.LH		: ['Shift-v'],      # LATER : w, 1
    Jongsung.M		: ['z'],
    Jongsung.B		: ['3'],
    Jongsung.BS		: ['Shift-x'],      # LATER : 3, q
    Jongsung.S		: ['q'],
    Jongsung.SS		: ['2'],            # LATER : q, q
    Jongsung.NG		: ['a'],
    Jongsung.J		: ['Shift-1'],
    Jongsung.C		: ['Shift-z'],
    Jongsung.K		: ['Shift-e'],
    Jongsung.T		: ['Shift-w'],
    Jongsung.P		: ['Shift-q'],
    Jongsung.H		: ['1']
}

NUMBER_OF_CHOSUNG = 19
NUMBER_OF_JUNGSUNG = 21
NUMBER_OF_JONGSUNG = 28
HANGUL_BASE = 0xAC00

# compose hangul with jaso
def compose_hangul(first, vowel, final=Jongsung.FILLER):
    code = (first - Chosung.G) * (NUMBER_OF_JUNGSUNG * NUMBER_OF_JONGSUNG) + \
            (vowel - Jungsung.A)* NUMBER_OF_JONGSUNG
    code += (final - Jongsung.FILLER) + HANGUL_BASE
    return chr(code)

def get_all_hangul_cases(key_seq):
    cases = {}
    for cho in range(Chosung.G, Chosung.H + 1):
        for jung in range(Jungsung.A, Jungsung.I + 1):
            for jong in range(Jongsung.FILLER, Jongsung.H + 1):
                code = compose_hangul(cho, jung, jong)
                ks = key_seq[cho] + key_seq[jung] + key_seq[jong]
                cases[code] = ks
    return cases

def get_2bulsik_test():
    return get_all_hangul_cases(dubulsik_keyboard)

def get_3bulsik_test():
    return get_all_hangul_cases(sebulsik_keyboard)


if __name__ == "__main__":
    code = compose_hangul(Chosung.G, Jungsung.A)
    assert(code == u"가")
    code = compose_hangul(Chosung.G, Jungsung.A, Jongsung.G)
    assert(code == u"각")
    code = compose_hangul(Chosung.H, Jungsung.I, Jongsung.H)
    assert(code == u"힣")

    import json
    all_cases = get_2bulsik_test()
    with open("test/2bulsik.json", "w") as outfile:
        json.dump(all_cases, outfile, indent=4, sort_keys=True)
