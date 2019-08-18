homme(adrien).
homme(hugo).
homme(bernard).
homme(alain).
homme(guy).
homme(pierre).
femme(veronique).
parent(adrien, hugo).
parent(hugo, bernard).
parent(hugo, alain).
parent(adrien, guy).
parent(guy, pierre).
parent(guy, veronique).

frere_soeur(X, Y) :- parent(P, X), parent(P, Y), X \= Y.
frere(X, Y) :- homme(X), frere_soeur(X, Y).
soeur(X, Y) :- femme(X), frere_soeur(X, Y).
neveu_niece(X, Y) :- parent(P, X), P \= Y, frere_soeur(P, Y).
neveu(X, Y) :- homme(X), neveu_niece(X, Y).
niece(X, Y) :- femme(X), neveu_niece(X, Y).
oncle(X, Y) :- homme(X), neveu_niece(Y, X).
tante(X, Y) :- femme(X), neveu_niece(Y, X).
cousin(X, Y) :- parent(Px, X), parent(Py, Y), frere_soeur(Px, Py).