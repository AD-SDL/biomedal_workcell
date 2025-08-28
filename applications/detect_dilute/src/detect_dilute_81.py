#!/usr/bin/env python3

"""PCR Experiment Using Golden Gate Products"""

from pathlib import Path

from wei import ExperimentClient
from wei.types.experiment_types import CampaignDesign, ExperimentDesign


def main() -> None:
    """Runs the Substrate Experiment Application"""

    # INITIAL EXPERIMENT SETUP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # define the ExperimentDesign object that will be used to register the experiment
    experiment_design = ExperimentDesign(
        experiment_name="DD_Experiment",
        experiment_description="DD Experiment",
    )

    # define a campaign object (useful if we want to group many of these substrate experiments together)
    campaign = CampaignDesign(
        campaign_name="ProteinDesign_Campaign",
        campaign_description="Protein Design Campaign",
    )

    # define the experiment client object that will communicate with the WEI server
    experiment_client = ExperimentClient(
        server_host="localhost",
        server_port="8000",
        experiment=experiment_design,
        campaign=campaign,
    )

    # DEFINING PATHS AND VARIABLES -------------------------------

    # directory path(s)
    app_directory = Path(__file__).parent.parent
    wf_directory = app_directory / "workflows"
    wf_run_instrument_directory = wf_directory / "run_instrument"
    wf_transfers_directory = wf_directory / "transfers"
    protocol_directory = app_directory / "protocols"

    # workflow paths (run instruments)
    run_thermocycler_wf = wf_run_instrument_directory / "run_thermocycler.yaml"
    run_flex_wf = wf_run_instrument_directory / "run_flex.yaml"
    run_hidex_wf = wf_run_instrument_directory / "run_hidex.yaml"

    # # workflow paths (set up and tear down related)

    # # workflow paths (pf400 transfers)
    remove_lid_move_to_flex = wf_transfers_directory / "remove_lid_move_to_flex.yaml"
    flex_to_thermocycler_wf = wf_transfers_directory / "flex_to_thermo_wf.yaml"
    thermocycler_to_flex_wf = wf_transfers_directory / "thermocycler_to_flex_wf.yaml"
    exchange_to_peeler_to_flexA_wf = wf_transfers_directory / "exchange_peeler_flexA_wf.yaml"
    flexA_peeler_flexA_wf = wf_transfers_directory / "flexA_peeler_flexA.yaml"
    flexA_sealer_flexA_wf = wf_transfers_directory / "flexA_sealer_flexA_wf.yaml"
    flexA_hidex_wf = wf_transfers_directory / "flex_to_hidex_wf.yaml"

    # protocol paths (for OT-Flex)
    run_dd = protocol_directory / "pd_dilute_81.py"
    move_source_to_staging_protocol = protocol_directory / "move_to_staging_C1_A4.py"
    move_from_staging_B2_protocol = protocol_directory / "move_from_staging_A4_B2.py"
    move_from_staging_C1_protocol = protocol_directory / "move_from_staging_A4_C1.py"
    move_from_staging_B3_protocol = protocol_directory / "move_from_staging_A4_B3.py"
    move_pcr_to_staging_protocol = protocol_directory / "move_pcr_to_staging.py"
    move_C2_to_A4_protocol = protocol_directory / "move_to_staging_C2_A4.py"

    #TODO: possibly break up in future when running multiple plates, ie make large quantity of master mix and use repeatedly

    # important variables
    payload = {"current_flex_protocol": str(run_dd)}


    # EXPERIMENT STEPS: --------------
    # 
    # --------------------------------

#TODO: remove pcr plate from thermo, peel, return, for now assume everything in place

    #assume pcr plate is thermocycled and on exchange, peel and return to B3

    # experiment_client.start_run(
    #     exchange_to_peeler_to_flexA_wf.resolve(),
    #     payload=payload,
    #     blocking=True,
    #     simulate=False,
    # )

    # payload = {"current_flex_protocol": str(move_from_staging_B3_protocol)}

    # experiment_client.start_run(
    #     run_flex_wf.resolve(),
    #     payload=payload,
    #     blocking=True,
    #     simulate=False,
    # )

    # run d&d

    payload = {"current_flex_protocol": str(run_dd)}

    experiment_client.start_run(
        run_flex_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    # remove sybrgreen plate at C2, move to hidex no seal

    payload = {"current_flex_protocol": str(move_C2_to_A4_protocol)}
    experiment_client.start_run(
        run_flex_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )
    experiment_client.start_run(
        flexA_hidex_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )
    experiment_client.start_run(
        run_hidex_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )
    

if __name__ == "__main__":
    main()
