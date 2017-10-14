$(document).ready(function () {
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

    var database = firebase.database();

    // Ao clicar no botão
    // addButton.addEventListener('click', function () {
        console.log(create('nameInput.value', 'ageInput.value'));
    // });

    // Função para criar um registro no Firebase
    function create(name, age) {
        var data = {
            description: name,
            options: age,
            test: {

            }
        };

        return database.ref().child('question').push(data);
    }
});
