homem(1, 'Socrates').
homem(2, 'Morpheu').
homem(3, 'Heisenberg').


mortal(ID, Homem) :- homem(ID, Homem), write(Homem).
