:- include(vegetacao).
:- include(engine).

question(Id,Question) :- 
	vegetacao(Id,Question,_).

answer(Id,Answer) :- ifThenElse(vegetacao(Id,_,Answer),writeln('1'),writeln('0')).

quizItem(Id) :-
	question(Id,Question),
	format('~w? ',[Question]),nl.

vegetacao(Id) :- 
	quizItem(Id).
