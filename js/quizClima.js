//ao comecar faz uma busca ajax pela questao;
//ao responder faz um verificação ajax pela sucesso da resposta

function ajax(fn, type) {
    $.ajax({
        url: 'http://localhost:8080/Programas/index.php',
        method: "POST",
        data: type,
        success: fn
    });
}

ajax(function (retorno) {
    $('#questao').html(retorno);
});


$('.nextButton').click(function () {
    console.log($('#resposta').val());
    $('.currentQuestion').html(Number($('.currentQuestion').html()) + 1);
    ajax(function (retorno) {
        $('#questao').html(retorno);
    });
});

//numero randomico
var maximo = 5;
var resultados = 5;

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

for (var i = 0; i < resultados; i++) {
    console.log(arr[i]);
}