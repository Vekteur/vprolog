import pkg_resources

from lark import Lark, Transformer, v_args
from lark.indenter import Indenter

from .prolog_structures import (Atom, Conjunction, Disjunction, List, Number,
                               Predicate, Rule, Variable)

class TreeToProlog(Transformer):
	program = list
	term_list = list

	@v_args(inline=True)
	def assertion(self, predicate):
		return Rule(predicate, Conjunction([]))
	@v_args(inline=True)
	def rule(self, predicate, body):
		return Rule(predicate, body)
	@v_args(inline=True)
	def request(self, body):
		return Rule(None, body)

	def disjunction(self, terms):
		return Disjunction(terms)
	def conjunction(self, terms):
		return Conjunction(terms)
	@v_args(inline=True)
	def term(self, term1, relation, term2):
		return Predicate(relation, [term1, term2])
	sum_ = product = exponent = term

	@v_args(inline=True)
	def predicate(self, relation, terms):
		return Predicate(relation, [] if terms is None else terms)
	@v_args(inline=True)
	def list_(self, terms, tail):
		return List([] if terms is None else terms, tail)
	@v_args(inline=True)
	def variable(self, value):
		return Variable(value.value)
	@v_args(inline=True)
	def atom(self, value):
		return Atom(value.value)
	main_op = sum_op = product_op = exponent_op = predicate_op = atom
	@v_args(inline=True)
	def number(self, value):
		return Number(value.value)

class PrologParser:
	def __init__(self, start='program'):
		grammar_path = pkg_resources.resource_filename('vprolog', 'prolog.lark')
		self.lark_parser = Lark.open(grammar_path, parser='lalr', \
			start=start, transformer=TreeToProlog())
	def parse(self, expression):
		return self.lark_parser.parse(expression)

if __name__ == '__main__':
	program_parser = PrologParser()
	with open('examples/example7.pl') as f:
		for rule in program_parser.parse(f.read()):
			print(str(rule))