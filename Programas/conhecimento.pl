:- dynamic(conhecimento/2).

conhecimento('oi', 
	['Olá!',
 	 'Oi, Como vai você?']).

conhecimento('como você se chama?', ['Meu nome é Professor SIEGE.']).

conhecimento('qual o seu nome?', ['Meu nome é Professor SIEGE.']).

conhecimento('tudo bem?', 
	['Tudo otimo!',
 	 'Tudo bem, e você?']).

conhecimento('quem é você?', 
	['Sou um robo.',
 	 'Por que vc quer saber?']).

conhecimento(bye, 
	['Ate mais! Foi otimo conversar com voce']).

conhecimento(_, []).
