#!/usr/bin/env python3
"""Experiment application for the Protein Design experiment"""

import time
from datetime import datetime
from pathlib import Path

import helper_functions
from madsci.common.types.experiment_types import ExperimentDesign
from madsci.common.types.node_types import NodeDefinition
from madsci.common.types.resource_types import Resource
from madsci.experiment_application import (
    ExperimentApplication,
    ExperimentApplicationConfig,
)
from pydantic import AnyUrl


class PDApp(ExperimentApplication):
    """PD Experiment Application

    # TODO:

    """

    experiment_design = ExperimentDesign(
        experiment_name="PD_App",
    )
    config = ExperimentApplicationConfig(node_url=AnyUrl("http://localhost:6000"))
    experiment_id = None
    experiment_label = None


    def __init__(self) -> None:
        """Initializes the PD Experiment App"""

        super().__init__()
        self.init_assay_plate_resource_template()
  

    def run_experiment(self) -> None:
        """main experiment function"""

        # DEFINE PATHS AND VARIABLES ========
        run_robots = False  # if False, no robots will run
        run_resources = True
        test_prints = True  # if True, will print out extra info for testing purposes

        # Experiment ID and name
        experiment_id = self.experiment.experiment_id
        experiment_label = "3"

        # Directory paths
        app_directory = Path(__file__).parent.parent   # experiment app
        wf_directory = app_directory / "workflows"  # workflows
        protocol_directory = app_directory / "protocols"    # protocols

        # Workflow paths
        run_ot2_wf = wf_directory / "run_ot2_wf.yaml"
        ot2_to_thermocycler = (
            wf_directory / "ot2_to_thermocycler_wf.yaml"
        )

        # # workflow paths (pf400 transfers)
        # ot2_temp_block_to_thermocycler = wf_directory / "ot2_temp_block_to_thermocycler.yaml"


        # Protocol paths (for OT-2)
        golden_gate_protocol = protocol_directory / "pd_golden_gate_ot2.py"

        payload = {}


    
        # EXPERIMENT ACTIONS -------------------------------------------------------

        #TODO: TEST HARDCODED VERSION
        #run ot2 protocol
        payload["current_ot2_protocol"] = golden_gate_protocol
        workflow = self.workcell_client.submit_workflow(
            run_ot2_wf.resolve(),
            file_inputs={
                "ot2_protocol": payload["current_ot2_protocol"],
            },
        )

        #transfer destination plate to thermocycler and run
        workflow = self.workcell_client.submit_workflow(
            ot2_to_thermocycler.resolve(),
        )
        




if __name__ == "__main__":
    exp_app = PDApp()

    current_time = datetime.now()

    # Start experiment run
    with exp_app.manage_experiment(
        run_name = f"PD_Experiment{current_time.strftime('%Y%m%d_%H%M%S')}",
        run_description = "PD experiment",
    ):
        exp_app.start_app()