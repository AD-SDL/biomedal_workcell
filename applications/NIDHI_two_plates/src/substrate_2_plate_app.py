#!/usr/bin/env python3
"""Experiment application for Chris and Nidhi's substrate experiment"""

from pathlib import Path

from wei import ExperimentClient
from wei.types.experiment_types import CampaignDesign, ExperimentDesign
from wei.types.workflow_types import Workflow

from ot2_offsets import ot2biobeta, ot2bioalpha
import helper_functions
import time
import csv
from datetime import datetime



"""
TODO:
- FIX SLEEP TIMES -> How long to sleep after plate 1 stops circulating. Check inner and outer loops.
- alter inoculation protocol to only drop tip the first transfer but replace tips the rest of the transfers
- why does the pf400 move before sciclops remove lid is done?
- does incubator prevent other communication during a incubation if counting down?
- why is ot2bioalpha not connecting?
- recalibrate bmg nest (small dropping sound needs to be fixed)
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
    wf_transfers_directory = wf_directory / "transfers"
    protocol_directory = app_directory / "protocols"

    # workflow paths (run instruments)
    setup_for_first_inoculation_wf = wf_set_up_tear_down_directory / "setup_for_first_inoculation_wf.yaml"
    run_ot2_wf = wf_run_instrument_directory / "run_ot2_wf.yaml"
    ot2_to_run_bmg_wf = wf_run_instrument_directory / "ot2_to_run_bmg_wf.yaml"
    bmg_to_run_incubator_wf = wf_run_instrument_directory / "bmg_to_run_incubator_wf.yaml"
    incubator_to_run_bmg_wf = wf_run_instrument_directory / "incubator_to_run_bmg_wf.yaml"
    incubator_to_run_bmg_PF400_LID_wf = wf_run_instrument_directory / "incubator_to_run_bmg_PF400_LID_wf.yaml"
    get_new_plate_wf = wf_set_up_tear_down_directory / "get_new_plate_wf.yaml"
    replace_ot2_old_wf = wf_transfers_directory / "replace_ot2_old_wf.yaml"
    remove_old_substrate_plate_wf = wf_set_up_tear_down_directory / "remove_old_substrate_plate_wf.yaml"
    at_end_bmg_to_trash_wf = wf_set_up_tear_down_directory / "at_end_bmg_to_trash_wf.yaml"


    # protocol paths (for OT-2)
    first_inoculate_both_protocol = protocol_directory / "first_inoculate_both.py"
    inoculate_protocol = protocol_directory / "inoculate.py"

    # experiment 1: incubation = 1 hr cycles, transfers every 10 hours
    exp1_variables = {
        "incubation_seconds": 720,   # TESTING
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
        "incubation_seconds": 200,   # TESTING
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
    csv_data_direcory = "/home/rpl/workspace/Nidhi_data"
    experiment_label = "2a"
    transfer_loop_num = 0       # outer loop
    incubation_loop_num = 0     # inner loop
    exp1_reading_num_in_plate = 1
    exp2_reading_num_in_plate = 1
    exp1_plate_num = 1
    exp2_plate_num = 1
    exp1_into_incubator_time = None
    exp2_into_incubator_time = None
    total_transfers = 20
    continue_exp1 = True
    continue_exp2 = True

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
        "trash_stack": exp1_variables["trash_stack"],
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

    # 3.) WFs: Transfer experiment 1 plate to bmg, read, then place into incubator -- Done
    timestamp_now = int(datetime.now().timestamp())
    payload["bmg_data_output_name"] = (
        f"{experiment_label}_{timestamp_now}_{experiment_id}_exp1_{exp1_plate_num}_{exp1_reading_num_in_plate}.txt"
    )
    # ot2 to bmg
    run_info = experiment_client.start_run(
        ot2_to_run_bmg_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )
    exp1_reading_num_in_plate += 1

    # write utc bmg timestamp to csv data file
    helper_functions.write_timestamps_to_csv(
        csv_directory_path=csv_data_direcory,
        experiment_id=experiment_id,
        bmg_filename=payload["bmg_data_output_name"],
        accurate_timestamp=run_info.steps[4].end_time,  # index 4 = bmg reading
    )

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

    # capture incubation start time
    exp1_into_incubator_time = time.time()
    print(f"experiment 1: incubation started at {exp1_into_incubator_time}")  # TESTING

    # 4.) WFs: Transfer experiment 2 plate to bmg, read, then place into incubator -- Done 
    # update payload variables
    payload["ot2_location"] = exp1_variables["ot2_old_plate_location"]   # ok that this says exp1!
    payload["lid_location"] = exp2_variables["lid_location"]
    payload["incubator_node"] = exp2_variables["incubator_node"]
    payload["incubator_location"] = exp2_variables["incubator_location"]
    payload["incubation_seconds"] = exp2_variables["incubation_seconds"]
    
    # # ot2 to bmg
    timestamp_now = int(datetime.now().timestamp())
    payload["bmg_data_output_name"] = (
        f"{experiment_label}_{timestamp_now}_{experiment_id}_exp2_{exp2_plate_num}_{exp2_reading_num_in_plate}.txt"
    )
    experiment_client.start_run(
        ot2_to_run_bmg_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )
    # write utc bmg timestamp to csv data file
    helper_functions.write_timestamps_to_csv(
        csv_directory_path=csv_data_direcory,
        experiment_id=experiment_id,
        bmg_filename=payload["bmg_data_output_name"],
        accurate_timestamp=run_info.steps[4].end_time,  # index 4 = bmg reading
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
    while time.time() - exp1_into_incubator_time < exp1_variables["incubation_seconds"]: 
        print(f"will continue in... {int(exp1_variables["incubation_seconds"]-(time.time() - exp1_into_incubator_time))} seconds")
        time.sleep(5) # 5 seconds

    """Now that both experiment plates are in the incubator, 
        we can start the both the outer transfers loop and
        the inner incubation loop."""
    
    # LOOP START -----------------------------------------------------------

    # TESTING
    incubation_loop_num = 8
    # continue_exp1 = False
    exp1_plate_num = 20
    transfer_loop_num = 2

    while exp1_plate_num < 21:   # TODO: What should this number be?
        while incubation_loop_num < 10: # Inner loop, each loop ~ 1 hr  -- DONE

            """NOTEs: 
                - ~ 8 min to remove, read, and replace
            """

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
                    f"{experiment_label}_{timestamp_now}_{experiment_id}_exp1_{exp1_plate_num}_{exp1_reading_num_in_plate}.txt"
                )
                # TESTING
                print("payload before reading plate 1")
                print(payload)

                edited_to_bmg_wf = helper_functions.replace_wf_node_names(
                    workflow=incubator_to_run_bmg_wf, 
                    payload=payload
                )
                run_info = experiment_client.start_run(
                    edited_to_bmg_wf,
                    payload=payload,
                    blocking=True,
                    simulate=False,
                )
                # write utc bmg timestamp to csv data file
                helper_functions.write_timestamps_to_csv(
                    csv_directory_path=csv_data_direcory,
                    experiment_id=experiment_id,
                    bmg_filename=payload["bmg_data_output_name"],
                    accurate_timestamp=run_info.steps[7].end_time,  # index 7 = bmg reading
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
                    f"{experiment_label}_{timestamp_now}_{experiment_id}_exp2_{exp2_plate_num}_{exp2_reading_num_in_plate}.txt"
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
                # write utc bmg timestamp to csv data file
                run_info = helper_functions.write_timestamps_to_csv(
                    csv_directory_path=csv_data_direcory,
                    experiment_id=experiment_id,
                    bmg_filename=payload["bmg_data_output_name"],
                    accurate_timestamp=run_info.steps[7].end_time,  # index 7 = bmg reading
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
            # TODO: HOW LONG TO SLEEP IF EXP 1 NOT RUNNING ANYMORE?
            while (time.time() - exp1_into_incubator_time) < exp1_variables["incubation_seconds"]: 
                print(f"will continue in... {int(exp1_variables["incubation_seconds"]-(time.time() - exp1_into_incubator_time))} seconds")
                time.sleep(5)

            incubation_loop_num += 1

        # TRANSFERS HANDLING --------------------------------------------
        """One loop in the transfers loop (outer loop, is roughly 
            10 hours or 10 incubation loops (inner loops)"""
        
        # TRASH exp 1 plate 20  --> DONE
        if exp1_plate_num == 20:    
            """means final incubaton cycle on experiment 1 plate is complete. 
                Need to complete the final absorbance reading on the final
                plate in experiment 1."""
            # TODO: replace with variables (total loop #?)
            continue_exp1 = False

            # change variables
            payload["lid_location"] = exp1_variables["lid_location"]
            payload["incubator_node"] = exp1_variables["incubator_node"]
            payload["incubator_location"] = exp1_variables["incubator_location"]
            payload["incubation_seconds"] = exp1_variables["incubation_seconds"]
            payload["trash_stack"] = exp1_variables["trash_stack"]

            # inheco incubator to bmg
            timestamp_now = int(datetime.now().timestamp())
            payload["bmg_data_output_name"] = (
                f"{experiment_label}_{timestamp_now}_{experiment_id}_exp1_{exp1_plate_num}_{exp1_reading_num_in_plate}.txt"
            )
            edited_to_bmg_wf = helper_functions.replace_wf_node_names(
                workflow=incubator_to_run_bmg_wf, 
                payload=payload
            )
            run_info = experiment_client.start_run(
                edited_to_bmg_wf,
                payload=payload,
                blocking=True,
                simulate=False,
            )
            # write utc bmg timestamp to csv data file
            helper_functions.write_timestamps_to_csv(
                csv_directory_path=csv_data_direcory,
                experiment_id=experiment_id,
                bmg_filename=payload["bmg_data_output_name"],
                accurate_timestamp=run_info.steps[7].end_time,  # index 7 = bmg reading
            )
            exp1_reading_num_in_plate += 1

            # bmg to trash stack   # TODO: TEST!
            experiment_client.start_run(
                at_end_bmg_to_trash_wf.resolve(),
                payload=payload,
                blocking=True,
                simulate=False,
            )


        if continue_exp1: 
            # set up variables 
            payload["ot2_node"] = exp1_variables["ot2_node"]
            payload["ot2_location"] = exp1_variables["ot2_old_plate_location"]   # is this right?
            payload["ot2_safe_path"] = exp1_variables["ot2_safe_path"]
            payload["stack"] = exp1_variables["new_stack"]
            payload["lid_location"] = exp1_variables["lid_location"]
            payload["tip_box_location"] = exp1_variables["tip_box_location"]
            payload["incubator_node"] = exp1_variables["incubator_node"]
            payload["incubator_location"] = exp1_variables["incubator_location"]
            payload["incubation_seconds"] = exp1_variables["incubation_seconds"]

            # inheco incubator to bmg (BUT REPLACE LID ON PF400 lidnest 3 narrow)  -- DONE
            timestamp_now = int(datetime.now().timestamp())
            payload["bmg_data_output_name"] = (
                f"{experiment_label}_{timestamp_now}_{experiment_id}_exp1_{exp1_plate_num}_{exp1_reading_num_in_plate}.txt"
            )
            edited_to_bmg_wf = helper_functions.replace_wf_node_names(
                workflow=incubator_to_run_bmg_PF400_LID_wf, 
                payload=payload
            )
            run_info = experiment_client.start_run(
                edited_to_bmg_wf,
                payload=payload,
                blocking=True,
                simulate=False,
            )
            # write utc bmg timestamp to csv data file
            helper_functions.write_timestamps_to_csv(
                csv_directory_path=csv_data_direcory,
                experiment_id=experiment_id,
                bmg_filename=payload["bmg_data_output_name"],
                accurate_timestamp=run_info.steps[7].end_time,  # index 7 = bmg reading
            )
            exp1_reading_num_in_plate += 1

            # bmg to OLD OT-2 location -- DONE
            experiment_client.start_run(
                replace_ot2_old_wf.resolve(),
                payload=payload,
                blocking=True,
                simulate=False,
            )

            # # get a new plate from the stack -- DONE
            payload["ot2_location"] = exp1_variables["ot2_new_plate_location"]
            payload["ot2_safe_path"] = exp1_variables["ot2_safe_path"]
            edited_get_new_plate_wf = helper_functions.replace_wf_node_names(
                workflow=get_new_plate_wf, 
                payload=payload
            )
            experiment_client.start_run(
                edited_get_new_plate_wf,
                payload=payload,
                blocking=True,
                simulate=False,
            )

            # run ot2 inoculation protocol  -- DONE
            ot2_replacement_variables = helper_functions.collect_ot2_replacement_variables(payload)
            temp_ot2_file_str = helper_functions.generate_ot2_protocol(inoculate_protocol, ot2_replacement_variables)
            payload["current_ot2_protocol"] = temp_ot2_file_str

            edited_ot2_wf = helper_functions.replace_wf_node_names(
                workflow=run_ot2_wf, 
                payload=payload
            )
            experiment_client.start_run(
                edited_ot2_wf,
                payload=payload,
                blocking=True,
                simulate=False,
            )

            # increase variables
            exp1_plate_num += 1
            exp1_variables["tip_box_location"] += 1
            
            # reset variables if necessary
            exp1_reading_num_in_plate = 1
            if exp1_variables["tip_box_location"] == 12:   
                exp1_variables["tip_box_location"] = 4

            # ot2 to bmg (new plate)  -- DONE
            payload["ot2_location"] = exp1_variables["ot2_new_plate_location"]
            timestamp_now = int(datetime.now().timestamp())
            payload["bmg_data_output_name"] = (
                f"{experiment_label}_{timestamp_now}_{experiment_id}_exp1_{exp1_plate_num}_{exp1_reading_num_in_plate}.txt"
            )
            run_info = experiment_client.start_run(
                ot2_to_run_bmg_wf.resolve(),
                payload=payload,
                blocking=True,
                simulate=False,
            )
            exp1_reading_num_in_plate += 1

            # write utc bmg timestamp to csv data file
            helper_functions.write_timestamps_to_csv(
                csv_directory_path=csv_data_direcory,
                experiment_id=experiment_id,
                bmg_filename=payload["bmg_data_output_name"],
                accurate_timestamp=run_info.steps[4].end_time,  # index 4 = bmg reading
            )

            # bmg to inheco incubator   -- DONE
            payload["incubator_node"] = exp1_variables["incubator_node"]  # redundant but feels safer
            payload["incubator_location"] = exp1_variables["incubator_location"]
            payload["incubation_seconds"] = exp1_variables["incubation_seconds"]
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

            # remove the old plate to trash stack -- DONE
            payload["trash_stack"] = exp1_variables["trash_stack"]
            payload["ot2_location"] = exp1_variables["ot2_old_plate_location"]
            edited_old_to_trash_wf = helper_functions.replace_wf_node_names(
                workflow=remove_old_substrate_plate_wf, 
                payload=payload
            )
            experiment_client.start_run(
                edited_old_to_trash_wf,
                payload=payload,
                blocking=True,
                simulate=False,
            )

        # trash experiment 2 plate if complete
        if exp2_plate_num == 20: 
            """means final incubaton cycle on experiment 2 plate is complete. 
                Need to complete the final absorbance reading on the final
                plate in experiment 2."""
            # TODO: replace with variables (total loop #?)
            continue_exp2 = False

            # change variables
            # payload["ot2_location"] = exp1_variables["ot2_new_plate_location"]   # needed?
            payload["lid_location"] = exp2_variables["lid_location"]
            payload["incubator_node"] = exp2_variables["incubator_node"]
            payload["incubator_location"] = exp2_variables["incubator_location"]
            payload["incubation_seconds"] = exp2_variables["incubation_seconds"]
            payload["trash_stack"] = exp2_variables["trash_stack"]

            # inheco incubator to bmg
            timestamp_now = int(datetime.now().timestamp())
            payload["bmg_data_output_name"] = (
                f"{experiment_label}_{timestamp_now}_{experiment_id}_exp2_{exp2_plate_num}_{exp2_reading_num_in_plate}.txt"
            )
            edited_to_bmg_wf = helper_functions.replace_wf_node_names(
                workflow=incubator_to_run_bmg_wf, 
                payload=payload
            )
            run_info = experiment_client.start_run(
                edited_to_bmg_wf,
                payload=payload,
                blocking=True,
                simulate=False,
            )
            # write utc bmg timestamp to csv data file
            helper_functions.write_timestamps_to_csv(
                csv_directory_path=csv_data_direcory,
                experiment_id=experiment_id,
                bmg_filename=payload["bmg_data_output_name"],
                accurate_timestamp=run_info.steps[7].end_time,  # index 7 = bmg reading
            )
            exp2_reading_num_in_plate += 1

            # bmg to trash stack  
            experiment_client.start_run(
                at_end_bmg_to_trash_wf.resolve(),
                payload=payload,
                blocking=True,
                simulate=False,
            )

        if transfer_loop_num % 2 == 0 and continue_exp2:
            """Only transfer exp 2 every 20 hours, one transfer loop = ~10 hrs"""
            
            # set up variables 
            payload["ot2_node"] = exp2_variables["ot2_node"]
            payload["ot2_location"] = exp2_variables["ot2_old_plate_location"]   
            payload["ot2_safe_path"] = exp2_variables["ot2_safe_path"]
            payload["stack"] = exp2_variables["new_stack"]
            payload["lid_location"] = exp2_variables["lid_location"]
            payload["tip_box_location"] = exp2_variables["tip_box_location"]
            payload["incubator_node"] = exp2_variables["incubator_node"]
            payload["incubator_location"] = exp2_variables["incubator_location"]
            payload["incubation_seconds"] = exp2_variables["incubation_seconds"]

            # inheco incubator to bmg (BUT REPLACE LID ON PF400 lidnest 3 narrow)  -- DONE
            timestamp_now = int(datetime.now().timestamp())
            payload["bmg_data_output_name"] = (
                f"{experiment_label}_{timestamp_now}_{experiment_id}_exp2_{exp2_plate_num}_{exp2_reading_num_in_plate}.txt"
            )
            edited_to_bmg_wf = helper_functions.replace_wf_node_names(
                workflow=incubator_to_run_bmg_PF400_LID_wf, 
                payload=payload
            )
            run_info = experiment_client.start_run(
                edited_to_bmg_wf,
                payload=payload,
                blocking=True,
                simulate=False,
            )
            # write utc bmg timestamp to csv data file
            helper_functions.write_timestamps_to_csv(
                csv_directory_path=csv_data_direcory,
                experiment_id=experiment_id,
                bmg_filename=payload["bmg_data_output_name"],
                accurate_timestamp=run_info.steps[7].end_time,  # index 7 = bmg reading
            )
            exp2_reading_num_in_plate += 1

            # bmg to OLD OT-2 location -- DONE
            experiment_client.start_run(
                replace_ot2_old_wf.resolve(),
                payload=payload,
                blocking=True,
                simulate=False,
            )

            # get a new plate from the stack  -- DONE
            payload["ot2_location"] = exp2_variables["ot2_new_plate_location"]
            payload["ot2_safe_path"] = exp2_variables["ot2_safe_path"]
            edited_get_new_plate_wf = helper_functions.replace_wf_node_names(
                workflow=get_new_plate_wf, 
                payload=payload
            )
            experiment_client.start_run(
                edited_get_new_plate_wf,
                payload=payload,
                blocking=True,
                simulate=False,
            )

            # # run ot2 inoculation protocol -- TODO
            # # TODO: GET OT2BIOALPHA WORKING
            # ot2_replacement_variables = helper_functions.collect_ot2_replacement_variables(payload)
            # temp_ot2_file_str = helper_functions.generate_ot2_protocol(inoculate_protocol, ot2_replacement_variables)
            # payload["current_ot2_protocol"] = temp_ot2_file_str

            # edited_ot2_wf = helper_functions.replace_wf_node_names(
            #     workflow=run_ot2_wf, 
            #     payload=payload
            # )
            # experiment_client.start_run(
            #     edited_ot2_wf,
            #     payload=payload,
            #     blocking=True,
            #     simulate=False,
            # )

            # increase variables
            exp2_plate_num += 1
            exp2_variables["tip_box_location"] += 1
            
            # reset variables if necessary
            exp2_reading_num_in_plate = 1
            if exp2_variables["tip_box_location"] == 12:   
                exp2_variables["tip_box_location"] = 4

            # ot2 to bmg (new plate) -- DONE
            payload["ot2_location"] = exp2_variables["ot2_new_plate_location"]
            timestamp_now = int(datetime.now().timestamp())
            payload["bmg_data_output_name"] = (
                f"{experiment_label}_{timestamp_now}_{experiment_id}_exp2_{exp2_plate_num}_{exp2_reading_num_in_plate}.txt"
            )
            run_info = experiment_client.start_run(
                ot2_to_run_bmg_wf.resolve(),
                payload=payload,
                blocking=True,
                simulate=False,
            )
            exp2_reading_num_in_plate += 1

            # write utc bmg timestamp to csv data file
            helper_functions.write_timestamps_to_csv(
                csv_directory_path=csv_data_direcory,
                experiment_id=experiment_id,
                bmg_filename=payload["bmg_data_output_name"],
                accurate_timestamp=run_info.steps[4].end_time,  # index 4 = bmg reading
            )

            # bmg to inheco incubator  -- DONE
            payload["incubator_node"] = exp2_variables["incubator_node"]  # redundant but feels safer
            payload["incubator_location"] = exp2_variables["incubator_location"]
            payload["incubation_seconds"] = exp2_variables["incubation_seconds"]
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

            # remove the old plate to trash stack  -- DONE
            payload["trash_stack"] = exp2_variables["trash_stack"]
            payload["ot2_location"] = exp2_variables["ot2_old_plate_location"]
            edited_old_to_trash_wf = helper_functions.replace_wf_node_names(
                workflow=remove_old_substrate_plate_wf, 
                payload=payload
            )
            experiment_client.start_run(
                edited_old_to_trash_wf,
                payload=payload,
                blocking=True,
                simulate=False,
            )

        # sleep until experiment 1 incubation time is complete
        if continue_exp1: 
            while (time.time() - exp1_into_incubator_time) < exp1_variables["incubation_seconds"]: 
                print(f"will continue in... {int(exp1_variables["incubation_seconds"]-(time.time() - exp1_into_incubator_time))} seconds")
                time.sleep(5)
        # else:    
        #     # TODO: HOW LONG TO SLEEP IN THIS CASE?
        #     if continue_exp2: 
        #         while (time.time() - exp2_into_incubator_time) < exp1_variables["incubation_seconds"]: 
        #             print(f"will continue in... {int(exp2_variables["incubation_seconds"]-(time.time() - exp1_into_incubator_time))} seconds")
        #             time.sleep(5)


        transfer_loop_num += 1







    

if __name__ == "__main__":
    main()
