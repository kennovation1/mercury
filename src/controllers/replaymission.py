# Test for scheduling events

# Environment: Python 2.7
  
import sched, time


s = sched.scheduler(time.time, time.sleep)


def setLed(led, state):
    print '{}: Setting LED {} {}'.format(time.time(), led, state)


def replayMission():
    eventTime = 1  # Event time in seconds from now
    s.enter(eventTime, 1, setLed, (123, 'ON'))

    eventTime += 0.3
    s.enter(eventTime, 1, setLed, (123, 'OFF'))
    s.enter(eventTime, 1, setLed, (456, 'ON'))
    s.run()


replayMission()
