import argparse

MUSIC_EXTENSIONS = [
    "mp3",
    "m4a",
]

IGNORED_EXTENSIONS = [
    "m3u",
]


def list_extensions(path: str):
    """This function crawls given path recursely and creates unique list of extensions."""
    print(f"Crawling path '{path}' files...")


def main():
    parser = argparse.ArgumentParser(
        prog="create_playlist",
        description="Create playlist - python script which creates a playlists, in subfolders",
    )
    parser.add_argument("path", type=str, help="Target path", default=".")
    parser.add_argument(
        "-l",
        "--list-extensions",
        action="store_true",
        help="This function crawls given path recursely and creates unique list of extensions.",
    )
    parser.parse_args()
    args = parser.parse_args()
    if args.list_extensions:
        list_extensions(args.path)


if __name__ == "__main__":
    main()
