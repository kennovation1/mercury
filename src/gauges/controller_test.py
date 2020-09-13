# Quick test to simulate the controller writing to the gauges pipe
import json
import os
import errno
from time import sleep

GaugesFIFO = '/tmp/gauge-commands'

def makeFifo(fifoName):
    ''' Create the fifo if it doesn't already exist '''
    try:
        os.mkfifo(fifoName)
    except OSError as oe: 
        if oe.errno != errno.EEXIST:
            raise


def setGauge(gauge, value):
    print('Setting gauge: {} = {}'.format(gauge, value))
    ''' Send a command to the gauges controller FIFO '''
    # Newline makes it possible to use readline on the other size so that I have a good message boundary
    message = {'gauge': gauge, 'value': value}
    buff = json.dumps(message) + '\n'
    GaugesFp.write(buff)
    GaugesFp.flush()


def initGauges():
    print('Initializing gauges')
    setGauge('LongAccel', 0)
    sleep(0.5)
    setGauge('Decent', 0)
    sleep(0.5)
    setGauge('Alt', 0)
    sleep(0.5)
    setGauge('CabinPressure', 14.7)
    sleep(0.5)
    setGauge('CabinAir', 80)
    sleep(0.5)
    setGauge('RelativeHumidity', 45)
    sleep(0.5)
    setGauge('CoolantQuantity', 70)
    sleep(0.5)
    setGauge('SteamTemp', 45)
    sleep(0.5)
    setGauge('DCVolts', 28)
    sleep(0.5)
    setGauge('DCAmps', 20)
    sleep(0.5)
    setGauge('ACVolts', 115)


############
# Main
############

makeFifo(GaugesFIFO)

# Open and writes will block if no reader on fifo (or if full)
GaugesFp = open(GaugesFIFO, 'w')

initGauges()

GaugesFp.close()
