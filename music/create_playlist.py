import argparse
import os

MUSIC_EXTENSIONS = [
    "flac",
    "it",
    "m4a",
    "mid",
    "mod",
    "mp3",
    "mtm",
    "opus",
    "pdf",
    "s3m",
    "sf2",
    "sng",
    "wav",
    "xm",
]

IGNORED_EXTENSIONS = [
    "669",
    "bat",
    "bbs",
    "dat",
    "dmf",
    "ds_store",
    "epub",
    "far",
    "html",
    "ini",
    "ins",
    "ion",
    "jpeg",
    "jpg",
    "m3u",
    "mobi",
    "nfo",
    "png",
    "prg",
    "txt",
    "ult",
]


def create_playlist(path: str, recursive: bool):
    pass


def list_extensions(path: str, recursive: bool) -> list[str]:
    """This function crawls given path recursely and creates unique list of extensions."""
    print(f"Crawling path '{path}' files...")

    def _list_extensions(p: str, r: bool) -> list[str]:
        _extensions = []
        dir_contents = os.listdir(p)
        for element in dir_contents:
            if r and os.path.isdir(os.path.join(p, element)):
                _extensions += _list_extensions(os.path.join(p, element), r)
            elif os.path.isfile(os.path.join(p, element)):
                ex = element.split(".")[-1].lower()
                if ex not in IGNORED_EXTENSIONS:
                    _extensions.append(ex)
        return _extensions

    _list_extensions = set(_list_extensions(path, recursive))
    return sorted(_list_extensions)


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
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Recursive.",
    )
    parser.add_argument(
        "-o",
        "--overwrite",
        action="store_true",
        help="Always overwrite existing playlist.",
    )
    parser.parse_args()
    args = parser.parse_args()
    if args.list_extensions:
        extensions = list_extensions(args.path, args.recursive)
        print(f"List of extensions in '{args.path}':")
        print("MUSIC_EXTENSIONS = [")
        for _ex in extensions:
            print(f'    "{_ex}",')
        print("]")
    else:
        pass


if __name__ == "__main__":
    main()
