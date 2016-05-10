:- dynamic(conhecimento/2).
%climas
conhecimento('qual e o clima predominante na maior parte do brasil',['Clima Tropical']).
conhecimento('qual e o clima quente mais proximo do arido',['Clima Semi-Árido']).
conhecimento('qual clima abrange a porcao do territorio brasileiro ao sul do tropico de capricornio',['Clima Subtropical']).
conhecimento('qual e o clima que compreende a amazonia brasileira',['Clima Equatorial']).
conhecimento('qual clima compreende as proximidades do litoral desde o rio grande do norte ate a parte setentrional do estado de sao paulo',['Clima litoraneo umido']).

%capitais
conhecimento('qual e a capital de roraima',['Boa Vista']).
conhecimento('qual e a capital do amazonas',['Manaus']).
conhecimento('qual e a capital do acre',['Rio Branco']).
conhecimento('qual e a capital do para',['Belém']).
conhecimento('qual e a capital de goias',['Goiânia']).

%conhecimento basico
conhecimento('oi', 
	['Ola!',
 	 'Oi, Como vai você?']).

conhecimento('como voce se chama?', ['Meu nome é Professor SIEGE.']).

conhecimento('qual o seu nome?', ['Meu nome é Professor SIEGE.']).

conhecimento('tudo bem', 
	['Tudo otimo!',
 	 'Tudo bem, e você?']).

conhecimento('quem e voce', 
	['Sou um robo.']).

conhecimento(bye, 
	['Ate mais! Foi otimo conversar com voce']).

conhecimento(_, []).
