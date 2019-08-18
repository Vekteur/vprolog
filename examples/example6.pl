bstExample( 
	tree(72,
		tree(50,
			tree(47,
				tree(8, null, null),
				null),
			tree(61,
				tree(55, null, null),
				null)),
		tree(90,
			tree(80, null, null),
			tree(100, null, null)))).

between2(Min, Max, Val) :- Min =< Val, Val =< Max. 
isBST(T) :- isBST(T, -1000, 1000).
isBST(null, _, _).
isBST(tree(Val, Left, Right), Min, Max) :-
	between2(Min, Max, Val),
	isBST(Left, Min, Val),
	isBST(Right, Val, Max).

isPresent(N, tree(N, _, _)) :- !.
isPresent(N, tree(Val, Left, _)) :- N < Val, !, isPresent(N, Left).
isPresent(N, tree(_, _, Right)) :- isPresent(N, Right).

insertBST(N, null, tree(N, null, null)).
insertBST(N, tree(Val, Left, Right), tree(Val, NT, Right)) :- N < Val, !, insertBST(N, Left, NT).
insertBST(N, tree(Val, Left, Right), tree(Val, Left, NT)) :- N > Val, insertBST(N, Right, NT).