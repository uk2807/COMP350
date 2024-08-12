import os
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(
    prog='pyls',
    description='Lists files in given or current dir',
    epilog="poor man\'s ls"
)

parser.add_argument('dirname', help="Name of directory to list the contents of",
                    action='store',
                    nargs='?',
                    default=".")

parser.add_argument('-l', '--long-format',
                    help="Presents more details about files in columnar format",
                    action='store_true')

parser.add_argument('-F', '--filetype',
                    help="""Adds an extra character to the end of the printed filename that indicates its type""",
                    action='store_true')

args = parser.parse_args()

def main():
    assert isinstance(args, argparse.Namespace), "Expected argparse.Namespace as argument for main"
    results = getDescriptionsOfFilesInDir(args.dirname, args.long_format, args.filetype)
    displayResults(results, args.long_format, args.filetype)

def getDescriptionsOfFilesInDir(dirname, long_format, filetype):
    """
    Lists the files and folders in the given directory 
    and constructs a list of dicts with the required info.

    Arguments:
    - dirname: The directory whose contents are to be listed (str).
    - long_format: Boolean flag to indicate long format (bool).
    - filetype: Boolean flag to indicate filetype display (bool).

    Returns:
    - A list of dictionaries each with the following fields:
      - "filename": The name of the file (str).
      - "filetype": A character indicating the file type: "/" for directories, "*" for executables, or "" for other files.
      - "modtime": Last modified time of the file as a string in "YYYY-MM-DD HH:MM:SS" format.
      - "filesize": Number of bytes in the file (0 for directories).
    """
    assert isinstance(dirname, str), "dirname should be a string"
    assert isinstance(long_format, bool), "long_format should be a boolean"
    assert isinstance(filetype, bool), "filetype should be a boolean"

    entries = []

    try:
        dir_entries = os.listdir(dirname)
    except FileNotFoundError:
        raise ValueError(f"The directory {dirname} does not exist")

    for entry_name in dir_entries:
        entry_path = os.path.join(dirname, entry_name)
        file_info = {
            "filename": entry_name,
            "filetype": "",
            "modtime": "",
            "filesize": 0
        }

        # Get file type
        if filetype:
            if os.path.isdir(entry_path):
                file_info["filetype"] = "/"
            elif os.path.isfile(entry_path) and os.access(entry_path, os.X_OK):
                file_info["filetype"] = "*"

        # Get long format details
        if long_format:
            modtime = datetime.fromtimestamp(os.path.getmtime(entry_path))
            file_info["modtime"] = modtime.strftime('%Y-%m-%d %H:%M:%S')
            if os.path.isfile(entry_path):
                file_info["filesize"] = os.path.getsize(entry_path)

        entries.append(file_info)

    assert isinstance(entries, list), "The function should return a list of dictionaries"
    return entries

def displayResults(results, long_format, filetype):
    """
    Takes a list of file descriptions and display control flags
    and prints to the standard output.

    Arguments:
    - results: List of dictionaries with file information.
    - long_format: Boolean flag to indicate long format (bool).
    - filetype: Boolean flag to indicate filetype display (bool).

    Returns:
    - None
    """
    assert isinstance(results, list), "results should be a list"
    assert all(isinstance(entry, dict) for entry in results), "Each entry in results should be a dictionary"
    assert isinstance(long_format, bool), "long_format should be a boolean"
    assert isinstance(filetype, bool), "filetype should be a boolean"

    for entry in results:
        if long_format:
            print(f"{entry['modtime']} {entry['filesize']:>8} {entry['filename']}{entry['filetype']}")
        else:
            print(f"{entry['filename']}{entry['filetype']}")

    return None

if __name__ == "__main__":
    main()

