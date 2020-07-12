# Example controller that reads switches and controller light outputs based on somewhat arbitrary mapping rules
# python readinputs.py -f &
# python lightoutupts.py &
# python funbox.py

import json
import os
import errno
from time import sleep
from threading import Timer
import subprocess
import signal

SwitchesFIFO = '/tmp/mercury-events'
LightsFIFO = '/tmp/light-commands'

Intensity = 50
DIM = 50
BRIGHT = 150
WarnIntensity = DIM

AudioProcess = None

WarnLightsState = {
        'CABIN PRESS': False,
        'O2 QUAN': False,
        'O2 EMER': False,
        'EXCESS SUIT H20': False,
        'EXCESS CABIN H20': False,
        'FUEL QUAN': False,
        'RETRO WARN': False,
        'RETRO RESET': False,
        'STBY AC-AUTO': False
        }

WarnAudioToneEvents = [
        'CABIN PRESS - AUDIO=>TONE',
        'O2 QUAN - AUDIO=>TONE',
        'O2 EMER - AUDIO=>TONE',
        'EXCESS SUIT H2O - AUDIO=>TONE',
        'EXCESS CABIN H2O - AUDIO=>TONE',
        'FUEL QUAN - AUDIO=>TONE',
        'RETRO WARN - AUDIO=>TONE',
        'RETRO RESET - AUDIO=>TONE'
        ]

WarnAudioOffEvents = [
        'CABIN PRESS - AUDIO=>OFF',
        'O2 QUAN - AUDIO=>OFF',
        'O2 EMER - AUDIO=>OFF',
        'EXCESS SUIT H2O - AUDIO=>OFF',
        'EXCESS CABIN H2O - AUDIO=>OFF',
        'FUEL QUAN - AUDIO=>OFF',
        'RETRO WARN - AUDIO=>OFF',
        'RETRO RESET - AUDIO=>OFF'
        ]

MainPanelFuseOffEvents = [
        'FUSE: SUIT FAN=>OFF',
        'FUSE: ENVIR CONTL=>OFF',
        'FUSE: RETRO JETT=>OFF',
        'FUSE: RETRO MAN=>OFF',
        'FUSE: PRO GRAMR=>OFF',
        'FUSE: BLOOD PRESS=>OFF'
        ]

MainPanelFuseOnEvents = [
        'FUSE: SUIT FAN=>ON',
        'FUSE: ENVIR CONTL=>ON',
        'FUSE: RETRO JETT=>ON',
        'FUSE: RETRO MAN=>ON',
        'FUSE: PRO GRAMR=>ON',
        'FUSE: BLOOD PRESS=>ON'
        ]


def makeFifo(fifoName):
    ''' Create the fifo if it doesn't already exist '''
    try:
        os.mkfifo(fifoName)
    except OSError as oe: 
        if oe.errno != errno.EEXIST:
            raise


def handleSwitchEvent(event):
    eventName = event['eventName']

    if eventName == 'TIME ZERO=>pressed':
        startMission()
    elif eventName == 'BLOOD PRESS - STOP=>pressed':
        stopAudio()
    elif eventName == 'FUSE: SUIT FAN=>ON':
        runSequencer(0.5)
    elif eventName == 'LIGHT TEST=>ON':
        lightTest(on=True)
    elif eventName == 'LIGHT TEST=>OFF':
        lightTest(on=False)
    elif eventName == 'WARN LIGHTS=>DIM':
        setWarnLightsBrightness(bright=False)
    elif eventName == 'WARN LIGHTS=>BRIGHT':
        setWarnLightsBrightness(bright=True)
    elif eventName in WarnAudioToneEvents:
        processWarnAudioEvent(eventName, tone=True)
    elif eventName in WarnAudioOffEvents:
        processWarnAudioEvent(eventName, tone=False)
    elif eventName in MainPanelFuseOnEvents:
        processMainPanelFuseEvents(eventName, state=True)
    elif eventName in MainPanelFuseOffEvents:
        processMainPanelFuseEvents(eventName, state=False)
    elif eventName == 'INLET VALVE PWR=>BYPASS':
        setLight('ABORT', True)
    elif eventName == 'INLET VALVE PWR=>NORM':
        setLight('ABORT', False)
    elif eventName == 'ISOL BTRY=>STBY':
        setLight('STBY AC-AUTO', True)
    elif eventName == 'ISOL BTRY=>NORM':
        setLight('STBY AC-AUTO', False)
    else:
        print '*** WARNING: Unhandled event name: ' + eventName


def lightTest(on):
    ''' Turn on or off all lights '''
    message = { 'type': 'LOGICAL', 'target': 'all', 'action': 'off', 'intensity': Intensity }
    if on:
        message['action'] = 'on'

    sendLightCommand(message)


def setWarnLightsBrightness(bright):
    ''' Set the brightness of the main panel warning lights to DIM or BRIGHT for lights already on '''
    global WarnIntensity

    if bright:
        WarnIntensity = BRIGHT
    else:
        WarnIntensity = DIM

    for target in WarnLightsState.keys():
        if WarnLightsState[target]:
            message = { 'type': 'LOGICAL', 'target': target, 'action': 'on', 'intensity': WarnIntensity }
            sendLightCommand(message)


def processWarnAudioEvent(eventName, tone):
    lightLabel = eventName.split(' - ')[0]
    message = { 'type': 'LOGICAL', 'target': lightLabel, 'action': 'off', 'intensity': WarnIntensity }
    if tone:
        message['action'] = 'on'
        WarnLightsState[lightLabel] = True
    else:
        WarnLightsState[lightLabel] = False

    sendLightCommand(message)


