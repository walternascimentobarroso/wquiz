<?php

if ($_POST['answer']) {
    echo getAnswer($_POST['answer']);
}

function getAnswer($answer) {
    $consulta = "swipl -s conhecimentoX.pl -g \"chat('$answer').\" -t halt.";
    return saida($consulta);
}

function saida($consulta) {
    unicode_decode($consulta);
    exec($consulta, $output);
    return unicode_decode($output[0]);
}

function replace_unicode_escape_sequence($match) {
    return mb_convert_encoding(pack('H*', $match[1]), 'UTF-8', 'UCS-2BE');
}

function unicode_decode($str) {
    return preg_replace_callback('/\\\\u([0-9a-f]{4})/i', 'replace_unicode_escape_sequence', $str);
}
