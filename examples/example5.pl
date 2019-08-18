subset2([], _).
subset2([X|L1], L2) :-
	member(X, L2),
	subset2(L1, L2).

subset3(S, L) :-
	forall(member(X, S), member(X, L)).

takeout(E, [E|L], L).
takeout(E, [X|L1], [X|L2]) :-
	takeout(E, L1, L2).

inverse(L1, L2):-
	inverse(L1, [], L2).
inverse([], Acc, Acc).
inverse([H|T], Acc, Res):-
	inverse(T, [H|Acc], Res).