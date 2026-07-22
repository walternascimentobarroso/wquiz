#!/usr/bin/env python3
"""Rebuild php_seed_data.py: English copy + structural fixes for broken items."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = Path(__file__).resolve().parent / "_questions_raw.json"
OUT = ROOT / "app" / "services" / "php_seed_data.py"

# 1-based question number -> full replacement dict
STRUCTURAL_FIXES: dict[int, dict] = {
    1: {
        "prompt": (
            "[Q1] An HTML form contains this form element:\n\n"
            '<input type="file" name="myFile">\n\n'
            "When this form is submitted, the following PHP code gets run:\n\n"
            "move_uploaded_file(\n"
            "    $_FILES['myFile']['tmp_name'],\n"
            "    'uploads/' . $_FILES['myFile']['name']\n"
            ");\n\n"
            "Which of the following actions would improve the security of this code snippet?"
        ),
        "options": [
            (
                "Check the charset encoding of the HTTP request to see whether it matches the "
                "encoding of the uploaded file.",
                False,
            ),
            (
                "Use $HTTP_POST_FILES instead of $_FILES to maintain upwards compatibility.",
                False,
            ),
            (
                "Check with is_uploaded_file() whether the uploaded file "
                "$_FILES['myFile']['tmp_name'] is valid.",
                False,
            ),
            (
                "Sanitize the file name in $_FILES['myFile']['name'] because this value "
                "could be forged.",
                True,
            ),
        ],
    },
    11: {
        "prompt": (
            "[Q11] Table data (table name \"users\" with primary key \"id\"):\n\n"
            "id   name    email\n"
            "-----------------------------------\n"
            "1    anna    alpha@example.com\n"
            "2    betty   beta@example.org\n"
            "3    clara   gamma@example.net\n"
            "5    siggi   sigma@example.info\n\n"
            "PHP code (assume the PDO connection is correctly established):\n\n"
            "$dsn = 'mysql:host=localhost;dbname=exam';\n"
            "$user = 'username';\n"
            "$pass = '********';\n"
            "$pdo = new PDO($dsn, $user, $pass);\n"
            '$cmd = "SELECT name, email FROM users LIMIT 1";\n'
            "$stmt = $pdo->prepare($cmd);\n"
            "$stmt->execute();\n"
            "$result = $stmt->fetchAll(PDO::FETCH_BOTH);\n"
            "$row = $result[0];\n\n"
            "What is the value of $row?"
        ),
        "options": [
            (
                "array(0 => 'anna', 'name' => 'anna', 1 => "
                "'alpha@example.com', 'email' => 'alpha@example.com')",
                True,
            ),
            ("array('name' => 'anna', 'email' => 'alpha@example.com')", False),
            ("array(0 => 'anna', 1 => 'alpha@example.com')", False),
            ("array('anna' => 'alpha@example.com')", False),
        ],
    },
    15: {
        "prompt": (
            "[Q15] How can the id attribute of the second paragraph element from the XML "
            "string below be retrieved from the SimpleXML object found inside $xml?\n\n"
            '<?xml version="1.0"?>\n'
            "<document>\n"
            "    <section>\n"
            '        <paragraph id="1">One</paragraph>\n'
            '        <paragraph id="2">Two</paragraph>\n'
            "    </section>\n"
            "</document>"
        ),
        "options": [
            ("$xml->foo->section->paragraph[1]['id']", False),
            ("$xml->document->paragraph[2]['id']", False),
            ("$xml->getElementById('2');", False),
            ("$xml->document->section->paragraph[2]['id']", False),
            ("$xml->section->paragraph[1]['id']", True),
        ],
    },
    19: {
        "prompt": (
            "[Q19] Which of the following expressions will evaluate to a random value "
            "from an array below?\n\n"
            '$array = ["Sue","Mary","John","Anna"];'
        ),
        "options": [
            ("$array[array_rand($array)];", True),
            ("array_values($array, ARRAY_RANDOM);", False),
            ("shuffle($array);", False),
            ("array_rand($array);", False),
            ("array_rand($array, 1);", False),
        ],
    },
    21: {
        "prompt": (
            "[Q21] What is the result of the following bitwise operation in PHP?\n\n"
            "1 ^ 2"
        ),
        "options": [
            ("-1", False),
            ("3", True),
            ("4", False),
            ("2", False),
            ("1", False),
        ],
    },
    25: {
        "prompt": (
            "[Q25] Which of these code snippets DO NOT write the exact content of the file "
            "source.txt to target.txt? (Choose 3)"
        ),
        "options": [
            (
                '$handle = fopen("target.txt", "w+");\n'
                'fwrite($handle, file_get_contents("source.txt"));\n'
                "fclose($handle);",
                False,
            ),
            (
                'file_put_contents("target.txt", join(file("source.txt"), "\\n"));',
                True,
            ),
            (
                'file_put_contents("target.txt", fopen("source.txt", "r"));',
                True,
            ),
            (
                'file_put_contents("target.txt", readfile("source.txt"));',
                True,
            ),
            (
                'file_put_contents("target.txt", file_get_contents("source.txt"));',
                False,
            ),
        ],
    },
    33: {
        "prompt": (
            "[Q33] Which of these PHP values may NOT be encoded to a JavaScript literal "
            "using PHP's ext/json capabilities?"
        ),
        "options": [
            ("'Hello, world!'", False),
            ("['Hello, world!']", False),
            ('function(){ alert("Hello, world!"); }', True),
            ("['message' => 'Hello, world!']", False),
        ],
    },
    35: {
        "prompt": (
            "[Q35] What will the following code print out?\n\n"
            "$str = '✓ one of the following';\n"
            "echo str_replace('✓', 'Check', $str);"
        ),
        "options": [
            ("Check one of the following", True),
            ("✓ one of the following", False),
            ("one of the following", False),
        ],
    },
    39: {
        "prompt": (
            "[Q39] Consider the following code:\n\n"
            "$xml = simplexml_load_string("
            "'<?xml version=\"1.0\"?><root><language>PHP</language></root>');\n"
            "$lang = $xml->xpath('//language');\n\n"
            'Which of the following commands will output "PHP"?'
        ),
        "options": [
            ("echo $lang[0];", True),
            ("echo $lang;", False),
            ("echo strval($lang);", False),
            ("echo $lang->toString();", False),
        ],
    },
    44: {
        "prompt": (
            "[Q44] What is the output of the following code?\n\n"
            "$a = ['apples', 'bananas', 'clementines'];\n"
            "unset($a[1]);\n"
            "print_r($a);"
        ),
        "options": [
            (
                "Array\n(\n    [1] => apples\n    [2] => clementines\n)",
                False,
            ),
            (
                "Array\n(\n    [0] => apples\n    [2] => clementines\n)",
                True,
            ),
            (
                "Array\n(\n    [0] => apples\n    [1] =>\n    [2] => clementines\n)",
                False,
            ),
            (
                "Array\n(\n    [0] => apples\n    [1] => clementines\n)",
                False,
            ),
        ],
    },
    45: {
        "prompt": (
            "[Q45] Consider the following table data and PHP code. What is the outcome?\n\n"
            "Table data (table name \"users\" with primary key \"id\"):\n\n"
            "id  name   email\n"
            "1   anna   alpha@example.com\n"
            "2   betty  beta@example.org\n"
            "3   clara  gamma@example.net\n"
            "5   sue    sigma@example.info\n\n"
            "PHP code (assume the PDO connection is correctly established):\n\n"
            "$dsn  = 'mysql:host=localhost;dbname=exam';\n"
            "$user = 'username';\n"
            "$pass = '********';\n"
            "$pdo  = new PDO($dsn, $user, $pass);\n"
            "try {\n"
            '    $cmd  = "INSERT INTO users (id, name, email) VALUES\n'
            "(:id, :name, :email)\";\n"
            "    $stmt = $pdo->prepare($cmd);\n"
            "    $stmt->bindValue(':id', 1);\n"
            "    $stmt->bindValue(':name', 'anna');\n"
            "    $stmt->bindValue(':email', 'alpha@example.com');\n"
            "    $stmt->execute();\n"
            '    echo "Success!";\n'
            "} catch (PDOException $e) {\n"
            '    echo "Failure!";\n'
            "    throw $e;\n"
            "}"
        ),
        "options": [
            (
                'The INSERT will fail because of a primary key violation, and the user will '
                'see the "Success!" message.',
                True,
            ),
            (
                'The INSERT will succeed and the user will see the "Success!" message.',
                False,
            ),
            (
                "The INSERT will fail because of a primary key violation, and the user "
                "will see a PDO warning message.",
                False,
            ),
            (
                'The INSERT will fail because of a primary key violation, and the user '
                'will see the "Failure!" message.',
                False,
            ),
        ],
    },
    47: {
        "prompt": (
            "[Q47] The following form is loaded in a recent browser. The user selects "
            "the second option and submits the form:\n\n"
            '<form method="post">\n'
            '  <select name="list">\n'
            "    <option>one</option>\n"
            "    <option>two</option>\n"
            "    <option>three</option>\n"
            "  </select>\n"
            "</form>\n\n"
            "In the server-side PHP code that handles the form data, what is the value of "
            "$_POST['list']?"
        ),
        "options": [
            ("2", False),
            ("1", False),
            ("null", False),
            ("two", True),
        ],
    },
    50: {
        # Verified with PHP 8.3: output is "Base B B A B"
        "options": [
            ("Base B B A B", True),
            ("Base A Base A B", False),
            ("B B B B B", False),
            ("Base B A A B", False),
        ],
    },
    52: {
        "prompt": (
            "[Q52] Which key of $_FILES['field'] contains the provisional name/path of "
            "the uploaded file on the server?"
        ),
        "options": [
            ("name", False),
            ("tmp_name", True),
            ("tmp", False),
            ("file", False),
            ("path", False),
        ],
    },
    55: {
        "prompt": (
            "[Q55] Which of these statements about PHP is false? (Choose 2)"
        ),
        "options": [
            ("A class with a final function may be extended.", False),
            ("A final class may be instantiated.", False),
            ("A final class can be extended.", True),
            ("A class may extend more than one parent class.", True),
        ],
    },
    58: {
        "prompt": (
            "[Q58] What will the following function call print?\n\n"
            "printf('%010.6f', 22);"
        ),
        "options": [
            ("22", False),
            ("22.000000", False),
            ("022.000000", True),
            ("22.00", False),
        ],
    },
}

EXPLANATIONS_EN: dict[int, str] = {
    1: (
        "$_FILES['myFile']['name'] comes from the client and can be forged "
        "(path traversal, unexpected extensions, colliding names). Always sanitize or "
        "replace that name before building the destination path.\n"
        "(a) Checking charset is not a relevant upload-security control here.\n"
        "(b) $HTTP_POST_FILES is legacy; $_FILES is the correct superglobal.\n"
        "(c) move_uploaded_file() already validates that the source is an uploaded file; "
        "is_uploaded_file() alone does not replace name sanitization.\n"
        "Correct answer: (d)."
    ),
    2: (
        "In PHP 8.1+, enum cases are accessed with the scope resolution operator (::).\n"
        "Category::Info is the correct way to pass that enum case.\n"
        "(a) Category['Info'] is invalid — enums are not arrays.\n"
        "(b) Category.Info is JavaScript-style, not PHP.\n"
        "(d) Category->Info uses object property access, not enum case access.\n"
        "Correct answer: Category::Info."
    ),
    3: (
        "file_get_contents() (with an HTTP stream context) can send POST requests "
        "using PHP's built-in wrappers — no extension required.\n"
        "curl_exec() needs the cURL extension.\n"
        "PHP supports POST; http_build_query() only builds query strings.\n"
        "Correct answer: file_get_contents()."
    ),
    4: (
        "CSRF exploits the browser automatically sending session cookies.\n"
        "Effective defenses include:\n"
        "(a) SameSite cookie flags (Strict/Lax) to limit cross-site cookie sending.\n"
        "(b) An anti-CSRF token validated on sensitive requests.\n"
        "(c) IP validation is unreliable.\n"
        "(d) Using POST alone does not prevent CSRF.\n"
        "(e) Disabling sessions is not a practical solution.\n"
        "Correct answers: (a) and (b)."
    ),
    5: (
        "Magic methods that apply here:\n"
        "(b) __get/__set/__call (and related) process access to undefined "
        "properties/methods.\n"
        "(c) __construct / __destruct handle initialization and cleanup.\n"
        "(e) __toString converts an object to a string.\n"
        "(a) Iteration requires Iterator/IteratorAggregate, not a magic method.\n"
        "(d) Stream wrappers are registered via stream_wrapper_register().\n"
        "(f) PHP does not support operator overloading via magic methods.\n"
        "Correct answers: (b), (c), and (e)."
    ),
    6: (
        "The ::class syntax returns the fully qualified class name as a string.\n"
        "Inside namespace MyNamespace, Test::class yields MyNamespace\\Test.\n"
        "Correct answer: MyNamespace\\Test."
    ),
    7: (
        "Composer is PHP's standard dependency manager for declaring and installing "
        "packages.\n"
        "Correct answer: Composer."
    ),
    8: (
        "PHP 8.4 asymmetric visibility uses public private(set) for a publicly readable, "
        "privately writable property.\n"
        "Correct answer: class User { public private(set) string $role; }"
    ),
    9: (
        "Persistent connections (PDO/mysqli with p:) are reused across requests in the "
        "same process.\n"
        "(a) Connection settings such as charset can persist.\n"
        "(d) Connection/authentication overhead is reduced.\n"
        "(b) Transactions do not resume across requests.\n"
        "(c) Persistence does not guarantee a single global connection.\n"
        "Correct answers: (a) and (d)."
    ),
    10: (
        "The phone-number samples use different separators (parentheses, space, hyphen, "
        "dot).\n"
        "A pattern like /^(\\d{3}).\\d{3}.\\d{4}$/ matches three digits, any single "
        "separator character, three digits, separator, then four digits.\n"
        "Patterns that allow arbitrary prefixes with .* are too loose.\n"
        "Correct answer: /^(\\d{3}).\\d{3}.\\d{4}$/."
    ),
    11: (
        "PDO::FETCH_BOTH returns both numeric and associative indexes for each column.\n"
        "SELECT name, email LIMIT 1 yields the first row (anna / alpha@example.com):\n"
        "0 => 'anna', 'name' => 'anna', 1 => 'alpha@example.com', "
        "'email' => 'alpha@example.com'.\n"
        "Correct answer: that FETCH_BOTH array."
    ),
    12: (
        "Casting ['a', 'b' => 'c'] to object maps keys to properties.\n"
        "'a' has implicit key 0, so property 'a' does not exist → false.\n"
        "Key 'b' becomes property b → true.\n"
        "Output: false-true."
    ),
    13: (
        "http_response_code() sets the HTTP status directly.\n"
        "header() can also set status via a status-line header "
        '(for example header("HTTP/1.1 404 Not Found")).\n'
        "header_add(), http_set_status(), and http_header_set() are not valid PHP APIs "
        "for this purpose.\n"
        "Correct answers: http_response_code() and header()."
    ),
    14: (
        "From PHP 8.2, dynamic properties on user classes are deprecated.\n"
        "(a) `dynamic class Person {}` is invalid syntax.\n"
        "(b) stdClass allows dynamic properties.\n"
        "(c) __get/__set can store arbitrary values safely.\n"
        "(d) #[\\AllowDynamicProperties] opts into dynamic properties.\n"
        "Correct answer: (a) — it does NOT solve the requirement."
    ),
    15: (
        "simplexml_load_string() makes <document> the root ($xml).\n"
        "The second <paragraph> is index [1] under section.\n"
        "Correct access: $xml->section->paragraph[1]['id']."
    ),
    16: (
        "Arguments are passed by value by default, so increment($val) does not change "
        "the outer $val.\n"
        "Output: 1."
    ),
    17: (
        "The + operator on arrays is a key-preserving union, not concatenation.\n"
        "[1,2,3] keeps keys 0..2; only key 3 from the second array is added (value 7).\n"
        "implode yields: 1, 2, 3, 7."
    ),
    18: (
        "match(true) evaluates arms in order and returns on the first match.\n"
        "$rnd is always <= 10, so the first arm always wins.\n"
        "Output is always 'high'."
    ),
    19: (
        "array_rand($array) returns a random key; indexing with that key returns a random "
        "value.\n"
        "array_values() has no ARRAY_RANDOM flag.\n"
        "shuffle() reorders in place and returns bool.\n"
        "array_rand() alone returns a key, not a value.\n"
        "Correct answer: $array[array_rand($array)];"
    ),
    20: (
        "Throwable is the most general catchable type for both Error and Exception "
        "(PHP 7+).\n"
        "Correct answer: Throwable."
    ),
    21: (
        "^ is bitwise XOR.\n"
        "1 is 01, 2 is 10, XOR is 11 binary = 3 decimal.\n"
        "Correct answer: 3."
    ),
    22: (
        "Namespaces organize symbols and avoid name collisions; they are not an "
        "alternative to classes and do not inherently improve performance.\n"
        "Correct answer: the option describing namespace purpose as organizing code / "
        "avoiding collisions."
    ),
    23: (
        "Heredoc interpolates variables.\n"
        "$text1 becomes 'This is text'.\n"
        "$text2 interpolates $text1, so it also becomes 'This is text'.\n"
        'echo "$text1 $text2" prints: This is text This is text.'
    ),
    24: (
        "renderVal(a $a) type-hints parameter $a as class a.\n"
        "Passing null is not an instance of a, so PHP raises a TypeError.\n"
        "Correct answer: An error, because null is not an instance of a."
    ),
    25: (
        "(a) and (e) correctly copy file contents via file_get_contents().\n"
        "(b) file() keeps trailing newlines; joining with \"\\n\" adds extra newlines.\n"
        "(c) fopen() returns a resource, not the file contents string.\n"
        "(d) readfile() echoes content to output and returns an int (byte count), "
        "so target.txt gets a number — not the file contents.\n"
        "Correct answers: (b), (c), and (d)."
    ),
    26: (
        "Both values are escaped with PDO::quote(), and $age is cast to int first.\n"
        "This specific snippet is protected from classic SQL injection, though prepared "
        "statements are still preferred.\n"
        "Correct answer: No, the code is fully protected from SQL Injection."
    ),
    27: (
        "XSS protection, HTTPS + Secure cookies, session.use_only_cookies=1, and "
        "session_regenerate_id() all reduce hijacking/fixation risk.\n"
        "session.cookie_lifetime=0 only makes the cookie a browser-session cookie; "
        "it does not protect against hijacking or fixation.\n"
        "Correct answer: Set the session.cookie_lifetime php.ini parameter to 0."
    ),
    28: (
        "PHP constants created with const or define() are always case-sensitive.\n"
        "(define() used to allow case-insensitive constants via a third argument; "
        "that behavior is removed in modern PHP.)\n"
        "Correct answer: Yes, they are always case-sensitive."
    ),
    29: (
        '"22" + "0.2" uses numeric addition → 22.2.\n'
        "23 . 1 concatenates as strings → '231'.\n"
        "With comma in echo, output is 22.2,231."
    ),
    30: (
        "POST supports much larger payloads than GET and is required for file uploads.\n"
        "POST alone does not prevent CSRF and does not encrypt data (HTTPS does).\n"
        "Correct answers: higher size limits, and possibility to upload files."
    ),
    31: (
        "sscanf() parses a formatted string into variables/array values.\n"
        "fgetcsv/strtok/sprintf solve different problems.\n"
        "Correct answer: sscanf()."
    ),
    32: (
        "(a)(b)(c) all produce ['one','two','three'] with keys 0,1,2.\n"
        "(d) uses keys starting at 1, so the array value differs under PHP comparison.\n"
        "Correct answer: [1 => 'one', 2 => 'two', 3 => 'three']."
    ),
    33: (
        "json_encode() can encode strings and arrays/objects.\n"
        "A function/closure cannot be represented as a JSON literal.\n"
        "Correct answer: function(){ alert(\"Hello, world!\"); }"
    ),
    34: (
        "Since PHP 5.6, both const and define() can define array constants.\n"
        "Correct answer: With const and define()."
    ),
    35: (
        "str_replace('✓', 'Check', $str) replaces the check mark with 'Check'.\n"
        "The string '✓ one of the following' becomes 'Check one of the following'.\n"
        "Correct answer: Check one of the following."
    ),
    36: (
        "Constructor property promotion (PHP 8+) declares and initializes protected "
        "properties with minimal code.\n"
        "Correct answer: the promoted-constructor approach."
    ),
    37: (
        "preg_split('/(the)/i', ..., PREG_SPLIT_DELIM_CAPTURE) splits on 'the' "
        "(case-insensitive) and keeps the captured delimiters.\n"
        "For \"The cat sat on the roof of their house.\" the pieces are:\n"
        "['', 'The', ' cat sat on ', 'the', ' roof of ', 'the', 'ir house.']\n"
        "(note: 'their' also matches the leading 'the').\n"
        "That is 7 elements.\n"
        "Correct answer: 7."
    ),
    38: (
        "Casting an object to array exposes public properties by name.\n"
        "Private properties become keys like \"\\0Class\\0prop\".\n"
        "array_keys() therefore includes the mangled private key and the public one."
    ),
    39: (
        "xpath('//language') returns an array of nodes.\n"
        "echo $lang[0]; prints the first node string value 'PHP'.\n"
        "echoing the array / strval(array) / toString() are invalid here.\n"
        "Correct answer: echo $lang[0];"
    ),
    40: (
        "open_basedir restrictions and filesystem permissions can block opening a file.\n"
        "Being under /tmp or running as CGI does not inherently prevent file access.\n"
        "Correct answers: outside open_basedir, and filesystem permissions."
    ),
    41: (
        "With declare(strict_types=1), float 2.0 is not accepted for int $b.\n"
        "That raises TypeError, which is caught by catch (Error $err).\n"
        "Output: Error."
    ),
    42: (
        "never means the function never returns normally (always throws or exits).\n"
        "Correct answer: It indicates that a function will never return a value."
    ),
    43: (
        "The native way to convert a PHP value to JSON is json_encode($value).\n"
        "Correct answer: json_encode(...)."
    ),
    44: (
        "unset($a[1]) removes key 1 and does not reindex the array.\n"
        "Remaining keys are 0 => apples and 2 => clementines.\n"
        "Correct print_r output is the array with keys 0 and 2."
    ),
    45: (
        "The table already has id=1, so INSERT id=1 fails with a primary key violation.\n"
        "PDO defaults to ERRMODE_SILENT: execute() returns false and does not throw.\n"
        "The catch block never runs, so the script still prints \"Success!\".\n"
        "Correct answer: PK violation + \"Success!\" message."
    ),
    46: (
        "++$val inside the function still uses pass-by-value, so the outer $val stays 1.\n"
        "Output: 1."
    ),
    47: (
        "Without a value attribute, the browser submits the option's text content.\n"
        "Selecting the second option submits 'two'.\n"
        "Correct answer: two."
    ),
    48: (
        "print returns 1; echo does not return a value.\n"
        "echo can take multiple arguments; print cannot.\n"
        "Correct answers: those two differences."
    ),
    49: (
        "header_remove() removes a previously set header before headers are sent.\n"
        "Correct answer: Use the header_remove() function."
    ),
    50: (
        "Late static binding with B::test() yields:\n"
        "Base::whoareyou() → Base\n"
        "self::whoareyou() → B\n"
        "parent::whoareyou() → B\n"
        "A::whoareyou() → A\n"
        "static::whoareyou() → B\n"
        "Output: Base B B A B."
    ),
    51: (
        "5xx status codes represent server error conditions.\n"
        "Correct answer: 5xx."
    ),
    52: (
        "tmp_name is the temporary path of the uploaded file on the server.\n"
        "name is the original client filename.\n"
        "Correct answer: tmp_name."
    ),
    53: (
        "counter($start--, ++$stop) passes the current $start, then increments $stop.\n"
        "Calls with ($start=5, $stop): (5,2) → (5,3) → (5,4) → (5,5) → (5,6).\n"
        "On (5,6), $stop > $start and it returns.\n"
        "That is 5 executions.\n"
        "Correct answer: 5."
    ),
    54: (
        "Statements that are NOT true:\n"
        "Anonymous functions created in object context are not automatically bound.\n"
        "Assigning a Closure to an object property does not bind it by itself.\n"
        "Correct answers: those two false statements."
    ),
    55: (
        "False statements:\n"
        "A final class cannot be extended.\n"
        "PHP does not allow multiple inheritance of classes "
        "(a class may extend only one parent).\n"
        "Note: since PHP 8.4, properties can be final — so that is no longer a false "
        "statement.\n"
        "Correct answers: (c) and (d)."
    ),
    56: (
        "Prepared statements with bound parameters are the preferred SQL injection "
        "defense.\n"
        "Correct answer: Always using prepared statements when available."
    ),
    57: (
        "__get() provides read access to inaccessible/virtual properties.\n"
        "Correct answer: __get."
    ),
    58: (
        "%010.6f formats 22 as 22.000000 (9 chars) and left-pads with 0 to width 10.\n"
        "Result: 022.000000."
    ),
    59: (
        "With strict_types=1, oops(12) passes an int to string and raises TypeError.\n"
        "Correct answer: Fatal error: Uncaught TypeError."
    ),
    60: (
        "?string accepts null, '' and 'null' without a TypeError.\n"
        "Correct answer: All of the above."
    ),
}


def merge_question(n: int, raw: dict) -> dict:
    fix = STRUCTURAL_FIXES.get(n, {})
    prompt = fix.get("prompt", raw["prompt"])
    # keep [Qn] prefix
    if not prompt.startswith(f"[Q{n}]"):
        prompt = f"[Q{n}] {prompt}"
    options = fix.get("options")
    if options is None:
        options = [(o["text"], o["correct"]) for o in raw["options"]]
    explanation = EXPLANATIONS_EN[n]
    return {
        "prompt": prompt,
        "explanation": explanation,
        "options": options,
    }


def main() -> None:
    raw_list = json.loads(RAW.read_text(encoding="utf-8"))
    assert len(raw_list) == 60
    assert set(EXPLANATIONS_EN) == set(range(1, 61))

    items = [merge_question(i, raw_list[i - 1]) for i in range(1, 61)]

    # validations
    for i, item in enumerate(items, 1):
        corrects = sum(1 for _, ok in item["options"] if ok)
        assert corrects >= 1, i
        if "Choose 2" in item["prompt"]:
            assert corrects == 2, (i, corrects)
        if "Choose 3" in item["prompt"]:
            assert corrects == 3, (i, corrects)
        for text, _ in item["options"]:
            assert "alternativa" not in text.lower(), (i, text)
            assert text.strip(), i
        assert "alternativa" not in item["prompt"].lower(), i
        # Q35 intentionally uses a check-mark character in the sample code.
        if i != 35:
            assert "✓" not in item["prompt"], i
            assert all("✓" not in t for t, _ in item["options"]), i

    header = '''"""Seed data from Zend PHP Certified Engineer 2025 (Maycon Douglas PDF).

