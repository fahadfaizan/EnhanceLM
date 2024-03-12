from pptx import Presentation
from ppt_module.utils.sort_elements import sort_elements
from ppt_module.meta_ppt.create_dict import create_dict
from ppt_module.generate_json import generate_output

def main(ppt_path):
    """
    Extracts the data from a ppt document and converts it into a JSON file.

    Args:
        ppt_path: (string) Path to the ppt document in string format.
    Returns:
        json_with_comment (JSON): JSON file containing all the data in string.
    """
    
    prs = Presentation(ppt_path)
    prs_data = sort_elements(create_dict(prs))
    json = generate_output(prs_data)
    return json