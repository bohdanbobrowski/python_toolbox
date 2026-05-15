import argparse
import csv
import math
import os
import subprocess
import sys
from fnmatch import filter


def exiftool_csv_save(save: bool = True):
    if not save:
        print("DRY RUN!")
    with open("exiftool.csv", newline="", encoding="utf8") as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
        for row in csv_reader:
            cnt = 0
            if os.path.isfile(row.get("SourceFile")):
                command = [
                    "exiftool",
                    # "-codedcharacterset=utf8", # TODO: fix title/object name encoding!
                    "-m",
                    "-overwrite_original",
                ]
                lat = None
                lng = None
                for key in row.keys():
                    try:
                        if key not in ["", "SourceFile"]:
                            value = row[key].strip()
                            if value:
                                if key == "Title":
                                    iptc_object_name = value[:64]
                                    command.append(f"-iptc:ObjectName={iptc_object_name}")
                                    command.append("-iptc:CodedCharacterSet=UTF8")
                                elif key in ["FocalLength", "ISO"]:
                                    try:
                                        command.append(f"-{key}={int(value)}")
                                    except ValueError:
                                        pass
                                elif key in ["latitude", "gpslatitude", "XMP:GPSLatitude"]:
                                    try:
                                        lat = float(value)
                                        ff = 10**5
                                        lat = math.ceil(lat * ff) / ff
                                    except ValueError:
                                        pass
                                elif key in ["longitude", "gpslongitude", "XMP:GPSLongitude"]:
                                    try:
                                        lng = float(value)
                                        ff = 10**6
                                        lng = math.ceil(lng * ff) / ff
                                    except ValueError:
                                        pass
                                else:
                                    command.append(f"-{key}={value}")
                    except IndexError:
                        pass

                    # TODO: This is broken, so FIX IT!
                    # if lat and lng:
                    #     command.append(
                    #         f'-GPSLongitude={lng} -GPSLongitudeRef={lng} -GPSLatitude={lat} -GPSLatitudeRef={lat}'
                    #     )

                command.append(row.get("SourceFile"))

                print(" ".join(command))
                if save:
                    subprocess.run(command)

                cnt += 1


def _get_files():
    files = os.listdir()
    sorted(files)
    return filter(files, "*.[Jj][Pp][Gg]")


def exiftool_csv_create():
    columns = [
        "SourceFile",
        "Artist",
        "Title",
        "Make",
        "Model",
        "SerialNumber",
        "Lens",
        "LensMake",
        "LensModel",
        "LensSerialNumber",
        "FocalLength",
        "ISO",
        # "latitude",
        # "longitude",
    ]
    file_content = ",".join(columns) + "\n"
    if not os.path.isfile("exiftool.csv"):
        for image_file in _get_files():
            empty_columns = "," * (len(columns) - 1)
            file_content += f"{image_file}{empty_columns}\n"
        print("blank exiftool.csv created:")
        print(file_content)
        with open("exiftool.csv", "w") as f:
            f.write(file_content)
            print("...and saved.")
    else:
        print("exiftool.csv exists!")


def main():
    parser = argparse.ArgumentParser(
        prog="exiftool_csv",
        description="Exiftool CSV - apply csv values to jpg files using exiftool.",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Dry run.",
    )
    parser.add_argument(
        "-c",
        "--create",
        action="store_true",
        help="Create csv template for given folder.",
    )
    parser.add_argument(
        "-s",
        "--save",
        action="store_true",
        help="Save csv.",
    )
    parser.parse_args()
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    if args.dry_run:
        exiftool_csv_save(save=False)
    elif args.create:
        exiftool_csv_create()
    elif args.save:
        exiftool_csv_save()


if __name__ == "__main__":
    main()
