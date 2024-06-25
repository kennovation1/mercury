- Copy gauges.html to /var/www/html
- View using:
  -  http://192.168.1.12/gauges.html

# TODO
- Decide what/where to print or not print
- Consider resilient retry logic in controller, gauges, and html to allow for restarts and async startups

# Kiosk mode
- Use "Guided Access" mode as an easy solution
- iPhone 7 instructions (iOS 13.5)
  - Settings > Accessibility > Guided Access > On
  - Don't set a passcode
  - Display Auto-Lock > Never
- Open Safari and triple click home to enable
  - Start
  - Enter 123456 as passcode (I thought that this was disabled?)
  - Triple click Home to exit guided access mode
