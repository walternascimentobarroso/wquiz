:- include(relevo).

questionRelevo(Id,Question) :- 
	relevo(Id,Question,_).

answerRelevo(Id,Answer) :- relevo(Id,_,Answer).

randomizeIdRelevo(RandomId) :-
	numberOfQuestions(Range),
	RandomId is integer(random(Range) + 1),		
	findall(Id,relevo(Id,_,_),Lista), 
	member(RandomId,Lista);
	findall(Id,relevo(Id,_,_),_),
	randomizeIdRelevo(RandomId).
		
quizItemRelevo(Id) :-
	questionRelevo(Id,Question),
	format('~w? ',[Question]),nl,
	write('Resposta:'), read(Choice),
	answerRelevo(Id,Choice).

quizEngineRelevo(Id) :- 
	quizItemRelevo(Id),
	newPoint,
	retract(relevo(Id,_,_)),
	writeln('Voce Acertou'),nl,
	aggregate_all(count, relevo(_,_,_), Count),
	ifThenElse(Count=:=0,gameOver,relevo).

quizEngineRelevo(Id) :-
	retract(relevo(Id,_,_)),
	writeln('Voce Errou'),nl,
	aggregate_all(count, relevo(_,_,_), Count),
	ifThenElse(Count=:=0,gameOver,relevo).

relevo :- 
	randomizeIdRelevo(RandomId),	
	quizEngineRelevo(RandomId).
