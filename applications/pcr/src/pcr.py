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
        experiment_name="PCR_Experiment",
        experiment_description="PCR Experiment",
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

    # # workflow paths (set up and tear down related)

    # # workflow paths (pf400 transfers)
    remove_lid_move_to_flex = wf_transfers_directory / "remove_lid_move_to_flex.yaml"
    flex_to_thermocycler_wf = wf_transfers_directory / "flex_to_thermo_wf.yaml"
    thermocycler_to_flex_wf = wf_transfers_directory / "thermocycler_to_flex_wf.yaml"
    exchange_to_peeler_to_flexA_wf = wf_transfers_directory / "exchange_peeler_flexA_wf.yaml"
    flexA_peeler_flexA_wf = wf_transfers_directory / "flexA_peeler_flexA.yaml"
    flexA_sealer_flexA_wf = wf_transfers_directory / "flexA_sealer_flexA_wf.yaml"

    # protocol paths (for OT-Flex)
    run_pcr = protocol_directory / "pd_pcr_01.py"
    move_source_to_staging_protocol = protocol_directory / "move_to_staging_C1_A4.py"
    move_from_staging_B2_protocol = protocol_directory / "move_from_staging_A4_B2.py"
    move_from_staging_C1_protocol = protocol_directory / "move_from_staging_A4_C1.py"
    move_pcr_to_staging_protocol = protocol_directory / "move_pcr_to_staging.py"

    #TODO: possibly break up in future when running multiple plates, ie make large quantity of master mix and use repeatedly

    # important variables
    payload = {"current_flex_protocol": str(run_pcr)}


    # EXPERIMENT STEPS: ----------------------------------------------

    # TODO: transfer plate into Flex: move to exchange (from where?), remove lid, move to flex

    #assume golden gate product sealed on exchange, dna and mm source plate sealed on C1


    #peel gg product, place in flex B2

    experiment_client.start_run(
        exchange_to_peeler_to_flexA_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    payload = {"current_flex_protocol": str(move_from_staging_B2_protocol)}

    experiment_client.start_run(
        run_flex_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    #peel source plate, place back on C1

    payload = {"current_flex_protocol": str(move_source_to_staging_protocol)}

    experiment_client.start_run(
        run_flex_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    experiment_client.start_run(
        flexA_peeler_flexA_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )


    payload = {"current_flex_protocol": str(move_from_staging_C1_protocol)}

    experiment_client.start_run(
        run_flex_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    payload = {"current_flex_protocol": str(run_pcr)}
    #run pcr experiment
    experiment_client.start_run(
        run_flex_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    #move pcr plate to staging, seal, thermocycle

    payload = {"current_flex_protocol": str(move_pcr_to_staging_protocol)}

    experiment_client.start_run(
        run_flex_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    experiment_client.start_run(
        flex_to_thermocycler_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    #peel pcr plate, return to flex




if __name__ == "__main__":
    main()
