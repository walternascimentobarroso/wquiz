//ao comecar faz uma busca ajax pela questao;
//ao responder faz um verificação ajax pela sucesso da resposta

var number = retornaAleatorio();
var i = 0;
var pts = 0;

function ajax(fn, dados) {
    $.ajax({
        url: 'http://localhost:8080/Programas/extremo.php',
        method: "POST",
        data: dados,
        success: fn
    });
}

function questao(retorno) {
    $('#questao').html(retorno);
}
function resposta(retorno) {
    retorno == 1 ? pts++ : pts;
}



ajax(questao, {question: number[i]});



$('.nextButton').click(avante);
$('.fimButton').click(finalizar);

$('#resposta').keypress(function (e) {
    if (e.wich == 13 || e.keyCode == 13) {
        if (Number($('.currentQuestion').html()) === Number($('.totalQuestion').html())) {
            finalizar();
        } else {
            avante();
        }
    }
});

function finalizar() {
    if (pts == 0) {
        $('.principal').html('Que pena');
        $('#pontos').html(pts + ' ponto');
        $('.mensagem').html('Continue tentando');
    } else if (pts > 1) {
        $('#pontos').html(pts + ' pontos');
    } else {
        $('#pontos').html(pts + ' ponto');
    }
    $('.fimQuestion').removeClass('hidden');
}

function avante() {
    if (Number($('.currentQuestion').html()) === Number($('.totalQuestion').html()) - 1) {
        $('.fimButton').removeClass('hidden');
        $('.nextButton').addClass('hidden');
    }
    ajax(resposta, {answer: $('#resposta').val(), idanswer: number[i]});
    $('.currentQuestion').html(Number($('.currentQuestion').html()) + 1);
    i++;
    ajax(questao, {question: number[i]});
    $('#resposta').val('');
    $('#resposta').focus();
}

function retornaAleatorio() {
    //numero randomico
    var maximo = 5;

    var i, arr = [];
    for (i = 0; i < maximo; i++) {
        arr[i] = i + 1;
    }

    var p, n, tmp;
    for (p = arr.length; p; ) {
        n = Math.random() * p-- | 0;
        tmp = arr[n];
        arr[n] = arr[p];
        arr[p] = tmp;
    }
    return arr;
//    for (var i = 0; i < 5; i++) {
//        console.log(arr[i]);
//    }
}