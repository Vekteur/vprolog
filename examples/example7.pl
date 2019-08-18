% 1
fib(0, 1).
fib(1, 1).
fib(X, Y) :-
	X > 1,
	X1 is X - 1,	
	fib(X1, N1),
	X2 is X - 2,
	fib(X2, N2),
	Y is N1 + N2.

fib2(0, 1).
fib2(1, 1).
fib2(X, Y) :- X > 1, fib2(X, 1, 1, Y).
fib2(2, N2, N1, Y) :- Y is N2 + N1.
fib2(X, N2, N1, Y) :-
	X > 2,
	X1 is X - 1,
	NN1 is N2 + N1,
	fib2(X1, N1, NN1, Y).

% 2
gcd2(A, 0, A).
gcd2(A, B, Y) :-
	B > 0,
	M is A mod B,
	gcd2(B, M, Y).

% 3
ack(0, N, Y) :-
	Y is N + 1.
ack(M, 0, Y) :-
	M > 0,
	M1 is M - 1,
	ack(M1, 1, Y).
ack(M, N, Y) :-
	M > 0,
	N > 0,
	M1 is M - 1,
	N1 is N - 1,
	ack(M, N1, T),
	ack(M1, T, Y).
