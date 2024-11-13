#!/usr/bin/env python3
"""Experiment application for Chris and Nidhi's substrate experiment"""

from pathlib import Path

from wei import ExperimentClient


def main() -> None:
    """Runs the Substrate Experiment Application"""

    # define the experiment object that will communicate with the WEI server
    exp = ExperimentClient("localhost", "8000", "Substrate_Experiment")

    # directory paths
    app_directory = Path(__file__).parent.parent
    wf_directory = app_directory / "workflows"
    protocol_directory = app_directory / "protocols"

    # workflow paths
    run_ot2_wf = wf_directory / "run_ot2_wf.yaml"
    incubate_read_and_replace_wf = wf_directory / "incubate_read_and_replace_wf.yaml"
    replace_lid_move_to_bmg_wf = wf_directory / "replace_lid_move_to_bmg_wf.yaml"
    run_bmg_wf = wf_directory / "run_bmg_wf.yaml"
    move_to_ot2_remove_lid_wf = wf_directory / "move_to_ot2_remove_lid_wf.yaml"
    remove_old_substrate_plate_wf = wf_directory / "remove_old_substrate_plate_wf.yaml"
    get_new_substrate_plate_wf = wf_directory / "get_new_substrate_plate_wf.yaml"
    cleanup_wf = wf_directory / "cleanup_wf.yaml"

    # protocol paths (for OT-2)
    plate_prep_and_first_inoculation_protocol = protocol_directory / "plate_prep_first_inoculation.py"
    inoculate_within_plate_protocol = protocol_directory / "inoculate_within_plate.yaml"
    inoculate_between_plates_protocol = protocol_directory / "inoculate_between_plates.yaml"

    # important variables 
    loop_num = 0
    total_loops = 24
    
    # initial payload setup
    payload = {
        "current_ot2_protocol": plate_prep_and_first_inoculation_protocol,
        "assay_plate_ot2_replacement_location": "ot2biobeta.deck1",
        "assay_plate_lid_location": "lidnest1"
    }
    
    # RUN THE EXPERIMENT --------------------------------------------

    """ Human needs to set up OT-2 deck before run starts """

    while loop_num < total_loops: 

        # add current loop_num variable to payload
        payload["loop_num"] = loop_num

        if loop_num == 0: # very first cycle 

            # Run first OT-2 workflow 
            exp.start_run(
                run_ot2_wf.resolve(),
                payload=payload,
                blocking=True,
                simulate=False,
            )

            # TESTING
            print("RUNNING FIRST OT2 PROTOCOL")

        else: # if not the very first cycle

            # set up variables 
            if loop_num % 4 == 0: 
                # set current ot-2 transfer as BETWEEN plate transfer 
                payload["current_ot2_protocol"] = inoculate_between_plates_protocol

                # run workflow to get a new substrate plate and place it onto OT-2
                exp.start_run(
                    get_new_substrate_plate_wf.resolve(),
                    payload=payload,
                    blocking=True,
                    simulate=False,
                )

            else: 
                # set current OT-2 protocol as WITHIN plate transffer
                payload["current_ot2_protocol"] = inoculate_within_plate_protocol

                # determine inoculation columns based on loop number and add to payload
                source_wells_list, destination_wells_list = determine_inoculation_columns(loop_num)
                payload["source_wells_list"] = source_wells_list
                payload["destination_wells_list"] = destination_wells_list

                if loop_num % 4 == 3: 
                    # if completing the last within plate transfer for a substrate plate, place plate at old position on ot2 (deck 3)
                    payload["assay_plate_ot2_replacement_location"] = "ot2biobeta.deck3"
                    payload["assay_plate_lid_location"] = "lidnest2"

                else: 
                    # otherwise, place current substrate plate at deck 1 in the ot-2
                    payload["assay_plate_ot2_replacement_location"] = "ot2biobeta.deck1"
                    payload["assay_plate_lid_location"] = "lidnest1"
                    
            # run workflow to run the specified OT-2 protocol
            exp.start_run(
                run_ot2_wf.resolve(),
                payload=payload,
                blocking=True,
                simulate=False,
            )

            # run workflow to collect plate from OT-2 and place into BMG plate reader 
            exp.start_run(
                replace_lid_move_to_bmg_wf.resolve(),
                payload=payload,
                blocking=True,
                simulate=False,
            )

            # run workflow to start bmg readings and incubation cycles
            exp.start_run(
                run_bmg_wf.resolve(),
                payload=payload,
                blocking=True,
                simulate=False,
            )            

            if loop_num % 4 == 0: 
                # TODO: have this run at the same time as the BMG readings/incubation
                # run workflow to collect the old assay plate used in the between plate inoculation
                exp.start_run(
                    remove_old_substrate_plate_wf.resolve(),
                    payload=payload,
                    blocking=True,
                    simulate=False,
                )             

            # run workflow to transfer the substrate plate from the BMG to the OT-2 and prep for next inoculation
            exp.start_run(
                move_to_ot2_remove_lid_wf.resolve(),
                payload=payload,
                blocking=True,
                simulate=False,
            )   

            # cleanup at the very end of the experiment
            if loop_num == total_loops - 1: 
                # run cleanup workflow
                exp.start_run(
                    cleanup_wf.resolve(),
                    payload=payload,
                    blocking=True,
                    simulate=False,
                )   

        # increase the loop number
        loop_num += 1



# HELPER FUNCTIONS
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

