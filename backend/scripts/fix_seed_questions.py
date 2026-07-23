#!/usr/bin/env python3
"""Apply content/correctness fixes to QUESTIONS_DATA in php_seed_data.py."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "app" / "services" / "php_seed_data.py"

FIXES: dict[int, dict] = {
    10: {
        "prompt": (
            "[Q10] Which regular expression will match each of these strings?\n\n"
            "```text\n"
            "(000) 555-1234\n"
            "000 555 1234\n"
            "000-555-1234\n"
            "000.555.1234\n"
            "```"
        ),
        "explanation": (
            "The samples use optional parentheses around the area code and different "
            "single-character separators (space, hyphen, or dot).\n"
            "Only /^\\(?\\d{3}\\)?[.\\-\\s]\\d{3}[.\\-\\s]\\d{4}$/ matches all four forms.\n"
            "Patterns that require digits without optional parentheses miss '(000) 555-1234'.\n"
            "Patterns that force parentheses miss the other three.\n"
            "Correct answer: /^\\(?\\d{3}\\)?[.\\-\\s]\\d{3}[.\\-\\s]\\d{4}$/."
        ),
        "options": [
            (r"/^.*\d{3}.\d{3}.\d{4}$/", False),
            (r"/^\(\d{3}\)[.\-\s]\d{3}[.\-\s]\d{4}$/", False),
            (r"/^\d{3}[.\-\s]\d{3}[.\-\s]\d{4}$/", False),
            (r"/^\(?\d{3}\)?[.\-\s]\d{3}[.\-\s]\d{4}$/", True),
        ],
    },
    22: {
        "prompt": "[Q22] What purpose do namespaces fulfill?",
        "explanation": (
            "Namespaces organize symbols (classes, functions, constants) and avoid name "
            "collisions between libraries.\n"
            "They are not an alternative to classes and do not improve performance by themselves.\n"
            "Correct answer: Organizing code and avoiding name collisions."
        ),
        "options": [
            ("Alternative to classes.", False),
            ("Improved performance.", False),
            ("Organizing code and avoiding name collisions.", True),
            ("All of the above.", False),
        ],
    },
    23: {
        "explanation": (
            "Heredoc interpolates variables.\n"
            "$text1 becomes 'This is text'.\n"
            "$text2 interpolates $text1, so it also becomes 'This is text'.\n"
            'echo "$text2" therefore prints: This is text.'
        ),
    },
    25: {
        "prompt": (
            "[Q25] Which of these code snippets DO NOT write the exact content of the file "
            "source.txt to target.txt? (Choose 2)"
        ),
        "explanation": (
            "(a) and (e) correctly copy the file via file_get_contents().\n"
            "(b) file() keeps trailing newlines; joining with \"\\n\" inserts extra newlines, "
            "so the copy is not exact.\n"
            "(c) file_put_contents() accepts a stream resource and copies remaining bytes "
            "(like stream_copy_to_stream()), so this DOES write the content.\n"
            "(d) readfile() echoes to output and returns an int (byte count); that integer "
            "is what gets written to target.txt.\n"
            "Correct answers: (b) and (d)."
        ),
        "options": [
            (
                '$handle = fopen("target.txt", "w+");\n'
                'fwrite($handle, file_get_contents("source.txt"));\n'
                "fclose($handle);",
                False,
            ),
            ('file_put_contents("target.txt", join(file("source.txt"), "\\n"));', True),
            ('file_put_contents("target.txt", fopen("source.txt", "r"));', False),
            ('file_put_contents("target.txt", readfile("source.txt"));', True),
            ('file_put_contents("target.txt", file_get_contents("source.txt"));', False),
        ],
    },
    26: {
        "prompt": (
            "[Q26] Is the following code vulnerable to SQL Injection?\n\n"
            "```php\n"
            "// assume $pdo is a valid PDO connection\n"
            "$age  = $pdo->quote((int) $age);\n"
            "$name = $pdo->quote($name);\n"
            '$query = "SELECT * FROM users WHERE name LIKE $name AND age = $age";\n'
            "$result = $pdo->query($query);\n"
            "```"
        ),
        "explanation": (
            "PDO::quote() returns a correctly quoted/escaped SQL string literal, and $age is "
            "cast to int before quoting.\n"
            "With those values interpolated (without wrapping quote() results in extra quotes), "
            "this snippet is protected from classic SQL injection.\n"
            "Prepared statements are still the preferred approach.\n"
            "Correct answer: No, the code is fully protected from SQL Injection."
        ),
        "options": [
            ("Yes, because the $name variable is improperly escaped.", False),
            (
                "Yes, because even though $age and $name are escaped, nothing prevents their "
                "contents from modifying the SQL.",
                False,
            ),
            ("Yes, because the $age variable is improperly escaped.", False),
            ("No, the code is fully protected from SQL Injection.", True),
            ("Yes, because you cannot prevent SQL Injection when using PDO.", False),
        ],
    },
    29: {
        "explanation": (
            '"22" + "0.2" uses numeric addition → 22.2.\n'
            "23 . 1 concatenates as strings → '231'.\n"
            "echo with a comma prints arguments one after another with no separator, "
            "so the output is 22.2231 (not 22.2,231)."
        ),
        "options": [
            ("56.2", False),
            ("22.2,231", False),
            ("22.2231", True),
            ("220.2231", False),
        ],
    },
    36: {
        "prompt": (
            "[Q36] The class Person should have the two protected properties lastName and "
            "firstName. The class should allow setting both properties upon object "
            "instantiation. You want to write as little code as possible to achieve this.\n"
            "Which of the following approaches satisfies these requirements?"
        ),
        "explanation": (
            "Constructor property promotion (PHP 8+) declares, types, and initializes "
            "protected properties in one short constructor signature.\n"
            "Manual properties + assignments work but are more code.\n"
            "TypeScript-style `protected $name: string` is invalid PHP.\n"
            "Public properties violate the protected requirement.\n"
            "Correct answer: the promoted `protected string` constructor."
        ),
        "options": [
            (
                "class Person {\n"
                "    protected $firstName;\n"
                "    protected $lastName;\n"
                "    public function __construct($firstName, $lastName) {\n"
                "        $this->firstName = $firstName;\n"
                "        $this->lastName = $lastName;\n"
                "    }\n"
                "}",
                False,
            ),
            (
                "class Person {\n"
                "    public function __construct(\n"
                "        protected string $firstName,\n"
                "        protected string $lastName\n"
                "    ) {\n"
                "    }\n"
                "}",
                True,
            ),
            (
                "class Person {\n"
                "    public function __construct(\n"
                "        protected $firstName: string,\n"
                "        protected $lastName: string\n"
                "    ) {\n"
                "    }\n"
                "}",
                False,
            ),
            (
                "class Person {\n"
                "    public string $firstName;\n"
                "    public string $lastName;\n"
                "    public function __construct($firstName, $lastName) {\n"
                "        $this->firstName = $firstName;\n"
                "        $this->lastName = $lastName;\n"
                "    }\n"
                "}",
                False,
            ),
        ],
    },
    38: {
        "explanation": (
            "Casting an object to array exposes public properties under their plain names "
            "(so 'c' exists).\n"
            'Private properties become mangled keys like "\\0Bar\\0a", so array_key_exists'
            "('a', $x) is false.\n"
            "Output: false-true."
        ),
    },
    41: {
        "prompt": (
            "[Q41] What is the output of the following code?\n\n"
            "```php\n"
            "<?php\n"
            "declare(strict_types=1);\n"
            "function add (int $a, int $b) {\n"
            "    return $a + $b;\n"
            "}\n"
            "try {\n"
            "    echo add(1, 2.0);\n"
            "} catch (Exception $ex) {\n"
            "    echo 'Exception';\n"
            "} catch (Error $err) {\n"
            "    echo 'Error';\n"
            "} catch (Throwable $e) {\n"
            "    echo 'Throwable';\n"
            "}\n"
            "```"
        ),
    },
    42: {
        "prompt": "[Q42] What is the purpose of the never return type?",
        "explanation": (
            "never means the function never returns normally — it must throw, exit, or "
            "otherwise terminate the request.\n"
            "That is stricter than void (which returns null / no value but still returns).\n"
            "Correct answer: the function never returns normally (always throws or exits)."
        ),
        "options": [
            (
                "It indicates that there will never be a type restriction on the value that "
                "the function returns.",
                False,
            ),
            ("It indicates that a variable will never have a value.", False),
            (
                "It indicates that a function never returns normally (it always throws or exits).",
                True,
            ),
            ("It indicates that a function will never be run.", False),
        ],
    },
    43: {
        "prompt": (
            "[Q43] Given a PHP value, which of these code samples shows how to convert the "
            "value to JSON?"
        ),
        "explanation": (
            "The standard PHP API is json_encode($value).\n"
            "There is no built-in Json class, __toJson() method, or Json::encode() helper "
            "in core PHP.\n"
            "Correct answer: $string = json_encode($value);"
        ),
        "options": [
            ("$json = new Json($value);", False),
            ("$string = $value->__toJson();", False),
            ("$string = Json::encode($value);", False),
            ("$string = json_encode($value);", True),
        ],
    },
    45: {
        "explanation": (
            "The table already has id=1, so INSERT id=1 fails with a primary key violation.\n"
            "As of PHP 8.0, PDO defaults to ERRMODE_EXCEPTION, so execute() throws "
            "PDOException.\n"
            'The catch block runs and prints "Failure!" (then rethrows).\n'
            'Correct answer: PK violation + "Failure!" message.'
        ),
        "options": [
            (
                'The INSERT will fail because of a primary key violation, and the user will '
                'see the "Success!" message.',
                False,
            ),
            (
                'The INSERT will succeed and the user will see the "Success!" message.',
                False,
            ),
            (
                "The INSERT will fail because of a primary key violation, and the user will "
                "see a PDO warning message.",
                False,
            ),
            (
                'The INSERT will fail because of a primary key violation, and the user will '
                'see the "Failure!" message.',
                True,
            ),
        ],
    },
    54: {
        "explanation": (
            "Statements that are NOT true:\n"
            "(c) Not always: a static anonymous function created in object context is not "
            "bound to $this.\n"
            "(d) Assigning a Closure to an object property does not bind it by itself — "
            "use bindTo()/Closure::bind().\n"
            "Non-static closures created inside a method are auto-bound, and bind()/bindTo() "
            "exist for rebinding.\n"
            "Correct answers: (c) and (d)."
        ),
    },
    55: {
        "explanation": (
            "False statements:\n"
            "A final class cannot be extended.\n"
            "PHP does not allow multiple inheritance of classes (a class may extend only one "
            "parent).\n"
            "A class with a final method may still be extended, and a final class may be "
            "instantiated.\n"
            "Correct answers: (c) and (d)."
        ),
    },
    59: {
        "prompt": (
            "[Q59] Given the following, what is the result of running test.php?\n\n"
            "functions.php:\n\n"
            "```php\n"
            "<?php\n"
            "function oops(string $input)\n"
            "{\n"
            "    return $input;\n"
            "}\n"
            "```\n\n"
            "test.php:\n\n"
            "```php\n"
            "<?php\n"
            "declare(strict_types=1);\n"
            "include 'functions.php';\n"
            "var_dump(oops(12));\n"
            "```"
        ),
        "explanation": (
            "strict_types=1 in test.php applies to function calls made from that file.\n"
            "oops(12) therefore passes an int where string is required and raises TypeError.\n"
            "Correct answer: Fatal error: Uncaught TypeError."
        ),
        "options": [
            ("Fatal error: Uncaught TypeError", True),
            ('string(2) "12"', False),
            ("Parse error: syntax error, unexpected 'string'", False),
            ("Recoverable fatal error", False),
        ],
    },
}


def _qnum(prompt: str) -> int | None:
    match = re.match(r"\[Q(\d+)\]", prompt)
    return int(match.group(1)) if match else None


def _format_str(value: str) -> str:
    if "\n" in value or "'" in value:
        # Prefer double quotes when the string has single quotes and no "
        if "'" in value and '"' not in value:
            escaped = (
                value.replace("\\", "\\\\")
                .replace('"', '\\"')
                .replace("\n", "\\n")
                .replace("\t", "\\t")
            )
            return f'"{escaped}"'
        return repr(value)
    return repr(value)


def _format_options(options: list[tuple[str, bool]]) -> str:
    lines = ["        \"options\": ["]
    for text, ok in options:
        lines.append(f"            ({_format_str(text)}, {ok}),")
    lines.append("        ],")
    return "\n".join(lines)


def main() -> None:
    # Import after path setup
    import sys

    sys.path.insert(0, str(ROOT))
    from app.services.php_seed_data import QUESTIONS_DATA  # noqa: WPS433

    for item in QUESTIONS_DATA:
        num = _qnum(item["prompt"])
        if num is None or num not in FIXES:
            continue
        patch = FIXES[num]
        item.update(patch)

    # Rebuild QUESTIONS_DATA literal while preserving header/footer of the module.
    source = SEED.read_text(encoding="utf-8")
    start = source.index("QUESTIONS_DATA: list[dict] = [")
    end = source.index("\n_assigned = ", start)

    chunks: list[str] = ["QUESTIONS_DATA: list[dict] = ["]
    for item in QUESTIONS_DATA:
        chunks.append("    {")
        chunks.append(f'        "prompt": {_format_str(item["prompt"])},')
        chunks.append(f'        "explanation": {_format_str(item["explanation"])},')
        chunks.append(_format_options(item["options"]))
        refs = item.get("references") or []
        if refs:
            chunks.append('        "references": [')
            for ref in refs:
                url = _format_str(ref["url"])
                label = _format_str(ref["label"])
                chunks.append(f'            {{"url": {url}, "label": {label}}},')
            chunks.append("        ],")
        chunks.append("    },")
    chunks.append("]")

    new_block = "\n".join(chunks) + "\n"
    SEED.write_text(source[:start] + new_block + source[end:], encoding="utf-8")
    print(f"Updated {len(FIXES)} questions in {SEED}")


if __name__ == "__main__":
    main()
