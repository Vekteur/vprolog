from prolog_parser import PrologParser
from inference import Inference
from copy import deepcopy
import sys
import lark

def read(file):
	with open(file) as f:
		return f.read()

class Interpreter:
	builtin_file = 'data/builtin.pl'

	def __init__(self, input_file):
		program_parser = PrologParser()
		self.request_parser = PrologParser('request')
		program = program_parser.parse(read(Interpreter.builtin_file) + read(input_file))
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
				print('Error : invalid syntax')
				continue
			try:
				self.process_request(request)
			except RecursionError:
				print('Error : stack overflow')