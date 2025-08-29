""" Python script to start a WEI node for the BMG plate reader in a new terminal window """

# TODO: TEST

import subprocess

subprocess.Popen(
    'start "BMG Plate Reader" cmd /K ".\\source\\repos\\bmg_module\\.venv\\Scripts\\activate & python C:\\Users\\RPL\\AppData\\Local\\Programs\\Python\\Python312-32\\python.exe .\\source\\repos\\bmg_module\\src\\bmg_rest_node.py --port 3003"', 
    shell=True
)

