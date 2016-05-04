<?php

if ($_POST['answer']) {
    echo getAnswer($_POST['answer']);
} else if ($_POST['question']) {
    echo getQuestion($_POST['question']);
}

function getAnswer($answer) {
    $consulta = "swipl -s quizX.pl -g \"answer($answer,'Clima Tropical').\" -t halt.";
    var_dump($consulta);
    return `$consulta`;
}

function getQuestion($id) {
    $consulta = "swipl -s quizX.pl -g \"clima($id).\" -t halt.";
    var_dump($consulta);
    return `$consulta`;
}
