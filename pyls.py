import argparse

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
	results = getDescriptionsOfFilesinDir(args)
	displayResults(results, args) 
	
def getDescriptionsOfFilesinDir(flags):
	"""
	Lists the files and folders in the given directory 
        and constructs a list of dicts with the required info.
	flags is a structure with the following fields -
	.dirname = The directory whose contents are to be listed.
	.long_format = True if the user has asked for the long format.
	.filetype = True if the user has asked for a file type info as well.

	The return value is a list of dictionaries each with the following fields - 
	"filename" = The name of the file.
	"filetype" = "d", "f", or "x" indicating "directory", "plain file", 
			or "executable file", respectively.
	"modtime" = Last modified time of the file as a 'datetime' object
	"filesize" = Number of bytes in the file.
	"""
	return []

def displayResults(results, controls):
	"""
	Takes a list of file descriptions and display control flags
	and prints to the standard output.

	Inputs - 
	results = List of dictionaries, like returned by getDescriptionsOfFilesInDir()
	controls = Object with attributes .long_format and .filetype
			indicating how to show the information.

	Outputs:
	To standard output. Returns None.
	"""

	return None

main(args)

