:- include(extremo).

questionExtremo(Id,Question) :- 
	extremo(Id,Question,_).

answerExtremo(Id,Answer) :- extremo(Id,_,Answer).

randomizeIdExtremo(RandomId) :-
	numberOfQuestions(Range),
	RandomId is integer(random(Range) + 1),		
	findall(Id,extremo(Id,_,_),Lista), 
	member(RandomId,Lista);
	findall(Id,extremo(Id,_,_),_),
	randomizeIdExtremo(RandomId).
		
quizItemExtremo(Id) :-
	questionExtremo(Id,Question),
	format('~w? ',[Question]),nl,
	write('Resposta:'), read(Choice),
	answerExtremo(Id,Choice).

quizEngineExtremo(Id) :- 
	quizItemExtremo(Id),
	newPoint,
	retract(extremo(Id,_,_)),
	writeln('Voce Acertou'),nl,
	aggregate_all(count, extremo(_,_,_), Count),
	ifThenElse(Count=:=0,gameOver,extremo).

quizEngineExtremo(Id) :-
	retract(extremo(Id,_,_)),
	writeln('Voce Errou'),nl,
	aggregate_all(count, extremo(_,_,_), Count),
	ifThenElse(Count=:=0,gameOver,extremo).

extremo :- 
	randomizeIdExtremo(RandomId),	
	quizEngineExtremo(RandomId).
