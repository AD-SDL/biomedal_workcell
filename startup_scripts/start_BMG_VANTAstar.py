# TODO: TEST

import subprocess

# activate the environment
result = subprocess.run(['.\source\repos\bmg_module\.venv\Scripts\activate'], shell=True, capture_output=True, text=True)
print(result.stdout)

# start the node
result = subprocess.run(['C:\Users\RPL\AppData\Local\Programs\Python\Python312-32\python.exe .\source\repos\bmg_module\src\bmg_rest_node.py --port 3003'], shell=True, capture_output=True, text=True)
print(result.stdout)




