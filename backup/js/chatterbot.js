var $messages = $('.messages-content'),
        d, h, m,
        i = 0;

function ajax(fn, dados) {
    $.ajax({
        url: '/Programas/conhecimento.php',
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

//function removeAcento(strToReplace) {
//    var str_acento = "áàãâäéèêëíìîïóòõôöúùûüçÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÖÔÚÙÛÜÇ";
//    var str_sem_acento = "aaaaaeeeeiiiiooooouuuucAAAAAEEEEIIIIOOOOOUUUUC";
//    var nova = "";
//    for (var i = 0; i < strToReplace.length; i++) {
//        if (str_acento.indexOf(strToReplace.charAt(i)) != -1) {
//            nova += str_sem_acento.substr(str_acento.search(strToReplace.substr(i, 1)), 1);
//        } else {
//            nova += strToReplace.substr(i, 1);
//        }
//    }
//    return nova;
//}

function removeAcento(s) {
    var map = {"â": "a", "Â": "A", "à": "a", "À": "A", "á": "a", "Á": "A", "ã": "a", "Ã": "A", "ê": "e", "Ê": "E", "è": "e", "È": "E", "é": "e", "É": "E", "î": "i", "Î": "I", "ì": "i", "Ì": "I", "í": "i", "Í": "I", "õ": "o", "Õ": "O", "ô": "o", "Ô": "O", "ò": "o", "Ò": "O", "ó": "o", "Ó": "O", "ü": "u", "Ü": "U", "û": "u", "Û": "U", "ú": "u", "Ú": "U", "ù": "u", "Ù": "U", "ç": "c", "Ç": "C"};
    return s.replace(/[\W\[\] ]/g, function (a) {
        return map[a] || a;
    });
}

function trim(str) {
    return str.replace(/^\s+|\s+$/g, "");
}

function fixString(word) {
    var newWord = removeAcento(word);
    newWord = newWord.replace(/[\\\^\$\*\+\?\!\,\.\(\)\|\{\}\[\]]/g, '');
    return trim(newWord);
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
    ajax(retorno, {answer: fixString(msg.toLowerCase())});
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
