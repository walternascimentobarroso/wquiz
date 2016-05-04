:- include(capital).

questionCapital(Id,Question) :- 
	content(Id,Question,_,_,_,_,_).

alternative(Id,1,FirstAlternative) :- 
	content(Id,_,FirstAlternative,_,_,_,_).

alternative(Id,2,SecondAlternative) :- 
	content(Id,_,_,SecondAlternative,_,_,_).

alternative(Id,3,ThirdAlternative) :- 
	content(Id,_,_,_,ThirdAlternative,_,_).

alternative(Id,4,FourthAlternative) :- 
	content(Id,_,_,_,_,FourthAlternative,_).

alternative(_,5,_) :- halt.

answerCapital(Id,Answer) :- content(Id,_,_,_,_,_,Answer).

randomizeIdCapital(RandomId) :-
	numberOfQuestions(Range),
	RandomId is integer(random(Range) + 1),		
	findall(Id,content(Id,_,_,_,_,_,_),Lista), 
	member(RandomId,Lista);
	findall(Id,content(Id,_,_,_,_,_,_),_),
	randomizeIdCapital(RandomId).
		
quizItemCapital(Id) :-
	questionCapital(Id,Question),
	format('Qual é a capital do(e) ~w? ',[Question]),nl,
	alternative(Id,1,FirstAlternative),
	write('  1) '),write(FirstAlternative),nl,
	alternative(Id,2,SecondAlternative),
	write('  2) '),write(SecondAlternative),nl,
	alternative(Id,3,ThirdAlternative),
	write('  3) '),write(ThirdAlternative),nl,
	alternative(Id,4,FourthAlternative),
	write('  4) '),write(FourthAlternative),nl,
	write('  5) Terminar Jogo'),nl,
	read(Choice),
	ifThenElse(Choice=:=5,gameOver,answerCapital(Id,Choice)).

quizEngineCapital(Id) :- 
	quizItemCapital(Id),
	newPoint,
	retract(content(Id,_,_,_,_,_,_)),
	writeln('Voce Acertou'),nl,
	aggregate_all(count, content(_,_,_,_,_,_,_), Count),
	ifThenElse(Count=:=0,gameOver,capital).

quizEngineCapital(Id) :-
	retract(content(Id,_,_,_,_,_,_)),
	writeln('Voce Errou'),nl,
	aggregate_all(count, content(_,_,_,_,_,_,_), Count),
	ifThenElse(Count=:=0,gameOver,capital).

capital :- 
	randomizeIdCapital(RandomId),	
	quizEngineCapital(RandomId).
