# TODO: TEST

import subprocess

# activate the environment
result = subprocess.run(['.\source\repos\hidex_module\.venv\Scripts\activate'], shell=True, capture_output=True, text=True)
print(result.stdout)

# start the node
result = subprocess.run(['python .\source\repos\hidex_module\src\hidex_rest_node.py --port 2005 --output_path "C:\\Users\\RPL\\Documents\\HidexData"'], shell=True, capture_output=True, text=True)
print(result.stdout)