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
    protocol_directory = app_directory / "protocols"

    # workflow paths (run instruments)
    run_ot2_wf = wf_run_instrument_directory / "run_ot2_wf.yaml"

    # protocol paths (for OT-2)
    # prep_dispense_media = protocol_directory / "prep_dispense_media.py"
    # test_protocol = protocol_directory / "TEST.yaml"
    inocualte_protocol = protocol_directory / "inoculate.py"

    # generate first inoculation ot-2 protocol
    inoculate_protocol_tip_box_location = 4
    current_ot2 = ot2biobeta
    inoculate_tip_box_offsets = current_ot2[inoculate_protocol_tip_box_location]
    ot2_replacement_variables = {
        "tip_location": inoculate_protocol_tip_box_location,
        "x": inoculate_tip_box_offsets[0],
        "y": inoculate_tip_box_offsets[1],
        "z": inoculate_tip_box_offsets[2],
    }
    temp_ot2_file = helper_functions.generate_ot2_protocol(inocualte_protocol, ot2_replacement_variables)
    print(temp_ot2_file)


    # initial payload setup
    payload = {
        "ot2_node": "ot2biobeta",
        "current_ot2_protocol": temp_ot2_file,
        "use_existing_resources": False,
    }

    print(payload)

    # EXPERIMENT LOOP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    """ Human needs to set up OT-2 deck before run starts """

    
    # workflow = Workflow.from_yaml(run_ot2_wf.resolve())
    # for step in workflow.flowdef:
    #     if step.module == "payload.incubator_node":
    #         step.module = ""

    # Run the current OT-2 protocol
    experiment_client.start_run(
        run_ot2_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )






if __name__ == "__main__":
    main()
