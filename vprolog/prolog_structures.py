from abc import ABC, abstractmethod


class Rule:
	def __init__(self, head, body):
		self.head = head
		self.body = body
	def __str__(self):
		return str(self.head) + ' :- ' + str(self.body)

class Clause(ABC):
	def __init__(self, terms):
		assert isinstance(terms, list)
		self.terms = terms
	@abstractmethod
	def separator(self):
		pass
	def __str__(self):
		return '(' + (self.separator() + ' ').join(
			list(map(str, self.terms))) + ')'

class Disjunction(Clause):
	def separator(self):
		return ';'

class Conjunction(Clause):
	def separator(self):
		return ','

class PredicateID:
	def __init__(self, name, arity):
		self.name = name
		self.arity = arity
	def __eq__(self, other):
		if not isinstance(other, PredicateID):
			return False
		return self.name == other.name and self.arity == other.arity
	def __hash__(self):
		return hash((self.name, self.arity))
	def __str__(self):
		return self.name + '/' + str(self.arity)

class Predicate:
	def __init__(self, relation, terms):
		self.relation = relation
		#print(relation)
		#print(terms)
		#assert terms is not None
		self.terms = terms
	def __str__(self):
		str_rel = str(self.relation)
		if not self.terms:
			return str_rel
		return str_rel + '(' + ', '.join(map(str, self.terms)) + ')'
	def id(self):
		return PredicateID(self.relation.value, len(self.terms))

class List:
	def __init__(self, terms=[], tail=None, start_index=0):
		self.terms = terms
		self.tail = tail
		self.start_index = start_index
	def empty(self):
		return self.start_index == len(self.terms) and self.tail is None
	def next_list(self):
		if self.empty():
			raise RuntimeError('Next item in empty list does not exist')
		next_index = self.start_index + 1
		if next_index == len(self.terms):
			if self.tail is None:
				return List([], None)
			return self.tail
		return List(self.terms, self.tail, next_index)
	def flatten(self):
		if isinstance(self.tail, List):
			flat_tail = self.tail.flatten()
		else:
			flat_tail = List([], None)
		return List(self.terms[self.start_index:] + flat_tail.terms, flat_tail.tail)
	def __str__(self):
		flat_list = self.flatten()
		str_tail = '' if flat_list.tail == None else ' | ' + str(flat_list.tail)
		return '[' + ', '.join(list(map(str, flat_list.terms))) + str_tail + ']'

class Variable:
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return self.value
	def is_anonym(self):
		return self.value[0] == '_'
	def __eq__(self, other):
		if not isinstance(other, Variable):
			return NotImplemented
		return self.value == other.value
	def __hash__(self):
		return hash(self.value)

class Constant:
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return str(self.value)

class Atom(Constant):
	pass

class Number(Constant):
	def __init__(self, value):
		super().__init__(int(value))