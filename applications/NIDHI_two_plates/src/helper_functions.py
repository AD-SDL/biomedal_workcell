
import tempfile
from pathlib import Path

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



