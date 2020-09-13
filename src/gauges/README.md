- Copy gauges.html to /var/www/html
- View using:
  -  http://192.168.1.12/gauges.html

# TODO
- Figure out why funbox.py would work with gauge_controller.py even though controller_test.py does work.

- Decide what/where to print or not print
- Consider resilient retry logic in controller, gauges, and html to allow for restarts and async startups
