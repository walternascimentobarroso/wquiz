document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    var quiz = [{
        "question": "What is the full form of IP?",
        "choices": ["Internet Provider", "Internet Port", "Internet Protocol"],
        "correct": "Internet Protocol"
    }, {
        "question": "Who is the founder of Microsoft?",
        "choices": ["Bill Gates", "Steve Jobs", "Steve Wozniak"],
        "correct": "Bill Gates"
    }, {
        "question": "1 byte = ?",
        "choices": ["8 bits", "64 bits", "1024 bits", "dasd"],
        "correct": "dasd"
    }, {
        "question": "The C programming language was developed by?",
        "choices": ["Brendan Eich", "Dennis Ritchie", "Guido van Rossum"],
        "correct": "Dennis Ritchie"
    }, {
        "question": "What does CC mean in emails?",
        "choices": ["Carbon Copy", "Creative Commons", "other"],
        "correct": "Carbon Copy"
    }];

    document.getElementById("imgconent").classList.add('hide');
    document.getElementById("contentnoimg").classList.remove('hide');


    // define elements
    var content = $("content"),
        questionContainer = $("question"),
        choicesContainer = $("choices"),
        backBtn = $("anterior"),
        submitBtn = $("submit"),
        gameoverBtn = $("gameover");

    // init vars
    var currentQuestion = 0,
        currentPage = 1,
        score = 0,
        askingQuestion = true;

    var totalQuestion = quiz.length;
    document.getElementById("progressbar").style.width = (currentQuestion + 1) / (totalQuestion / 100) + "%";
    document.getElementById("totalquestion").innerHTML = totalQuestion;

    function $(id) {
        return document.getElementById(id);
    }

    function askQuestion() {
        var choices = quiz[currentQuestion].choices,
            choicesHtml = "";

        // loop through choices, and create radio buttons
        for (var i = 0; i < choices.length; i++) {
            choicesHtml += "<input type='radio' name='quiz" + currentQuestion +
                "' id='choice" + (i + 1) +
                "' value='" + choices[i] + "'>" +
                " <label for='choice" + (i + 1) + "'>" + choices[i] + "</label><br>";
        }

        // load the question
        questionContainer.textContent = "Q" + (currentQuestion + 1) + ". " +
            quiz[currentQuestion].question;

        // load the choices
        choicesContainer.innerHTML = choicesHtml;

        // setup for the first time
        if (currentQuestion === 0) {
            submitBtn.textContent = "Enviar";
        }
    }

    function checkAnswer() {

        // are we asking a question, or proceeding to next question?
        if (askingQuestion) {
            submitBtn.textContent = "Próximo";
            askingQuestion = false;

            // determine which radio button they clicked
            var userpick,
                correctIndex,
                radios = document.getElementsByName("quiz" + currentQuestion);
            for (var i = 0; i < radios.length; i++) {
                if (radios[i].checked) { // if this radio button is checked
                    userpick = radios[i].value;
                }

                // get index of correct answer
                if (radios[i].value == quiz[currentQuestion].correct) {
                    correctIndex = i;
                }
            }

            // setup if they got it right, or wrong
            var labelStyle = document.getElementsByTagName("label")[correctIndex].style;
            labelStyle.fontWeight = "bold";
            if (userpick == quiz[currentQuestion].correct) {
                score++;
                labelStyle.color = "green";
            } else {
                labelStyle.color = "red";
            }

            if (currentQuestion + 1 == totalQuestion) {
                document.querySelector('#submit').setAttribute('disabled', 'disabled');
            }

        } else { // move to next question
            document.querySelector('#anterior').removeAttribute('disabled');
            currentPage = currentPage + 1
            document.getElementById("questionpage").innerHTML = currentPage;
            // setting up so user can ask a question
            askingQuestion = true;
            // change button text back to "Submit Answer"
            submitBtn.textContent = "Enviar";
            // if we're not on last question, increase question number
            if (currentQuestion < quiz.length - 1) {
                currentQuestion++;
                askQuestion();
            } else {
                showFinalResults();
            }
        }
    }

    function showFinalResults() {
        content.innerHTML = "<h2>You've complited the quiz!</h2>" +
            "<h2>Below are your results:</h2>" +
            "<h2>" + score + " out of " + quiz.length + " questions, " +
            Math.round(score / quiz.length * 100) + "%<h2>";
    }

    function backQuestion() {
        if (currentQuestion == 1) {
            document.querySelector('#anterior').setAttribute('disabled', 'disabled');
        }
        document.querySelector('#submit').removeAttribute('disabled');
        currentQuestion--;
        document.getElementById("questionpage").innerHTML = currentPage;
        // setting up so user can ask a question
        askingQuestion = true;
        // change button text back to "Submit Answer"
        submitBtn.textContent = "Enviar";
        // if we're not on last question, increase question number
        askQuestion();
    }

    window.addEventListener("load", askQuestion, false);
    submitBtn.addEventListener("click", checkAnswer, false);
    backBtn.addEventListener("click", backQuestion, false);
    gameoverBtn.addEventListener("click", showFinalResults, false);


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
