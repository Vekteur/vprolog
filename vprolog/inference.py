from collections import defaultdict
from functools import singledispatch

from .methdispatch import methdispatch
from .prolog_operator import operators
from .prolog_structures import (Atom, Conjunction, Disjunction, List, Number,
                               Predicate, Rule, Variable)
from .substitution import Substitution, substitute, unify


class Inference:
	def __init__(self, kb):
		self.fetched_rules = defaultdict(list)
		for rule in kb:
			if rule.head is not None:
				self.fetched_rules[rule.head.relation.value].append(rule)

	def fetch_rules(self, relation):
		return self.fetched_rules[relation.value]

	def next_var_id(self):
		id = self.var_id
		self.var_id += 1
		return id

	def standardise(self, rule):
		@singledispatch
		def standardise_rec(x):
			return x
		@standardise_rec.register(Conjunction)
		def _(x):
			return Conjunction(standardise_rec(List(x.terms)).terms)
		@standardise_rec.register(Disjunction)
		def _(x):
			return Disjunction(standardise_rec(List(x.terms)).terms)
		@standardise_rec.register(Predicate)
		def _(x):
			return Predicate(x.relation, standardise_rec(List(x.terms)).terms)
		@standardise_rec.register(List)
		def _(x):
			return List([standardise_rec(term) for term in x.terms], standardise_rec(x.tail), x.start_index)
		@standardise_rec.register(Variable)
		def _(x):
			if x.value in new_names:
				return Variable(new_names[x.value])
			id = '_g' + str(self.next_var_id())
			if x.value != '_':
				new_names[x.value] = id
			return Variable(id)
		
		new_names = {}
		return Rule(standardise_rec(rule.head), standardise_rec(rule.body))
	
	@methdispatch
	def resolve(self, goal, subst, depth):
		raise RuntimeError('Incorrect type : ' + str(type(goal)))
	
	@resolve.register(Disjunction)
	def _(self, goal, subst, depth):
		goals = goal.terms
		for sub_goal in goals:
			subst.add_layer()
			yield from self.resolve(sub_goal, subst, depth)
			subst.pop_layer()

	def resolve_conjunction(self, goal, subst, depth, index):
		goals = goal.terms
		if self.cut_depth is not None or subst is None:
			return None
		elif index == len(goals):
			yield subst
		else:
			sub_goal = goals[index]
			for new_subst in self.resolve(sub_goal, subst, depth):
				yield from self.resolve_conjunction(goal, new_subst, depth, index + 1)

	@resolve.register(Conjunction)
	def _(self, goal, subst, depth):
		yield from self.resolve_conjunction(goal, subst, depth, 0)

	@resolve.register(Predicate)
	def _(self, goal, subst, depth):
		if subst is None:
			return None
		goal = substitute(goal, subst)
		depth += 1
		operatorID = goal.id()
		if operatorID in operators:
			yield from operators[operatorID](self, subst, depth, *goal.terms)
		else:
			for rule in self.fetch_rules(goal.relation):
				standard_rule = self.standardise(rule)
				subst.add_layer()
				unified_goal = unify(standard_rule.head, goal, subst)
				yield from self.resolve(standard_rule.body, unified_goal, depth)
				subst.pop_layer()
		if depth == self.cut_depth:
			self.cut_depth = None
	
	@resolve.register(Variable)
	def _(self, goal, subst, depth):
		if goal in subst:
			yield from self.resolve(subst[goal], subst, depth)
		else:
			raise RuntimeError('Calling uninstantiated variable')

	def __call__(self, goals):
		self.cut_depth = None
		self.var_id = 0
		yield from self.resolve(goals, Substitution(), 0)