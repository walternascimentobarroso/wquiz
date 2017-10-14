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

//idquestion = create('nameInput.value').key;
// function create(question) {
//     var data = {
//         description: question,
//         options: ""
//     };

//     return db.ref('question').push(data);
// }

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
