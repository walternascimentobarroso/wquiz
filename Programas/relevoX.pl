:- include(relevo).
:- include(engine).

question(Id,Question) :- 
	relevo(Id,Question,_).

answer(Id,Answer) :- ifThenElse(relevo(Id,_,Answer),writeln('1'),writeln('0')).

quizItem(Id) :-
	question(Id,Question),
	format('~w? ',[Question]),nl.

relevo(Id) :- 
	quizItem(Id).
