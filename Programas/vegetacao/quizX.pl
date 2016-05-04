:- include(vegetacao).

questionVegetacao(Id,Question) :- 
	vegetacao(Id,Question,_).

answerVegetacao(Id,Answer) :- vegetacao(Id,_,Answer).

randomizeIdVegetacao(RandomId) :-
	numberOfQuestions(Range),
	RandomId is integer(random(Range) + 1),		
	findall(Id,vegetacao(Id,_,_),Lista), 
	member(RandomId,Lista);
	findall(Id,vegetacao(Id,_,_),_),
	randomizeIdVegetacao(RandomId).
		
quizItemVegetacao(Id) :-
	questionVegetacao(Id,Question),
	format('~w? ',[Question]),nl,
	write('Resposta:'), read(Choice),
	answerVegetacao(Id,Choice).

quizEngineVegetacao(Id) :- 
	quizItemVegetacao(Id),
	newPoint,
	retract(vegetacao(Id,_,_)),
	writeln('Voce Acertou'),nl,
	aggregate_all(count, vegetacao(_,_,_), Count),
	ifThenElse(Count=:=0,gameOver,vegetacao).

quizEngineVegetacao(Id) :-
	retract(vegetacao(Id,_,_)),
	writeln('Voce Errou'),nl,
	aggregate_all(count, vegetacao(_,_,_), Count),
	ifThenElse(Count=:=0,gameOver,vegetacao).

vegetacao :- 
	randomizeIdVegetacao(RandomId),	
	quizEngineVegetacao(RandomId).
