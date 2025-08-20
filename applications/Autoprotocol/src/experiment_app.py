"""Experiment application for Priyanka and Rory's autoprotocol experiment"""

from pathlib import Path

from wei import ExperimentClient
from wei.types.experiment_types import CampaignDesign, ExperimentDesign

def main() -> None:
    """Runs autoprotocol workflow"""

    # INITIAL EXPERIMENT SETUP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # define the ExperimentDesign object that will be used to register the experiment
    experiment_design = ExperimentDesign(
        experiment_name="Autoprotocol_Experiment",
        experiment_description="autoprotocol experiment",
        email_addresses=["ryan.lewis@anl.gov", "cstone@anl.gov"],
    )
    # define a campaign object (useful if we want to group many of these substrate experiments together)
    campaign = CampaignDesign(
        campaign_name="Autoprotocol_Campaign",
        campaign_description="Campaign to collect all autoprotocol experiments",
    )
    # define the experiment client object that will communicate with the WEI server
    experiment_client = ExperimentClient(
        server_host="localhost",
        server_port="8000",
        experiment=experiment_design,
        campaign=campaign,
    )

    # DEFINE PATHS AND VARIABLES ---------------------------------
    # directory paths
    app_directory = Path(__file__).parent.parent
    wf_directory = app_directory / "workflows"
    protocol_directory = app_directory / "protocols"

    # workflow paths
    pcr_workflow = wf_directory / "workflow_with_notes.yaml"

    # protocol paths (for OT-2)
    liquid_protocol_python = protocol_directory / "liquid_protocol_2.py"
    # liquid_protocol_yaml = protocol_directory / "liquid_protocol_2.yaml"


    # initial payload setup
    payload = {
        "ot2_protocol": str(liquid_protocol_python),
    }

    # EXPERIMENT STEPS: ------------------------------------------------------------------------------
    # run PCR workflow
    experiment_client.start_run(
        pcr_workflow.resolve(),
        payload=payload,
        blocking=True,
        simulate=False,
    )


if __name__ == "__main__":
    main()
