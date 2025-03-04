#!/usr/bin/env python3
"""Experiment application for Chris and Nidhi's substrate experiment"""

from pathlib import Path

from wei import ExperimentClient
from wei.types.experiment_types import CampaignDesign, ExperimentDesign


def main() -> None:
    """Runs the Substrate Experiment Application"""

    # INITIAL EXPERIMENT SETUP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

    # DEFININE PATHS AND VARIABLES ---------------------------------

    # capture the expriment ID
    experiment_id = experiment_client.experiment.experiment_id

    # directory paths
    app_directory = Path(__file__).parent.parent
    wf_directory = app_directory / "workflows"
    wf_set_up_tear_down_directory = wf_directory / "set_up_tear_down"
    wf_run_instrument_directory = wf_directory / "run_instrument"
    wf_transfers_directory = wf_directory / "transfers"
    protocol_directory = app_directory / "protocols"

    # workflow paths (run instruments)
    run_ot2_wf = wf_run_instrument_directory / "run_ot2_wf.yaml"
    incubator_to_run_bmg_wf = (
        wf_run_instrument_directory / "incubator_to_run_bmg_wf.yaml"
    )
    bmg_to_run_incubator_wf = (
        wf_run_instrument_directory / "bmg_to_run_incubator_wf.yaml"
    )

    # workflow paths (set up and tear down related)
    get_new_substrate_plate_wf = (
        wf_set_up_tear_down_directory / "get_new_substrate_plate_wf.yaml"
    )
    remove_old_substrate_plate_wf = (
        wf_set_up_tear_down_directory / "remove_old_substrate_plate_wf.yaml"
    )

    # workflow paths (pf400 transfers)
    switch_lid_move_to_ot2_wf = (
        wf_transfers_directory / "switch_lid_move_to_ot2_wf.yaml"
    )
    move_to_bmg_switch_lid_read_wf = (
        wf_transfers_directory / "move_to_bmg_switch_lid_read_wf.yaml"
    )

    # protocol paths (for OT-2)
    plate_prep_and_first_inoculation_protocol = (
        protocol_directory / "plate_prep_first_inoculation.py"
    )
    inoculate_within_plate_protocol = protocol_directory / "inoculate_within_plate.yaml"
    inoculate_between_plates_protocol = (
        protocol_directory / "inoculate_between_plates.yaml"
    )

    # important variables
    loop_num = 0
    current_substrate_stack = 1
    current_substrate_plate_num = 1
    transfer_in_plate_number = 1
    reading_number_in_column = 1

    total_loops = 20  # CHANGED TO 20 TO USE 5 plates instead of 6!!!! 24 outer loops in full experiment

    # initial payload setup
    payload = {
        "current_ot2_protocol": str(plate_prep_and_first_inoculation_protocol),
        "current_substrate_stack": "tower_deck" + str(current_substrate_stack),
        "current_stack_safe_path": "safe_path_tower_deck"
        + str(current_substrate_stack),
        "remove_lid_location": "lidnest_1_wide",
        "remove_lid_safe_path": "safe_path_lidnest_1",
        "bmg_assay_name": "NIDHI",
        "assay_plate_ot2_replacement_location": "ot2biobeta_deck1",
    }

    # EXPERIMENT LOOP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    """ Human needs to set up OT-2 deck before run starts """

    while loop_num < total_loops:
        # SET UP ALL EXPERIMENTAL VARIABLES ------------------------
        payload["loop_num"] = loop_num
        payload["bmg_data_output_name"] = (
            f"{experiment_id}_{current_substrate_plate_num}_{transfer_in_plate_number}_{reading_number_in_column}.txt"
        )
        print(f"\nCURRENT LOOP #: {loop_num}")  # HELPFUL PRINT

        # If very first cycle, set variables for running the initial ot-2 protocol
        if loop_num == 0:
            payload["use_existing_resources"] = False
            payload["current_ot2_protocol"] = str(
                plate_prep_and_first_inoculation_protocol
            )

        # If it's not the very first cycle, set variables depending on loop number % 4
        else:
            # Keep track of OT-2 tip usage after loop number 1 (2nd OT-2 protocol)
            if loop_num == 1:
                payload["use_existing_resources"] = False
            else:
                payload["use_existing_resources"] = True

            # Set variables for a BETWEEN plate transfer every 4th round (when loop num % 0 == 4)
            # This means we've used up all columns in one substrate plate and now need to inoculate between substrate plates into a new substrate plate
            if loop_num % 4 == 0:
                payload["current_ot2_protocol"] = str(inoculate_between_plates_protocol)
                payload["assay_plate_ot2_replacement_location"] = "ot2biobeta_deck1"
                payload["remove_lid_location"] = "lidnest_1_wide"
                payload["remove_lid_safe_path"] = "safe_path_lidnest_1"
                print("BETWEEN PLATE TRANSFER")  # HELPFUL PRINT

            # If loop num % 4 is not 0, we are innoculating using columns in the same plate (WITHIN PLATE TRANSFER)
            else:
                payload["current_ot2_protocol"] = str(inoculate_within_plate_protocol)
                print("WITHIN PLATE TRANSFER")  # HELPFUL PRINT

                # determine inoculation columns based on loop number and add to payload
                source_wells_list, destination_wells_list = (
                    determine_inoculation_columns(loop_num)
                )
                payload["source_wells_1"] = [source_wells_list[0]]
                payload["source_wells_2"] = [source_wells_list[1]]
                payload["source_wells_3"] = [source_wells_list[2]]
                payload["destination_wells_1"] = [destination_wells_list[0]]
                payload["destination_wells_2"] = [destination_wells_list[1]]
                payload["destination_wells_3"] = [destination_wells_list[2]]

                if loop_num % 4 == 3:
                    # set variables to replace completely used substrate plate on ot2 deck 3 in preparation for next between plate transfer
                    payload["assay_plate_ot2_replacement_location"] = "ot2biobeta_deck3"

                else:
                    # Otherwise, set default to return substrate plate to ot2 deck 1 for prep for next within plate transfer, also set to use lid nest 1
                    payload["assay_plate_ot2_replacement_location"] = "ot2biobeta_deck1"
                    payload["remove_lid_location"] = "lidnest_1_wide"
                    payload["remove_lid_safe_path"] = "safe_path_lidnest_1"

        # DEBUG PRINT
        # print(f"Payload before run: {payload}\n")

        # RUN THE EXPERIMENTAL WORKFLOWS ----------------------------------------

        # Run the current OT-2 protocol
        if not loop_num == 0:  # ADDED FOR 2ND RUN (CHANGE FOR FUTURE RUNS!!!!!!)
            print(
                f"Running OT2 protoccol: {payload['current_ot2_protocol']}"
            )  # HELPFUL PRINT
            experiment_client.start_run(
                run_ot2_wf.resolve(),
                payload=payload,
                blocking=True,
                simulate=False,
            )

        # Remove an old/used substrate plate from ot2 deck 3 if necessary
        if loop_num % 4 == 0 and not loop_num == 0:
            print(
                f"Removing old substrate plate to: {payload['current_substrate_stack']} using {payload['current_stack_safe_path']}"
            )  # HELPFUL PRINT
            experiment_client.start_run(
                remove_old_substrate_plate_wf.resolve(),
                payload=payload,
                blocking=True,
                simulate=False,
            )
            # Update variables to reflect the used tower location
            current_substrate_stack += 1
            payload["current_substrate_stack"] = "tower_deck" + str(
                current_substrate_stack
            )
            payload["current_stack_safe_path"] = "safe_path_tower_deck" + str(
                current_substrate_stack
            )

        # Transfer from ot2 deck 1 to bmg, replacing the lid in the process, and take first absorbance reading
        print(
            f"Moving to bmg, replacing lid FROM {payload['remove_lid_location']} using {payload['remove_lid_safe_path']}, and reading, bmg output file name: {payload['bmg_data_output_name']}"
        )  # HELPFUL PRINT
        experiment_client.start_run(
            move_to_bmg_switch_lid_read_wf.resolve(),
            payload=payload,
            blocking=True,
            simulate=False,
        )
        # Set up variables for next absorbance reading
        reading_number_in_column += 1
        payload["bmg_data_output_name"] = (
            f"{experiment_id}_{current_substrate_plate_num}_{transfer_in_plate_number}_{reading_number_in_column}.txt"
        )

        # INNER LOOP
        for i in range(21):  # T21 inner loops in full experiment
            # Transfer from bmg to tekmatic incubator and incubate
            print("---> Moving to tekmatic and incubating")  # HELPFUL PRINT
            experiment_client.start_run(
                bmg_to_run_incubator_wf.resolve(),
                payload=payload,
                blocking=True,
                simulate=False,
            )

            # Transfer from tekmatic incubator to bmg and take an absorbance reading
            print(
                f"---> Moving to bmg and reading, bmg output file name: {payload['bmg_data_output_name']}"
            )  # HELPFUL PRINT
            experiment_client.start_run(
                incubator_to_run_bmg_wf.resolve(),
                payload=payload,
                blocking=True,
                simulate=False,
            )
            # Set up variables for next absorbance reading
            reading_number_in_column += 1
            payload["bmg_data_output_name"] = (
                f"{experiment_id}_{current_substrate_plate_num}_{transfer_in_plate_number}_{reading_number_in_column}.txt"
            )

        # If we've completed all absorbance readings on the last columns of a substrate plate, set variables to replace the lid at the old substrate plate lid location (lid nest 2)
        if loop_num % 4 == 3:
            payload["remove_lid_location"] = "lidnest_2_wide"
            payload["remove_lid_safe_path"] = "safe_path_lidnest_2"

        # After readings and incubations are complete, return the substrate plate to OT-2 at correct location (deck 1 if columns remaining, deck 3 if all columns used)
        print(
            f"Returning plate to OT-2 deck: {payload['assay_plate_ot2_replacement_location']}, returning lid TO {payload['remove_lid_location']} using {payload['remove_lid_safe_path']}"
        )  # HELPFUL PRINT
        experiment_client.start_run(
            switch_lid_move_to_ot2_wf.resolve(),
            payload=payload,
            blocking=True,
            simulate=False,
        )

        # Get a new (unused) substrate from the stack if necessary
        if (
            loop_num % 4 == 3 and not loop_num == total_loops - 1
        ):  # new substrate plate not needed on the last round
            print(
                f"Getting a new substrate plate from stack: {payload['current_substrate_stack']} using {payload['current_stack_safe_path']}"
            )  # HELPFUL PRINT
            experiment_client.start_run(
                get_new_substrate_plate_wf.resolve(),
                payload=payload,
                blocking=True,
                simulate=False,
            )

        # Format remaining variables for the next round
        reading_number_in_column = 1

        if loop_num % 4 == 3 and not loop_num == 0:
            transfer_in_plate_number = 1
            current_substrate_plate_num += 1
        else:
            transfer_in_plate_number += 1

        # Increase the loop number
        loop_num += 1


# HELPER FUNCTION(S) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

    """
    mod = loop_num % 4

    if mod == 0:
        source_columns = [4, 8, 12]
        destination_columns = [1, 5, 9]

    else:
        source_columns = [mod, mod + 4, mod + 8]
        destination_columns = [mod + 1, mod + 5, mod + 9]

    source_well_list = [
        [f"{row}{column}" for row in "ABCDEFGH"] for column in source_columns
    ]
    destination_well_list = [
        [f"{row}{column}" for row in "ABCDEFGH"] for column in destination_columns
    ]

    return source_well_list, destination_well_list


if __name__ == "__main__":
    main()
