<!Doctype html>
<html lang="pt-br">
    <head>
        <meta charset="UTF-8" />
        <title>Login</title>
    </head>
    <body>
        <h4>Cadastro de perguntas e respostas</h4>
        <form method="POST">
            <fieldset>
                <legend>Entre com a pergunta: </legend>
                <label>Tema:
                    <select>
                        <option>Linux</option>
                        <option>PHP</option>
                        <option>CSS</option>
                        <option>HTML</option>
                        <option>JAVASCRIPT</option>
                    </select>
                </label><br />
                <label>Pergunta: <input type="text" name="user" /></label><br />
                <legend>Entre com as Respostas: </legend>
                <label>Resposta Certa: <input type="text" name="certa" /></label><br />
                <label>Resposta Errada: <input type="text" name="errada1" /></label><br />
                <label>Resposta Errada: <input type="text" name="errada2" /></label><br />
                <label>Resposta Errada: <input type="text" name="errada3" /></label><br />
                <button>Enviar</button>
            </fieldset>
        </form>
    </body>
</html>