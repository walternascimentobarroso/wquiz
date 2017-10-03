:- encoding(utf8).
:- include(conhecimento).

search(Input, Found) :-
	conhecimento(Input, Found), !.

quit(Input):- 
	Input = bye.
	
response([], Response) :- 
	write('Nao entendo o que vc quer dizer.'), nl,
	write('Por favor, escreva uma pergunta e me ensine a resposta.'), nl,
	write('Pergunta: '),
	read(Q),
	write('Resposta: '),
	read(A),
	asserta(conhecimento(Q,[A])),
	Response = 'Ok, continue falando comigo.', !.

response(RespList, Response) :-
	length(RespList, NumOfResponse),
	IndexOfResponse is random(NumOfResponse),
	nth0(IndexOfResponse, RespList, Response), !.
		
chat(Input):- 
	search(Input, ListOfResponse),
	response(ListOfResponse, Response),
	write(Response), nl,
	quit(Input).

