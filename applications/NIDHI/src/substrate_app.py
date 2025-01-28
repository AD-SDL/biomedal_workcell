#!/usr/bin/env python3
"""Experiment application for Chris and Nidhi's substrate experiment"""

from pathlib import Path

from wei import ExperimentClient
from wei.types.experiment_types import CampaignDesign, ExperimentDesign

"""
TODOs: 



"""


def main() -> None:
    """Runs the Substrate Experiment Application"""

    # INITIAL EXPERIMENT SETUP
    # define the ExperimentDesign object that will be used to register the experiment
    experiment_design = ExperimentDesign(
        experiment_name="Substrate_Experiment",
        experiment_description="Experiment application for the adaptive evolution to substrates experiment",
    )
    # define a campaign object (useful if we want to group many of these substrate experiments together)
    campaign = CampaignDesign(
        campaign_name="Substrate_Campaign",
        campaign_description="Campaign to collect substrate experiments",
    )
    # define the experiment client object that will communicate with the WEI server
    experiment_client = ExperimentClient(
        server_host="localhost",
        server_port="8000",
        experiment=experiment_design,
        campaign=campaign,
    )


    # DEFINING PATHS AND VARIABLES
    # directory paths
    app_directory = Path(__file__).parent.parent
    wf_directory = app_directory / "workflows"
    wf_set_up_tear_down_directory = wf_directory / "set_up_tear_down"
    wf_run_instrument_directory = wf_directory / "run_instrument"
    wf_transfers_directory = wf_directory / "transfers"
    protocol_directory = app_directory / "protocols"

    # workflow paths (run instruments)
    run_ot2_wf = wf_run_instrument_directory / "run_ot2_wf.yaml"
    incubator_to_run_bmg_wf = wf_run_instrument_directory / "incubator_to_run_bmg_wf.yaml"
    bmg_to_run_incubator_wf = wf_run_instrument_directory / "bmg_to_run_incubator_wf.yaml"

    # workflow paths (set up and tear down related)
    tear_down_old_substrate_plate_wf = wf_set_up_tear_down_directory / "remove_old_substrate_plate_wf.yaml"
    incubate_read_and_replace_wf = wf_directory / "incubate_read_and_replace_wf.yaml"
    get_new_substrate_plate_wf = wf_set_up_tear_down_directory / "get_new_substrate_plate_wf.yaml"
    cleanup_wf = wf_set_up_tear_down_directory / "cleanup_wf.yaml"

    # workflow paths (pf400 transfers)
    remove_lid_move_to_ot2_wf = wf_transfers_directory / "remove_lid_move_to_ot2_wf.yaml"
    move_to_bmg_replace_lid_READ_wf = wf_transfers_directory / "move_to_bmg_replace_lid_READ_wf.yaml"
    
    # protocol paths (for OT-2)
    plate_prep_and_first_inoculation_protocol = protocol_directory / "plate_prep_first_inoculation.py"
    inoculate_within_plate_protocol = protocol_directory / "inoculate_within_plate.yaml"
    inoculate_between_plates_protocol = protocol_directory / "inoculate_between_plates.yaml"

    # important variables 
    loop_num = 0
    current_substrate_stack = 1
    current_substrate_plate_num = 1
    transfer_in_plate_number = 1
    # total_loops = 24
    total_loops=1 # TESTING
    # initial payload setup
    payload = {
        "current_ot2_protocol": str(plate_prep_and_first_inoculation_protocol),
        "current_substrate_stack": "tower_deck" + str(current_substrate_stack),
        "remove_lid_location": "lidnest_1_wide",
        "bmg_assay_name": "NIDHI", 
        "assay_plate_ot2_replacement_location": "ot2biobeta.deck1",
        # "assay_plate_lid_location": "lidnest1"
    }
    
    # RUN THE EXPERIMENT --------------------------------------------

    """ Human needs to set up OT-2 deck before run starts """

    while loop_num < total_loops: 

        #* SET UP ALL EXPERIMENTAL VARIABLES
        
        # add current loop_num variable to payload
        payload["loop_num"] = loop_num
        print(f"CURRENT LOOP #: {loop_num}")   # TESTING
        payload["bmg_data_output_name"] = f"{current_substrate_plate_num}_{transfer_in_plate_number}.txt"
        print(payload["bmg_data_output_name"])  # TESTING
        

        if loop_num == 0: # very first cycle 
            print("FIRST LOOP") # TESTING

            payload["use_existing_resources"] = False
            payload["current_ot2_protocol"] = str(plate_prep_and_first_inoculation_protocol) # TODO: Redundant

        else: # if not the very first cycle

            if loop_num == 1: 
                payload["use_existing_resources"] = False
            else: 
                payload["use_existing_resources"] = True
 
            if loop_num % 4 == 0: 
                # set current ot-2 transfer as BETWEEN plate transfer 
                print("BETWEEN PLATE TRANSFER")  # TESTING
                payload["current_ot2_protocol"] = str(inoculate_between_plates_protocol)
                current_substrate_stack += 1
                payload["current_substrate_stack"] = "tower_deck" + str(current_substrate_stack)

            else: 

                print("WITHIN PLATE TRANSFER")  # TESTING
                
                # set current OT-2 protocol as WITHIN plate transfer
                payload["current_ot2_protocol"] = str(inoculate_within_plate_protocol)

                # determine inoculation columns based on loop number and add to payload
                source_wells_list, destination_wells_list = determine_inoculation_columns(loop_num) 

                if loop_num % 4 == 3: 
                    # if completing the last within plate transfer for a substrate plate, place plate at old position on ot2 (deck 3)
                    payload["assay_plate_ot2_replacement_location"] = "ot2biobeta.deck3"
                    payload["remove_lid_location"] = "lidnest_2_wide"
                    
                else: 
                    # otherwise, place current substrate plate at deck 1 in the ot-2
                    payload["assay_plate_ot2_replacement_location"] = "ot2biobeta.deck1"
                    payload["remove_lid_location"] = "lidnest_1_wide"

                payload["source_wells_1"] = [source_wells_list[0]]
                payload["source_wells_2"] = [source_wells_list[1]]
                payload["source_wells_3"] = [source_wells_list[2]]

                payload["destination_wells_1"] = [destination_wells_list[0]]
                payload["destination_wells_2"] = [destination_wells_list[1]]
                payload["destination_wells_3"] = [destination_wells_list[2]]



        # # Run the current OT-2 protocol
        # experiment_client.start_run(
        #     run_ot2_wf.resolve(),
        #     payload=payload,
        #     blocking=True,
        #     simulate=False,
        # )

        # update variable for formatting bmg output filenames
        if loop_num % 4 == 3 and not loop_num == 0: 
            transfer_in_plate_number = 1
            current_substrate_plate_num += 1
        else:
            transfer_in_plate_number += 1


        



        # TESTING
        print(f"{payload}\n")


        """Note!!!: 
            Human needs to place lid from substrate plate at position 1 on lid_nest_1_wide before the following transfer!"""

        # Transfer to bmg for first reading (a custom transfer)  # TESTED, a couple calibration todos left
        # experiment_client.start_run(
        #     move_to_bmg_replace_lid_READ_wf.resolve(),
        #     payload=payload,
        #     blocking=True,
        #     simulate=False,
        # )

        # TODO: LOOP THESE TWO WORKFLOWS
        # Transfer from bmg to tekmatic incubator   # WORKING
        experiment_client.start_run(
            bmg_to_run_incubator_wf.resolve(),
            payload=payload,
            blocking=True,
            simulate=False,
        )

        # Transfer from bmg to tekmatic incubator   # TESTED, needs bmg calibration
        # experiment_client.start_run(
        #     incubator_to_run_bmg_wf.resolve(),
        #     payload=payload,
        #     blocking=True,
        #     simulate=False,
        # )

        # after loop is done, return to ot-2 at correct location   # TESTED, needs exchange height and lid nest calibration
        # experiment_client.start_run(
        #     remove_lid_move_to_ot2_wf.resolve(),
        #     payload=payload,
        #     blocking=True,
        #     simulate=False,
        # )
































        # # add current loop_num variable to payload
        # payload["loop_num"] = loop_num
        # print(f"CURRENT LOOP #: {loop_num}")   # TESTING

        # if loop_num == 0: # very first cycle 
        #     print("FIRST LOOP") # TESTING

        #     payload["use_existing_resources"] = False

        #     # Run first OT-2 workflow  
        #     experiment_client.start_run(
        #         str(run_ot2_wf),
        #         payload=payload,
        #         blocking=True,
        #         simulate=False,
        #     )

        # else: # if not the very first cycle

        #     if loop_num == 1: 
        #         payload["use_existing_resources"] = False
        #     else: 
        #         payload["use_existing_resources"] = True

        #     # set up variables 
        #     if loop_num % 4 == 0: 
        #         # set current ot-2 transfer as BETWEEN plate transfer 
        #         payload["current_ot2_protocol"] = str(inoculate_between_plates_protocol)

        #         print("BETWEEN PLATE TRANSFER")  # TESTING

        #         # run workflow to get a new substrate plate and place in onto OT-2
        #         experiment_client.start_run(
        #             get_new_substrate_plate_wf.resolve(),
        #             payload=payload,
        #             blocking=True,
        #             simulate=False,
        #         )
        #         current_substrate_stack += 1
        #         payload["current_substrate_stack"] = "Stack.deck" + str(current_substrate_stack)

        #     else: 

        #         print("WITHIN PLATE TRANSFER")  # TESTING
                
        #         # set current OT-2 protocol as WITHIN plate transfer
        #         payload["current_ot2_protocol"] = str(inoculate_within_plate_protocol)

        #         # determine inoculation columns based on loop number and add to payload
        #         source_wells_list, destination_wells_list = determine_inoculation_columns(loop_num) 

        #         if loop_num % 4 == 3: 
        #             # if completing the last within plate transfer for a substrate plate, place plate at old position on ot2 (deck 3)
        #             payload["assay_plate_ot2_replacement_location"] = "ot2biobeta.deck3"
        #             payload["assay_plate_lid_location"] = "lidnest2"
                    
        #         else: 
        #             # otherwise, place current substrate plate at deck 1 in the ot-2
        #             payload["assay_plate_ot2_replacement_location"] = "ot2biobeta.deck1"
        #             payload["assay_plate_lid_location"] = "lidnest1"

        #         payload["source_wells_1"] = [source_wells_list[0]]
        #         payload["source_wells_2"] = [source_wells_list[1]]
        #         payload["source_wells_3"] = [source_wells_list[2]]

        #         payload["destination_wells_1"] = [destination_wells_list[0]]
        #         payload["destination_wells_2"] = [destination_wells_list[1]]
        #         payload["destination_wells_3"] = [destination_wells_list[2]]

        #     # TESTING
        #     print(f"PAYLOAD: {payload}")

        #     # # run workflow to run the specified OT-2 protocol
        #     # experiment_client.start_run(
        #     #     run_ot2_wf.resolve(),
        #     #     payload=payload,
        #     #     blocking=True,
        #     #     simulate=False,
        #     # )












































            # # Clean up the old substrate plate if it was a between plate transfer
            #     # TODO: maybe do in parallel to first 30 min incubation?
            # if loop_num % 4 == 0:
            #     experiment_client.start_run(
            #     run_ot2_wf.resolve(),
            #     payload=payload,
            #     blocking=True,
            #     simulate=False,
            # )

        # -------------------------------------------------------------------------------
        # Run loop  
        #     # run workflow to collect plate from OT-2 and place into BMG plate reader 
        #     experiment_client.start_run(
        #         replace_lid_move_to_bmg_wf.resolve(),
        #         payload=payload,
        #         blocking=True,
        #         simulate=False,
        #     )

        #     # run workflow to start bmg readings and incubation cycles
        #     experiment_client.start_run(
        #         run_bmg_wf.resolve(),
        #         payload=payload,
        #         blocking=True,
        #         simulate=False,
        #     )            

        #     if loop_num % 4 == 0: 
        #         # TODO: have this run at the same time as the BMG readings/incubation
        #         # run workflow to collect the old assay plate used in the between plate inoculation
        #         experiment_client.start_run(
        #             remove_old_substrate_plate_wf.resolve(),
        #             payload=payload,
        #             blocking=True,
        #             simulate=False,
        #         )             

        #     # run workflow to transfer the substrate plate from the BMG to the OT-2 and prep for next inoculation
        #     experiment_client.start_run(
        #         move_to_ot2_remove_lid_wf.resolve(),
        #         payload=payload,
        #         blocking=True,
        #         simulate=False,
        #     )   

        #     # cleanup at the very end of the experiment
        #     if loop_num == total_loops - 1: 
        #         # run cleanup workflow
        #         experiment_client.start_run(
        #             cleanup_wf.resolve(),
        #             payload=payload,
        #             blocking=True,
        #             simulate=False,
        #         )   

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

    # return source_wells_dict, destination_wells_dict
    return source_well_list, destination_well_list

if __name__ == "__main__":
    main()

