<!Doctype html>
<html lang="pt-br">
    <head>
        <meta charset="UTF-8" />
        <title>Login</title>
    </head>
    <body>
        <h4>Cadastro de perguntas e respostas</h4>
        <form action="configuracao.php" method="POST">
            <fieldset>
                <legend>Entre com a pergunta: </legend>
                <label>Pergunta: <input type="text" name="user" /></label>
                <legend>Entre com as Respostas: </legend>
                <label>Resposta Certa: <input type="text" name="certa" /></label>
                <label>Resposta Errada: <input type="text" name="errada1" /></label>
                <label>Resposta Errada: <input type="text" name="errada2" /></label>
                <label>Resposta Errada: <input type="text" name="errada3" /></label>
                <button>Enviar</button>
            </fieldset>
        </form>
    </body>
</html>