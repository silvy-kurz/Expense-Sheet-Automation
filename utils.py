from typing import Dict, List
import numpy as np
import subprocess
import pandas as pd
import json


def reverse_number_bool(bool_number):
    """returns reverse of number bool, converts 1 to 0 etc"""
    return int(abs(bool_number - 1))


def larger_than_threshold_number_bool(number, threshold):
    return int(np.ceil((number - threshold) / (abs(number - threshold) + 1)))


def oddness_number_boolean(number):
    """checks for oddness of input, returns 1 if it is"""
    odd_number_branchless_bool = np.ceil(number / 2 - number // 2)
    bool_accounting_for_zero = np.ceil(number / (number + 1)) * reverse_number_bool(
        odd_number_branchless_bool
    )
    return int(bool_accounting_for_zero)


def write_to_clipboard(output, function):
    process = subprocess.Popen(
        function, env={"LANG": "en_US.UTF-8"}, stdin=subprocess.PIPE
    )
    process.communicate(output.encode("utf-8"))


def read_file(file_name):
    """reads a txt file and returns a list output with each line being an item"""
    with open(file_name) as rf:
        file = rf.readlines()
        lis = [line[: len(line) - 1] for line in file]

    return lis


def list_dicts_to_excel(data_list, file_name):
    """
    Convert a list of dictionaries to an Excel file.

    :param data_list: List of dictionaries where each dictionary represents a row.
    :param file_name: Name of the output Excel file.
    """
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data_list)

    # Write the DataFrame to an Excel file
    df.to_excel(file_name, index=False, engine="openpyxl")


def dict_categories_to_excel_single_sheet(data_dict, file_name):
    """
    Convert a dictionary of categories (each with a list of dictionaries) to a single Excel sheet,
    with each category having its own header row, followed by column headers and then data rows.
    If a category has no items, only the category header and a blank row will be added.

    :param data_dict: Dictionary where each key is a category and each value is a list of dictionaries (or an empty list).
    :param file_name: Name of the output Excel file.
    """
    # Initialize an empty list to hold the data
    combined_data = []

    for category, item_list in data_dict.items():
        if item_list:  # If the item list is not empty
            # Convert the list of dictionaries to a DataFrame
            df: pd.DataFrame = pd.DataFrame(item_list)

            # Create a DataFrame for the category header
            header_df = pd.DataFrame(
                [[category] + [""] * (len(df.columns) - 1)], columns=df.columns
            )

            # Create a DataFrame for the column headers
            column_headers_df = pd.DataFrame([df.columns.tolist()], columns=df.columns)

            # Append the category header row
            combined_data.append(header_df)
            # Append the column headers row
            combined_data.append(column_headers_df)
            # Append the actual data rows
            combined_data.append(df)

        else:  # If the item list is empty
            # Create a simple header with one column for the category name
            header_df = pd.DataFrame(
                [[category] + [""] * (len(df.columns) - 1)], columns=df.columns
            )
            combined_data.append(header_df)

        # Append a blank row as a buffer between categories
        # sub_total_df = pd.DataFrame([["SUBTOTAL"] + ["0"] + [''] * (len(df.columns) - 2)], columns=df.columns)
        # combined_data.append(sub_total_df)
        combined_data.append(
            pd.DataFrame([[""] * len(header_df.columns)], columns=header_df.columns)
        )

    # Concatenate all parts into a single DataFrame
    final_df = pd.concat(combined_data, ignore_index=True)

    # Write the final DataFrame to an Excel file
    final_df.to_excel(file_name, index=False, header=False, engine="openpyxl")


# IF EVER YOU NEED TO CONVERT THIS TO READING FROM EXCEL ASK GPT FOR A FUNCTION TO READ AN EXCEL FILE
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


def read_dict_from_json(file_path) -> Dict[str, List[Dict[str, str | int]]]:
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


def determine_if_just_string(item: str) -> bool:
    return all(character.isalpha() or character.isspace() for character in item)


def determine_if_just_numbers(item: str) -> bool:
    while "." in item:
        item = item[0 : item.index(".")] + item[item.index(".") + 1 :]
        print(item)
    while "," in item:
        item = item[0 : item.index(",")] + item[item.index(",") + 1 :]

    return item.isnumeric()


def determine_if_date_format(item: str) -> bool:
    if item[0:2].isnumeric() and item[2] == "-" and item[3:5].isnumeric():
        return int(item[3:5]) <= 12
    return False