Questions keep a theme tag aligned with official Zend exam topics:
https://www.zend.com/training/php-certification-exam

Prompts, options, and explanations are maintained in English.
"""

from __future__ import annotations

SAMPLE_QUIZ_TITLE = "Zend PHP Certified Engineer 2025"
SAMPLE_QUIZ_DESCRIPTION = (
    "Practice quiz based on Zend PHP Certified Engineer 2025 material "
    "(Maycon Douglas). In study mode you can filter by topic or practice all."
)
SAMPLE_QUIZ_CATEGORY = "Zend PHP"

# 1-based indices into QUESTIONS_DATA, aligned with Zend exam topics.
THEME_QUIZZES: list[dict] = [
    {
        "title": "PHP Basics",
        "description": (
            "Language fundamentals: syntax, constants, namespaces, "
            "operators and basic constructs (match, print/echo)."
        ),
        "question_numbers": [18, 21, 22, 28, 48],
    },
    {
        "title": "Functions",
        "description": (
            "Functions, parameter passing, return types (never), "
            "anonymous functions and recursion."
        ),
        "question_numbers": [16, 42, 46, 53, 54],
    },
    {
        "title": "Data Format and Types",
        "description": (
            "Data types, enums, JSON, XML/SimpleXML, type juggling "
            "and nullable typing."
        ),
        "question_numbers": [2, 15, 29, 33, 39, 43, 60],
    },
    {
        "title": "Web Features",
        "description": (
            "HTTP, forms, headers, status codes, POST/GET "
            "and uploads ($_FILES)."
        ),
        "question_numbers": [3, 13, 30, 47, 49, 51, 52],
    },
    {
        "title": "Object-Oriented Programming",
        "description": (
            "Classes, magic methods, visibility, inheritance, late static "
            "binding and virtual properties."
        ),
        "question_numbers": [5, 6, 8, 14, 24, 36, 38, 50, 55, 57],
    },
    {
        "title": "Security",
        "description": (
            "CSRF, SQL injection, session hijacking/fixation and safe uploads."
        ),
        "question_numbers": [1, 4, 26, 27, 56],
    },
    {
        "title": "I/O",
        "description": "File read/write and factors that prevent opening files.",
        "question_numbers": [25, 40],
    },
    {
        "title": "Strings and Patterns",
        "description": (
            "String manipulation, heredoc, regex, sscanf and formatting (printf)."
        ),
        "question_numbers": [10, 23, 31, 35, 37, 58],
    },
    {
        "title": "Databases and SQLs",
        "description": "PDO, persistent connections and SQL queries in PHP.",
        "question_numbers": [9, 11, 45],
    },
    {
        "title": "Arrays",
        "description": (
            "Array operators, unset, array constants and random selection."
        ),
        "question_numbers": [12, 17, 19, 32, 34, 44],
    },
    {
        "title": "Error Handling",
        "description": "Throwable, TypeError, strict_types and error handling.",
        "question_numbers": [20, 41, 59],
    },
    {
        "title": "Other PHP Concepts",
        "description": "Additional exam concepts (e.g. Composer).",
        "question_numbers": [7],
    },
]


def _theme_by_question_number() -> dict[int, str]:
    mapping: dict[int, str] = {}
    for theme in THEME_QUIZZES:
        for number in theme["question_numbers"]:
            mapping[number] = theme["title"]
    return mapping


def seeded_questions() -> list[dict]:
    """Questions with theme field for the single Zend PHP quiz."""
    theme_map = _theme_by_question_number()
    items: list[dict] = []
    for index, item in enumerate(QUESTIONS_DATA, start=1):
        items.append({**item, "theme": theme_map[index]})
    return items


QUESTIONS_DATA: list[dict] = [
'''

    lines = [header]
    for item in items:
        lines.append("    {")
        lines.append(f"        \"prompt\": {item['prompt']!r},")
        lines.append(f"        \"explanation\": {item['explanation']!r},")
        lines.append("        \"options\": [")
        for text, ok in item["options"]:
            lines.append(f"            ({text!r}, {ok}),")
        lines.append("        ],")
        lines.append("    },")
    lines.append("]")
    lines.append("")
    lines.append(
        "_assigned = [n for theme in THEME_QUIZZES for n in theme[\"question_numbers\"]]"
    )
    lines.append(
        "if sorted(_assigned) != list(range(1, len(QUESTIONS_DATA) + 1)):"
    )
    lines.append(
        "    missing = set(range(1, len(QUESTIONS_DATA) + 1)) - set(_assigned)"
    )
    lines.append(
        "    dupes = [n for n in _assigned if _assigned.count(n) > 1]"
    )
    lines.append(
        "    raise RuntimeError("
    )
    lines.append(
        '        f"Theme assignment incomplete: missing={sorted(missing)} '
        'dupes={sorted(set(dupes))}"'
    )
    lines.append("    )")
    lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT} with {len(items)} English questions")


if __name__ == "__main__":
    main()
