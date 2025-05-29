#!/usr/bin/env python3
"""Experiment application for Chris and Nidhi's substrate experiment"""

from pathlib import Path

from wei import ExperimentClient
from wei.types.experiment_types import CampaignDesign, ExperimentDesign
from wei.types.workflow_types import Workflow

from ot2_offsets import ot2biobeta, ot2bioalpha
import helper_functions


"""
TODO:
- stack 2 to exchange looked rough, recalibrate!
- why does the pf400 move before sciclops remove lid is done?
- does incubator prevent other communication during a incubation if counting down?
- why is ot2bioalpha not connecting?
- inheco logging
- how to return accurate timestamps from bmg readings?

"""


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
    ot2_to_run_bmg_wf = wf_run_instrument_directory / "ot2_to_run_bmg_wf.yaml"
    bmg_to_run_incubator_wf = wf_run_instrument_directory / "bmg_to_run_incubator_wf.yaml"
    incubator_to_run_bmg_wf = wf_run_instrument_directory / "incubator_to_run_bmg_wf.yaml"
    get_new_plate_wf = wf_set_up_tear_down_directory / "get_new_plate_wf.yaml"

    # protocol paths (for OT-2)
    first_inoculate_both_protocol = protocol_directory / "first_inoculate_both.py"
    inocualte_protocol = protocol_directory / "inoculate.py"

    # other variables
    # ot2bioalpha_tip_box_location = 6
    # ot2biobeta_tip_box_location = 4

    # experiment 1 variables
    "experiment 1: incubation = 1 hr cycles, transfers every 10 hours"
    exp1_incubation_seconds = 120   # TESTING
    exp1_lid_location = "lidnest1"
    exp1_ot2_location_name = "ot2biobeta_deck1_wide"   # starting OT2 location
    exp1_ot2_new_plate_location_name = "ot2biobeta_deck1_wide"
    exp1_ot2_node = "ot2biobeta"
    exp1_ot2_safe_path = "safe_path_ot2biobeta"
    exp1_incubator_node = "inheco_devID2_floor0"
    exp1_incubator_location_name = "inheco_devID2_floor0_nest"
    exp1_tip_box_location = 6 # TESTING
    exp1_stack = "stack1"

    # experiment 2 variables
    """experiment 2: incubation = 2hr cycles, transfers every 20 hours"""
    exp2_incubation_seconds = 240   # TESTING
    exp2_lid_location = "lidnest2" 
    exp2_ot2_location_name = "ot2biobeta_deck3_wide"   # starting OT2 location
    exp2_ot2_location_name = ""
    exp2_ot2_node = "ot2bioalpha"
    exp2_ot2_safe_path = "safe_path_ot2bioalpha"
    exp2_incubator_node = "inheco_devID2_floor1"
    exp2_incubator_location_name = "inheco_devID2_floor1_nest"
    exp2_tip_box_location = 4  # TESTING
    exp2_stack = "stack2"

    # initial payload setup
    payload = {
        # "current_assay_plate_location": "ot2biobeta_deck1_wide",
        # "current_assay_safe_path": "safe_path_ot2biobeta"
        "ot2_node": exp1_ot2_node,
        "ot2_location_name": exp1_ot2_location_name,
        "ot2_new_plate_location": exp1_ot2_new_plate_location_name,
        "ot2_safe_path_name": exp1_ot2_safe_path,
        "tip_box_location": exp1_tip_box_location,
        "stack": exp1_stack,
        "lid_location": exp1_lid_location,
        "incubator_node": exp1_incubator_node,
        "incubator_location_name": exp1_incubator_location_name,
        "incubation_seconds": exp1_incubation_seconds,  
        "current_ot2_protocol": None,    # defined later
        "use_existing_resources": False,
        
    }


    # TESTING generate first inoculation ot-2 protocol and update payload
    # ot2_replacement_variables = helper_functions.collect_ot2_replacement_variables(payload)
    # temp_ot2_file = helper_functions.generate_ot2_protocol(inocualte_protocol, ot2_replacement_variables)
    # payload["current_ot2_protocol"] = temp_ot2_file

    # print(payload)

    # EXPERIMENT LOOP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    """Human needs to set up all labware before run"""
    
    # # Prep ot2biobeta for first inoculation protocol  # WORKING
    # experiment_client.start_run(
    #     setup_for_first_inoculation_wf.resolve(),
    #     payload=payload,
    #     blocking=True,
    #     simulate=False,
    # )

    # # Run first innoculation OT-2 protocol   # WORKING, TODO: test full OT-2 protocol
    # payload["current_ot2_protocol"] = str(first_inoculate_both_protocol)
    # edited_ot2_wf = helper_functions.replace_wf_node_names(
    #     workflow = run_ot2_wf, 
    #     payload = payload
    # )
    # # experiment_client.start_run(   # Don't run ot2 for testing
    # #     edited_ot2_wf,
    # #     payload=payload,
    # #     blocking=True,
    # #     simulate=False,
    # # )

    # # GET BOTH OF THE PLATES INTO THE INCUBATORS
    # # FRIST PLATE
    # # Transfer first plate (experiment 1) into bmg for reading   # WORKING # TODO: Lower z height on BMG location
    # experiment_client.start_run(
    #     ot2_to_run_bmg_wf.resolve(),
    #     payload=payload,
    #     blocking=True,
    #     simulate=False,
    # )

    # # Transfer first plate (experiment 1) from BMG to inheco and start incubation   # WORKING
    # edited_to_inheco_wf = helper_functions.replace_wf_node_names(
    #     workflow=bmg_to_run_incubator_wf, 
    #     payload=payload
    # )
    # experiment_client.start_run(
    #     edited_to_inheco_wf,
    #     payload=payload,
    #     blocking=True,
    #     simulate=False,
    # )

    # SECOND PLATE
    payload["ot2_location_name"] = exp2_ot2_location_name
    payload["lid_location"] = exp2_lid_location
    payload["incubator_node"] = exp2_incubator_node
    payload["incubator_location_name"] = exp2_incubator_location_name
    payload["incubation_seconds"] = exp2_incubation_seconds

    # # Transfer first plate (experiment 2) into bmg for reading   # WORKING # TODO: Lower z height on BMG location
    # experiment_client.start_run(
    #     ot2_to_run_bmg_wf.resolve(),
    #     payload=payload,
    #     blocking=True,
    #     simulate=False,
    # )

    # Transfer first plate (experiment 2) from BMG to inheco and start incubation   # WORKING
    # edited_to_inheco_wf = helper_functions.replace_wf_node_names(
    #     workflow=bmg_to_run_incubator_wf, 
    #     payload=payload
    # )
    # experiment_client.start_run(
    #     edited_to_inheco_wf,
    #     payload=payload,
    #     blocking=True,
    #     simulate=False,
    # )


    # WORKING UNTIL HERE! --------------------------------------------

    # START READING/INCUBATION LOOP
    # set up payload variables
    exp1_ot2_location_name = "ot2biobeta_deck3_wide"
    exp2_ot2_location_name = "ot2bioalpha_deck3_wide"

    # FOR EXPERIMENT 1 PLATE  # WORKING
    payload["ot2_node"] = exp1_ot2_node
    payload["ot2_location_name"] = exp1_ot2_location_name  # when is this needed?
    payload["ot2_safe_path_name"] = exp1_ot2_safe_path
    payload["lid_location"] = exp1_lid_location
    payload["incubator_node"] = exp1_incubator_node
    payload["incubator_location_name"] = exp1_incubator_location_name
    payload["incubation_seconds"] = exp1_incubation_seconds

    # # Transfer plate from exp 1 from incubator to bmg for reading   # WORKING  # TODO: recalibrate z height of exchange
    edited_to_bmg_wf = helper_functions.replace_wf_node_names(
        workflow=incubator_to_run_bmg_wf, 
        payload=payload
    )
    experiment_client.start_run(
        edited_to_bmg_wf,
        payload=payload,
        blocking=True,
        simulate=False,
    )

    # # Transfer back into incubator again (REPEAT STEP FROM ABOVE)
    # edited_to_inheco_wf = helper_functions.replace_wf_node_names(
    #     workflow=bmg_to_run_incubator_wf, 
    #     payload=payload
    # )
    # experiment_client.start_run(
    #     edited_to_inheco_wf,
    #     payload=payload,
    #     blocking=True,
    #     simulate=False,
    # )

    # FOR EXPERIMENT 2 PLATE  
    # payload["ot2_node"] = exp2_ot2_node
    # payload["ot2_location_name"] = exp2_ot2_location_name  # when is this needed?
    # payload["ot2_safe_path_name"] = exp2_ot2_safe_path
    # payload["lid_location"] = exp2_lid_location
    # payload["incubator_node"] = exp2_incubator_node
    # payload["incubator_location_name"] = exp2_incubator_location_name
    # payload["incubation_seconds"] = exp2_incubation_seconds # for TESTING   (exp 2 inc time)

    
    # # Transfer plate from exp 2 from incubator to bmg for reading   # WORKING  # TODO: recalibrate z height of exchange
    # edited_to_bmg_wf = helper_functions.replace_wf_node_names(
    #     workflow=incubator_to_run_bmg_wf, 
    #     payload=payload
    # )
    # experiment_client.start_run(
    #     edited_to_bmg_wf,
    #     payload=payload,
    #     blocking=True,
    #     simulate=False,
    # )

    # # Transfer back into incubator again (REPEAT STEP FROM ABOVE)
    # edited_to_inheco_wf = helper_functions.replace_wf_node_names(
    #     workflow=bmg_to_run_incubator_wf, 
    #     payload=payload
    # )
    # experiment_client.start_run(
    #     edited_to_inheco_wf,
    #     payload=payload,
    #     blocking=True,
    #     simulate=False,
    # )

    # INOCULATION STEPS!!
    payload["ot2_node"] = exp1_ot2_node
    payload["ot2_location_name"] = exp1_ot2_location_name  # when is this needed?
    payload["ot2_safe_path_name"] = exp1_ot2_safe_path
    payload["lid_location"] = exp1_lid_location
    payload["incubator_node"] = exp1_incubator_node
    payload["incubator_location_name"] = exp1_incubator_location_name
    payload["incubation_seconds"] = exp1_incubation_seconds # for TESTING  

    # # Get a new plate from stack   # WORKS
    # edited_get_new_plate_wf = helper_functions.replace_wf_node_names(
    #     workflow=get_new_plate_wf, 
    #     payload=payload
    # )
    # experiment_client.start_run(
    #     edited_get_new_plate_wf,
    #     payload=payload,
    #     blocking=True,
    #     simulate=False,
    # )

    # Transfer a plate from the bmg to old position on ot2





    

























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
