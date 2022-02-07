from .methdispatch import methdispatch
from .prolog_structures import (Conjunction, Constant, Disjunction, List,
                               Predicate, Rule, Variable)


class Substitution:
	def __init__(self):
		self.theta = {}
		self.layers = [[]]
	def __setitem__(self, var, sub):
		if var not in self.theta:
			self.theta[var] = sub
			self.layers[-1].append((var, sub))
		else:
			if self.theta[var] != sub:
				raise ValueError("Can't override the existing subtitution for " + var)
	def __getitem__(self, var):
		return self.theta[var]
	def __contains__(self, var):
		if not isinstance(var, Variable):
			return False
		return var in self.theta
	def __str__(self):
		key_values = [str(var) + ' = ' + str(substitute(sub, self, subst_rec_anonym=True)) \
			for (var, sub) in self.theta.items() if not var.is_anonym()]
		return ', '.join(key_values)
	def count_visible(self):
		return sum(not var.is_anonym() for var in self.theta)
	def add_layer(self):
		self.layers.append([])
	def pop_layer(self):
		for (var, _sub) in self.layers[-1]:
			self.theta.pop(var)
		self.layers.pop()

class Unifier:
	def __init__(self, expr_only=False):
		self.expr_only = expr_only

	@methdispatch
	def unify_rec(self, x, y, subst):
		assert x is not None and y is not None
		return None
	
	@unify_rec.register(Disjunction)
	def _(self, x, y, subst):
		if not isinstance(y, Disjunction):
			return None
		return self(List(x.terms), List(y.terms), subst)

	@unify_rec.register(Conjunction)
	def _(self, x, y, subst):
		if not isinstance(y, Conjunction):
			return None
		return self(List(x.terms), List(y.terms), subst)

	@unify_rec.register(Predicate)
	def _(self, x, y, subst):
		if not isinstance(y, Predicate):
			return None
		return self(List(x.terms), List(y.terms), self(x.relation, y.relation, subst))

	@unify_rec.register(List)
	def _(self, x, y, subst):
		if not isinstance(y, List):
			return None
		if x.empty() and y.empty():
			return subst
		if x.empty() or y.empty():
			return None
		subst = self(x.terms[x.start_index], y.terms[y.start_index], subst)
		return self(x.next_list(), y.next_list(), subst)

	@unify_rec.register(Variable)
	def _(self, x, y, subst):
		if self.expr_only:
			return subst if isinstance(y, Variable) and \
				x.value == y.value else None
		if x in subst:
			return self(subst[x], y, subst)
		elif y in subst:
			return self(x, subst[y], subst)
		if x != y:
			subst[x] = y
		return subst

	@unify_rec.register(Constant)
	def _(self, x, y, subst):
		if not isinstance(y, Constant):
			return None
		if x.value == y.value:
			return subst
		return None

	def __call__(self, x, y, subst):
		if subst is None:
			return None
		if not isinstance(x, Variable) and isinstance(y, Variable):
			return self.unify_rec(y, x, subst)
		return self.unify_rec(x, y, subst)

def unify(x, y, subst, expr_only=False):
	return Unifier(expr_only)(x, y, subst)

class Substituter:
	def __init__(self, subst, subst_rec_anonym=False):
		self.subst_rec_anonym = subst_rec_anonym
		self.subst = subst

	@methdispatch
	def substitute(self, x):
		return x

	@substitute.register(Disjunction)
	def _(self, x):
		return Disjunction(self.substitute(List(x.terms)).terms)

	@substitute.register(Conjunction)
	def _(self, x):
		return Conjunction(self.substitute(List(x.terms)).terms)

	@substitute.register(Predicate)
	def _(self, x):
		return Predicate(x.relation, self.substitute(List(x.terms)).terms)

	@substitute.register(List)
	def _(self, x):
		return List([self.substitute(term) for term in x.terms], \
				self.substitute(x.tail), x.start_index)

	@substitute.register(Variable)
	def _(self, x):
		if x in self.subst:
			if self.subst_rec_anonym:
				if x.is_anonym():
					return self.substitute(self.subst[x])
			else:
				return self.subst[x]
		return x

def substitute(x, subst, subst_rec_anonym=False):
	return Substituter(subst, subst_rec_anonym).substitute(x)