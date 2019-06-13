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

    // Função para criar uma questão no Firebase
    document.getElementById("createQuestion").addEventListener('click', function createquestion() {
        var question = document.getElementById("question");
        var idquestion = create(question.value);
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

    // Função para manipular respostas
    document.querySelector('fieldset').addEventListener('click', function (e) {
        if (e.target && e.target.nodeName == 'BUTTON' && e.target.hasAttribute('data')) {
            if (e.target.getAttribute('data') == "inserirAnswer") {
                addAnswer(e);
            } else if (e.target.getAttribute('data') == "deleteAnswer") {
                removeAnswer(e);
            }
        }
    }, false);

    // Função para adicionar resposta
    function addAnswer(e) {
        var idquestion = document.getElementById("secret").value
        var ef = "question/" + idquestion + "/options";
        var ref = db.ref(ef);
        var answer_text = e.target.parentNode.parentNode.querySelector("input[type='text']").value;
        var answer_true = e.target.parentNode.parentNode.querySelector("input[type='checkbox']").checked;

        var data = {
            answer: answer_text,
            is_true: answer_true
        };
        var idanswer = ref.push(data);
        e.target.parentNode.parentNode.querySelector("input[type='hidden'].answersecret").value = idanswer.key;
        e.target.parentNode.parentNode.querySelector("input[type='text']").setAttribute('disabled', 'disabled');
        e.target.parentNode.parentNode.querySelector("input[type='checkbox']").setAttribute('disabled', 'disabled');
        e.target.parentNode.parentNode.querySelector("button[data='inserirAnswer']").parentNode.classList.add('hide');
        e.target.parentNode.parentNode.querySelector("button[data='deleteAnswer']").parentNode.classList.remove('hide');


        var $wrapper = e.target.parentNode.parentNode,
            HTMLNovo = `<div class="row">
                    <div class="input-field col s6"><i class="material-icons prefix">info_outline</i>
                      <input class="validate" type="text">
                      <input class="answersecret" type="hidden">
                      <label for="answer">Resposta</label>
                    </div>
                    <div class="switch col s4"><br><br>
                      <label>Falso
                        <input type="checkbox"><span class="lever"></span>Verdadeiro
                      </label>
                    </div>
                    <div class="col s2"><br><br>
                      <button class="btn waves-effect waves-light" data="inserirAnswer"><i class="material-icons">add_circle_outline</i></button>
                    </div>
                    <div class="col s2 hide"><br><br>
                      <button class="btn waves-effect waves-light red" data="deleteAnswer"><i class="material-icons">delete_forever</i></button>
                    </div>
                  </div>`;
        $wrapper.insertAdjacentHTML('afterend', HTMLNovo);

        console.log('dsad');
    }

    // Função para adicionar resposta
    function removeAnswer(e) {
        // var answer_text = e.target.parentNode.parentNode.querySelector("input[type='text']");
        // answer_text.removeAttribute('disabled');
        // answer_text.value = '';
        // answer_text.focus();

        // var answer_text = e.target.parentNode.parentNode.querySelector("input[type='checkbox']");
        // answer_text.removeAttribute('disabled');

        var idquestion = document.getElementById("secret").value
        var idanswer = e.target.parentNode.parentNode.querySelector("input[type='hidden'].answersecret").value
        var ef = "question/" + idquestion + "/options/" + idanswer;
        var ref = db.ref(ef);
        ref.remove();

        // e.target.parentNode.parentNode.querySelector("input[type='checkbox']").checked = false;
        // e.target.parentNode.parentNode.querySelector("button[data='inserirAnswer']").parentNode.classList.remove('hide');
        // e.target.parentNode.parentNode.querySelector("button[data='deleteAnswer']").parentNode.classList.add('hide');
        // if (document.querySelectorAll('fieldset > div').length > 1) {
        e.target.parentNode.parentNode.remove();
        // }
    }
});
