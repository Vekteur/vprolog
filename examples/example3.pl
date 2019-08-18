a(1).
a(a).
b(2).
b(3).
p(X, X) :- a(X).
p(X, Y) :- a(X), !, b(Y).
p(X, X) :- b(X).

% p(A, B).