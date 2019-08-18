autruche(titi).
autruche(zoe).
pingouin(fred).
roti(al).
transgenique(titi).

oiseau(lulu).
oiseau(X) :- autruche(X); pingouin(X); roti(X).

a_des_ailes(X) :- oiseau(X).

ne_vole_pas(X) :- transgenique(X), !, fail.
ne_vole_pas(X) :- autruche(X); pingouin(X); roti(X).
vole(X) :- ne_vole_pas(X), !, fail.
vole(X) :- oiseau(X).