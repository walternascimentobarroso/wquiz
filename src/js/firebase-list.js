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
        // console.log(data.val());
        data.forEach(function (data) {
            // console.log(data.val());
            document.querySelector('.card-title').innerHTML = data.val().description;
            document.querySelector('#answers').innerHTML = data.val().options;
        });
    }

    time = 30;
    setInterval( function(){
        document.querySelector('#time').innerHTML = time;
        document.querySelector('.determinate.red').style.width = (100 - (time/0.3))+'%';
        time = time - 1;
        if(time == 0) {
            location.href="gameover.html";
        }
    }, 1000);

});
