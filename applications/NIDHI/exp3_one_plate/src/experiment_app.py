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

    # workflow paths (run instruments)
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

    # incubation_seconds_initial = 36000  # 10 hours
    incubation_seconds_initial = 20 # TESTING
    incubation_seconds_between_readings = 3600  # 1 hour

    # # initial payload setup
    # payload = {
    #     "current_ot2_protocol": str(inoculate_protocol),
    #     "ot2_new_plate_location": "ot2biobeta_deck1_wide",
    #     "ot2_old_plate_location": "ot2biobeta_deck3_wide",
    #     "ot2_safe_path": "safe_path_ot2biobeta",
    #     "tip_box_location": 4,
    #     "stack": "stack1",
    #     "new_lid_location": "lidnest1",
    #     "old_lid_location": "lidnest2",
    #     "remove_lid_safe_path": "safe_path_lidnest_1",
    #     "bmg_assay_name": "NIDHI",
    #     "incubator_node": "inheco_devID2_floor0",
    #     "incubator_location": "inheco_devID2_floor1_nest",
    #     "incubation_seconds": incubation_seconds_initial,
    # }

    exp1_variables = {
        "lid_location": "lidnest_2_wide",  # use old lid location at start
        "safe_lid_location": "safe_path_lidnest_2",
        "ot2_node": "ot2biobeta",
        "ot2_new_plate_location": "ot2biobeta_deck1_wide",
        "ot2_old_plate_location": "ot2biobeta_deck3_wide",
        "ot2_safe_path": "safe_path_ot2biobeta",
        "incubator_node": "inheco_devID2_floor0",
        "incubator_location": "inheco_devID2_floor0_nest",
        "tip_box_location": 4,
        "new_stack": "stack1",
        "trash_stack": "stack4",
    }

        # initial payload setup  (experiment 1 focused at start)
    payload = {
        "lid_location": exp1_variables["lid_location"],
        "safe_lid_location": exp1_variables["safe_lid_location"],
        "ot2_node": exp1_variables["ot2_node"],
        "ot2_location": exp1_variables["ot2_new_plate_location"],
        "ot2_safe_path": exp1_variables["ot2_safe_path"],
        "tip_box_location": exp1_variables["tip_box_location"],
        "incubator_node": exp1_variables["incubator_node"],
        "incubator_location": exp1_variables["incubator_location"],
        "incubation_seconds": incubation_seconds_initial,
        "current_ot2_protocol": None,
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

    # # Move immediately into incubator with lid on for 10 hours  # WORKS
    # experiment_client.start_run(
    #     exchange_to_run_incubator_wf.resolve(),
    #     payload=payload,
    #     blocking=True,
    #     simulate=False,

    # )

    # transfer plate 0 into bmg and take reading (plate0_T10)   # NOT TESTED
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
    # # write utc bmg timestamp to csv data file
    # helper_functions.write_timestamps_to_csv(
    #     csv_directory_path=csv_data_directory,
    #     experiment_id=experiment_id,
    #     bmg_filename=payload["bmg_data_output_name"],
    #     accurate_timestamp=run_info.steps[7].end_time,  # index 7 = bmg reading
    # )
    # if test_prints:
    #     print(f"\twriting data to csv: {payload['bmg_data_output_name']}")
    #     # print(f"\twriting data to csv: {payload['bmg_data_output_name']}, with timestamp {run_info.steps[7].end_time}")


    # # modify variables
    # plate_num += 1
    # reading_in_plate_num = 0

    # # get new substrate plate, take contam reading, then move to OT-2
    # timestamp_now = int(datetime.now().timestamp())
    # payload["bmg_data_output_name"] = (
    #     f"{experiment_label}_{timestamp_now}_{experiment_id}_exp1_{plate_num}_contam.txt"
    # )
    # experiment_client.start_run(
    #     get_new_plate_and_run_bmg_wf.resolve(),
    #     payload=payload,
    #     blocking=True,
    #     simulate=False,
    # )
    # # write utc bmg timestamp to csv data file
    # helper_functions.write_timestamps_to_csv(
    #     csv_directory_path=csv_data_directory,
    #     experiment_id=experiment_id,
    #     bmg_filename=payload["bmg_data_output_name"],
    #     accurate_timestamp=run_info.steps[5].end_time,  # index 5 = bmg reading
    # )
    # if test_prints:
    #     print(f"\twriting data to csv: {payload['bmg_data_output_name']}, with timestamp {run_info.steps[5].end_time}")


    # # Take T10 (endpoint reading) of plate 0 in incubator then move to OT-2 old location






if __name__ == "__main__":
    main()
