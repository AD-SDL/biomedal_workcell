""" Python script to start WEI nodes for each of the Biometra TRobotII thermocyclers in separate terminal windows. 

NOTE: only the 96-well TRobotII is included in this script for now

other notes: 
- use the 'adding_python' branch of the biometra module 
- use wei 0.6.2

"""
# TODO: TEST
# TODO: include 384 thermocycler

import subprocess

subprocess.Popen(
    'start "Biometra TRobotII Thermocycler" cmd /K "C:\\Users\\RPL\\source\\repos\\biometra_module\\.venv\\Scripts\\activate & python C:\\Users\\RPL\\source\\repos\\biometra_module\\src\\biometra_rest_node.py --host "0.0.0.0" --port 2008"', 
    shell=True
)


