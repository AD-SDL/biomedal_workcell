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
    wf_run_instrument_directory = wf_directory / "run_instrument"
    wf_transfers_directory = wf_directory / "transfers"
    protocol_directory = app_directory / "protocols"

    # # workflow paths (run instruments)
    run_hidex_wf = wf_run_instrument_directory / "run_hidex.yaml"
    run_flex_wf = wf_run_instrument_directory / "run_flex.yaml"
    run_sealer_wf = wf_run_instrument_directory / "run_sealer.yaml"
    run_peeler_wf = wf_run_instrument_directory / "run_peeler.yaml"


    # # workflow paths (set up and tear down related)

    # # workflow paths (pf400 transfers)
    remove_lid_move_to_flex = wf_transfers_directory / "remove_lid_move_to_flex.yaml"
    flex_to_hidex_wf = wf_transfers_directory / "flex_to_hidex_wf.yaml"
    hidex_to_flex_wf = wf_transfers_directory / "hidex_to_flex_wf.yaml"
    flex_to_sealer_wf = wf_transfers_directory / "flex_to_sealer_wf.yaml"
    sealer_to_hidex_wf = wf_transfers_directory / "sealer_to_hidex_wf.yaml"
    hidex_to_peeler_wf = wf_transfers_directory / "hidex_to_peeler_wf.yaml"
    peeler_to_flex_wf = wf_transfers_directory / "peeler_to_flex_wf.yaml"

    # protocol paths (for OT-Flex)
    add_enzyme_protocol = protocol_directory / "pd_cfpe_final.yaml"
    add_substrate_protocol = protocol_directory / "pd_cfpe_final_2.yaml"
    move_from_temp_to_staging_protocol = protocol_directory / "move_C1_A4_temp_mod.py"
    move_to_staging_2_protocol = protocol_directory / "move_to_staging_D1_A4.yaml"
    move_from_staging_to_temp_protocol = protocol_directory / "move_A4_C1_temp_mod.py"


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

    payload = {"current_flex_protocol": str(add_enzyme_protocol)}

    # add fluorescence and enzyme
    experiment_client.start_run(
        run_flex_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    payload = {"current_flex_protocol": str(move_from_temp_to_staging_protocol)}

    # add fluorescence and enzyme
    experiment_client.start_run(
        run_flex_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    # #move from flex to hidex
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

    # move from flex to sealer
    experiment_client.start_run(
        flex_to_sealer_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    # seal
    experiment_client.start_run(
        run_sealer_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    # sealer to hidex
    experiment_client.start_run(
        sealer_to_hidex_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    # run hidex incubate #TODO: specific file name needed in payload
    experiment_client.start_run(
        run_hidex_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    # hidex to peeler
    experiment_client.start_run(
        hidex_to_peeler_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    # run peeler
    experiment_client.start_run(
        run_peeler_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    # peeler to flex staging
    experiment_client.start_run(
        peeler_to_flex_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )


    # flex staging to temp block
    payload = {"current_flex_protocol": str(move_from_staging_to_temp_protocol)}

    experiment_client.start_run(
        run_flex_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )



    # #     #move from hidex to flex 
    # experiment_client.start_run(
    #     hidex_to_flex_wf.resolve(),
    #     payload=payload,
    #     blocking=True,
    #     simulate=False,
    # )

    # payload = {"current_flex_protocol": str(move_from_staging_protocol)}

#     # add fluorescence and enzyme
#     experiment_client.start_run(
#         run_flex_wf.resolve(),
#         payload=payload,
#         blocking=True,
#         simulate=False,
#     )

#     payload = {"current_flex_protocol": str(add_substrate_protocol)}

#     #add substrate
#     experiment_client.start_run(
#         run_flex_wf.resolve(),
#         payload=payload,
#         blocking=True,
#         simulate=False,
#     )

#     payload = {"current_flex_protocol": str(move_to_staging_2_protocol)}

#     # add fluorescence and enzyme
#     experiment_client.start_run(
#         run_flex_wf.resolve(),
#         payload=payload,
#         blocking=True,
#         simulate=False,
#     )

#     #flex to hidex
#     experiment_client.start_run(
#     flex_to_hidex_wf.resolve(),
#     payload=payload,
#     blocking=True,
#     simulate=False,
# )
#     #hidex run?
#     experiment_client.start_run(
#     run_hidex_wf.resolve(),
#     payload=payload,
#     blocking=True,
#     simulate=False,
# )


if __name__ == "__main__":
    main()
