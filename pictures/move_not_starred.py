#!/usr/bin/env python3
# -*- coding : utf-8 -*-
import argparse
import os
import subprocess
from pathlib import Path

VERSION = "1.0"


def get_exiftool_rating(jpeg_file: str) -> int | None:
    rating = None
    exiftool_response = subprocess.check_output(["exiftool", "-rating", jpeg_file]).decode()  # type: ignore
    exiftool_response = exiftool_response.split(":")
    if len(exiftool_response) == 2:
        rating = str(exiftool_response[1]).strip()
        rating = int(rating)
    return rating


def move_raw_file(raw_file: str, move_to_folder: str, dry_run: bool = False) -> None:
    if dry_run:
        print(f"[DRY RUN] Moving {raw_file} to `{move_to_folder}` folder.")
    else:
        Path(move_to_folder).mkdir(exist_ok=True)
        print(f"Moving {raw_file} to `{move_to_folder}` folder.")
        os.replace(raw_file, f"{move_to_folder}/{raw_file}")


def main():
    parser = argparse.ArgumentParser(
        prog="move_not_starred",
        description="Move raw files for jpegs that are not starred to subfolder. Requires exiftool.",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Dry run.",
    )
    parser.add_argument(
        "-p",
        "--picture_extension",
        type=str,
        help="Picture file extension (by default JPG).",
        default="JPG",
    )
    parser.add_argument(
        "-r",
        "--raw_extension",
        type=str,
        help="RAW file extension (by default DNG).",
        default="DNG",
    )
    parser.add_argument(
        "-t",
        "--target",
        type=str,
        help="Target path (by default creates sub folder with the same name as current one).",
    )
    parser.parse_args()
    args = parser.parse_args()
    if args.target is None:
        dir_path = os.getcwd()
        move_to_folder = dir_path.split("\\")[-1]
    else:
        move_to_folder = args.target
    list_of_all_files = os.listdir()
    list_of_all_files = sorted(list_of_all_files)
    list_of_faved_jpegs = []
    # move raw files that jpegs does not exist
    for raw_file in list_of_all_files:
        if raw_file.upper().endswith(f".{args.raw_extension}"):
            jpeg_file = f"{raw_file[:-4]}.{args.picture_extension}"
            jpeg_file_path = Path(jpeg_file)
            if jpeg_file_path.is_file():
                jpeg_rating = get_exiftool_rating(jpeg_file)
                if jpeg_rating and jpeg_rating > 0:
                    print(f"{jpeg_file} - {jpeg_rating}")
                    list_of_faved_jpegs.append(jpeg_file)
                else:
                    # moving raw file of not ranked jpeg
                    move_raw_file(raw_file, move_to_folder, args.dry_run)
            else:
                # moving raw files of not existing jpegs
                move_raw_file(raw_file, move_to_folder, args.dry_run)


if __name__ == "__main__":
    main()
