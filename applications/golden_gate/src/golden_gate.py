#!/usr/bin/env python3

"""Golden Gate Experiment"""

from pathlib import Path

from wei import ExperimentClient
from wei.types.experiment_types import CampaignDesign, ExperimentDesign


def main() -> None:
    """Runs the Substrate Experiment Application"""

    # INITIAL EXPERIMENT SETUP
    # define the ExperimentDesign object that will be used to register the experiment
    experiment_design = ExperimentDesign(
        experiment_name="GG_Experiment",
        experiment_description="",
    )
    # define a campaign object (useful if we want to group many of these substrate experiments together)
    campaign = CampaignDesign(
        campaign_name="GG_Campaign",
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
    # directory path
    app_directory = Path(__file__).parent.parent
    wf_directory = app_directory / "workflows"
    wf_run_instrument_directory = wf_directory / "run_instrument"
    wf_transfers_directory = wf_directory / "transfers"
    protocol_directory = app_directory / "protocols"

    # # workflow paths (run instruments)
    run_thermocycler_wf = wf_run_instrument_directory / "run_thermocycler.yaml"
    run_flex_wf = wf_run_instrument_directory / "run_flex.yaml"

    # # workflow paths (set up and tear down related)

    # # workflow paths (pf400 transfers)
    remove_lid_move_to_flex = wf_transfers_directory / "remove_lid_move_to_flex.yaml"
    flex_to_thermocycler_wf = wf_transfers_directory / "flex_to_thermo_wf.yaml"
    thermocycler_to_flex_wf = wf_transfers_directory / "thermocycler_to_flex_wf.yaml"

    # protocol paths (for OT-Flex)
    run_gg = protocol_directory / "gg_flex.py"
    move_to_staging_protocol = protocol_directory / "move_to_staging_B1_A4.yaml"

    #TODO: possibly break up in future when running multiple plates, ie make large quantity of master mix and use repeatedly


    # important variables

    #
    # move to exchange, remove lid, move to flex
    payload = {}

    payload = {"current_flex_protocol": str(run_gg)}

    # add fluorescence and enzyme
    experiment_client.start_run(
        run_flex_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    payload = {"current_flex_protocol": str(move_to_staging_protocol)}

    experiment_client.start_run(
        run_flex_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    # move from flex to thermo
    experiment_client.start_run(
        flex_to_thermocycler_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    #run thermo
    experiment_client.start_run(
        run_thermocycler_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )
    #TODO: make thermocycler file and add to payload
    # move thermo to flex
    # experiment_client.start_run(
    #     hidex_to_flex_wf.resolve(),
    #     payload=payload,
    #     blocking=True,
    #     simulate=False,
    # )

    

if __name__ == "__main__":
    main()
