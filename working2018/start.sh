cd lightOutputs/
nohup python lightcontroller.py &
cd ../switchInputs/
nohup python readswitches.py -f &
cd ../controllers/
nohup python funbox.py &
