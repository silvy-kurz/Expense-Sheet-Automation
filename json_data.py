import json
from typing import Dict, List


def write_dict_to_json(data, file_path):
    """
    Writes a dictionary to a JSON file.

    Parameters:
    data (dict): The dictionary to write to the JSON file.
    file_path (str): The path to the JSON file.
    """
    try:
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data successfully written to {file_path}")
    except Exception as e:
        print(f"Error writing to JSON file: {e}")


def read_dict_from_json(file_path) -> Dict[str, List[Dict[str, str]]]:
    """
    Reads a dictionary from a JSON file.

    Parameters:
    file_path (str): The path to the JSON file.

    Returns:
    dict: The dictionary read from the JSON file.
    """
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
        return data
    except Exception as e:
        print(f"Error reading from JSON file: {e}")
        return {"": [{"": ""}]}
