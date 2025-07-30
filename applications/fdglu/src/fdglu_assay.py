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
        experiment_name="Cell_free_Experiment",
        experiment_description="Cell_free Experiment",
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
    thermo_to_exchange_wf = wf_transfers_directory / "thermo_to_exchange_wf.yaml"
 
    thermocycler_to_flex_wf = wf_transfers_directory / "thermocycler_to_flex_wf.yaml"
    exchange_to_peeler_to_flexA_wf = wf_transfers_directory / "exchange_peeler_flexA_wf.yaml"
    flexA_peeler_flexA_wf = wf_transfers_directory / "flexA_peeler_flexA.yaml"
    flexA_sealer_flexA_wf = wf_transfers_directory / "flexA_sealer_flexA_wf.yaml"
    flexA_hidex_wf = wf_transfers_directory / "flexA_hidex_wf.yaml"

    # protocol paths (for OT-Flex)
    run_fdglu = protocol_directory / "pd_fdglu_assay_01.py"
    move_source_to_staging_protocol = protocol_directory / "move_to_staging_A3_A4.py"
    move_from_staging_B2_protocol = protocol_directory / "move_from_staging_A4_B2.py"
    move_from_staging_C1_protocol = protocol_directory / "move_from_staging_A4_C1.py"
    move_pcr_to_staging_protocol = protocol_directory / "move_pcr_to_staging.py"

    #TODO: possibly break up in future when running multiple plates, ie make large quantity of master mix and use repeatedly

    # important variables
    payload = {"current_flex_protocol": str(run_fdglu)}
    experiment_client.start_run(
        run_flex_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    # move dest plate to the staging area
    payload = {"current_flex_protocol": str(move_source_to_staging_protocol)}
    experiment_client.start_run(
        run_flex_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    #move dest plate to hidex, no seal
    run_info = experiment_client.start_run(
        flexA_hidex_wf.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )

    # TODO: Collect the Hidex data from the run info and do something with it
    hidex_file_name = run_info["hist"]["run Hidex"]["action_msg"]
    output_dir = Path.home() / "runs" / run_info["experiment_id"]
    output_dir.mkdir(parents=True, exist_ok=True)
    experiment_client.get_wf_result_file(run_id=run_info["run_id"], filename=hidex_file_name, output_filepath=output_dir / hidex_file_name)





if __name__ == "__main__":
    main()
