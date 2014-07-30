<!Doctype html>
<html lang="pt-br">
    <head>
        <meta charset="UTF-8" />
        <title>Pergunta</title>
    </head>
    <body>
        <h4>Cadastro de perguntas e respostas</h4>
        <form action="configuracao.php" method="POST">
            <fieldset>
                <legend>Pergunta 1: </legend>
                <label><strong>Qual o Comando para listar o diretorio atual</strong></label>
                <span>Marque a Resposta correta: </span>
                <label><input type="radio" name="resposta" />put </label>
                <label>echo <input type="radio" name="resposta" /></label>
                <label>pwd <input type="radio" name="resposta" /></label>
                <label>ls <input type="radio" name="resposta" /></label>
                <button>Enviar</button>
            </fieldset>
        </form>
    </body>
</html>