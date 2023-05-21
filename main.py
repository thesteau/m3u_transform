import os
import sys
import json
from typing import Dict, Union, Type

from src.m3u_transform import M3UTransformer

key_list: Dict[str, Type[Union[str, bool]]] = {
    "initiator": str, # key to determine replacement
    "replacement": str,  # repalcement key
    "kill_line": str,  # line to remove
    "header": str,  # Fixed constant header on output
    "replace_file": bool, # true to inplace replacement
    "replace_file_value": str # on replacement, the value that will be used such as "-updated", Must not be empty 
}

def validate_settings(settings_file):
    if not os.path.isfile(settings_file):
        print("A settings.json file does not exist. Either pass it as a 3rd argument or include the file in the root directory of the program.")
        sys.exit()

    with open(settings_file) as f:
        settings = json.load(f)

        if not all(key in settings for key in key_list.keys()):
            print("The settings file is missing one or more required keys.")
            print(key_list)
            sys.exit()

        for key, value in settings.items():
            if not value:
                print("Settings entry for " + key + " is empty.")
                sys.exit()

            if not isinstance(value, key_list[key]):
                print("The value of the key " + key + " is not the correct data type " + str(key_list[key]))
                print("The value "+ str(value) + " is of the data type " + str(type(value)) + ", expected "+ str(key_list[key]))
                sys.exit()

    return settings


def validate_folder_and_files(folder):
    if not os.path.isdir(folder):
        print("The specified folder does not exist.")
        os.mkdir(folder)
        print("Creating the folder, please add the appropriate m3u files in.")
        sys.exit()

    files = [f for f in os.listdir(folder) if f.endswith(".m3u")]
    if not files:
        print("No files with the .m3u extension found in the specified folder.")
        sys.exit()

    return files


def process_files(folder, settings_file):
    files = validate_folder_and_files(folder)
    settings = validate_settings(settings_file)

    for file in files:
        file_path = os.path.join(folder, file)
        transformer = M3UTransformer(file_path, settings)
        transformer.transform()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the folder path as an argument.")
        sys.exit()

    folder_path = sys.argv[1]
    settings_file = sys.argv[2] if len(sys.argv) >= 3 else os.path.join(os.curdir, "settings.json")

    process_files(folder_path, settings_file)
