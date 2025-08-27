"""
General Notes: 
- use the 'adding_python' branch of the biometra module 
- use wei 0.6.2

# TODO: Test

"""
import subprocess

# activate the environment
result = subprocess.run(['.\source\repos\biometra_module\.venv\Scripts\activate'], shell=True, capture_output=True, text=True)
print(result.stdout)

# start the node
result = subprocess.run(['python .\source\repos\biometra_module\src\biometra_rest_node.py, --host "0.0.0.0" --port 2008'], shell=True, capture_output=True, text=True)
print(result.stdout)




