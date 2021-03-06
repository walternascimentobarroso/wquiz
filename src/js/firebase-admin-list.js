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
        var tbody = document.querySelector('tbody');
        data.forEach(function (data) {
            var tr = document.createElement('tr');

            var td = document.createElement('td');
            td.innerHTML = data.key;
            tr.appendChild(td);

            var td = document.createElement('td');
            var texto = data.val().description
            td.innerHTML = texto.substring(0, 50) + "...";
            td.className = "truncate";
            tr.appendChild(td);

            var td = document.createElement('td');
            td.innerHTML = '<i class="material-icons blue-text text-accent-4">visibility</i>';
            tr.appendChild(td);

            var td = document.createElement('td');
            td.innerHTML = '<i class="material-icons yellow-text text-accent-4">edit</i>';
            tr.appendChild(td);

            var td = document.createElement('td');
            td.innerHTML = '<a href="#" data="' + data.key + '"><i class="material-icons red-text text-accent-4">delete_forever</i></a>';
            tr.appendChild(td);

            tbody.appendChild(tr);
        });
    }

    // Pega o elemento e adiciona um listener para click
    document.querySelector('tbody').addEventListener('click', function (e) {
        if (e.target && e.target.nodeName == 'I' && e.target.parentNode.hasAttribute('data')) {
            e.target.parentNode.parentNode.parentNode.remove();
            db.ref('question/' + e.target.parentNode.getAttribute('data')).remove();
        }
    }, false);
});
