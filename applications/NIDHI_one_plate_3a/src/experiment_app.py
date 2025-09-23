#!/usr/bin/env python3
"""Experiment application for Chris and Nidhi's substrate experiment"""

from pathlib import Path

from wei import ExperimentClient
from wei.types.experiment_types import CampaignDesign, ExperimentDesign

from datetime import datetime
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
    experiment_label = "3a"

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
    exchange_to_run_incubator_wf = (
        wf_run_instrument_directory / "exchange_to_run_incubator_wf.yaml"
    )


    # workflow paths (set up and tear down related)
    get_new_plate_and_run_bmg_wf = (
        wf_set_up_tear_down_directory / "get_new_plate_and_run_bmg_wf.yaml"
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
    inoculate_protocol = protocol_directory / "inoculate.yaml"

    # important variables
    loop_num = 0
    total_outer_loops = 33 # inoculations into new plate every 10ish hours
    total_inner_loops = 10 # readings every hour for 10 hours

    plate_num = 0
    reading_in_plate_num = 10

    csv_data_directory = "/home/rpl/workspace/Nidhi_data"

    test_prints = True  # if True, print out extra info for testing purposes



    # initial payload setup
    payload = {
        "current_ot2_protocol": str(inoculate_protocol),
        "new_lid_location": "lidnest1",
        "old_lid_location": "lidnest2",
        "remove_lid_safe_path": "safe_path_lidnest_1",
        "bmg_assay_name": "NIDHI",
        "ot2_new_plate_location": "ot2biobeta_deck1_wide", 
        "ot2_old_plate_location": "ot2biobeta_deck3_wide",
        "ot2_safe_path": "safe_path_ot2bioalpha", 
        "incubator_node": "inheco_devID2_floor1",
        "incubator_location": "inheco_devID2_floor1_nest",
        "incubation_seconds": 36000,  # 10 hours
        "stack": "stack1",
    }

    # EXPERIMENT LOOP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # start with inoculated assay plate with lid on exchange and extra assay plates in Plate Crane stack 1


    # move immediately into incubator with lid on for 10 hours
    experiment_client.start_run(
        exchange_to_run_incubator_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    # transfer plate 0 into bmg and take reading (plate0_T10)
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
    if test_prints == True: 
        print(f"\twriting data to csv: {payload['bmg_data_output_name']}, with timestamp {run_info.steps[7].end_time}")


    # modify variables
    plate_num += 1
    reading_in_plate_num = 0
    
    # get new substrate plate, take contam reading, then move to OT-2
    timestamp_now = int(datetime.now().timestamp())
    payload["bmg_data_output_name"] = (
        f"{experiment_label}_{timestamp_now}_{experiment_id}_exp1_{plate_num}_contam.txt"
    )
    experiment_client.start_run(
        get_new_plate_and_run_bmg_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )
    # write utc bmg timestamp to csv data file
    helper_functions.write_timestamps_to_csv(
        csv_directory_path=csv_data_directory,
        experiment_id=experiment_id,
        bmg_filename=payload["bmg_data_output_name"],
        accurate_timestamp=run_info.steps[5].end_time,  # index 5 = bmg reading
    )
    if test_prints == True: 
        print(f"\twriting data to csv: {payload['bmg_data_output_name']}, with timestamp {run_info.steps[5].end_time}")


    # Take T10 (endpoint reading) of plate 0 in incubator then move to OT-2 old location
    





if __name__ == "__main__":
    main()
