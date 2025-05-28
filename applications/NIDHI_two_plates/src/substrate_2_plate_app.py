#!/usr/bin/env python3
"""Experiment application for Chris and Nidhi's substrate experiment"""

from pathlib import Path

from wei import ExperimentClient
from wei.types.experiment_types import CampaignDesign, ExperimentDesign
from wei.types.workflow_types import Workflow

from ot2_offsets import ot2biobeta, ot2bioalpha
import helper_functions


def main() -> None:
    """Runs the OT-2 protocol to create extra media plates"""

    # INITIAL EXPERIMENT SETUP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # define the ExperimentDesign object that will be used to register the experiment
    experiment_design = ExperimentDesign(
        experiment_name="Substrate_Experiment_Prep_Extra_Media_Plates",
        experiment_description="Experiment application to prep 5 extra media plates for the substrate application",
    )
    # define a campaign object (useful if we want to group many of these substrate experiments together)
    campaign = CampaignDesign(
        campaign_name="Substrate_Campaign",
        campaign_description="Campaign to collect all substrate experiments",
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
    wf_run_instrument_directory = wf_directory / "run_instrument"
    wf_set_up_tear_down_directory = wf_directory / "set_up_tear_down"
    protocol_directory = app_directory / "protocols"

    # workflow paths (run instruments)
    setup_for_first_inoculation_wf = wf_set_up_tear_down_directory / "setup_for_first_inoculation_wf.yaml"
    run_ot2_wf = wf_run_instrument_directory / "run_ot2_wf.yaml"
    ot2_to_run_incubator_wf = wf_run_instrument_directory / "ot2_to_run_bmg_wf.yaml"


    # protocol paths (for OT-2)
    first_inoculate_both_protocol = protocol_directory / "first_inoculate_both.py"
    inocualte_protocol = protocol_directory / "inoculate.py"

    # other variables
    ot2bioalpha_tip_box_location = 6
    ot2biobeta_tip_box_location = 4


    # initial payload setup
    payload = {
        # "current_assay_plate_location": "ot2biobeta_deck1_wide",
        # "current_assay_safe_path": "safe_path_ot2biobeta"
        "ot2_node": "ot2biobeta",
        "ot2_location_name": "ot2biobeta_deck1_wide",
        "ot2_safe_path_name": "safe_path_ot2biobeta",
        "ot2bioalpha_tip_box_location": ot2bioalpha_tip_box_location,
        "ot2biobeta_tip_box_location": ot2biobeta_tip_box_location,
        "incubator_node": "inheco_dev2_floor0",
        "incubaton_seconds": 3600,   # 1 hour to start
        "current_ot2_protocol": None,    # defined later
        "use_existing_resources": False,
    }

    # TESTING
    # payload["ot2_node"] = "ot2bioalpha"

    # TESTING generate first inoculation ot-2 protocol and update payload
    # ot2_replacement_variables = helper_functions.collect_ot2_replacement_variables(payload)
    # temp_ot2_file = helper_functions.generate_ot2_protocol(inocualte_protocol, ot2_replacement_variables)
    # payload["current_ot2_protocol"] = temp_ot2_file

    # print(payload)

    # EXPERIMENT LOOP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    """Human needs to set up all labware before run"""
    
    # Prep ot2biobeta for first inoculation protocol  # WORKING
    experiment_client.start_run(
        setup_for_first_inoculation_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    # Run first innoculation OT-2 protocol   # WORKING, TODO: test full OT-2 protocol
    payload["current_ot2_protocol"] = str(first_inoculate_both_protocol)
    edited_ot2_wf = helper_functions.replace_wf_node_names(
        workflow = run_ot2_wf, 
        payload = payload
    )
    experiment_client.start_run(
        edited_ot2_wf,
        payload=payload,
        blocking=True,
        simulate=False,
    )

    # transfer first plate (experiment 1) into bmg for reading   # WORKING # TODO: Lower z height on BMG location
    experiment_client.start_run(
        ot2_to_run_incubator_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )






    # # RUN OT-2
    # # edit workflow for current incubator and ot2 nodes
    # run_ot2_wf = Workflow.from_yaml(run_ot2_wf.resolve())
    # for step in run_ot2_wf.flowdef:
    #     if step.module == "payload.incubator_node":
    #         step.module = ""
    #     if step.module == "payload.ot2_node": 
    #         step.module = payload["ot2_node"]

    # # # TESTING
    # # for step in run_ot2_wf: 
    # #     print(step)

    # # Run the current OT-2 protocol
    # run_info = experiment_client.start_run(
    #     run_ot2_wf,
    #     payload=payload,
    #     blocking=True,
    #     simulate=False,
    # )

    # print(run_info)






if __name__ == "__main__":
    main()
