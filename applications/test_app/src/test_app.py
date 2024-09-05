#!/usr/bin/env python3
"""Test experiment application that uses the WEI client to run test workflow."""

from pathlib import Path

from wei import ExperimentClient


def main() -> None:
    """Runs a test WEI workflow"""
    # This defines the Experiment object that will communicate with the WEI server
    exp = ExperimentClient("localhost", "8000", "Test_Experiment")

    # The path to the Workflow definition yaml file
    wf_path = Path(__file__).parent.parent / "workflows" / "test.workflow.yaml"

    # This runs the workflow
    for i in range(1, 4):
        exp.start_run(
            wf_path.resolve(),
            payload={"ot2_protocol": f"/home/rpl/biomedal_workcell/applications/test_app/protocols/ot2_{i}.py"},
            blocking=True,
        )

if __name__ == "__main__":
    main()
