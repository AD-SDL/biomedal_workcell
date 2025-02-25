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
    # directory path
    app_directory = Path(__file__).parent.parent
    wf_directory = app_directory / "workflows"
    # wf_run_instrument_directory = wf_directory / "run_instrument"
    wf_transfers_directory = wf_directory / "transfers"
    # protocol_directory = app_directory / "protocols"

    # # workflow paths (run instruments)
    # run_hidex_wf = wf_run_instrument_directory / "run_hidex.yaml"
    # run_flex_wf = wf_run_instrument_directory / "run_flex.yaml"

    # # workflow paths (set up and tear down related)

    # # workflow paths (pf400 transfers)
    _ = wf_transfers_directory / "remove_lid_move_to_flex.yaml"
    _ = wf_transfers_directory / "flex_to_hidex_wf.yaml"
    hidex_to_flex_wf = wf_transfers_directory / "hidex_to_flex_wf.yaml"

    # protocol paths (for OT-Flex)
    # fluorescence_and_enzyme
    # substrate
    # stop_reaction

    # important variables

    #
    # move to exchange, remove lid, move to flex
    payload = {}

    # print("here")

    # WORKING!
    # experiment_client.start_run(
    #     remove_lid_move_to_flex.resolve(),
    #     payload=payload,
    #     blocking=True,
    #     simulate=False,
    # )

    # add fluorescence and enzyme
    #     experiment_client.start_run(
    #     run_flex_wf.resolve(),
    #     payload=payload,
    #     blocking=True,
    #     simulate=False,
    # )

    #     #move from flex to hidex  WORKING!
    # experiment_client.start_run(
    #     flex_to_hidex_wf.resolve(),
    #     payload=payload,
    #     blocking=True,
    #     simulate=False,
    # )

    #     #run hidex to detect fluorescence
    #     experiment_client.start_run(
    #     run_hidex_wf.resolve(),
    #     payload=payload,
    #     blocking=True,
    #     simulate=False,
    # )

    #     #move from hidex to flex   WORKING!
    experiment_client.start_run(
        hidex_to_flex_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )


#     #add substrate
#     experiment_client.start_run(
#     run_flex_wf.resolve(),
#     payload=payload,
#     blocking=True,
#     simulate=False,
# )

#     #flex to hidex
#     experiment_client.start_run(
#     flex_to_hidex_wf.resolve(),
#     payload=payload,
#     blocking=True,
#     simulate=False,
# )
#     #kinetic run, 20-30 mins, no lid
#     experiment_client.start_run(
#     run_hidex_wf.resolve(),
#     payload=payload,
#     blocking=True,
#     simulate=False,
# )
#     #hidex to flex
#     experiment_client.start_run(
#     hidex_to_flex_wf.resolve(),
#     payload=payload,
#     blocking=True,
#     simulate=False,
# )

#     #add 10x stop reaction
#     experiment_client.start_run(
#     run_flex_wf.resolve(),
#     payload=payload,
#     blocking=True,
#     simulate=False,
# )

#     #flex to hidex
#     experiment_client.start_run(
#     flex_to_hidex_wf.resolve(),
#     payload=payload,
#     blocking=True,
#     simulate=False,
# )

# run hidex?

if __name__ == "__main__":
    main()
