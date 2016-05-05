:- include(extremo).
:- include(engine).

question(Id,Question) :- 
	extremo(Id,Question,_).

answer(Id,Answer) :- ifThenElse(extremo(Id,_,Answer),writeln('1'),writeln('0')).

quizItem(Id) :-
	question(Id,Question),
	format('~w? ',[Question]),nl.

extremo(Id) :- 
	quizItem(Id).
