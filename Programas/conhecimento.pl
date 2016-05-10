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

%extremos
conhecimento('qual o ponto do monte caburai, roraima',['Norte']).
conhecimento('qual o ponto do chui, rio grande do sul', ['Sul']).
conhecimento('qual o Ponta do seixas, em cabo branco',['Leste']).
conhecimento('qual o nascente do rio moa, na serra de contamana ', ['Oeste']).
conhecimento('qual o ponto mais alto do brasil', ['Pico da Neblina']).

%relevos
conhecimento('sao formas de relevo elevadas, com altitudes superiores a 300 metros',['Planaltos']).
conhecimento('sao areas rebaixadas em consequencia da erosao, que se formam entre as bacias sedimentares e os escudos cristalinos', ['Depressões']).
conhecimento('sao unidades de relevo geologicamente muito recentes',['Planícies']).
conhecimento('caracterizam-se pela formacao de escarpas em areas de fronteira com as depressoes',['Planaltos']).
conhecimento('sua formacao ocorre em virtude da sucessiva deposicao de material de origem marinha',['Planícies']).

%vegetações
conhecimento('milhares de especies vegetais nao perde suas folhas no outono ou seja esta sempre verde e dividida em 3 tipos de matas: igapo varzea terra firme',['Floresta Amazonica']).
conhecimento('e menos densa que a floresta amazonica quase 100% dela ja foi destruida porem antes podiamos encontrar o pau-brasil cedro peroba e o jacaranda', ['Mata Atlantica']).
conhecimento('vegetacao tipica do clima semi-arido do sertao nordestino vegetacao pobre com plantas que sao adaptadas a aridez sao as chamadas plantas xerofilas',['Caatinga']).
conhecimento('corresponde as areas de clima subtropical e uma mata homogenea pois ha o predominio de pinheiros erva-mate imbuia canela cedros e ipes',['Mata de Araucaria']).
conhecimento('tipica da regiao centro-oeste do brasil e formada por plantas tropofilas ou seja plantas adaptadas a uma estacao seca e outra umida',['Cerrado']).

%conhecimento basico
conhecimento('oi', 
	['Ola!',
 	 'Oi, Como vai você?']).

conhecimento('como voce se chama', ['Meu nome é Professor SIEGE.']).

conhecimento('qual o seu nome', ['Meu nome é Professor SIEGE.']).

conhecimento('tudo bem', 
	['Tudo otimo!',
 	 'Tudo bem, e você?']).

conhecimento('quem e voce', 
	['Sou um robo.']).

conhecimento(bye, 
	['Ate mais! Foi otimo conversar com voce']).

conhecimento(_, []).
