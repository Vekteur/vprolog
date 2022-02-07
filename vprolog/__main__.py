"""Interpreter for a subset of Prolog
"""
import pkg_resources
import argparse
from pathlib import Path

from .interpreter import Interpreter

def file_type(string):
	path = Path(string)
	if path.is_file():
		return path
	raise FileNotFoundError(string)

def main():
	parser = argparse.ArgumentParser(description='Interpreter for a subset of Prolog')
	parser.add_argument('input_file', type=file_type, nargs='?', help='Path of the input file')
	args = parser.parse_args()

	if args.input_file is None:
		input_path = pkg_resources.resource_filename('vprolog', 'data/default_input.pl')
	else:
		input_path = args.input_file

	Interpreter(input_path).start()

if __name__ == '__main__':
	main()
