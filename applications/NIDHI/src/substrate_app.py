#!/usr/bin/env python3
"""Experiment application for Chris and Nidhi's substrate experiment"""

from pathlib import Path

from wei import ExperimentClient


def main() -> None:
    """Runs the Substrate Experiment Application"""

    # Define the Experiment object that will communicate with the WEI server
    exp = ExperimentClient("localhost", "8000", "Substrate_Experiment")

    # Specify the paths to the Workflow definition yaml file
    app_directory = Path(__file__).parent.parent
    wf_directory = app_directory / "workflows"
    protocol_directory = app_directory / "protocols"

    run_ot2_workflow = wf_directory / "run_ot2_protocol.yaml"

    plate_prep_and_first_inoculation_protocol = protocol_directory / "plate_prep_first_inoculation.py"

    # important variables 
    loop_num = 0
    total_loops = 24
    incubation_time = 86400 # 86400 seconds = 24 hours 
    
    # initial payload setup
    payload = {
        "current_ot2_protocol": plate_prep_and_first_inoculation_protocol,
        "assay_plate_ot2_replacement_location": "1"
    }
    
    
    # RUN THE EXPERIMENT

    # 1.) Human loads the ot-2 deck with the correct labware
    
    # 2.) Run first OT-2 protocol with the OT-2 running workflow 
    #        --> Dispense 150uL from substrate columns into each well of 6 substrate plates (OT-2 pos 1,7,8,9,10,11)
    #        --> Innoculate the first substrate plate (OT-2 position 1)

    exp.start_run(
        run_ot2_workflow.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    # 3.) Run the 



if __name__ == "__main__":
    main()
