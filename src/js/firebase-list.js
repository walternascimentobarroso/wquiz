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
    }

    document.querySelector('#proxima').addEventListener('click', function (e) {
        if (questionpage != totalQuestion - 1) {
            if (questionpage == totalQuestion - 2) {
                this.setAttribute('disabled', 'disabled');
            }
            document.querySelector('#anterior').removeAttribute('disabled');
            questionpage = questionpage + 1;
            document.getElementById("progressbar").style.width = (questionpage + 1) / (totalQuestion / 100) + "%";
            document.getElementById("questionpage").innerHTML = questionpage + 1;
        }
        montedQuestion(questionBase.child(keyIndex[questionpage]));
    }, false);

    document.querySelector('#anterior').addEventListener('click', function (e) {
        if (questionpage != 0) {
            if (questionpage == 1) {
                this.setAttribute('disabled', 'disabled');
            }
            document.querySelector('#proxima').removeAttribute('disabled');
            questionpage = questionpage - 1;
            document.getElementById("progressbar").style.width = (questionpage + 1) / (totalQuestion / 100) + "%";
            document.getElementById("questionpage").innerHTML = questionpage + 1;
        }
        montedQuestion(questionBase.child(keyIndex[questionpage]));
    }, false);

    function montedQuestion(data) {
        document.querySelector('.card-title').innerHTML = data.val().description;
        var answers = data.val().options;
        for (var key in answers) {
            document.querySelector('#answers').innerHTML = answers[key].answer;
        }
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

});
