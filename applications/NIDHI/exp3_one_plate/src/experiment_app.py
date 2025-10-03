#!/usr/bin/env python3
"""
Experiment application for Chris and Nidhi's substrate experiment

TODO:
- automatic data transfer
- TEST everything


"""

from pathlib import Path

from wei import ExperimentClient
from wei.types.experiment_types import CampaignDesign, ExperimentDesign

from datetime import datetime
import time
import helper_functions


def main() -> None:
    """Runs the Substrate Experiment Application"""

    # INITIAL EXPERIMENT SETUP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # define the ExperimentDesign object that will be used to register the experiment
    experiment_design = ExperimentDesign(
        experiment_name="Substrate_Experiment_3a",
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


    # DEFINE PATHS AND VARIABLES ---------------------------------
    # capture the expriment ID
    experiment_id = experiment_client.experiment.experiment_id
    experiment_label = "3"

    # directory paths
    app_directory = Path(__file__).parent.parent   # experiment app
    wf_directory = app_directory / "workflows"  # workflows
    protocol_directory = app_directory / "protocols"    # protocols

    # workflow paths
    run_ot2_wf = wf_directory / "run_ot2_wf.yaml"
    exchange_to_run_incubator_wf = (
        wf_directory / "exchange_to_run_incubator_wf.yaml"
    )
    incubator_to_run_bmg_wf = (
        wf_directory / "incubator_to_run_bmg_wf.yaml"
    )
    get_new_plate_and_run_bmg_wf = (
        wf_directory / "get_new_plate_and_run_bmg_wf.yaml"
    )
    bmg_to_ot2_wf = wf_directory / "bmg_to_ot2_wf.yaml"
    ot2_to_run_bmg_wf = wf_directory / "ot2_to_run_bmg_wf.yaml"
    bmg_to_run_incubator_wf = wf_directory / "bmg_to_run_incubator_wf.yaml"
    remove_old_substrate_plate_wf = wf_directory / "remove_old_substrate_plate_wf.yaml"
    at_end_ot2_to_exchange_wf = wf_directory / "at_end_ot2_to_exchange_wf.yaml"

    # protocol paths (for OT-2)
    inoculate_protocol = protocol_directory / "inoculate.py"

    # important variables
    loop_num = 0
    total_outer_loops = 33 # inoculations into new plate every 10ish hours
    total_inner_loops = 10 # readings every hour for 10 hours
    plate_num = 0
    reading_in_plate_num = 10
    current_tower_deck = 1
    csv_data_directory = "/home/rpl/workspace/Nidhi_data"
    test_prints = True  # if True, print out extra info for testing purposes
    incubation_seconds_initial = 40 # TESTING change back to 36000 seconds = 10 hours
    incubation_seconds_between_readings = 180 # TESTING change back to 3600 seconds = 1 hour

    exp1_variables = {
        "old_lid_location": "lidnest_2_wide", # use old lid location at start
        "new_lid_location": "lidnest_1_wide",
        "old_safe_lid_location": "safe_path_lidnest_2",
        "new_safe_lid_location": "safe_path_lidnest_1",
        "ot2_node": "ot2biobeta",
        "new_ot2_plate_location": "ot2biobeta_deck1_wide",
        "old_ot2_plate_location": "ot2biobeta_deck3_wide",
        "ot2_safe_path": "safe_path_ot2biobeta",
        "incubator_node": "inheco_devID2_floor0",
        "incubator_location": "inheco_devID2_floor0_nest",
        "tip_box_location": 4,
        "new_stack": "stack1",
        "trash_stack": "stack4",
    }

        # initial payload setup  (experiment 1 focused at start)
    payload = {
        "lid_location": exp1_variables["old_lid_location"],
        "lid_safe_path": exp1_variables["old_safe_lid_location"],
        "ot2_node": exp1_variables["ot2_node"],
        "ot2_location": exp1_variables["old_ot2_plate_location"],
        "ot2_safe_path": exp1_variables["ot2_safe_path"],
        "tip_box_location": exp1_variables["tip_box_location"],
        "incubator_node": exp1_variables["incubator_node"],
        "incubator_location": exp1_variables["incubator_location"],
        "incubation_seconds": incubation_seconds_initial,
        "current_ot2_protocol": None,
        "current_tower_deck": "tower_deck" + str(current_tower_deck),
        "current_tower_deck_safe_path": "safe_path_tower_deck" + str(current_tower_deck),
        "use_existing_resources": False,
        "bmg_assay_name": "NIDHI",
    }


    # # EXPERIMENT LOOP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    """
    Experiment setup at start:

    Location:
        exchange: inoculated plate with lid
        Stack 1: extra substrate plates with lids
        OT-2 (ot2biobeta) decks 4-11: tip racks
        ALL OTHER LOCATIONS: EMPTY
    """

    # Move immediately into incubator with lid on for 10 hours  # WORKING
    experiment_client.start_run(
        exchange_to_run_incubator_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    # transfer plate 0 into bmg and take reading (plate0_T10)   # WORKING
    timestamp_now = int(datetime.now().timestamp())
    payload["bmg_data_output_name"] = (
        f"{experiment_label}_{timestamp_now}_{experiment_id}_exp1_{plate_num}_T{reading_in_plate_num}.txt"
    )
    run_info = experiment_client.start_run(
        incubator_to_run_bmg_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )
    # write utc bmg timestamp to csv data file
    helper_functions.write_timestamps_to_csv(
        csv_directory_path=csv_data_directory,
        experiment_id=experiment_id,
        bmg_filename=payload["bmg_data_output_name"],
        accurate_timestamp=run_info.steps[7].end_time,  # index 7 = bmg reading
    )
    if test_prints:
        # print(f"\twriting data to csv: {payload['bmg_data_output_name']}")
        print(f"\twriting data to csv: {payload['bmg_data_output_name']}, with timestamp {run_info.steps[7].end_time}")

    # transfer old plate into the OT-2   # WORKING
    experiment_client.start_run(
        bmg_to_ot2_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )


    # OUTER LOOP START HERE (TODO: HOW MANY OUTER LOOPS?)
    ##########################################################################################
    for i in range(total_outer_loops):

        # modify variables
        plate_num += 1
        reading_in_plate_num = 0
        payload["lid_location"] = exp1_variables["new_lid_location"]
        payload["lid_safe_path"] = exp1_variables["new_safe_lid_location"]
        payload["ot2_location"] = exp1_variables["new_ot2_plate_location"]
        payload["incubation_seconds"] = incubation_seconds_between_readings

        # get new substrate plate, take contam reading (T0), then move to OT-2 new location   # WORKING
        timestamp_now = int(datetime.now().timestamp())
        payload["bmg_data_output_name"] = (
            f"{experiment_label}_{timestamp_now}_{experiment_id}_exp1_{plate_num}_contam.txt"
        )
        run_info = experiment_client.start_run(
            get_new_plate_and_run_bmg_wf.resolve(),
            payload=payload,
            blocking=True,
            simulate=False,
        )
        # # write utc bmg timestamp to csv data file
        helper_functions.write_timestamps_to_csv(
            csv_directory_path=csv_data_directory,
            experiment_id=experiment_id,
            bmg_filename=payload["bmg_data_output_name"],
            accurate_timestamp=run_info.steps[5].end_time,  # index 5 = bmg reading
        )
        if test_prints:
            print(f"\twriting data to csv: {payload['bmg_data_output_name']}, with timestamp {run_info.steps[5].end_time}")

        # modify variables
        reading_in_plate_num += 1

        # transfer new plate from bmg to new ot2 location  # WORKING
        experiment_client.start_run(
            bmg_to_ot2_wf.resolve(),
            payload=payload,
            blocking=True,
            simulate=False,
        )

        # run inoculation ot2 protocol   # WORKS
        ot2_replacement_variables = helper_functions.collect_ot2_replacement_variables(payload)
        temp_ot2_file_str = helper_functions.generate_ot2_protocol(inoculate_protocol, ot2_replacement_variables)
        payload["current_ot2_protocol"] = temp_ot2_file_str
        experiment_client.start_run(
            run_ot2_wf.resolve(),
            payload=payload,
            blocking=True,
            simulate=False,
        )

        # modify variables
        exp1_variables["tip_box_location"] += 1
        if exp1_variables["tip_box_location"] == 12:  # reset if necessary
            exp1_variables["tip_box_location"] = 4
        payload["tip_box_location"] = exp1_variables["tip_box_location"]

        # transfer new plate into bmg and take T1 reading - WORKING
        timestamp_now = int(datetime.now().timestamp())
        payload["bmg_data_output_name"] = (
            f"{experiment_label}_{timestamp_now}_{experiment_id}_exp1_{plate_num}_contam.txt"
        )
        run_info = experiment_client.start_run(
            ot2_to_run_bmg_wf.resolve(),
            payload=payload,
            blocking=True,
            simulate=False,
        )
        # write utc bmg timestamp to csv data file
        helper_functions.write_timestamps_to_csv(
            csv_directory_path=csv_data_directory,
            experiment_id=experiment_id,
            bmg_filename=payload["bmg_data_output_name"],
            accurate_timestamp=run_info.steps[4].end_time,  # index 5 = bmg reading
        )
        if test_prints:
            print(f"\twriting data to csv: {payload['bmg_data_output_name']}, with timestamp {run_info.steps[4].end_time}")

        # transfer from bmg to incubator and incubate (1hr)  # WORKING
        experiment_client.start_run(
            bmg_to_run_incubator_wf.resolve(),
            payload=payload,
            blocking=True,
            simulate=False,
        )

        # capture incubation start time
        incubation_start_time = time.time()

        # modify variables
        payload["lid_location"] = exp1_variables["old_lid_location"]
        payload["lid_safe_path"] = exp1_variables["old_safe_lid_location"]
        payload["ot2_location"] = exp1_variables["old_ot2_plate_location"]

        # get rid of the old substrate plate  # WORKING
        experiment_client.start_run(
            remove_old_substrate_plate_wf.resolve(),
            payload=payload,
            blocking=True,
            simulate=False,
        )

        # modify variables
        current_tower_deck += 1
        if current_tower_deck == 6:  # reset if necessary
            current_tower_deck = 1
        payload["current_tower_deck"] = "tower_deck" + str(current_tower_deck)
        payload["current_tower_deck_safe_path"] = "safe_path_tower_deck" + str(current_tower_deck)

        # wait for incubation to finish
        while time.time() - incubation_start_time < incubation_seconds_between_readings:
            print(f"will continue in... {int(exp1_variables["incubation_seconds"]-(time.time() - incubation_start_time))} seconds")
            time.sleep(5) # 5 seconds

        # INNER LOOP START HERE
        for j in range(total_inner_loops):

            # NOTE: lid can be removed to old location this whole time

            if test_prints:
                print()
                print(j)

            # Incubator to run BMG  (T1 - T10 readings)
            if test_prints:
                print(f"running incubator to bmg, taking T{j+1} reading")
            timestamp_now = int(datetime.now().timestamp())
            payload["bmg_data_output_name"] = (
                f"{experiment_label}_{timestamp_now}_{experiment_id}_exp1_{plate_num}_T{reading_in_plate_num}.txt"
            )
            run_info = experiment_client.start_run(
                incubator_to_run_bmg_wf.resolve(),
                payload=payload,
                blocking=True,
                simulate=False,
            )

            # write utc bmg timestamp to csv data file
            helper_functions.write_timestamps_to_csv(
                csv_directory_path=csv_data_directory,
                experiment_id=experiment_id,
                bmg_filename=payload["bmg_data_output_name"],
                accurate_timestamp=run_info.steps[7].end_time,  # index 7 = bmg reading
            )
            if test_prints:
                # print(f"\twriting data to csv: {payload['bmg_data_output_name']}")
                print(f"\twriting data to csv: {payload['bmg_data_output_name']}, with timestamp {run_info.steps[7].end_time}")

            # modify variables
            reading_in_plate_num += 1

            if j < 9:
                # bmg to run incubator
                if test_prints:
                    print("running bmg to incubator")
                # transfer from bmg to incubator and incubate
                experiment_client.start_run(
                    bmg_to_run_incubator_wf.resolve(),
                    payload=payload,
                    blocking=True,
                    simulate=False,
                )
                # capture incubation start time
                incubation_start_time = time.time()

                # sleep for incubation
                if test_prints:
                    print("running incubaton")
                while time.time() - incubation_start_time < incubation_seconds_between_readings:
                    print(f"will continue in... {int(exp1_variables["incubation_seconds"]-(time.time() - incubation_start_time))} seconds")
                    time.sleep(5) # 5 seconds


            else:  # plate will end in the bmg with bmg open
                # bmg to ot2 old location
                if test_prints:
                    print("running bmg to ot2")
                experiment_client.start_run(
                    bmg_to_ot2_wf.resolve(),
                    payload=payload,
                    blocking=True,
                    simulate=False,
                )

        # INNER LOOP END HERE

    # OUTER LOOP ENDS HERE

    # NOTE: if no more outer loops, plate ends at old ot-2 location with lid on lidnest 2
    # can't return plate to tower since we didn't grab a new substrate plate

    # move from old ot-2 location to exchange, replace lid.
    if test_prints:
        print("END OF EXPEREMENT APP: returning old plate from ot2 to exchange")
    experiment_client.start_run(
        at_end_ot2_to_exchange_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    print("YAY WE MADE IT!")






























if __name__ == "__main__":
    main()
