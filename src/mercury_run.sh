# Run the processes to control lights and read switches
# Each listens to and writes to named piped (FIFOs)
# Then run controller process (funbox) that reads switches and controls lights
# by reading and writing the respective FIFOs
python /home/pi/mercury/src/lightOutputs/lightcontroller.py &
python /home/pi/mercury/src/gauges/gauge_controller.py &
python /home/pi/mercury/src/switchInputs/readswitches.py -f &
python /home/pi/mercury/src/controllers/funbox.py &
