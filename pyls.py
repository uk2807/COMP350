import argparse
import os
from datetime import datetime

parser = argparse.ArgumentParser(
			prog='pyls',
			description='Lists files in given or current dir',
			epilog="poor man's ls")

parser.add_argument('dirname', help="Name of directory to list the contents of",
				action='store',
				nargs='?',
				default=".")

parser.add_argument('-l', '--long-format', 
		help="Presents more details about files in columnar format",
		action='store_true')

parser.add_argument('-F', '--filetype', 
		help="""Adds an extra character to the end of the printed filename that indicates its type""", action='store_true')

args = parser.parse_args()

def main(args):
	results = getDescriptionsOfFilesInDir(args)
	displayResults(results, args) 
	
def getDescriptionsOfFilesInDir(flags):
    """
    Lists the files and folders in the given directory 
    and constructs a list of dicts with the required info.
    flags is an object with the following fields:
    .dirname = The directory whose contents are to be listed.
    .long_format = True if the user has asked for the long format.
    .filetype = True if the user has asked for a file type info as well.

    The return value is a list of dictionaries each with the following fields: 
    - "filename": The name of the file.
    - "filetype": A character indicating the file type: "/" for directories, "*" for executables, or "" for other files.
    - "modtime": Last modified time of the file as a string in "YYYY-MM-DD HH:MM:SS" format.
    - "filesize": Number of bytes in the file (0 for directories).
    """
    entries = []
    directory_items = os.listdir(flags.dirname)

    for item in directory_items:
        path = os.path.join(flags.dirname, item)
        file_info = {
            "filename": item,
            "filetype": "",
            "modtime": "",
            "filesize": 0
        }

        # Get file type
        if flags.filetype:
            if os.path.isdir(path):
                file_info["filetype"] = "/"
            elif os.path.isfile(path) and os.access(path, os.X_OK):
                file_info["filetype"] = "*"

        # Get long format details
        if flags.long_format:
            file_info["modtime"] = datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S')
            if os.path.isfile(path):
                file_info["filesize"] = os.path.getsize(path)

        entries.append(file_info)
    
    return entries

def displayResults(results, controls):
    """
    Takes a list of file descriptions and display control flags
    and prints to the standard output.

    Inputs: 
    - results: List of dictionaries, like returned by getDescriptionsOfFilesInDir().
    - controls: Object with attributes .long_format and .filetype
                indicating how to show the information.

    Outputs:
    To standard output. Returns None.
    """
    for entry in results:
        if controls.long_format:
            print(f"{entry['modtime']} {entry['filesize']:>8} {entry['filename']}{entry['filetype']}")
        elif controls.filetype:
            print(f"{entry['filename']}{entry['filetype']}")
        else:
            print(entry['filename'])

main(args)

