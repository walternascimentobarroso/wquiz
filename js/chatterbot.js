var $messages = $('.messages-content'),
        d, h, m,
        i = 0;

function ajax(fn, dados) {
    $.ajax({
        url: 'http://siege.localhost/Programas/conhecimento.php',
        method: "POST",
        data: dados,
        success: fn
    });
}

$(window).load(function () {
    $messages.mCustomScrollbar();
});

function updateScrollbar() {
    $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
        scrollInertia: 10,
        timeout: 0
    });
}

function setDate() {
    d = new Date()
    if (m != d.getMinutes()) {
        m = d.getMinutes();
        $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
    }
}

function insertMessage() {
    msg = $('.message-input').val();
    if ($.trim(msg) == '') {
        return false;
    }
    $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
    setDate();
    $('.message-input').val(null);
    updateScrollbar();
    ajax(retorno, {answer: msg.toLowerCase()});
}

$('.message-submit').click(function () {
    insertMessage();
});

$(window).on('keydown', function (e) {
    if (e.which == 13) {
        insertMessage();
        return false;
    }
});

function retorno(retorno) {
    if ($('.message-input').val() != '') {
        return false;
    }
    $('<div class="message loading new"><figure class="avatar"><img src="img/mapabrasil.png" /></figure><span></span></div>').appendTo($('.mCSB_container'));
    updateScrollbar();

    setTimeout(function () {
        $('.message.loading').remove();
        $('<div class="message new"><figure class="avatar"><img src="img/mapabrasil.png" /></figure>' + retorno + '</div>').appendTo($('.mCSB_container')).addClass('new');
        setDate();
        updateScrollbar();
    }, 1000);
}