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

        200: {
            'ipac4': 'KLR',
            'type': 'SPDT',
            'mainLabel': 'ASCS AC BUS',
            'offLabel': 'OFF',
            'offPosition': 'CENTER',
            'onLabel': 'RIGHT',
            'onPosition': 'RIGHT'
            },

        201: {
            'ipac4': 'KLR',
            'type': 'SPDT',
            'mainLabel': 'ASCS AC BUS',
            'offLabel': 'OFF',
            'offPosition': 'CENTER',
            'onLabel': 'STBY',
            'onPosition': 'LEFT'
            }


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
    print getSwitchInfo(400)
    print getSwitchInfo(38)
    print getSwitchInfo(200)
    print getSwitchInfo(201)
    printSwitchInfo(38)
    printSwitchInfo(400)
    printSwitchInfo(500)
