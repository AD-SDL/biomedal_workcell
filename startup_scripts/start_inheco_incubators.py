# TODO: TEST 
# TODO: Separate these each into separate terminals

import subprocess

# FastAPI Server ------------------------------------------
# activate the environment
result = subprocess.run(['.\source\repos\inheco_incubator_module\.venv\Scripts\activate'], shell=True, capture_output=True, text=True)
print(result.stdout)

# start the node
result = subprocess.run(['python .\source\repos\inheco_incubator_module\src\inheco_interface_FastAPI_wrapper.py --host "0.0.0.0" --device "COM5" --port 7000 --dll_path "C:\\Program Files\\INHECO\\Incubator-Control\\ComLib.dll"'], shell=True, capture_output=True, text=True)
print(result.stdout)


# Device @ Stack Floor 0 -----------------------------------
# activate the environment
result = subprocess.run(['.\source\repos\inheco_incubator_module\.venv\Scripts\activate'], shell=True, capture_output=True, text=True)
print(result.stdout)

# start the node
result = subprocess.run(['python .\source\repos\inheco_incubator_module\src\inheco_incubator_module.py --port 3005 --device_id 2 --stack_floor 0 --interface_host "localhost" --interface_port 7000'], shell=True, capture_output=True, text=True)
print(result.stdout)


# Device @ Stack Floor 1 -----------------------------------
# activate the environment
result = subprocess.run(['.\source\repos\inheco_incubator_module\.venv\Scripts\activate'], shell=True, capture_output=True, text=True)
print(result.stdout)

# start the node
result = subprocess.run(['python .\source\repos\inheco_incubator_module\src\inheco_incubator_module.py --port 3006 --device_id 2 --stack_floor 1 --interface_host "localhost" --interface_port 7000'], shell=True, capture_output=True, text=True)
print(result.stdout)