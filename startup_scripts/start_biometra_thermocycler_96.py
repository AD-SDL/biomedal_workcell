"""
General Notes: 
- use the 'adding_python' branch of the biometra module 
- use wei 0.6.2

# TODO: Write bash
# NOTE: this python script works :) 

"""
import subprocess

subprocess.Popen(
    'start "Biometra TRobotII Thermocycler" cmd /K "C:\\Users\\RPL\\source\\repos\\biometra_module\\.venv\\Scripts\\activate & python C:\\Users\\RPL\\source\\repos\\biometra_module\\src\\biometra_rest_node.py --host "0.0.0.0" --port 2008"', 
    shell=True
)


