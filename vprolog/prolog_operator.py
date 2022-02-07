import operator

from .prolog_structures import Atom, Number, Predicate, PredicateID, Variable
from .substitution import unify

operators = {}

def add_operator(name, arity, func):
	operators[PredicateID(name, arity)] = func

def negate(name):
	def impl(inference, subst, depth, *terms):
		yield from inference.resolve(Predicate(Atom('not'), \
			[Predicate(Atom(name), terms)]), subst, depth)
	return impl

def unify_helper(term1, term2, subst, expr_only=False):
	res = unify(term1, term2, subst, expr_only)
	if res is not None:
		yield res

def operator_eq(expr_only=False):
	def impl(inference, subst, depth, term1, term2):
		yield from unify_helper(term1, term2, subst, expr_only)
	return impl

def operator_is(inference, subst, depth, term1, term2):
	yield from unify_helper(term1, eval_arithm(term2, subst), subst)

def operator_arithm_eq(inference, subst, depth, term1, term2):
	yield from unify_helper(eval_arithm(term1, subst), \
		eval_arithm(term2, subst), subst)

def operator_cut(inference, subst, depth):
	yield subst
	inference.cut_depth = depth - 1

def bin_comp(func):
	def impl(inference, subst, depth, term1, term2):
		if not isinstance(term1, Number) or not isinstance(term2, Number):
			print(term1, term2)
			raise TypeError('Invalid comparison between ' +
				type(term1).__name__ + ' and ' + type(term2).__name__)
		if func(term1.value, term2.value):
			yield subst
	return impl

def add_bin_comp(name, func):
	add_operator(name, 2, bin_comp(func))

def eval_arithm(term, subst):
	if isinstance(term, Number):
		return term
	elif isinstance(term, Variable):
		return eval_arithm(subst[term], subst)
	elif isinstance(term, Predicate) and term.id() in arithm_operators:
		return Number(arithm_operators[term.id()](*[eval_arithm(child, subst).value \
			for child in term.terms]))
	raise TypeError('Invalid arithmetic type : ' + type(term).__name__)

add_operator('!', 0, operator_cut)
add_operator('=', 2, operator_eq())
add_operator(r'\=', 2, negate('='))
add_operator('==', 2, operator_eq(expr_only=True))
add_operator(r'\==', 2, negate('=='))
add_operator('is', 2, operator_is)
add_operator('=:=', 2, operator_arithm_eq)
add_operator(r'=\=', 2, negate('=:='))
add_bin_comp('<', operator.lt)
add_bin_comp('=<', operator.le)
add_bin_comp('>', operator.gt)
add_bin_comp('>=', operator.ge)

arithm_operators = {}

def add_arithm_op(name, arity, func):
	arithm_operators[PredicateID(name, arity)] = func

add_arithm_op('+', 2, operator.add)
add_arithm_op('-', 2, operator.sub)
add_arithm_op('*', 2, operator.mul)
add_arithm_op('/', 2, operator.truediv)
add_arithm_op('div', 2, operator.floordiv)
add_arithm_op('mod', 2, operator.mod)
add_arithm_op('**', 2, operator.pow)