$.ajax({
    url: 'index.php',
    success: function (data) {
        alert(data);
    }
});


$('.nextButton').click(function () {
    $('.currentQuestion').html(Number($('.currentQuestion').html()) + 1);
    $('#questao').html(Number($('.currentQuestion').html()) + 1);
});