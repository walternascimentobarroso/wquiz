:- dynamic(gamePoint/1).
:- dynamic(ifThenElse/3).
:- dynamic(incrementPoint/2).

gamePoint(0).
numberOfQuestions(5).

	
ifThenElse(X, Y, _) :- X, !, Y. 
ifThenElse(_, _, Z) :- Z.

incrementPoint(Point,PointMoreOne) :- PointMoreOne is Point+1.

gameOver :- 
	writeln('Fim de jogo'),nl,
	write('Sua pontuação final foi: '),
	gamePoint(Point),writeln(Point),halt.

newPoint :- 
	gamePoint(Point), 
	incrementPoint(Point,PointMoreOne),
	retract(gamePoint(Point)),
	assertz(gamePoint(PointMoreOne)).
