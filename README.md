# Python toolbox
This is my python toolbox.

## Installation

    pip install git+https://github.com/bohdanbobrowski/python_toolbox.git

#### Local (dev) environment

    pip install -e .

## Included scripts

### Music

#### [create_playlist](music/create_playlist.py)
    usage: create_playlist [-h] [-l] [-r] [-o] path

    Create playlist - python script which creates a playlists, in subfolders

    positional arguments:
      path                  Target path
    
    options:
      -h, --help            show this help message and exit
      -l, --list-extensions
                            This function crawls given path recursely and creates unique list of extensions.
      -r, --recursive       Recursive.
      -o, --overwrite       Always overwrite existing playlist.

### Pictures

#### [exiftool_csv](pictures/exiftool_csv.py)
    usage: exiftool_csv [-h] [-d] [-c] [-s]

    Exiftool CSV - apply csv values to jpg files using exiftool.
    
    options:
      -h, --help        show this help message and exit
      -d, --dry-run     Dry run.
      -c, --create      Create csv template for given folder.
      -s, --save        Save csv.

#### [move_not_starred](pictures/move_not_starred.py)
    usage: move_not_starred [-h] [-d] [-p PICTURE_EXTENSION] [-r RAW_EXTENSION] [-t TARGET]
    
    Move raw files for jpegs that are not starred to subfolder. Requires exiftool.
    
    options:
      -h, --help            show this help message and exit
      -d, --dry-run         Dry run.
      -p PICTURE_EXTENSION, --picture_extension PICTURE_EXTENSION
                            Picture file extension (by default JPG).
      -r RAW_EXTENSION, --raw_extension RAW_EXTENSION
                            RAW file extension (by default DNG).
      -t TARGET, --target TARGET
                            Target path (by default creates sub folder with the same name as current one).

