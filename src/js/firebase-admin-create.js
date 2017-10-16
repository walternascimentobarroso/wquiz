$(document).ready(function () {
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

    // Função para criar uma questão no Firebase
    document.getElementById("createQuestion").addEventListener('click', function createquestion() {
        var question = document.getElementById("question");
        var idquestion = create(question.value);
        console.log(idquestion.key);
        document.getElementById("secret").value = idquestion.key;
        question.setAttribute('disabled', 'disabled');
        this.classList.add('hide');
        document.getElementById("deleteQuestion").classList.remove('hide');

        document.getElementsByTagName('fieldset')[0].classList.remove('hide');
    });

    // Função para remover uma questão no Firebase
    document.getElementById("deleteQuestion").addEventListener('click', function createquestion() {
        var question = document.getElementById("question");
        question.removeAttribute('disabled');
        question.value = '';
        question.focus();
        this.classList.add('hide');
        document.getElementById("createQuestion").classList.remove('hide');

        document.getElementsByTagName('fieldset')[0].classList.add('hide');

        db.ref('question/' + document.getElementById("secret").value).remove();
    });

    // var idquestion = create('nameInput.value').key;
    function create(question) {
        var data = {
            description: question,
            options: ""
        };

        return db.ref('question').push(data);
    }

    // var ref = db.ref("question/" + idquestion + "/options");

    // // Ler as respostas
    // ref.on("value", function (snapshot) {
    //     console.log(snapshot.val());
    // }, function (errorObject) {
    //     console.log("The read failed: " + errorObject.code);
    // });

    // // Função para criar as respostas
    // // createAnswer('nameInput.value');
    // function createAnswer(answer) {
    //     var data = {
    //         description: answer,
    //         is_true: "true"
    //     };

    //     return ref.push(data);
    // }
});
