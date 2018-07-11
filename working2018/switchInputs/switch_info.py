'''
Dictionary of objects that are indexed by the key scancode int returned by reading an IPAC-4.

Key meanings:
    'ipac4': Silk screened label for the signal on the IPAC-4
    'type': 'SPST' or 'SPDT' (2-way or 3-way switch). Note that a SPDT switch will have 2 entries since it is treated
            as two SPST switches
    'mainLabel': Main label for a switch as printed on panel
    'offLabel': Label for the 'off' (key up) position of the switch
    'offPosition': Physical position of the switch to be off (key up)
    'onLabel': Label for the 'on' (key down/hold) position of the switch
    'onPosition' Physical position of the switch to be on (key down)
    
    Positions must be one of: 'LEFT', 'RIGHT', 'UP', 'DOWN', 'CENTER'. CENTER is only used for SPDT switches.
'''
import json

switches = {
        49: {
            'ipac4': '3RGHT',
            'type': 'SPST',
            'mainLabel': 'WARN LIGHTS',
            'offLabel': 'BRIGHT',
            'offPosition': 'RIGHT',
            'onLabel': 'DIM',
            'onPosition': 'LEFT'
            },

        39: {
            'ipac4': '3LEFT',
            'type': 'SPST',
            'mainLabel': 'CABIN PRESS - AUDIO',
            'offLabel': 'TONE',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },
            
        18: {
            'ipac4': '3UP',
            'type': 'SPST',
            'mainLabel': 'O2 QUAN - AUDIO',
            'offLabel': 'TONE',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },
            
        41: {
            'ipac4': '3DOWN',
            'type': 'SPST',
            'mainLabel': 'O2 EMER',
            'offLabel': 'TONE',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },
            
        43: {
            'ipac4': '3SW1',
            'type': 'SPST',
            'mainLabel': 'EXCESS SUIT H2O - AUDIO',
            'offLabel': 'TONE',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },
            
        44: {
            'ipac4': '3SW2',
            'type': 'SPST',
            'mainLabel': 'EXCESS CABIN H2O - AUDIO',
            'offLabel': 'TONE',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },
            
        45: {
            'ipac4': '3SW3',
            'type': 'SPST',
            'mainLabel': 'FUEL QUAN - AUDIO',
            'offLabel': 'TONE',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },
            
        46: {
            'ipac4': '3SW4',
            'type': 'SPST',
            'mainLabel': 'RETRO WARN - AUDIO',
            'offLabel': 'TONE',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },
            
        47: {
            'ipac4': '3SW5',
            'type': 'SPST',
            'mainLabel': 'RETRO RESET - AUDIO',
            'offLabel': 'TONE',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },

        79: {
            'ipac4': '3SW7',
            'type': 'SPDT',
            'mainLabel': 'SUIT FAN',
            'offLabel': 'No 1',
            'offPosition': 'CENTER',
            'onLabel': 'NORM',
            'onPosition': 'RIGHT'
            },
            
        82: {
            'ipac4': '3SW8',
            'type': 'SPDT',
            'mainLabel': 'SUIT FAN',
            'offLabel': 'No 1',
            'offPosition': 'CENTER',
            'onLabel': 'No 2',
            'onPosition': 'LEFT'
            },
            
        81: {
            'ipac4': '3STRT',
            'type': 'SPST',
            'mainLabel': 'CABIN FAN',
            'offLabel': 'NORM',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },
            
        80: {
            'ipac4': '3COIN',
            'type': 'SPDT',
            'mainLabel': 'ASCS AC BUS',
            'offLabel': 'OFF',
            'offPosition': 'CENTER',
            'onLabel': 'NORM',
            'onPosition': 'RIGHT'
            },
            
        4: {
            'ipac4': '1RGHT',
            'type': 'SPDT',
            'mainLabel': 'ASCS AC BUS',
            'offLabel': 'OFF',
            'offPosition': 'CENTER',
            'onLabel': 'STBY',
            'onPosition': 'LEFT'
            },
            
        6: {
            'ipac4': '1DOWN',
            'type': 'SPST',
            'mainLabel': 'ISOL BTRY',
            'offLabel': 'NORM',
            'offPosition': 'RIGHT',
            'onLabel': 'STBY',
            'onPosition': 'LEFT'
            },
            
        7: {
            'ipac4': '1LEFT',
            'type': 'SPDT',
            'mainLabel': 'AMMETER',
            'offLabel': 'PWR OFF',
            'offPosition': 'CENTER',
            'onLabel': 'NORM',
            'onPosition': 'RIGHT'
            },

        5: {
            'ipac4': '1UP',
            'type': 'SPDT',
            'mainLabel': 'AMMETER',
            'offLabel': 'PWR OFF',
            'offPosition': 'CENTER',
            'onLabel': 'BYPASS',
            'onPosition': 'LEFT'
            },
            
        8: {
            'ipac4': '1SW1',
            'type': 'SPDT',
            'mainLabel': 'FANS AC BUS',
            'offLabel': 'OFF',
            'offPosition': 'CENTER',
            'onLabel': 'NORM',
            'onPosition': 'RIGHT'
            },
            
        9: {
            'ipac4': '1SW2',
            'type': 'SPDT',
            'mainLabel': 'FANS AC BUS',
            'offLabel': 'OFF',
            'offPosition': 'CENTER',
            'onLabel': 'STBY',
            'onPosition': 'LEFT'
            },
            
        12: {
            'ipac4': '1SW5',
            'type': 'SPST',
            'mainLabel': 'AC VOLTS',
            'offLabel': 'FANS',
            'offPosition': 'RIGHT',
            'onLabel': 'ASCS',
            'onPosition': 'LEFT'
            },
            
        11: {
            'ipac4': '1SW4',
            'type': 'SPST',
            'mainLabel': 'AUDIO BUS',
            'offLabel': 'NORM',
            'offPosition': 'RIGHT',
            'onLabel': 'EMER',
            'onPosition': 'LEFT'
            },
            
        10: {
            'ipac4': '1SW3',
            'type': 'SPST',
            'mainLabel': 'INLET VALVE PWR',
            'offLabel': 'NORM',
            'offPosition': 'RIGHT',
            'onLabel': 'BYPASS',
            'onPosition': 'LEFT'
            },
            
        16: {
            'ipac4': '1STRT',
            'type': 'SPST',
            'mainLabel': 'BEACON',
            'offLabel': 'CONT',
            'offPosition': 'RIGHT',
            'onLabel': 'GRND COMD',
            'onPosition': 'LEFT'
            },
            
        14: {
            'ipac4': '1SW7',
            'type': 'SPDT',
            'mainLabel': 'TRANSMIT',
            'offLabel': 'OFF',
            'offPosition': 'CENTER',
            'onLabel': 'UHF',
            'onPosition': 'RIGHT'
            },
            
        15: {
            'ipac4': '1SW8',
            'type': 'SPDT',
            'mainLabel': 'TRANSMIT',
            'offLabel': 'OFF',
            'offPosition': 'CENTER',
            'onLabel': 'HF',
            'onPosition': 'LEFT'
            },
            
        13: {
            'ipac4': '1SW6',
            'type': 'SPST',
            'mainLabel': 'UHF SELECT',
            'offLabel': 'HI PWR',
            'offPosition': 'RIGHT',
            'onLabel': 'LO PWR',
            'onPosition': 'LEFT'
            },
            
        48: {
            'ipac4': '3SW6',
            'type': 'SPST',
            'mainLabel': 'O2 FLOW',
            'offLabel': 'PRIM',
            'offPosition': 'RIGHT',
            'onLabel': 'SEC.',
            'onPosition': 'LEFT'
            },

        112: {
            'ipac4': '4RGHT',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=112',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        113: {
            'ipac4': '4LEFT',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=113',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        116: {
            'ipac4': '4UP',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=116',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        42: {
            'ipac4': '4DOWN',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=42',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        117: {
            'ipac4': '4SW1',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=117',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        58: {
            'ipac4': '4SW2',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=58',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        59: {
            'ipac4': '4SW3',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=59',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        60: {
            'ipac4': '4SW4',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=60',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        61: {
            'ipac4': '4SW5',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=61',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        62: {
            'ipac4': '4SW6',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=62',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        63: {
            'ipac4': '4SW7',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=63',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        64: {
            'ipac4': '4SW8',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=64',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        65: {
            'ipac4': '4STRT',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=65',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        66: {
            'ipac4': '4COIN',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=66',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        17: {
            'ipac4': '2RGHT',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=17',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        20: {
            'ipac4': '2LEFT',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=20',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        18: {
            'ipac4': '2UP',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=18',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        19: {
            'ipac4': '2DOWN',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=19',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        21: {
            'ipac4': '2SW1',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=21',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        22: {
            'ipac4': '2SW2',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=22',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        23: {
            'ipac4': '2SW3',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=23',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        24: {
            'ipac4': '2SW4',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=24',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        25: {
            'ipac4': '2SW5',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=25',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        26: {
            'ipac4': '2SW6',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=26',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        27: {
            'ipac4': '2SW7',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=27',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        28: {
            'ipac4': '2SW8',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=28',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        29: {
            'ipac4': '2STRT',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=29',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            }
}


def getSwitchInfo(key):
    '''
    Return switch info given a key scancode.
    Returns None if switch not found.
    '''
    return switches.get(key)

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def printSwitchInfo(key, state, debug=False):
    ''' Pretty print switch info '''
    if debug:
        printSwitchInfoDebug(key, state)
        return

    swinfo = getSwitchInfo(key)
    if swinfo is None:
        print color.RED + 'Missing mapping for key: ' + str(key) + color.END
    else:
        if state == 0:
            label = swinfo['offLabel']
            position = color.BOLD + color.BLUE + swinfo['offLabel'] + color.END
        else:
            position = color.BOLD + color.BLUE + swinfo['onLabel'] + color.END

        print color.BOLD + color.DARKCYAN + swinfo['mainLabel'] + color.END + ' -> ' + position

def printSwitchInfoDebug(key, state):
    ''' Pretty print switch info '''
    swinfo = getSwitchInfo(key)
    if swinfo is None:
        print color.RED + 'Missing mapping for key: ' + str(key) + color.END
    else:
        if state == 0:
            off = color.BOLD + color.PURPLE + 'off'
            on = color.END + 'on'
        else:
            off = 'off'
            on = color.BOLD + color.BLUE + 'on'

        print '{} {} {}:   {}   {}:{}/{} {}:{}/{}{}'.format(key,
                swinfo['ipac4'],
                swinfo['type'],
                swinfo['mainLabel'],
                off,
                swinfo['offLabel'],
                swinfo['offPosition'],
                on,
                swinfo['onLabel'],
                swinfo['onPosition'],
                color.END
                )

def makeEventMessage(key, state):
    ''' Create an event message '''
    eventType = 'toggleSwitch'

    swinfo = getSwitchInfo(key)
    if swinfo is None:
        eventName = 'INVALID_KEY'
        eventDescription = 'Umapped key found: ' + str(key)
    else:
        if state == 0:
            stateLabel = swinfo['offLabel']
        else:
            stateLabel = swinfo['onLabel']

        eventName = swinfo['mainLabel'] + '=>' + stateLabel
        eventDescription = swinfo['mainLabel'] + ' toggled to ' + stateLabel

    return {
            'eventName': eventName,
            'eventType': eventType,
            'eventDescription': eventDescription
            }

########
# MAIN #
########
if __name__ == '__main__':
    print '\ngetSwitchInfo'
    print getSwitchInfo(1000)
    print getSwitchInfo(47)
    print getSwitchInfo(79)
    print getSwitchInfo(82)
    for debug in (False, True):
        print '\nprintSwitchInfo debug=' + str(debug)
        printSwitchInfo(47, 0, debug)
        printSwitchInfo(47, 1, debug)
        printSwitchInfo(79, 0, debug)
        printSwitchInfo(82, 0, debug)
        printSwitchInfo(79, 1, debug)
        printSwitchInfo(82, 1, debug)

    print '\nmakeEventMessage'
    print(json.dumps(makeEventMessage(82, 0), indent=4))
    print(json.dumps(makeEventMessage(82, 1), indent=4))
