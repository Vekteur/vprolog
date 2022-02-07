true.
call(X) :- X.

not(C) :- C, !, fail.
not(_).

once(Goal) :- Goal, !.

ignore(Goal) :- Goal, !.
ignore(_).

forall(Cond, Action) :-
	not((Cond, not(Action))).

if_then_else(C, T, _) :- C, !, T.
if_then_else(_, _, E) :- E.

member(X, [X|_]).
member(X, [_|L]) :- member(X, L).

append([], X, X).
append([X | Y], Z, [X | W]) :- append(Y, Z, W).