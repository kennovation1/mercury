import os
import subprocess
import signal
from time import sleep

audioFile = 'mp3s/ma-6-audio-1.mp3'
args = ['omxplayer', '--no-keys', 'mp3s/ma-6-audio-1.mp3']
p = subprocess.Popen(args, preexec_fn=os.setsid)
print 'Started'
sleep(5)
os.killpg(os.getpgid(p.pid), signal.SIGTERM)  # Send the signal to all the process groups
