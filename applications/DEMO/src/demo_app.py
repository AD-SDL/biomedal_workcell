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
- Improve comments (continue with numbering steps)
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
        experiment_name="DEMO_Application",
        experiment_description="DEMO experiment application",
    )
    # define a campaign object (useful if we want to group many of these substrate experiments together)
    campaign = CampaignDesign(
        campaign_name="DEMO_Campaign",
        campaign_description="Demo campaign to collect demo experiments",
    )
    # define the experiment client object that will communicate with the WEI server
    experiment_client = ExperimentClient(
        server_host="localhost",
        server_port="8000",
        experiment=experiment_design,
        campaign=campaign,
    )

    # DEFINE PATHS AND VARIABLES ---------------------------------

    # # capture the expriment ID
    experiment_id = experiment_client.experiment.experiment_id

    # directory paths
    app_directory = Path(__file__).parent.parent
    wf_directory = app_directory / "workflows"
    protocol_directory = app_directory / "protocols"

    # workflow paths (run instruments)
    demo_wf = wf_directory / "demo_wf.yaml"

    # protocol paths (for OT-2)
    inoculate_protocol = protocol_directory / "inoculate.py"

    exp1_variables = {
        "incubation_seconds": 15,  # 15 seconds for demo
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

    # initial payload setup  (experiment 1 focused at start)
    payload = {
        "ot2_node": exp1_variables["ot2_node"],
        "ot2_location": exp1_variables["ot2_new_plate_location"],
        "ot2_safe_path": exp1_variables["ot2_safe_path"],
        "tip_box_location": exp1_variables["tip_box_location"],
        "incubator_node": exp1_variables["incubator_node"],
        "incubator_location": exp1_variables["incubator_location"],
        "incubation_seconds": exp1_variables["incubation_seconds"],
        "current_ot2_protocol": None,
        "use_existing_resources": False,
        "bmg_assay_name": "NIDHI",
    }


    # EXPERIMENT STEPS: ------------------------------------------------------------------------------
    """Before running this experiment, extra substrate plates should be prepped
        by running extra_media_plates_app.py. The prepped plates for experiment 1 should
        be placed in ScoClops stack 1, and the prepped plates for experiment 2 should be
        placed in SciClops stack2. The OT-2 deck of ot2biobeta should be prepped for
        first_inoculate_both.py"""

    # edit the ot-2 protocol
    ot2_replacement_variables = helper_functions.collect_ot2_replacement_variables(payload)
    temp_ot2_file_str = helper_functions.generate_ot2_protocol(inoculate_protocol, ot2_replacement_variables)
    payload["current_ot2_protocol"] = temp_ot2_file_str


    # run the demo workflow
    experiment_client.start_run(
        demo_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )


if __name__ == "__main__":
    main()
