<?php

if ($_POST['answer']) {
    echo getAnswer($_POST['answer'], $_POST['idanswer']);
} else if ($_POST['question']) {
    echo getQuestion($_POST['question']);
}

function getAnswer($answer, $idanswer) {
    $consulta = "swipl -s capitalX.pl -g \"answer($idanswer,'$answer').\" -t halt.";
    return `$consulta`;
}

function getQuestion($id) {
    $consulta = "swipl -s capitalX.pl -g \"capital($id).\" -t halt.";
    return `$consulta`;
}
