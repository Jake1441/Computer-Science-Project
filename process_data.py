import glob
import json
import os.path

"""
    Loads csv data, scraping json and invalid json
    looks for relevant json fields to process against VIAF.
    mainly it is useful only for testing concepts and statistical inferences.
    Author: Jacob Reid
    Date: 8/03/2023
    Compatibilities:
    This program is recommended to run on Python 3.10.x
    Some packages may fail if they are run on older versions or run with unpredictable
    results. 

    The packages required will be provided in a requirements.txt
"""

# GLOBALS
INPUTPATH = {
    "base": "Data",
    "Filtered": "Data\\Filtered",
    "Valid_Json": "Data\\Filtered",
    "Scraped": "Data\\Scraped",
    "Invalid_Data": "Data\\Filtered\\InvalidData"
}

"""
    Check for validity of JSON and check if keys exist
    Debug function resides in this section.   
"""

"""Commonly used functions or loops"""


def write_data(csv_file, file_data):
    """Commits the data back to file."""
    with open(csv_file, 'w', encoding='utf-8') as file:
        for line in file_data:
            file.write(f"{line}" + "\n")


def clean_file(file_name, input_location):
    """Cleans the file name based on its input location."""
    if input_location == "Valid_Json":
        split_file = file_name.split('\\')[-1]
        file_name = f"{INPUTPATH[input_location]}\\filtered_{split_file}"

    if input_location == "Invalid_Data":
        split_file = file_name.split('\\')[-1]
        file_name = f"{INPUTPATH[input_location]}\\invalid_{split_file}"

    if input_location == "Scraped":
        file_name = file_name.split("_")[-2:]
        file_name = "_".join(file_name)
        file_name = f"{INPUTPATH[input_location]}\\scraped_{file_name}"
    return file_name


def validate_json(data):
    """
    Validates the json to make sure its proper data
    """
    try:
        json.loads(data)
    except ValueError:
        return False
    return True


def if_keys_exist(key_vals, json_data):
    """
    Checks if the keys exist in the json data.
    """
    data = {}
    for key in key_vals:
        key_present = json_data.get(key)
        if key_present is None:
            return None
        data[key] = key_present
    return json.dumps(data)


def read_json_file(file_loc):
    """Reads the JSON file and sends its data to the key checker."""
    infile = open(file_loc, "r", encoding='utf-8')
    data = infile.read().splitlines()
    infile.close()
    valid_json = []
    keys_exist = ["name", "remote_ids"]  # these keys must exist so the json can be parsed.
    for json_line in data:
        if json_line != "":
            try:
                json_data = json.loads(json_line.strip())
            except json.decoder.JSONDecodeError as e:
                print(f"Error decoding JSON object: {e}")
            else:
                # this line makes sure that the keys necessary exist in the filtered data.
                # todo: validate keys is causing the quote issues, found and fixed using json.dumps.
                validate_keys = if_keys_exist(keys_exist, json_data)
                if validate_keys is not None:
                    valid_json.append(validate_keys)
    """Make sure the new name has scraped instead of filtered."""
    if valid_json:
        new_name = clean_file(file_loc, "Scraped")
        write_data(new_name, valid_json)


def load_data(csv_file):
    """
    Loads the CSV Data and runs a JSON Validator
    on the string after the first opening curly bracket

    appends string to valid json if valid
    appends string to invalid json if not

    Send details to write data
    """
    valid_json_array = []
    invalid_json_array = []
    with open(csv_file, 'r') as file:
        for line in file:
            if '\x00' not in line:
                start_index = line.index('{')
                line_validity = validate_json(str(line[start_index:]))
                if line_validity:
                    valid_json_array.append(line[start_index:])
                else:
                    invalid_json_array.append(str(line[start_index:]))
        # writing valid json
        file_name = clean_file(csv_file, "Valid_Json")
        write_data(file_name, valid_json_array)  # could this be made simpler ie valid invalid and flag?
        read_json_file(file_name)
        # logic for invalid json data.
        if len(invalid_json_array) > 0:
            file_name = clean_file(csv_file, "Invalid_Data")
            write_data(file_name, invalid_json_array)


def call_load_data(f_name):
    """Call to load the data from the names given."""
    csv_list = glob.glob(os.path.join(INPUTPATH["base"], (f"{f_name}*" + ".csv")))
    for name in csv_list:
        load_data(name)


def jre141_proc_data():
    """
    The main program
    """
    # logic to run load data
    # names to call has an entry and call load data finds entries beginning with
    # each name and loops through them
    names_to_call = ["authors", "works", "editions"]
    for names in names_to_call:
        call_load_data(names)

