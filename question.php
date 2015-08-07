<!Doctype html>
<html lang="pt-br">
    <head>
        <meta charset="UTF-8" />
        <title>Pergunta</title>
        <!-- Latest compiled and minified CSS -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">

        <!-- Optional theme -->
        <!--<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">-->
        <link rel="stylesheet" href="styli.css">

        <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
        <!-- Latest compiled and minified JavaScript -->
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
        <script language="JavaScript" src="change.js"></script>
    </head>
    <body>
        <h4>Cadastro de perguntas e respostas</h4>
        <form method="POST">
            <fieldset>
                <legend>Pergunta 1: </legend>
                <label><strong>Qual o Comando para listar o diretorio atual</strong></label><br />
                <span>Marque a Resposta correta: </span><br />
                <label><input type="radio" name="resposta" /> put </label><br />
                <label><input type="radio" name="resposta" /> echo</label><br />
                <label><input type="radio" name="resposta" /> pwd</label><br />
                <label><input type="radio" name="resposta" /> ls</label><br />
                <button>Enviar</button>
            </fieldset>
        </form>
        <div class="container-fluid bg-info">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h3><span class="label label-warning" id="qid">2</span> THREE is CORRECT</h3>
                    </div>
                    <div class="modal-body">
                        <div class="col-xs-3 col-xs-offset-5">
                            <div id="loadbar" style="display: none;">
                                <div class="blockG" id="rotateG_01"></div>
                                <div class="blockG" id="rotateG_02"></div>
                                <div class="blockG" id="rotateG_03"></div>
                                <div class="blockG" id="rotateG_04"></div>
                                <div class="blockG" id="rotateG_05"></div>
                                <div class="blockG" id="rotateG_06"></div>
                                <div class="blockG" id="rotateG_07"></div>
                                <div class="blockG" id="rotateG_08"></div>
                            </div>
                        </div>

                        <div class="quiz" id="quiz" data-toggle="buttons">
                            <label class="element-animation1 btn btn-lg btn-primary btn-block"><span class="btn-label"><i class="glyphicon glyphicon-chevron-right"></i></span> <input type="radio" name="q_answer" value="1">1 One</label>
                            <label class="element-animation2 btn btn-lg btn-primary btn-block"><span class="btn-label"><i class="glyphicon glyphicon-chevron-right"></i></span> <input type="radio" name="q_answer" value="2">2 Two</label>
                            <label class="element-animation3 btn btn-lg btn-primary btn-block"><span class="btn-label"><i class="glyphicon glyphicon-chevron-right"></i></span> <input type="radio" name="q_answer" value="3">3 Three</label>
                            <label class="element-animation4 btn btn-lg btn-primary btn-block"><span class="btn-label"><i class="glyphicon glyphicon-chevron-right"></i></span> <input type="radio" name="q_answer" value="4">4 Four</label>
                        </div>
                    </div>
                    <div class="modal-footer text-muted">
                        <span id="answer"></span>
                    </div>
                </div>
            </div>
        </div>
    </body>
</html>