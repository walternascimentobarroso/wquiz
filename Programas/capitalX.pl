:- include(capital).
:- include(engine).

question(Id,Question) :- 
	capital(Id,Question,_).

answer(Id,Answer) :- ifThenElse(capital(Id,_,Answer),writeln('1'),writeln('0')).

quizItem(Id) :-
	question(Id,Question),
	format('~w? ',[Question]),nl.

capital(Id) :- 
	quizItem(Id).
