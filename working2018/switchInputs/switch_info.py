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

switches = {
        38: {
            'ipac4': 'KLR',
            'type': 'SPST',
            'mainLabel': 'WARN LIGHTS',
            'offLabel': 'BRIGHT',
            'offPosition': 'RIGHT',
            'onLabel': 'DIM',
            'onPosition': 'LEFT'
            },

        36: {
            'ipac4': 'KLR',
            'type': 'SPST',
            'mainLabel': 'CABIN PRESS - AUDIO',
            'offLabel': 'TONE',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },
            
        23: {
            'ipac4': 'KLR',
            'type': 'SPST',
            'mainLabel': 'O2 QUAN - AUDIO',
            'offLabel': 'TONE',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },
            
        37: {
            'ipac4': 'KLR',
            'type': 'SPST',
            'mainLabel': 'O2 EMER',
            'offLabel': 'TONE',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },
            
        97: {
            'ipac4': 'KLR',
            'type': 'SPST',
            'mainLabel': 'EXCESS SUIT H2O - AUDIO',
            'offLabel': 'TONE',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },
            
        54: {
            'ipac4': 'KLR',
            'type': 'SPST',
            'mainLabel': 'EXCESS CABIN H2O - AUDIO',
            'offLabel': 'TONE',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },
            
        28: {
            'ipac4': 'KLR',
            'type': 'SPST',
            'mainLabel': 'FUEL QUAN - AUDIO',
            'offLabel': 'TONE',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },
            
        24: {
            'ipac4': 'KLR',
            'type': 'SPST',
            'mainLabel': 'RETRO WARN - AUDIO',
            'offLabel': 'TONE',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },
            
        63: {
            'ipac4': 'KLR',
            'type': 'SPST',
            'mainLabel': 'RETRO RESET - AUDIO',
            'offLabel': 'TONE',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },

        65: {
            'ipac4': 'KLR',
            'type': 'SPDT',
            'mainLabel': 'SUIT FAN',
            'offLabel': 'No 1',
            'offPosition': 'CENTER',
            'onLabel': 'NORM',
            'onPosition': 'RIGHT'
            },
            
        66: {
            'ipac4': 'KLR',
            'type': 'SPDT',
            'mainLabel': 'SUIT FAN',
            'offLabel': 'No 1',
            'offPosition': 'CENTER',
            'onLabel': 'No 2',
            'onPosition': 'LEFT'
            },
            
        4: {
            'ipac4': 'KLR',
            'type': 'SPST',
            'mainLabel': 'CABIN FAN',
            'offLabel': 'NORM',
            'offPosition': 'RIGHT',
            'onLabel': 'OFF',
            'onPosition': 'LEFT'
            },
            
        8: {
            'ipac4': 'KLR',
            'type': 'SPDT',
            'mainLabel': 'ASCS AC BUS',
            'offLabel': 'OFF',
            'offPosition': 'CENTER',
            'onLabel': 'NORM',
            'onPosition': 'RIGHT'
            },
            
        106: {
            'ipac4': 'KLR',
            'type': 'SPDT',
            'mainLabel': 'ASCS AC BUS',
            'offLabel': 'OFF',
            'offPosition': 'CENTER',
            'onLabel': 'STBY',
            'onPosition': 'LEFT'
            },
            
        108: {
            'ipac4': 'KLR',
            'type': 'SPST',
            'mainLabel': 'ISOL BTRY',
            'offLabel': 'NORM',
            'offPosition': 'RIGHT',
            'onLabel': 'STBY',
            'onPosition': 'LEFT'
            },
            
        105: {
            'ipac4': 'KLR',
            'type': 'SPDT',
            'mainLabel': 'AMMETER',
            'offLabel': 'PWR OFF',
            'offPosition': 'CENTER',
            'onLabel': 'NORM',
            'onPosition': 'RIGHT'
            },

        103: {
            'ipac4': 'KLR',
            'type': 'SPDT',
            'mainLabel': 'AMMETER',
            'offLabel': 'PWR OFF',
            'offPosition': 'CENTER',
            'onLabel': 'BYPASS',
            'onPosition': 'LEFT'
            },
            
        29: {
            'ipac4': 'KLR',
            'type': 'SPDT',
            'mainLabel': 'FANS AC BUS',
            'offLabel': 'OFF',
            'offPosition': 'CENTER',
            'onLabel': 'NORM',
            'onPosition': 'RIGHT'
            },
            
        56: {
            'ipac4': 'KLR',
            'type': 'SPDT',
            'mainLabel': 'FANS AC BUS',
            'offLabel': 'OFF',
            'offPosition': 'CENTER',
            'onLabel': 'STBY',
            'onPosition': 'LEFT'
            },
            
        44: {
            'ipac4': 'KLR',
            'type': 'SPST',
            'mainLabel': 'AC VOLTS',
            'offLabel': 'FANS',
            'offPosition': 'RIGHT',
            'onLabel': 'ASCS',
            'onPosition': 'LEFT'
            },
            
        42: {
            'ipac4': 'KLR',
            'type': 'SPST',
            'mainLabel': 'AUDIO BUS',
            'offLabel': 'NORM',
            'offPosition': 'RIGHT',
            'onLabel': 'EMER',
            'onPosition': 'LEFT'
            },
            
        57: {
            'ipac4': 'KLR',
            'type': 'SPST',
            'mainLabel': 'INLET VALVE PWR',
            'offLabel': 'NORM',
            'offPosition': 'RIGHT',
            'onLabel': 'BYPASS',
            'onPosition': 'LEFT'
            },
            
        2: {
            'ipac4': 'KLR',
            'type': 'SPST',
            'mainLabel': 'BEACON',
            'offLabel': 'CONT',
            'offPosition': 'RIGHT',
            'onLabel': 'GRND COMD',
            'onPosition': 'LEFT'
            },
            
        46: {
            'ipac4': 'KLR',
            'type': 'SPDT',
            'mainLabel': 'TRANSMIT',
            'offLabel': 'OFF',
            'offPosition': 'CENTER',
            'onLabel': 'UHF',
            'onPosition': 'RIGHT'
            },
            
        47: {
            'ipac4': 'KLR',
            'type': 'SPDT',
            'mainLabel': 'TRANSMIT',
            'offLabel': 'OFF',
            'offPosition': 'CENTER',
            'onLabel': 'HF',
            'onPosition': 'LEFT'
            },
            
        45: {
            'ipac4': 'KLR',
            'type': 'SPST',
            'mainLabel': 'UHF SELECT',
            'offLabel': 'HI PWR',
            'offPosition': 'RIGHT',
            'onLabel': 'LO PWR',
            'onPosition': 'LEFT'
            },
            
        64: {
            'ipac4': 'KLR',
            'type': 'SPST',
            'mainLabel': 'O2 FLOW',
            'offLabel': 'PRIM',
            'offPosition': 'RIGHT',
            'onLabel': 'SEC.',
            'onPosition': 'LEFT'
            },
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


########
# MAIN #
########
if __name__ == '__main__':
    print getSwitchInfo(1000)
    print getSwitchInfo(64)
    print getSwitchInfo(65)
    print getSwitchInfo(66)
    for debug in (False, True):
        printSwitchInfo(64, 0, debug)
        printSwitchInfo(64, 1, debug)
        printSwitchInfo(65, 0, debug)
        printSwitchInfo(66, 0, debug)
        printSwitchInfo(65, 1, debug)
        printSwitchInfo(66, 1, debug)

