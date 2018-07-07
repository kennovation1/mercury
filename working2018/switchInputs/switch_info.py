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
            'onLabel': 'ON',
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

def printSwitchInfo(key):
    ''' Pretty print switch info '''
    swinfo = getSwitchInfo(key)
    if swinfo is None:
        print 'Missing mapping'
        print """
        %d: {
            'ipac4': 'KLR',
            'type': 'SPDT',
            'mainLabel': 'KLR',
            'offLabel': 'KLR',
            'offPosition': 'RIGHT',
            'onLabel': 'KLR',
            'onPosition': 'LEFT'
            },
            """ % (key)
    else:
        print '{} {} {}:   {}   off:{}/{} on:{}/{}'.format(key,
                swinfo['ipac4'],
                swinfo['type'],
                swinfo['mainLabel'],
                swinfo['offLabel'],
                swinfo['offPosition'],
                swinfo['onLabel'],
                swinfo['onPosition']
                )


########
# MAIN #
########
if __name__ == '__main__':
    print getSwitchInfo(1000)
    print getSwitchInfo(64)
    print getSwitchInfo(65)
    print getSwitchInfo(66)
    printSwitchInfo(64)
    printSwitchInfo(65)
    printSwitchInfo(66)

