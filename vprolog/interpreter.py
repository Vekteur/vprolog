import pkg_resources
from pathlib import Path

import lark

from .inference import Inference
from .prolog_parser import PrologParser


def read(path):
	with open(path) as f:
		return f.read()

class Interpreter:
	def __init__(self, input_path):
		program_parser = PrologParser()
		self.request_parser = PrologParser('request')
		builtin_path = Path(pkg_resources.resource_filename('vprolog', 'data/builtin.pl'))
		program = program_parser.parse(read(builtin_path) + read(input_path))
		self.inference = Inference(program)

	def process_request(self, request):
		nb_sols = 0
		for sol in self.inference(request.body):
			if sol.count_visible() == 0:
				print('true.')
			else:
				print(sol)
			nb_sols += 1
		if nb_sols == 0:
			print('false.')
	
	def start(self):
		while True:
			prefix = '?- '
			try:
				str_request = input(prefix)
			except KeyboardInterrupt:
				break
			if not str_request:
				break
			try:
				request = self.request_parser.parse(prefix + str_request)
			except lark.exceptions.LarkError:
				print('Error: invalid syntax')
				continue
			try:
				self.process_request(request)
			except RecursionError:
				print('Error: stack overflow')