def processMainPanelFuseEvents(eventName, state):
    lightLabel = 'ABORT'
    message = { 'type': 'LOGICAL', 'target': lightLabel, 'action': 'off', 'intensity': Intensity }
    if state:
        message['action'] = 'on'

    sendLightCommand(message)


def startAudio():
    audioFile = '/home/pi/mercury/src/audio/mp3s/ma-6-audio-1.mp3'
    args = ['omxplayer', '--no-keys', audioFile]
    # preexec_fn is needed so that we can later kill by process group
    global AudioProcess
    stopAudio()
    AudioProcess = subprocess.Popen(args, preexec_fn=os.setsid)


def stopAudio():
    global AudioProcess
    if AudioProcess is not None:
        os.killpg(os.getpgid(AudioProcess.pid), signal.SIGTERM)  # Send the signal to all the process groups
        AudioProcess = None


def startMission():
    startAudio()

    startDelay = 1.0  # Initial delay from button press (in seconds)
    # Function args must be a sequence type. Therefore, if passing only a single
    # arg, be careful to add a comma so that Python knows it is a sequence.
    # E.g., use (True,) and not (True).
    # List of lists. Inner list: deltaTime in seconds, function, function args list
    sequence = [
                   [0.0,    lightTest, (True,)],
                   [0.3,    lightTest, (False,)],
                   [0.35,   setSequenceLight, ('JETT TOWER', 'red')],
                   [0.45,   setSequenceLight, ('JETT TOWER', 'off')],
                   [0.5,    setSequenceLight, ('JETT TOWER', 'green')],
                   [1.0,    setSequenceLight, ('SEP CAPSULE', 'red')],
                   [1.4,    setSequenceLight, ('SEP CAPSULE', 'off')],
                   [1.5,    setSequenceLight, ('SEP CAPSULE', 'green')],
                   [2.0,    setSequenceLight, ('JETT TOWER', 'off')],
                   [2.5,    flashLight, ('ABORT', 0.1, 0.1, 10)],
                   [4.0,    lightTest, (True,)],
                   [6.0,    lightTest, (False,)],
                   [8.0,    runSequencer, (0.5,) ],
                   [10.2,   runAlarmSequence, (0.5,) ],
                   [14.0,   flashLight, ('CABIN PRESS', 0.5, 0.2, 100)],
                   [30.0,   setSequenceLight, ('LANDING BAG', 'off')],
                   [30.5,   setSequenceLight, ('LANDING BAG', 'red')],
            ]

    for event in sequence:
        Timer(startDelay+event[0], event[1], event[2]).start()


def flashLight(light, onTime, offTime, count):
    et = 0
    for i in range(count):
        Timer(et, setLight, (light, True)).start()
        et += onTime
        Timer(et, setLight, (light, False)).start()
        et += offTime


def runAlarmSequence(delay):
    alarmLights = [
            'CABIN PRESS',
            'O2 QUAN',
            'O2 EMER',
            'EXCESS SUIT H2O',
            'EXCESS CABIN H2O',
            'FUEL QUAN',
            'RETRO WARN',
            'RETRO RESET',
            'STBY AC-AUTO'
            ]

    et = 0
    for light in alarmLights:
        Timer(et, setLight, (light, True)).start()
        et += delay
        Timer(et, setLight, (light, False)).start()
        et += delay


def runSequencer(delay):
    sequenceLights = [
            'JETT TOWER',
            'SEP CAPSULE',
            'RETRO SEQ',
            'RETRO ATT',
            'FIRE RETRO',
            'JETT RETRO',
            'RETRACT SCOPE',
            '.05G',
            'MAIN',
            'LANDING BAG',
            'RESCUE'
            ]
    et = 0
    for light in sequenceLights:
        Timer(et, setSequenceLight, (light, 'red')).start()
        et += delay
        Timer(et, setSequenceLight, (light, 'off')).start()
        Timer(et, setSequenceLight, (light, 'green')).start()
        et += delay


def setSequenceLight(light, color):
    message = { 'type': 'LOGICAL', 'target': light, 'action': 'off', 'intensity': Intensity }
    if color != 'off':
        message['action'] = 'on'
        message['subtarget'] = color

    sendLightCommand(message)


def setLight(light, state):
    message = { 'type': 'LOGICAL', 'target': light, 'action': 'off', 'intensity': Intensity }
    if state:
        message['action'] = 'on'

    sendLightCommand(message)


def sendLightCommand(message):
    ''' Send a command to the lights controller FIFO '''
    # Newline makes it possible to use readline on the other size so that I have a good message boundary
    buff = json.dumps(message) + '\n'
    LightsFp.write(buff)
    LightsFp.flush()


############
# Main
############

makeFifo(SwitchesFIFO)
makeFifo(LightsFIFO)

# Open and writes will block if no reader on fifo (or if full)
LightsFp = open(LightsFIFO, 'w')

# Open will block until there is a writer and a message is written
with open(SwitchesFIFO, 'r') as switchesFp:
    while True:
        # This does not block. Will return 0 if nothing to read
        mesg = switchesFp.readline()
        if len(mesg) > 0:
            event = json.loads(mesg)
            print(json.dumps(event, indent=4))
            handleSwitchEvent(event)
        else:
            # Could go off and do other things here...
            pass

LightsFp.close()
