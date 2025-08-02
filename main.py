import os
import sys

from src import validate_settings, validate_folder_and_files
from src.m3u_transform import M3UTransformer


def process_files(folder, settings_file):
    files = validate_folder_and_files(folder)
    settings = validate_settings(settings_file)

    print("FILE NAMES", files)
    print("SETTING DETAILS", settings)

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
