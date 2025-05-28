
import tempfile
from pathlib import Path

from ot2_offsets import ot2biobeta, ot2bioalpha
from wei.types.workflow_types import Workflow

def generate_ot2_protocol(template_path, replacement_dict: dict) -> str: 

    # collect template contents and replace variables
    with template_path.open(mode="r") as f: 
        edited_template_contents = f.read()
        for key in replacement_dict.keys(): 
            edited_template_contents = edited_template_contents.replace("$" + key, str(replacement_dict[key]))
            
    # write to another temp file 
    output_file_name = None
    """ create a temporary file using a context manager"""
    with tempfile.NamedTemporaryFile(delete=False) as fp:
        fp.write(edited_template_contents.encode('utf-8'))
        output_file_name = fp.name

    return output_file_name


def collect_ot2_replacement_variables(payload: dict) -> dict:
    replacement_dict = {}
    if payload["ot2_node"] == "ot2bioalpha": 
        tip_box_location = payload["ot2bioalpha_tip_box_location"]
        replacement_dict["tip_location"] = tip_box_location
        replacement_dict["x"] = ot2bioalpha[tip_box_location][0]
        replacement_dict["y"] = ot2bioalpha[tip_box_location][1]
        replacement_dict["z"] = ot2bioalpha[tip_box_location][2]
    elif payload["ot2_node"] == "ot2biobeta": 
        tip_box_location = payload["ot2biobeta_tip_box_location"]
        replacement_dict["tip_location"] = tip_box_location
        replacement_dict["x"] = ot2biobeta[tip_box_location][0]
        replacement_dict["y"] = ot2biobeta[tip_box_location][1]
        replacement_dict["z"] = ot2biobeta[tip_box_location][2]
    else: 
        print("TESTING: unable to collect ot2 replacement variables")
    return replacement_dict


def replace_wf_node_names(workflow: Path, payload: dict): 
    edited_wf = Workflow.from_yaml(workflow.resolve())
    for step in edited_wf.flowdef:
        if step.module == "payload.incubator_node":
            step.module = payload["incubator_node"]
        if step.module == "payload.ot2_node": 
            step.module = payload["ot2_node"]
    return edited_wf


# TESTING
def test_generate_protocol(): 

    replacement_dictionary = {
        "tip_location": 4,
        "x" : 0.0,
        "y": 0.0,
        "z": 0.0,
    }

    # directory paths
    app_directory = Path(__file__).parent.parent
    protocol_directory = app_directory / "protocols"

    # protocol paths (for OT-2)
    inocualte_protocol = protocol_directory / "inoculate.py"
    test_file = generate_ot2_protocol(inocualte_protocol, replacement_dict=replacement_dictionary)
    print(test_file)



