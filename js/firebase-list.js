document.addEventListener('DOMContentLoaded', function () {
    'use strict';
    // Initialize Firebase
    var config = {
        apiKey: "AIzaSyAjLgBoeUEMAGZSRK3QXL3ZhceitQFMUE8",
        authDomain: "w-quiz.firebaseapp.com",
        databaseURL: "https://w-quiz.firebaseio.com",
        projectId: "w-quiz",
        storageBucket: "w-quiz.appspot.com",
        messagingSenderId: "1087904511091"
    };
    firebase.initializeApp(config);
    var db = firebase.database();

    //Lista questões existente
    db.ref("question/").on("value", function (data) {
        listando(data);
    }, function (errorObject) {
        console.log("Falha: " + errorObject.code);
    });

    var keyIndex = [];
    var totalQuestion = 0;
    var questionBase = '';
    var questionpage = 0;
    var totalPontos = 0;
    var gameChecked = {};

    function listando(data) {
        totalQuestion = data.numChildren();
        document.getElementById("progressbar").style.width = (questionpage + 1) / (totalQuestion / 100) + "%";
        document.getElementById("totalquestion").innerHTML = totalQuestion;
        var index = 0;
        questionBase = data;
        data.forEach(function (data) {
            keyIndex[index] = data.key;
            index = index + 1;
        });
        montedQuestion(data.child(keyIndex[0]));
        document.getElementById("imgconent").classList.add('hide');
        document.getElementById("contentnoimg").classList.remove('hide');
    }

    document.querySelector('#proxima').addEventListener('click', function (e) {
        gamePoint('next');
    }, false);

    /**
     * Função que realiza as operações do jogo(soma de pontos e verifica de respostas)
     */
    function gamePoint(direction) {
        console.log(gameChecked);
        var checado = document.querySelector('input[type="radio"]:checked');
        if (checado != null) {
            gameChecked[keyIndex[questionpage]] = {};
            gameChecked[keyIndex[questionpage]].questionChecked = checado.id;
        }
        if (direction == 'next') {
            if (questionpage != totalQuestion - 1) {
                if (questionpage == totalQuestion - 2) {
                    document.querySelector('#proxima').setAttribute('disabled', 'disabled');
                }
                document.querySelector('#anterior').removeAttribute('disabled');
                questionpage = questionpage + 1;
                document.getElementById("progressbar").style.width = (questionpage + 1) / (totalQuestion / 100) + "%";
                document.getElementById("questionpage").innerHTML = questionpage + 1;
            }

            montedQuestion(questionBase.child(keyIndex[questionpage]));
        } else {
            if (questionpage != 0) {
                if (questionpage == 1) {
                    document.querySelector('#anterior').setAttribute('disabled', 'disabled');
                }
                document.querySelector('#proxima').removeAttribute('disabled');
                questionpage = questionpage - 1;
                document.getElementById("progressbar").style.width = (questionpage + 1) / (totalQuestion / 100) + "%";
                document.getElementById("questionpage").innerHTML = questionpage + 1;
            }
            montedQuestion(questionBase.child(keyIndex[questionpage]));
        }
    }

    document.querySelector('#gameover').addEventListener('click', function (e) {
        // gamePoint(questionatual);
        this.classList.add('hide');
        document.querySelector('#back').classList.remove('hide');

        document.querySelector('#proxima').setAttribute('disabled', 'disabled');
        document.querySelector('#anterior').setAttribute('disabled', 'disabled');
        document.querySelector('.card-title').innerHTML = "Parabéns";
        var respostas = document.querySelector('#answers');
        respostas.innerHTML = `Você acertou ${totalPontos}/${totalQuestion}`;
        respostas.classList.remove('left-align');
        respostas.insertAdjacentHTML('afterend', '<div id="#answers"></div>');
        creatChart();
    }, false);

    document.querySelector('#anterior').addEventListener('click', function (e) {
        gamePoint('back');
    }, false);

    function montedQuestion(data) {
        document.querySelector('.card-title').innerHTML = data.val().description;
        var answers = data.val().options;
        var HTMLAnswers = '';
        var checado = 'checked="checked"';
        for (var key in answers) {
            var HTMLAnswer = '';
            if (gameChecked[data.key] != undefined && gameChecked[data.key].questionChecked == key) {
                HTMLAnswer = `<p><input name="group1" type="radio" id="${key}" value="${answers[key].is_true}" ${checado} />
                 <label for="${key}">${answers[key].answer}</label></p>`;
            } else {
                HTMLAnswer = `<p><input name="group1" type="radio" id="${key}" value="${answers[key].is_true}" />
                              <label for="${key}">${answers[key].answer}</label></p>`;
            }
            HTMLAnswers = HTMLAnswers + HTMLAnswer;
        }
        document.querySelector('#answers').innerHTML = HTMLAnswers;
    }

    var time = 30;
    setInterval(function () {
        document.querySelector('#time').innerHTML = time;
        document.querySelector('.determinate.red').style.width = (100 - (time / 0.3)) + '%';
        // time = time - 1;
        if (time == 0) {
            location.href = "gameover.html";
        }
    }, 1000);

    function creatChart() {
        google.charts.load('current', {
            'packages': ['corechart']
        });
        google.charts.setOnLoadCallback(drawChart);

        function drawChart() {
            google.charts.load('current', {
                'packages': ['corechart']
            });
            google.charts.setOnLoadCallback(drawChart);

            function drawChart() {
                var data = google.visualization.arrayToDataTable([
                    ['Descrição', 'Pontos'],
                    ['Certas', totalPontos],
                    ['Erradas', totalQuestion - totalPontos]
                ]);
                var options = {
                    title: 'Respostas',
                    pieHole: 0.4,
                    is3D: true,
                };
                var chart = new google.visualization.PieChart(document.getElementById('piechart'));
                chart.draw(data, options);
            }
        }
    }
});
