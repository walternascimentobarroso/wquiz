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

    function listando(data) {
        data.forEach(function (data) {
            document.querySelector('.card-title').innerHTML = data.val().description;
            var answers = data.val().options;
            for (var key in answers) {
                document.querySelector('#answers').innerHTML = answers[key].answer;
            }
        });
    }

    var time = 30;
    setInterval(function () {
        document.querySelector('#time').innerHTML = time;
        document.querySelector('.determinate.red').style.width = (100 - (time / 0.3)) + '%';
        time = time - 1;
        if (time == 0) {
            location.href = "gameover.html";
        }
    }, 1000);

});
