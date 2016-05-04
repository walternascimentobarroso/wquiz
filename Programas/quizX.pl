:- include(clima).
:- include(engine).

question(Id,Question) :- 
	clima(Id,Question,_).

answer(Id,Answer) :- clima(Id,_,Answer).

quizItem(Id) :-
	question(Id,Question),
	format('~w? ',[Question]),nl.
	%write('Resposta:'), read(Choice),
	%answer(Id,Choice).

quizEngine(Id) :- 
	quizItem(Id).
	%newPoint,
	%retract(clima(Id,_,_)),
	%writeln('Voce Acertou'),nl,
	%aggregate_all(count, clima(_,_,_), Count),
	%ifThenElse(Count=:=0,gameOver,clima).

	%retract(clima(Id,_,_)),
	%writeln('Voce Errou'),nl,
	%aggregate_all(count, clima(_,_,_), Count),
	%ifThenElse(Count=:=0,gameOver,clima).

clima(Id) :- 
	quizEngine(Id).
