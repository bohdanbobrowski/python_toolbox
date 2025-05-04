#!/usr/bin/env python3
# -*- coding : utf-8 -*-

import subprocess
import os
from pathlib import Path

VERSION = "1.0"

def get_exiftool_rating(jpeg_file: str) -> int|None:
    rating = None
    exiftool_response = subprocess.check_output(["exiftool", "-rating", jpeg_file]).decode()
    exiftool_response = exiftool_response.split(":")
    if len(exiftool_response) == 2:
        rating = str(exiftool_response[1]).strip()
        rating = int(rating)
    return rating

def move_raw_file(raw_file: str, move_to_folder:str):
    Path(move_to_folder).mkdir(exist_ok=True)
    print(f"Moving {raw_file} to `{move_to_folder}` folder.")
    os.replace(raw_file, f"{move_to_folder}/{raw_file}")    

def main(raw_file_extension:str = "DNG", move_to_folder:str|None = None):
    if move_to_folder is None:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        move_to_folder = dir_path.split("\\")[-1]
    list_of_all_files = os.listdir()
    list_of_all_files = sorted(list_of_all_files)
    list_of_faved_jpegs = []
    # move raw files that jpegs does not exist
    for raw_file in list_of_all_files:
        if raw_file.upper().endswith(f".{raw_file_extension}"):
            jpeg_file = f"{raw_file[:-4]}.JPG" 
            jpeg_file_path = Path(jpeg_file)
            if jpeg_file_path.is_file():
                jpeg_rating = get_exiftool_rating(jpeg_file)
                if jpeg_rating and jpeg_rating>0:
                    print(f"{jpeg_file} - {jpeg_rating}")
                    list_of_faved_jpegs.append(jpeg_file)
                else:
                    # moving raw file of not ranked jpeg
                    move_raw_file(raw_file,move_to_folder)
            else:
                # moving raw files of not existing jpegs
                move_raw_file(raw_file,move_to_folder)

if __name__ == "__main__":
    main()
