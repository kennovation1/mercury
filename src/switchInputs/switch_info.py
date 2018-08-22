'''
Dictionary of objects that are indexed by the key scancode int returned by reading an IPAC-4.

Key meanings:
    'ipac4': Silk screened label for the signal on the IPAC-4
    'type': 'SPST', 'SPST-MOM', or 'SPDT'. For 2-way toggle, 2-way momentary, or 3-way toggle.
             Note that a SPDT switch will have 2 entries since it is treated as two SPST switches
    'mainLabel': Main label for a switch as printed on panel
    'offLabel': Label for the 'off' (key up) position of the switch
    'offPosition': Physical position of the switch to be off (key up)
    'onLabel': Label for the 'on' (key down/hold) position of the switch
    'onPosition' Physical position of the switch to be on (key down)
    
    Positions must be one of: 'LEFT', 'RIGHT', 'UP', 'DOWN', 'CENTER'. CENTER is only used for SPDT switches.
    Positions for SPST-MOM must be one of: 'PRESSED' or 'RELEASED'
'''
import json

switches = {
        30: {
            'ipac4': '3RGHT',
            'type': 'SPST',
            'mainLabel': 'WARN LIGHTS',
            'offLabel': 'BRIGHT',
            'offPosition': 'RIGHT',
            'onLabel': 'DIM',
            'onPosition': 'LEFT'
            },

        48: {
            'ipac4': '3LEFT',
            'type': 'SPST',
            'mainLabel': 'CABIN PRESS - AUDIO',
            'offLabel': 'TONE',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },
            
        46: {
            'ipac4': '3UP',
            'type': 'SPST',
            'mainLabel': 'O2 QUAN - AUDIO',
            'offLabel': 'TONE',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },
            
        32: {
            'ipac4': '3DOWN',
            'type': 'SPST',
            'mainLabel': 'O2 EMER - AUDIO',
            'offLabel': 'TONE',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },
            
        18: {
            'ipac4': '3SW1',
            'type': 'SPST',
            'mainLabel': 'EXCESS SUIT H2O - AUDIO',
            'offLabel': 'TONE',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },
            
        33: {
            'ipac4': '3SW2',
            'type': 'SPST',
            'mainLabel': 'EXCESS CABIN H2O - AUDIO',
            'offLabel': 'TONE',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },
            
        34: {
            'ipac4': '3SW3',
            'type': 'SPST',
            'mainLabel': 'FUEL QUAN - AUDIO',
            'offLabel': 'TONE',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },
            
        35: {
            'ipac4': '3SW4',
            'type': 'SPST',
            'mainLabel': 'RETRO WARN - AUDIO',
            'offLabel': 'TONE',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },
            
        23: {
            'ipac4': '3SW5',
            'type': 'SPST',
            'mainLabel': 'RETRO RESET - AUDIO',
            'offLabel': 'TONE',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },

        36: {
            'ipac4': '3SW6',
            'type': 'SPST',
            'mainLabel': 'O2 FLOW',
            'offLabel': 'PRIM',
            'offPosition': 'RIGHT',
            'onLabel': 'SEC.',
            'onPosition': 'LEFT'
            },

        37: {
            'ipac4': '3SW7',
            'type': 'SPDT',
            'mainLabel': 'SUIT FAN',
            'offLabel': 'No 1',
            'offPosition': 'CENTER',
            'onLabel': 'NORM',
            'onPosition': 'RIGHT'
            },
            
        38: {
            'ipac4': '3SW8',
            'type': 'SPDT',
            'mainLabel': 'SUIT FAN',
            'offLabel': 'No 1',
            'offPosition': 'CENTER',
            'onLabel': 'No 2',
            'onPosition': 'LEFT'
            },
            
        50: {
            'ipac4': '3STRT',
            'type': 'SPST',
            'mainLabel': 'CABIN FAN',
            'offLabel': 'NORM',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },
            
        49: {
            'ipac4': '3COIN',
            'type': 'SPDT',
            'mainLabel': 'ASCS AC BUS',
            'offLabel': 'OFF',
            'offPosition': 'CENTER',
            'onLabel': 'NORM',
            'onPosition': 'RIGHT'
            },
            
        24: {
            'ipac4': '1RGHT',
            'type': 'SPDT',
            'mainLabel': 'ASCS AC BUS',
            'offLabel': 'OFF',
            'offPosition': 'CENTER',
            'onLabel': 'STBY',
            'onPosition': 'LEFT'
            },

         25: {
            'ipac4': '1LEFT',
            'type': 'SPDT',
            'mainLabel': 'AMMETER',
            'offLabel': 'PWR OFF',
            'offPosition': 'CENTER',
            'onLabel': 'NORM',
            'onPosition': 'RIGHT'
            },
            
        16: {
            'ipac4': '1UP',
            'type': 'SPDT',
            'mainLabel': 'AMMETER',
            'offLabel': 'PWR OFF',
            'offPosition': 'CENTER',
            'onLabel': 'BYPASS',
            'onPosition': 'LEFT'
            },
            
        19: {
            'ipac4': '1DOWN',
            'type': 'SPST',
            'mainLabel': 'ISOL BTRY',
            'offLabel': 'NORM',
            'offPosition': 'RIGHT',
            'onLabel': 'STBY',
            'onPosition': 'LEFT'
            },

        31: {
            'ipac4': '1SW1',
            'type': 'SPDT',
            'mainLabel': 'FANS AC BUS',
            'offLabel': 'OFF',
            'offPosition': 'CENTER',
            'onLabel': 'NORM',
            'onPosition': 'RIGHT'
            },
            
        20: {
            'ipac4': '1SW2',
            'type': 'SPDT',
            'mainLabel': 'FANS AC BUS',
            'offLabel': 'OFF',
            'offPosition': 'CENTER',
            'onLabel': 'STBY',
            'onPosition': 'LEFT'
            },
                     
        22: {
            'ipac4': '1SW3',
            'type': 'SPST',
            'mainLabel': 'INLET VALVE PWR',
            'offLabel': 'NORM',
            'offPosition': 'RIGHT',
            'onLabel': 'BYPASS',
            'onPosition': 'LEFT'
            },
   
        47: {
            'ipac4': '1SW4',
            'type': 'SPST',
            'mainLabel': 'AUDIO BUS',
            'offLabel': 'NORM',
            'offPosition': 'RIGHT',
            'onLabel': 'EMER',
            'onPosition': 'LEFT'
            },

        17: {
            'ipac4': '1SW5',
            'type': 'SPST',
            'mainLabel': 'AC VOLTS',
            'offLabel': 'FANS',
            'offPosition': 'RIGHT',
            'onLabel': 'ASCS',
            'onPosition': 'LEFT'
            },

        45: {
            'ipac4': '1SW6',
            'type': 'SPST',
            'mainLabel': 'UHF SELECT',
            'offLabel': 'HI PWR',
            'offPosition': 'RIGHT',
            'onLabel': 'LO PWR',
            'onPosition': 'LEFT'
            },
                      
        21: {
            'ipac4': '1SW7',
            'type': 'SPDT',
            'mainLabel': 'TRANSMIT',
            'offLabel': 'OFF',
            'offPosition': 'CENTER',
            'onLabel': 'UHF',
            'onPosition': 'RIGHT'
            },
            
        44: {
            'ipac4': '1SW8',
            'type': 'SPDT',
            'mainLabel': 'TRANSMIT',
            'offLabel': 'OFF',
            'offPosition': 'CENTER',
            'onLabel': 'HF',
            'onPosition': 'LEFT'
            },
             
        2: {
            'ipac4': '1STRT',
            'type': 'SPST',
            'mainLabel': 'BEACON',
            'offLabel': 'CONT',
            'offPosition': 'RIGHT',
            'onLabel': 'GRND COMD',
            'onPosition': 'LEFT'
            },
                       
        3: {
            'ipac4': '1COIN',
            'type': 'SPST',
            'mainLabel': 'VOX PWR',
            'offLabel': 'ON',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT',
            },

        4: {
            'ipac4': '4RGHT',
            'type': 'SPST-MOM',
            'mainLabel': 'BLOOD PRESS - STOP',
            'offLabel': 'released',
            'offPosition': 'RELEASED',
            'onLabel': 'pressed',
            'onPosition': 'PRESSED',
            },

        5: {
            'ipac4': '4LEFT',
            'type': 'SPST-MOM',
            'mainLabel': 'BLOOD PRESS - START',
            'offLabel': 'released',
            'offPosition': 'RELEASED',
            'onLabel': 'pressed',
            'onPosition': 'PRESSED',
            },

        6: {
            'ipac4': '4UP',
            'type': 'SPST-MOM',
            'mainLabel': 'KEY',
            'offLabel': 'released',
            'offPosition': 'RELEASED',
            'onLabel': 'pressed',
            'onPosition': 'PRESSED',
            },

        7: {
            'ipac4': '4DOWN',
            'type': 'SPST-MOM',
            'mainLabel': 'TIME ZERO',
            'offLabel': 'released',
            'offPosition': 'RELEASED',
            'onLabel': 'pressed',
            'onPosition': 'PRESSED',
            },

        8: {
            'ipac4': '4SW1',
            'type': 'SPST',
            'mainLabel': 'LIGHT TEST',
            'offLabel': 'OFF',
            'offPosition': 'RIGHT',
            'onLabel': 'ON',
            'onPosition': 'LEFT',
            },

        9: {
            'ipac4': '4SW2',
            'type': 'SPST',
            'mainLabel': 'RATE IND',
            'offLabel': 'MAN ON',
            'offPosition': 'RIGHT',
            'onLabel': 'AUTO',
            'onPosition': 'LEFT',
            },

        10: {
            'ipac4': '4SW3',
            'type': 'SPST',
            'mainLabel': 'STBT BTRY',
            'offLabel': 'OFF',
            'offPosition': 'RIGHT',
            'onLabel': 'ON',
            'onPosition': 'LEFT',
            },

        11: {
            'ipac4': '4SW4',
            'type': 'SPST',
            'mainLabel': 'UHF DF',
            'offLabel': 'R/T',
            'offPosition': 'RIGHT',
            'onLabel': 'NORM',
            'onPosition': 'LEFT',
            },

        103: {
            'ipac4': '4SW5',
            'type': 'SPST',
            'mainLabel': 'FUSE: SUIT FAN',
            'offLabel': 'OFF',
            'offPosition': 'DOWN',
            'onLabel': 'ON',
            'onPosition': 'UP',
            },

        29: {
            'ipac4': '4SW6',
            'type': 'SPST',
            'mainLabel': 'FUSE: ENVIR CONTL',
            'offLabel': 'OFF',
            'offPosition': 'DOWN',
            'onLabel': 'ON',
            'onPosition': 'UP',
            },

        106: {
            'ipac4': '4SW7',
            'type': 'SPST',
            'mainLabel': 'FUSE: RETRO JETT',
            'offLabel': 'OFF',
            'offPosition': 'DOWN',
            'onLabel': 'ON',
            'onPosition': 'UP',
            },

        105: {
            'ipac4': '4SW8',
            'type': 'SPST',
            'mainLabel': 'FUSE: RETRO MAN',
            'offLabel': 'OFF',
            'offPosition': 'DOWN',
            'onLabel': 'ON',
            'onPosition': 'UP',
            },

        108: {
            'ipac4': '4STRT',
            'type': 'SPST',
            'mainLabel': 'FUSE: PRO GRAMR',
            'offLabel': 'OFF',
            'offPosition': 'DOWN',
            'onLabel': 'ON',
            'onPosition': 'UP',
            },

        999: {
            'ipac4': '4COIN',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=999 DO NOT USE',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        56: {
            'ipac4': '2RGHT',
            'type': 'SPST',
            'mainLabel': 'FUSE: BLOOD PRESS',
            'offLabel': 'OFF',
            'offPosition': 'DOWN',
            'onLabel': 'ON',
            'onPosition': 'UP',
            },

        216: {
            'ipac4': '2LEFT',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        217: {
            'ipac4': '2UP',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        218: {
            'ipac4': '2DOWN',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        219: {
            'ipac4': '2SW1',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        220: {
            'ipac4': '2SW2',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        221: {
            'ipac4': '2SW3',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        222: {
            'ipac4': '2SW4',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        223: {
            'ipac4': '2SW5',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        224: {
            'ipac4': '2SW6',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        225: {
            'ipac4': '2SW7',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        226: {
            'ipac4': '2SW8',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=',
            'offLabel': 'OFFLABEL_NOTSET',
            'offPosition': 'RIGHT',
            'onLabel': 'ONLABEL_NOTSET',
            'onPosition': 'LEFT',
            },

        227: {
            'ipac4': '2STRT',
            'type': 'SPST',
            'mainLabel': '*UNSET* scancode=',
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
