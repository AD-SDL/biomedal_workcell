""" Python script to start the Inheco FastAPI server and WEI nodes for each Inheco single plate incubator device in new terminal windows """

# TODO: TEST

import subprocess

# FastAPI Server ------------------------------------------
subprocess.Popen(
    'start "Inheco FastAPI Server" cmd /K ".\\source\\repos\\inheco_incubator_module\\.venv\\Scripts\\activate & python .\\source\\repos\\inheco_incubator_module\\src\\inheco_interface_FastAPI_wrapper.py --host "127.0.0.1" --device "COM5" --port 7000 --dll_path "C:\\Program Files\\INHECO\\Incubator-Control\\ComLib.dll"', 
    shell=True
)

# Device @ Stack Floor 0 -----------------------------------
subprocess.Popen(
    'start "Inheco SF0 BOTTOM" cmd /K ".\\source\\repos\\inheco_incubator_module\\.venv\\Scripts\\activate & python .\\source\\repos\\inheco_incubator_module\\src\\inheco_incubator_module.py --port 3005 --device_id 2 --stack_floor 0 --interface_host "localhost" --interface_port 7000', 
    shell=True
)

# Device @ Stack Floor 1 -----------------------------------
subprocess.Popen(
    'start "Inheco SF1 TOP" cmd /K ".\\source\\repos\\inheco_incubator_module\\.venv\\Scripts\\activate & python .\\source\\repos\\inheco_incubator_module\\src\\inheco_incubator_module.py --port 3006 --device_id 2 --stack_floor 1 --interface_host "localhost" --interface_port 7000', 
    shell=True
)


# might be able to open them all as tabs in the same terminal window
# TODO: experiment with this

# import subprocess

# # Shared paths
# venv_activate = ".\\source\\repos\\inheco_incubator_module\\.venv\\Scripts\\activate"
# interface_script = ".\\source\\repos\\inheco_incubator_module\\src\\inheco_interface_FastAPI_wrapper.py"
# device_script = ".\\source\\repos\\inheco_incubator_module\\src\\inheco_incubator_module.py"

# # Build each command as a Windows Terminal tab
# commands = [
#     f'new-tab -p "Command Prompt" --title "Inheco FastAPI Server" cmd /k "{venv_activate} & python {interface_script} --host 0.0.0.0 --device COM5 --port 7000 --dll_path \\"C:\\Program Files\\INHECO\\Incubator-Control\\ComLib.dll\\""',
    
#     f'; new-tab -p "Command Prompt" --title "Inheco SF0 BOTTOM" cmd /k "{venv_activate} & python {device_script} --port 3005 --device_id 2 --stack_floor 0 --interface_host localhost --interface_port 7000"',
    
#     f'; new-tab -p "Command Prompt" --title "Inheco SF1 TOP" cmd /k "{venv_activate} & python {device_script} --port 3006 --device_id 2 --stack_floor 1 --interface_host localhost --interface_port 7000"'
# ]

# # Combine the commands into one `wt` call
# full_command = 'wt ' + ''.join(commands)

# # Launch
# subprocess.Popen(full_command, shell=True)