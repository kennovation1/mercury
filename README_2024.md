Notes from bringing Mercury back to life after years being idle.

- Current state is that init after boot works usually
  - If it doesn't work, a reboot fixes
- Added an HDMI 7" display, this also serves as audio output
  - 1024 x 600
- Set desktop wall paper
  - This did not work...
      - `export DISPLAY=:0`
      - `pcmanfm --set-wallpaper resources/Roll_Pitch_Yaw_Indicator.jpg --wallpaper-mode=fit`
- Desktop config
  - Connect USB mouse
  - Right click to get Desktop Preferences (or from Raspberry menu)
  - Set all paper to `/home/pi/mercury/resources/Roll_Pitch_Yaw_Indicator.jpg`
    - Set mode to "Fit"
  - Remove trash can icon from desktop


# Funbox buttons
- Button X starts LED sequence and plays audio Y
- Button X starts LED sequence and plays audio Y
- Button X starts LED sequence and plays audio Y
- Button X starts LED sequence and plays audio Y
- Light Test (bottom left) turns on all and then all off
- X-Y turns on telelight
- Z sets telelight intensity
- Button X sets an LED sequence
- Button Z stop current sequence of lights and audio

# TODO
- Mount display
- Connect cable to enable touch input on display
- Think about how to push debug to screen
- Need to make knobs and pins more rigid
- Need to tighted all switch nuts
- Right O2 EMER LED is not working intermittently
- I needed to comment out guages in mercury_run.sh and in funbox.py
- Document button usage
- Would be nice to have a better light program with audio
- Should I try to fix gauges?
  - Use browser on 7" display?
