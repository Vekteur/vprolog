"""Prolog interpreter

Usage:
	vprolog.py [<input_file>]
"""
from docopt import docopt

from interpreter import Interpreter

if __name__ == '__main__':
	args = docopt(__doc__)
	input_file = 'data/default_input.pl'
	if args['<input_file>'] is not None:
		input_file = args['<input_file>']
	Interpreter(input_file).start()