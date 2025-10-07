""" Python script to start a WEI node for the Hidex Sense plate reader in a new terminal window """

# TODO: TEST

import subprocess

subprocess.Popen(
    'start "Hidex Plate Reader" cmd /K ".\\source\\repos\\hidex_module\\.venv\\Scripts\\activate & python .\\source\\repos\\hidex_module\\src\\hidex_rest_node.py --port 2005 --output_path "C:\\Users\\RPL\\Documents\\HidexData""', 
    shell=True
)
