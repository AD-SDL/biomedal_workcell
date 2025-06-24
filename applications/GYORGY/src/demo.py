#!/usr/bin/env python3
"""Experiment application for Chris and Nidhi's substrate experiment"""

from pathlib import Path

from wei import ExperimentClient
from wei.types.experiment_types import CampaignDesign, ExperimentDesign
from wei.types.workflow_types import Workflow

import time
import csv
from datetime import datetime



"""
TODO:
- why does the pf400 move before sciclops remove lid is done?
- does incubator prevent other communication during a incubation if counting down?
- recalibrate bmg nest (small dropping sound needs to be fixed)

"""


def main() -> None:
    """Runs the OT-2 protocol to create extra media plates"""

    # INITIAL EXPERIMENT SETUP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # define the ExperimentDesign object that will be used to register the experiment
    experiment_design = ExperimentDesign(
        experiment_name="GyorgyDemo",
        experiment_description="DemoForGyorgysExp",
    )
    # define a campaign object (useful if we want to group many of these substrate experiments together)
    campaign = CampaignDesign(
        campaign_name="GyorgyDemoCampaign",
        campaign_description="GyorgyDemoCampaign",
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
    run_instrument_wf_directory = wf_directory / "run_instrument"
    protocol_directory = app_directory / "protocols"

    # workflow paths
    demo_wf = wf_directory / "demo_wf.yaml"
    run_flex_wf = run_instrument_wf_directory / "run_flex.yaml"
    # setup_for_first_inoculation_wf = wf_set_up_tear_down_directory / "setup_for_first_inoculation_wf.yaml"

    # protocol paths


    payload = {
    }

    run_info = experiment_client.start_run(
        demo_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

if __name__ == "__main__":
    main()


