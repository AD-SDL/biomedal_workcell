#!/usr/bin/env python3
"""Experiment application for Chris and Nidhi's substrate experiment"""

from pathlib import Path

from wei import ExperimentClient
from wei.types.experiment_types import CampaignDesign, ExperimentDesign
from wei.types.workflow_types import Workflow

from ot2_offsets import ot2biobeta, ot2bioalpha
import helper_functions
import time
from datetime import datetime



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

    # DEFINE PATHS AND VARIABLES ---------------------------------

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

    # experiment 1: incubation = 1 hr cycles, transfers every 10 hours
    exp1_variables = {
        "incubation_seconds": 30,   # TESTING
        "lid_location": "lidnest1",
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

    # experiment 2: incubation = 2 hr cycles, transfers every 20 hours
    exp2_variables = {
        "incubation_seconds": 60,   # TESTING
        "lid_location": "lidnest2",
        "ot2_node": "ot2bioalpha",
        "ot2_new_plate_location": "ot2bioalpha_deck1_wide", 
        "ot2_old_plate_location": "ot2bioalpha_deck3_wide",
        "ot2_safe_path": "safe_path_ot2bioalpha", 
        "incubator_node": "inheco_devID2_floor1",
        "incubator_location": "inheco_devID2_floor1_nest",
        "tip_box_location": 4,
        "new_stack": "stack2",
        "trash_stack": "stack5",
    }

    # other variables (for loop tracking)
    experiment_label = "2a"
    transfer_loop_num = 0       # outer loop
    incubation_loop_num = 0     # inner loop
    exp1_reading_num_in_plate = 1
    exp2_reading_num_in_plate = 1
    exp1_plate_num = 1
    exp2_plate_num = 1
    total_transfers = 20
    continue_exp1 = True

    # initial payload setup  (experiment 1 focused at start)
    payload = {
        "ot2_node": exp1_variables["ot2_node"],
        "ot2_location": exp1_variables["ot2_new_plate_location"],
        "ot2_safe_path": exp1_variables["ot2_safe_path"],
        "tip_box_location": exp1_variables["tip_box_location"],
        "stack": exp1_variables["new_stack"],
        "lid_location": exp1_variables["lid_location"],
        "incubator_node": exp1_variables["incubator_node"],
        "incubator_location": exp1_variables["incubator_location"],
        "incubation_seconds": exp1_variables["incubation_seconds"],  
        "current_ot2_protocol": None,    # defined later
        "use_existing_resources": False,
        "bmg_assay_name": "NIDHI", 
    }


    # EXPERIMENT STEPS: ------------------------------------------------------------------------------
    """Before running this experiment, extra substrate plates should be prepped 
        by running extra_media_plates_app.py. The prepped plates for experiment 1 should 
        be placed in ScoClops stack 1, and the prepped plates for experiment 2 should be
        placed in SciClops stack2. The OT-2 deck of ot2biobeta should be prepped for 
        first_inoculate_both.py"""
    
    # 1.) WF: Transfer a new plate from each experiment stack to ot2biobeta for first inoculation -- Done
    experiment_client.start_run(
        setup_for_first_inoculation_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    # 2.) WF: Run first_inoculate_both OT-2 protocol  --> Time (with full mixing)= ~22 min   -- Done
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

    # 3.) WFs: Transfer experiment 1 plate to bmg, read, then place into incubator -- Done WITH SOME TODO s
    # TODO: collect accurate timestamp from bmg  --> where to report this if data filename has to be specified first

    timestamp_now = int(datetime.now().timestamp())
    payload["bmg_data_output_name"] = (
        f"{experiment_label}_exp1_{timestamp_now}_{experiment_id}_{exp1_plate_num}_{exp1_reading_num_in_plate}.txt"
    )
    # ot2 to bmg
    experiment_client.start_run(
        ot2_to_run_bmg_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )
    exp1_reading_num_in_plate += 1

    # bmg to inheco incubator
    edited_to_inheco_wf = helper_functions.replace_wf_node_names(
        workflow=bmg_to_run_incubator_wf, 
        payload=payload
    )
    experiment_client.start_run(
        edited_to_inheco_wf,
        payload=payload,
        blocking=True,
        simulate=False,
    )

    # # capture incubation start time
    exp1_into_incubator_time = time.time()
    print(f"experiment 1: incubation started at {exp1_into_incubator_time}")  # TESTING

    # # 4.) WFs: Transfer experiment 2 plate to bmg, read, then place into incubator -- Done 
    # # update payload variables
    payload["ot2_location"] = exp1_variables["ot2_old_plate_location"]   # ok that this says exp1!
    payload["lid_location"] = exp2_variables["lid_location"]
    payload["incubator_node"] = exp2_variables["incubator_node"]
    payload["incubator_location"] = exp2_variables["incubator_location"]
    payload["incubation_seconds"] = exp2_variables["incubation_seconds"]
    
    # ot2 to bmg
    timestamp_now = int(datetime.now().timestamp())
    payload["bmg_data_output_name"] = (
        f"{experiment_label}_exp2_{timestamp_now}_{experiment_id}_{exp2_plate_num}_{exp2_reading_num_in_plate}.txt"
    )
    experiment_client.start_run(
        ot2_to_run_bmg_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )
    exp2_reading_num_in_plate += 1

    # bmg to inheco incubator
    edited_to_inheco_wf = helper_functions.replace_wf_node_names(
        workflow=bmg_to_run_incubator_wf, 
        payload=payload
    )
    experiment_client.start_run(
        edited_to_inheco_wf,
        payload=payload,
        blocking=True,
        simulate=False,
    )
    exp2_into_incubator_time = time.time()
    print(f"experiment 2: incubation started at {exp2_into_incubator_time}")

    # increase variables
    transfer_loop_num += 1

    # sleep until experiment 1 plate is ready for next reading (1 hr total)
    # TODO: imporove this! 
    while time.time() - exp1_into_incubator_time < exp1_variables["incubation_seconds"]: 
        print(f"will continue in... {time.time() - exp1_into_incubator_time}")
        time.sleep(5) # 5 seconds

    """Now that both experiment plates are in the incubator, 
        we can start the both the outer transfers loop and
        the inner incubation loop."""
    

    # TESTING
    incubation_loop_num = 8

    while exp1_plate_num < 21:   # TODO: What should this number be?
        while incubation_loop_num < 10: # Inner loop, each loop ~ 1 hr

            # TESTING
            print(f"incubation_loop_num: {incubation_loop_num}")

            if continue_exp1: 
                # 5.) WFs: Transfer experiment 1 plate from incubator, to bmg, read, and return to incubator
                # TESTING
                print(f"continue exp1?: {continue_exp1}")
                print("exp1: taking reading and returning to incubator")
                print(f"exp1: reading in plate number: {exp1_reading_num_in_plate}")

                # update payload variables
                payload["ot2_location"] = exp1_variables["ot2_new_plate_location"]  
                payload["lid_location"] = exp1_variables["lid_location"]
                payload["incubator_node"] = exp1_variables["incubator_node"]
                payload["incubator_location"] = exp1_variables["incubator_location"]
                payload["incubation_seconds"] = exp1_variables["incubation_seconds"]
                
                # inheco incubator to bmg
                timestamp_now = int(datetime.now().timestamp())
                payload["bmg_data_output_name"] = (
                    f"{experiment_label}_exp1_{timestamp_now}_{experiment_id}_{exp1_plate_num}_{exp1_reading_num_in_plate}.txt"
                )
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
                exp1_reading_num_in_plate += 1

                # bmg to inheco incubator
                edited_to_inheco_wf = helper_functions.replace_wf_node_names(
                    workflow=bmg_to_run_incubator_wf, 
                    payload=payload
                )
                experiment_client.start_run(
                    edited_to_inheco_wf,
                    payload=payload,
                    blocking=True,
                    simulate=False,
                )
                exp1_reading_num_in_plate += 1

                # bmg to inheco incubator
                edited_to_inheco_wf = helper_functions.replace_wf_node_names(
                    workflow=bmg_to_run_incubator_wf, 
                    payload=payload
                )
                experiment_client.start_run(
                    edited_to_inheco_wf,
                    payload=payload,
                    blocking=True,
                    simulate=False,
                )
                exp1_into_incubator_time = time.time()

            if incubation_loop_num % 2 == 0:   # only read exp 2 plate every 2 hours (each loop =~ 1hr)
                # 6.) Wfs: Transfer experiment 2 plate from incubator, to bmg, read, and return to incubator
                # TESTING
                print("exp2: taking reading and returning to incubator")
                print(f"exp2: reading in plate number: {exp2_reading_num_in_plate}")

                # update payload variables
                payload["lid_location"] = exp2_variables["lid_location"]
                payload["incubator_node"] = exp2_variables["incubator_node"]
                payload["incubator_location"] = exp2_variables["incubator_location"]
                payload["incubation_seconds"] = exp2_variables["incubation_seconds"]

                # inheco incubator to bmg
                timestamp_now = int(datetime.now().timestamp())
                payload["bmg_data_output_name"] = (
                    f"{experiment_label}_exp2_{timestamp_now}_{experiment_id}_{exp2_plate_num}_{exp2_reading_num_in_plate}.txt"
                )
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
                exp2_reading_num_in_plate += 1

                # # bmg to inheco incubator
                edited_to_inheco_wf = helper_functions.replace_wf_node_names(
                    workflow=bmg_to_run_incubator_wf, 
                    payload=payload
                )
                experiment_client.start_run(
                    edited_to_inheco_wf,
                    payload=payload,
                    blocking=True,
                    simulate=False,
                )

            # sleep until experiment 1 incubation time is complete
            while (time.time() - exp1_into_incubator_time) < exp1_variables["incubation_seconds"]: 
                print(f"will continue in... {time.time() - exp1_into_incubator_time}")
                time.sleep(5)


            # # TESTING
            # print(f"experiment 1 plate num: {exp1_plate_num}")
            # print(f"experiment 2 plate num: {exp2_plate_num}")

            incubation_loop_num += 1

        exp1_plate_num += 1
        exp2_plate_num += 1

    

    

     
    

    





    




























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

    # # SECOND PLATE
    # payload["ot2_location_name"] = exp2_ot2_location_name
    # payload["lid_location"] = exp2_lid_location
    # payload["incubator_node"] = exp2_incubator_node
    # payload["incubator_location_name"] = exp2_incubator_location_name
    # payload["incubation_seconds"] = exp2_incubation_seconds

    # # # Transfer first plate (experiment 2) into bmg for reading   # WORKING # TODO: Lower z height on BMG location
    # # experiment_client.start_run(
    # #     ot2_to_run_bmg_wf.resolve(),
    # #     payload=payload,
    # #     blocking=True,
    # #     simulate=False,
    # # )

    # # Transfer first plate (experiment 2) from BMG to inheco and start incubation   # WORKING
    # # edited_to_inheco_wf = helper_functions.replace_wf_node_names(
    # #     workflow=bmg_to_run_incubator_wf, 
    # #     payload=payload
    # # )
    # # experiment_client.start_run(
    # #     edited_to_inheco_wf,
    # #     payload=payload,
    # #     blocking=True,
    # #     simulate=False,
    # # )


    # # WORKING UNTIL HERE! --------------------------------------------

    # # START READING/INCUBATION LOOP
    # # set up payload variables
    # exp1_ot2_location_name = "ot2biobeta_deck3_wide"
    # exp2_ot2_location_name = "ot2bioalpha_deck3_wide"

    # # FOR EXPERIMENT 1 PLATE  # WORKING
    # payload["ot2_node"] = exp1_ot2_node
    # payload["ot2_location_name"] = exp1_ot2_location_name  # when is this needed?
    # payload["ot2_safe_path_name"] = exp1_ot2_safe_path
    # payload["lid_location"] = exp1_lid_location
    # payload["incubator_node"] = exp1_incubator_node
    # payload["incubator_location_name"] = exp1_incubator_location_name
    # payload["incubation_seconds"] = exp1_incubation_seconds

    # # # Transfer plate from exp 1 from incubator to bmg for reading   # WORKING  # TODO: recalibrate z height of exchange
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

    # # # Transfer back into incubator again (REPEAT STEP FROM ABOVE)
    # # edited_to_inheco_wf = helper_functions.replace_wf_node_names(
    # #     workflow=bmg_to_run_incubator_wf, 
    # #     payload=payload
    # # )
    # # experiment_client.start_run(
    # #     edited_to_inheco_wf,
    # #     payload=payload,
    # #     blocking=True,
    # #     simulate=False,
    # # )

    # # FOR EXPERIMENT 2 PLATE  
    # # payload["ot2_node"] = exp2_ot2_node
    # # payload["ot2_location_name"] = exp2_ot2_location_name  # when is this needed?
    # # payload["ot2_safe_path_name"] = exp2_ot2_safe_path
    # # payload["lid_location"] = exp2_lid_location
    # # payload["incubator_node"] = exp2_incubator_node
    # # payload["incubator_location_name"] = exp2_incubator_location_name
    # # payload["incubation_seconds"] = exp2_incubation_seconds # for TESTING   (exp 2 inc time)

    
    # # # Transfer plate from exp 2 from incubator to bmg for reading   # WORKING  # TODO: recalibrate z height of exchange
    # # edited_to_bmg_wf = helper_functions.replace_wf_node_names(
    # #     workflow=incubator_to_run_bmg_wf, 
    # #     payload=payload
    # # )
    # # experiment_client.start_run(
    # #     edited_to_bmg_wf,
    # #     payload=payload,
    # #     blocking=True,
    # #     simulate=False,
    # # )

    # # # Transfer back into incubator again (REPEAT STEP FROM ABOVE)
    # # edited_to_inheco_wf = helper_functions.replace_wf_node_names(
    # #     workflow=bmg_to_run_incubator_wf, 
    # #     payload=payload
    # # )
    # # experiment_client.start_run(
    # #     edited_to_inheco_wf,
    # #     payload=payload,
    # #     blocking=True,
    # #     simulate=False,
    # # )

    # # INOCULATION STEPS!!
    # payload["ot2_node"] = exp1_ot2_node
    # payload["ot2_location_name"] = exp1_ot2_location_name  # when is this needed?
    # payload["ot2_safe_path_name"] = exp1_ot2_safe_path
    # payload["lid_location"] = exp1_lid_location
    # payload["incubator_node"] = exp1_incubator_node
    # payload["incubator_location_name"] = exp1_incubator_location_name
    # payload["incubation_seconds"] = exp1_incubation_seconds # for TESTING  

    # # # Get a new plate from stack   # WORKS
    # # edited_get_new_plate_wf = helper_functions.replace_wf_node_names(
    # #     workflow=get_new_plate_wf, 
    # #     payload=payload
    # # )
    # # experiment_client.start_run(
    # #     edited_get_new_plate_wf,
    # #     payload=payload,
    # #     blocking=True,
    # #     simulate=False,
    # # )

    # # Transfer a plate from the bmg to old position on ot2





    

























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
