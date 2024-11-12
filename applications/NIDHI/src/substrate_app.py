#!/usr/bin/env python3
"""Experiment application for Chris and Nidhi's substrate experiment"""

from pathlib import Path

#from wei import ExperimentClient


def main() -> None:
    """Runs the Substrate Experiment Application"""

    # Define the Experiment object that will communicate with the WEI server
    #exp = ExperimentClient("localhost", "8000", "Substrate_Experiment")

    # Specify the paths to the Workflow definition yaml file
    app_directory = Path(__file__).parent.parent
    wf_directory = app_directory / "workflows"
    protocol_directory = app_directory / "protocols"

    run_ot2_wf = wf_directory / "run_ot2_wf.yaml"
    incubate_read_and_replace_wf = wf_directory / "incubate_read_and_replace_wf.yaml"
    get_new_substrate_plate_wf = wf_directory / "get_new_substrate_plate.yaml"
    

    plate_prep_and_first_inoculation_protocol = protocol_directory / "plate_prep_first_inoculation.py"
    inoculate_within_plate_protocol = protocol_directory / "inoculate_within_plate.yaml"
    inoculate_between_plate_protocol = protocol_directory / "inoculate_between_plates.yaml"

    # important variables 
    loop_num = 0
    total_loops = 24
    incubation_time = 86400 # 86400 seconds = 24 hours 
    
    # initial payload setup
    payload = {
        "current_ot2_protocol": plate_prep_and_first_inoculation_protocol,

        "assay_plate_ot2_replacement_location": "ot2bioalpha.deck1"
    }
    
    
    # RUN THE EXPERIMENT

    # 1.) Human loads the ot-2 deck with the correct labware

    while loop_num < total_loops: 
        # add current loop_num variable to payload
        payload["loop_num"] = loop_num

        if loop_num == 0:   # very first cycle 
            # 2.) Run first OT-2 protocol with the OT-2 running workflow 
            #        --> Dispense 150uL from substrate columns into each well of 6 substrate plates (OT-2 pos 1,7,8,9,10,11)
            #        --> Inoculate the first substrate plate (OT-2 position 1)

            # exp.start_run(
            #     run_ot2_wf.resolve(),
            #     payload=payload,
            #     blocking=True,
            #     simulate=False,
            # )

            print("RUNNING FIRST OT2 PROTOCOL")

        else: # if not the very first cycle

            # determine inoculation columns based on loop number and add to payload
            source_well_list, destination_well_list = determine_inoculation_columns(loop_num)
            payload["source_wells_list"] = source_well_list
            payload["destination_wells_list"] = destination_well_list
            
            # TESTING
            print("*********************")

            if not loop_num % 4 == 0: 
                # change current ot2 protocol to within plate transfer
                payload["current_ot2_protocol"] = inoculate_within_plate_protocol
                print("WITHIN PLATE TRANSFER")

            else: 
                # change the current ot2 protocol to a between plate transfer
                payload["current_ot2_protocol"] = inoculate_within_plate_protocol
                print("BETWEEN PLATE TRANSFER")

                # TODO: make sure that the old assay plate was placed on position 3
                # TODO: Get a new substrate assay plate from the stack




                
            
            # Run the current ot2 protocol (either within or between plate transfer)
                # exp.start_run(
                #     run_ot2_wf.resolve(),
                #     payload=payload,
                #     blocking=True,
                #     simulate=False,
                # )

        

        



        # 3.) Replace lid, transfer to BMG, read/incubate, then replace onto OT-2
            # exp.start_run(
            #     incubate_read_and_replace_wf.resolve(),
            #     payload=payload,
            #     blocking=True,
            #     simulate=False,
            # )


        # increase the loop number when cycle is complete
        loop_num += 1




def determine_inoculation_columns(loop_num): 
    """determine_inoculation_columns

    Description: determines source and destination columns for inoculations based on the loop number

    Args: 
        loop_num (int) = loop number or current cycle number 

    Returns: 
        source_wells ([str]): String list of source wells
        destination_wells ([str]) String list of destination wells

    Notes:
        loop_num % 4 = 1
            source_columns = [1,5,9]
            destination_columns = [2,6,10]
        loop_num % 4 = 2
            source_columns = [2,6,10]
            destination_columns = [3,7,11]
        loop_num % 4 = 3
            source_columns = [3,7,11]
            destination_columns = [4,8,12]

        This means that...
            source_columns = [loop_num % 4, (loop_num % 4) + 4, (loop_num % 4) +8]
            destination_columns = [loop_num % 4, (loop_num % 4) + 4, (loop_num % 4) +8]

    TODOs: 
        - Protopiler has rows and columns switched for multichannel transfers currently. CHAOS!!!
  
    """
    print("DETERMINE INOCULATION COlUMNS CALLED")

    mod = loop_num % 4

    if mod == 0: 
        source_columns = [4,8,12]
        destination_columns = [1,5,9]

    else: 
        source_columns = [mod, mod + 4, mod + 8]
        destination_columns = [mod + 1, mod + 5, mod + 9]

    # TESTING
    print(source_columns)
    print(destination_columns)

    source_well_list = [[f"{row}{column}" for row in "ABCDEFGH"] for column in source_columns]
    destination_well_list = [[f"{row}{column}" for row in "ABCDEFGH"] for column in destination_columns]

    # TESTING
    print(source_well_list)
    print(destination_well_list)

    return source_well_list, destination_well_list

if __name__ == "__main__":
    main()

