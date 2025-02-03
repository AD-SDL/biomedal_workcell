#!/usr/bin/env python3

"""Final operations of Gyorgy experiment"""

from pathlib import Path

from wei import ExperimentClient
from wei.types.experiment_types import CampaignDesign, ExperimentDesign


def main() -> None:
    """Runs the Substrate Experiment Application"""

    # INITIAL EXPERIMENT SETUP
    # define the ExperimentDesign object that will be used to register the experiment
    experiment_design = ExperimentDesign(
        experiment_name="PD_Experiment",
        experiment_description="",
    )
    # define a campaign object (useful if we want to group many of these substrate experiments together)
    campaign = CampaignDesign(
        campaign_name="PD_Campaign",
        campaign_description="",
    )
    # define the experiment client object that will communicate with the WEI server
    experiment_client = ExperimentClient(
        server_host="localhost",
        server_port="8000",
        experiment=experiment_design,
        campaign=campaign,
    )

    # DEFINING PATHS AND VARIABLES
    # directory paths
    app_directory = Path(__file__).parent.parent
    wf_directory = app_directory / "workflows"
    wf_set_up_tear_down_directory = wf_directory / "set_up_tear_down"
    wf_run_instrument_directory = wf_directory / "run_instrument"
    wf_transfers_directory = wf_directory / "transfers"
    protocol_directory = app_directory / "protocols"

    # workflow paths (run instruments)
    run_hidex_fluorescence_wf
    run_flex_wf

    # workflow paths (set up and tear down related)

    # workflow paths (pf400 transfers)
    remove_lid_move_to_flex = wf_transfers_directory / "remove_lid_move_to_flex.yaml"
    flex_to_hidex_wf
    hidex_to_flex_wf

    # protocol paths (for OT-Flex)
    fluorescence_and_enzyme

    # important variables 


    #
    #move to exchange, remove lid, move to flex
    payload = {}

    experiment_client.start_run(
    remove_lid_move_to_flex.resolve(),
    payload=payload,
    blocking=True,
    simulate=False,
)
    #add fluorescence and enzyme

    #move from flex to hidex
    experiment_client.start_run(
    flex_to_hidex_wf.resolve(),
    payload=payload,
    blocking=True,
    simulate=False,
)

    #run hidex to detect fluorescence
    experiment_client.start_run(
    run_hidex_fluorescence_wf.resolve(),
    payload=payload,
    blocking=True,
    simulate=False,
)

    #move from hidex to flex

    #add substrate

    #flex to hidex, kinetic run, 20-30 mins, no lid

    #hidex to flex

    #add 10x stop reaction

    #flex to hidex

    #run hidex?