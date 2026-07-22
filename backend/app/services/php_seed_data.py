"""Seed data from Zend PHP Certified Engineer 2025 (Maycon Douglas PDF).

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
    {
        "prompt": '[Q1] An HTML form contains this form element:\n\n```html\n<input type="file" name="myFile">\n```\n\nWhen this form is submitted, the following PHP code gets run:\n\n```php\nmove_uploaded_file(\n    $_FILES[\'myFile\'][\'tmp_name\'],\n    \'uploads/\' . $_FILES[\'myFile\'][\'name\']\n);\n```\n\nWhich of the following actions would improve the security of this code snippet?',
        "explanation": "$_FILES['myFile']['name'] comes from the client and can be forged (path traversal, unexpected extensions, colliding names). Always sanitize or replace that name before building the destination path.\n(a) Checking charset is not a relevant upload-security control here.\n(b) $HTTP_POST_FILES is legacy; $_FILES is the correct superglobal.\n(c) move_uploaded_file() already validates that the source is an uploaded file; is_uploaded_file() alone does not replace name sanitization.\nCorrect answer: (d).",
        "options": [
            ('Check the charset encoding of the HTTP request to see whether it matches the encoding of the uploaded file.', False),
            ('Use $HTTP_POST_FILES instead of $_FILES to maintain upwards compatibility.', False),
            ("Check with is_uploaded_file() whether the uploaded file $_FILES['myFile']['tmp_name'] is valid.", False),
            ("Sanitize the file name in $_FILES['myFile']['name'] because this value could be forged.", True),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/features.file-upload.php', "label": 'Handling file uploads'},
            {"url": 'https://www.php.net/manual/en/function.move-uploaded-file.php', "label": 'move_uploaded_file'},
        ],
    },
    {
        "prompt": '[Q2] Given the following code:\nWhich expression may be used instead of the *** placeholder to log an "Info" message?\n\n```php\nnamespace PHP;\nenum Category {\n    case Info;\n    case Warning;\n    case Error;\n};\nfunction log(string $message, Category $category) {\n    echo "$message {$category->name}";\n}\nlog("My message", ***);\n```',
        "explanation": "In PHP 8.1+, enum cases are accessed with the scope resolution operator (::).\nCategory::Info is the correct way to pass that enum case.\n(a) Category['Info'] is invalid — enums are not arrays.\n(b) Category.Info is JavaScript-style, not PHP.\n(d) Category->Info uses object property access, not enum case access.\nCorrect answer: Category::Info.",
        "options": [
            ("Category['Info']", False),
            ('Category.Info', False),
            ('Category::Info', True),
            ('Category->Info', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/language.enumerations.php', "label": 'Enumerations'},
            {"url": 'https://www.php.net/manual/en/language.enumerations.basics.php', "label": 'Enum basics'},
        ],
    },
    {
        "prompt": '[Q3] How can you create an HTTP POST request in PHP without having to install or activate a\nPHP extension?',
        "explanation": "file_get_contents() (with an HTTP stream context) can send POST requests using PHP's built-in wrappers — no extension required.\ncurl_exec() needs the cURL extension.\nPHP supports POST; http_build_query() only builds query strings.\nCorrect answer: file_get_contents().",
        "options": [
            ('file_get_contents()', True),
            ('curl_exec()', False),
            ('PHP only supports GET requests', False),
            ('http_build_query()', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/function.file-get-contents.php', "label": 'file_get_contents'},
            {"url": 'https://www.php.net/manual/en/context.http.php', "label": 'HTTP context options'},
        ],
    },
    {
        "prompt": '[Q4] Which of these approaches is recommended to protect a web site against Cross-Site\nRequest Forgery (CSRF)? (Choose 2)',
        "explanation": 'CSRF exploits the browser automatically sending session cookies.\nEffective defenses include:\n(a) SameSite cookie flags (Strict/Lax) to limit cross-site cookie sending.\n(b) An anti-CSRF token validated on sensitive requests.\n(c) IP validation is unreliable.\n(d) Using POST alone does not prevent CSRF.\n(e) Disabling sessions is not a practical solution.\nCorrect answers: (a) and (b).',
        "options": [
            ('Use the SameSite flag for cookies.', True),
            ('Add an additional token to the HTTP request.', True),
            ('Validate the IP address of the user.', False),
            ('Use POST instead of GET.', False),
            ('Disable sessions.', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/session.security.php', "label": 'Sessions and security'},
            {"url": 'https://www.php.net/manual/en/session.configuration.php#ini.session.cookie-samesite', "label": 'session.cookie_samesite'},
        ],
    },
    {
        "prompt": '[Q5] Which of the following tasks can be achieved by using magic methods? (Choose 3)',
        "explanation": 'Magic methods that apply here:\n(b) __get/__set/__call (and related) process access to undefined properties/methods.\n(c) __construct / __destruct handle initialization and cleanup.\n(e) __toString converts an object to a string.\n(a) Iteration requires Iterator/IteratorAggregate, not a magic method.\n(d) Stream wrappers are registered via stream_wrapper_register().\n(f) PHP does not support operator overloading via magic methods.\nCorrect answers: (b), (c), and (e).',
        "options": [
            ('Creating an iterable object.', False),
            ('Processing access to undefined methods or properties.', True),
            ('Initializing or uninitializing object data.', True),
            ('Creating a new stream wrapper.', False),
            ('Converting objects to string representation.', True),
            ('Overloading operators like +, *, etc.', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/language.oop5.magic.php', "label": 'Magic methods'},
        ],
    },
    {
        "prompt": '[Q6] What is the output of the following code?\n\n```php\nnamespace MyNamespace;\nclass Test {\n}\necho Test::class;\n```',
        "explanation": 'The ::class syntax returns the fully qualified class name as a string.\nInside namespace MyNamespace, Test::class yields MyNamespace\\Test.\nCorrect answer: MyNamespace\\Test.',
        "options": [
            ('parse error', False),
            ('empty string', False),
            ('MyNamespace\\Test', True),
            ('Test', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/language.oop5.basic.php#language.oop5.basic.class.class', "label": '::class'},
            {"url": 'https://www.php.net/manual/en/language.namespaces.basics.php', "label": 'Namespaces'},
        ],
    },
    {
        "prompt": '[Q7] Which of the following is a package manager that allows adding dependencies to a PHP\nproject?',
        "explanation": "Composer is PHP's standard dependency manager for declaring and installing packages.\nCorrect answer: Composer.",
        "options": [
            ('PHAR', False),
            ('Composer', True),
            ('Maven', False),
            ('TAR', False),
        ],
        "references": [
            {"url": 'https://getcomposer.org/doc/', "label": 'Composer documentation'},
        ],
    },
    {
        "prompt": '[Q8] Your User class has a $role property. All code working with an instance of that class shall be able to retrieve the property’s value, but only the class itself must be allowed to change it. Which snippet is correct in PHP 8.4 asymmetric visibility?',
        "explanation": 'PHP 8.4 asymmetric visibility uses public private(set) for a publicly readable, privately writable property.\nCorrect answer: class User { public private(set) string $role; }',
        "options": [
            ('class User { public private(set) string $role; }', True),
            ('class User { private public(get) string $role; }', False),
            ('class User { public private string $role; }', False),
            ('class User { public(get) private(set) string $role; }', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/language.oop5.visibility.php#language.oop5.visibility-asymmetric', "label": 'Asymmetric property visibility'},
        ],
    },
    {
        "prompt": '[Q9] What is the benefit of using persistent database connections in PHP? (Choose 2)',
        "explanation": 'Persistent connections (PDO/mysqli with p:) are reused across requests in the same process.\n(a) Connection settings such as charset can persist.\n(d) Connection/authentication overhead is reduced.\n(b) Transactions do not resume across requests.\n(c) Persistence does not guarantee a single global connection.\nCorrect answers: (a) and (d).',
        "options": [
            ('Allows connection settings such as character set encoding to be remembered after a\nPHP script ends.', True),
            ('Allows for resumption of transactions across multiple requests.', False),
            ('Ensures that only a single connection is open to the database from PHP.', False),
            ('Reduces the connection & authentication overhead of connecting to the database.', True),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/pdo.connections.php', "label": 'PDO connections'},
            {"url": 'https://www.php.net/manual/en/features.persistent-connections.php', "label": 'Persistent connections'},
        ],
    },
    {
        "prompt": '[Q10] Which regular expression will match each of these strings?',
        "explanation": 'The phone-number samples use different separators (parentheses, space, hyphen, dot).\nA pattern like /^(\\d{3}).\\d{3}.\\d{4}$/ matches three digits, any single separator character, three digits, separator, then four digits.\nPatterns that allow arbitrary prefixes with .* are too loose.\nCorrect answer: /^(\\d{3}).\\d{3}.\\d{4}$/.',
        "options": [
            ('/^.*\\d{3}.\\d{3}.\\d{4}$/', False),
            ('/^(\\d{3}).\\d{3}.\\d{4}$/', False),
            ('/^.*(\\d{3}.\\d{3}.\\d{4})$/', False),
            ('/^(\\d{3}).\\d{3}.\\d{4}$/\n(000) 555-1234\n000 555 1234\n000-555-1234\n000.555.1234', True),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/reference.pcre.pattern.syntax.php', "label": 'PCRE pattern syntax'},
            {"url": 'https://www.php.net/manual/en/function.preg-match.php', "label": 'preg_match'},
        ],
    },
    {
        "prompt": '[Q11] Table data (table name "users" with primary key "id"):\n\n```text\nid   name    email\n-----------------------------------\n1    anna    alpha@example.com\n2    betty   beta@example.org\n3    clara   gamma@example.net\n5    siggi   sigma@example.info\n```\n\nPHP code (assume the PDO connection is correctly established):\n\n```php\n$dsn = \'mysql:host=localhost;dbname=exam\';\n$user = \'username\';\n$pass = \'********\';\n$pdo = new PDO($dsn, $user, $pass);\n$cmd = "SELECT name, email FROM users LIMIT 1";\n$stmt = $pdo->prepare($cmd);\n$stmt->execute();\n$result = $stmt->fetchAll(PDO::FETCH_BOTH);\n$row = $result[0];\n```\n\nWhat is the value of $row?',
        "explanation": "PDO::FETCH_BOTH returns both numeric and associative indexes for each column.\nSELECT name, email LIMIT 1 yields the first row (anna / alpha@example.com):\n0 => 'anna', 'name' => 'anna', 1 => 'alpha@example.com', 'email' => 'alpha@example.com'.\nCorrect answer: that FETCH_BOTH array.",
        "options": [
            ("array(0 => 'anna', 'name' => 'anna', 1 => 'alpha@example.com', 'email' => 'alpha@example.com')", True),
            ("array('name' => 'anna', 'email' => 'alpha@example.com')", False),
            ("array(0 => 'anna', 1 => 'alpha@example.com')", False),
            ("array('anna' => 'alpha@example.com')", False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/pdostatement.fetchall.php', "label": 'PDOStatement::fetchAll'},
            {"url": 'https://www.php.net/manual/en/pdo.constants.php#pdo.constants.fetch-both', "label": 'PDO::FETCH_BOTH'},
        ],
    },
    {
        "prompt": "[Q12] What is the output of the following code?\n\n```php\n$a = ['a', 'b' => 'c'];\necho property_exists((object) $a, 'a') ? 'true' : 'false';\necho '-';\necho property_exists((object) $a, 'b') ? 'true' : 'false';\n```",
        "explanation": "Casting ['a', 'b' => 'c'] to object maps keys to properties.\n'a' has implicit key 0, so property 'a' does not exist → false.\nKey 'b' becomes property b → true.\nOutput: false-true.",
        "options": [
            ('false-false', False),
            ('true-false', False),
            ('true-true', False),
            ('false-true', True),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/language.types.object.php#language.types.object.casting', "label": 'Converting to object'},
        ],
    },
    {
        "prompt": '[Q13] Which of the following PHP functions can be used to set the HTTP response code?\n(Choose 2)',
        "explanation": 'http_response_code() sets the HTTP status directly.\nheader() can also set status via a status-line header (for example header("HTTP/1.1 404 Not Found")).\nheader_add(), http_set_status(), and http_header_set() are not valid PHP APIs for this purpose.\nCorrect answers: http_response_code() and header().',
        "options": [
            ('http_response_code()', True),
            ('header_add()', False),
            ('http_set_status()', False),
            ('http_header_set()', False),
            ('header()', True),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/function.http-response-code.php', "label": 'http_response_code'},
            {"url": 'https://www.php.net/manual/en/function.header.php', "label": 'header'},
        ],
    },
    {
        "prompt": '[Q14] You want to work with a class where you can set arbitrary properties. You end up with the following code:\n\n```php\nclass Person {\n}\n$person = new Person();\n$person->firstName = "Jane";\n$person->lastName = "Doe";\n```\n\nWhen running this code, you notice that you get a deprecation notice on some systems, and you are anticipating that this code might not work at all in a future PHP version.\n\nWhich of these approaches does NOT allow you to fulfill your requirements while getting rid of the deprecation messages?',
        "explanation": 'From PHP 8.2, dynamic properties on user classes are deprecated.\n(a) `dynamic class Person {}` is invalid syntax.\n(b) stdClass allows dynamic properties.\n(c) __get/__set can store arbitrary values safely.\n(d) #[\\AllowDynamicProperties] opts into dynamic properties.\nCorrect answer: (a) — it does NOT solve the requirement.',
        "options": [
            ('Replace the class with:\n\ndynamic class Person {\n}', True),
            ('Replace the class with stdClass:\n\n$person = new stdClass();\n$person->firstName = "Jane";\n$person->lastName = "Doe";', False),
            ('Replace the class with magic methods:\n\nclass Person {\n    protected $properties = [];\n    public function __get($key) {\n        return $this->properties[$key] ?? null;\n    }\n    public function __set($key, $value) {\n        $this->properties[$key] = $value;\n    }\n}', False),
            ('Allow dynamic properties explicitly:\n\n#[\\AllowDynamicProperties]\nclass Person {\n}', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/language.oop5.properties.php#language.oop5.properties.dynamic-properties', "label": 'Dynamic properties'},
            {"url": 'https://www.php.net/manual/en/class.allowdynamicproperties.php', "label": 'AllowDynamicProperties'},
        ],
    },
    {
        "prompt": '[Q15] How can the id attribute of the second paragraph element from the XML string below be retrieved from the SimpleXML object found inside $xml?\n\n```xml\n<?xml version="1.0"?>\n<document>\n    <section>\n        <paragraph id="1">One</paragraph>\n        <paragraph id="2">Two</paragraph>\n    </section>\n</document>\n```',
        "explanation": "simplexml_load_string() makes <document> the root ($xml).\nThe second <paragraph> is index [1] under section.\nCorrect access: $xml->section->paragraph[1]['id'].",
        "options": [
            ("$xml->foo->section->paragraph[1]['id']", False),
            ("$xml->document->paragraph[2]['id']", False),
            ("$xml->getElementById('2');", False),
            ("$xml->document->section->paragraph[2]['id']", False),
            ("$xml->section->paragraph[1]['id']", True),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/simplexml.examples-basic.php', "label": 'SimpleXML basic usage'},
            {"url": 'https://www.php.net/manual/en/function.simplexml-load-string.php', "label": 'simplexml_load_string'},
        ],
    },
    {
        "prompt": '[Q16] What is the output of the following code?\n\n```php\nfunction increment ($val) {\n    $val = $val + 1;\n}\n$val = 1;\nincrement($val);\necho $val;\n```',
        "explanation": 'Arguments are passed by value by default, so increment($val) does not change the outer $val.\nOutput: 1.',
        "options": [
            ('1', True),
            ('2', False),
            ('parse error', False),
            ('null', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/functions.arguments.php#functions.arguments.passing', "label": 'Passing arguments by value'},
        ],
    },
    {
        "prompt": "[Q17] What is the output of the following code?\n\n```php\n$a = [1, 2, 3] + [4, 5, 6, 7];\necho implode(', ', $a);\n```",
        "explanation": 'The + operator on arrays is a key-preserving union, not concatenation.\n[1,2,3] keeps keys 0..2; only key 3 from the second array is added (value 7).\nimplode yields: 1, 2, 3, 7.',
        "options": [
            ('1, 2, 3, 4, 5, 6, 7', False),
            ('1, 2, 3, 7', True),
            ('4, 5, 6, 7', False),
            ('5, 7, 9, 7', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/language.operators.array.php', "label": 'Array operators'},
            {"url": 'https://www.php.net/manual/en/function.implode.php', "label": 'implode'},
        ],
    },
    {
        "prompt": "[Q18] What is the output of the following code?\n\n```php\n$rnd = rand(1, 10);\n$category = match (true) {\n    $rnd <= 10 => 'high',\n    $rnd <= 6  => 'mid',\n    $rnd < 3   => 'low'\n};\necho $category;\n```",
        "explanation": "match(true) evaluates arms in order and returns on the first match.\n$rnd is always <= 10, so the first arm always wins.\nOutput is always 'high'.",
        "options": [
            ("Always 'high'", True),
            ("Always 'low'", False),
            ('Fatal error', False),
            ("Either 'high' or 'mid' or 'low', determined at random", False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/control-structures.match.php', "label": 'match'},
        ],
    },
    {
        "prompt": '[Q19] Which of the following expressions will evaluate to a random value from an array below?\n\n```php\n$array = ["Sue","Mary","John","Anna"];\n```',
        "explanation": 'array_rand($array) returns a random key; indexing with that key returns a random value.\narray_values() has no ARRAY_RANDOM flag.\nshuffle() reorders in place and returns bool.\narray_rand() alone returns a key, not a value.\nCorrect answer: $array[array_rand($array)];',
        "options": [
            ('$array[array_rand($array)];', True),
            ('array_values($array, ARRAY_RANDOM);', False),
            ('shuffle($array);', False),
            ('array_rand($array);', False),
            ('array_rand($array, 1);', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/function.array-rand.php', "label": 'array_rand'},
        ],
    },
    {
        "prompt": '[Q20] What is the most general PHP type to use in a catch block in order to catch all errors and\nexceptions?',
        "explanation": 'Throwable is the most general catchable type for both Error and Exception (PHP 7+).\nCorrect answer: Throwable.',
        "options": [
            ('Exception', False),
            ('Error', False),
            ('Throwable', True),
            ('ErrorException', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/class.throwable.php', "label": 'Throwable'},
            {"url": 'https://www.php.net/manual/en/language.exceptions.php', "label": 'Exceptions'},
        ],
    },
    {
        "prompt": '[Q21] What is the result of the following bitwise operation in PHP?\n\n1 ^ 2',
        "explanation": '^ is bitwise XOR.\n1 is 01, 2 is 10, XOR is 11 binary = 3 decimal.\nCorrect answer: 3.',
        "options": [
            ('-1', False),
            ('3', True),
            ('4', False),
            ('2', False),
            ('1', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/language.operators.bitwise.php', "label": 'Bitwise operators'},
        ],
    },
    {
        "prompt": '[Q22] What purpose do namespaces fulfill?',
        "explanation": 'Namespaces organize symbols and avoid name collisions; they are not an alternative to classes and do not inherently improve performance.\nCorrect answer: the option describing namespace purpose as organizing code / avoiding collisions.',
        "options": [
            ('Alternative to classes.', False),
            ('Improved performance.', False),
            ('Encapsulation.', True),
            ('All of the above.', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/language.namespaces.rationale.php', "label": 'Namespaces rationale'},
        ],
    },
    {
        "prompt": '[Q23] What is the output of the following code?\n\n```php\n$text = \'This is text\';\n$text1 = <<<TEXT\n$text\nTEXT;\n$text2 = <<<TEXT\n$text1\nTEXT;\necho "$text2";\n```',
        "explanation": 'Heredoc interpolates variables.\n$text1 becomes \'This is text\'.\n$text2 interpolates $text1, so it also becomes \'This is text\'.\necho "$text1 $text2" prints: This is text This is text.',
        "options": [
            ('$text2', False),
            ('$text1', False),
            ('$text', False),
            ('This is text', True),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/language.types.string.php#language.types.string.syntax.heredoc', "label": 'Heredoc syntax'},
        ],
    },
    {
        "prompt": '[Q24] What is the output of the following code?\n\n```php\nclass a\n{\n    public $val;\n}\nfunction renderVal (a $a)\n{\n    if ($a) {\n        echo $a->val;\n    }\n}\nrenderVal(null);\n```',
        "explanation": 'renderVal(a $a) type-hints parameter $a as class a.\nPassing null is not an instance of a, so PHP raises a TypeError.\nCorrect answer: An error, because null is not an instance of a.',
        "options": [
            ('An error, because null is not an instance of a.', True),
            ('A syntax error in the function declaration line.', False),
            ('Nothing, because a null value is being passed to renderVal().', False),
            ('NULL', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/language.types.declarations.php', "label": 'Type declarations'},
            {"url": 'https://www.php.net/manual/en/class.typeerror.php', "label": 'TypeError'},
        ],
    },
    {
        "prompt": '[Q25] Which of these code snippets DO NOT write the exact content of the file source.txt to target.txt? (Choose 3)',
        "explanation": '(a) and (e) correctly copy file contents via file_get_contents().\n(b) file() keeps trailing newlines; joining with "\\n" adds extra newlines.\n(c) fopen() returns a resource, not the file contents string.\n(d) readfile() echoes content to output and returns an int (byte count), so target.txt gets a number — not the file contents.\nCorrect answers: (b), (c), and (d).',
        "options": [
            ('$handle = fopen("target.txt", "w+");\nfwrite($handle, file_get_contents("source.txt"));\nfclose($handle);', False),
            ('file_put_contents("target.txt", join(file("source.txt"), "\\n"));', True),
            ('file_put_contents("target.txt", fopen("source.txt", "r"));', True),
            ('file_put_contents("target.txt", readfile("source.txt"));', True),
            ('file_put_contents("target.txt", file_get_contents("source.txt"));', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/function.file-get-contents.php', "label": 'file_get_contents'},
            {"url": 'https://www.php.net/manual/en/function.file-put-contents.php', "label": 'file_put_contents'},
            {"url": 'https://www.php.net/manual/en/function.readfile.php', "label": 'readfile'},
        ],
    },
    {
        "prompt": '[Q26] Is the following code vulnerable to SQL Injection?\n\n```php\n// assume $pdo is a valid PDO connection\n$age  = $pdo->quote((int) $age);\n$name = $pdo->quote($name);\n$query = "SELECT * FROM users WHERE name LIKE\n\'$name\' AND age = $age";\n$result = $pdo->query($query);\n```',
        "explanation": 'Both values are escaped with PDO::quote(), and $age is cast to int first.\nThis specific snippet is protected from classic SQL injection, though prepared statements are still preferred.\nCorrect answer: No, the code is fully protected from SQL Injection.',
        "options": [
            ('Yes, because the $name variable is improperly escaped.', False),
            ('Yes, because even though $age and $name are escaped, nothing prevents their\ncontents from modifying the SQL.', False),
            ('Yes, because the $age variable is improperly escaped.', False),
            ('No, the code is fully protected from SQL Injection.', True),
            ('Yes, because you cannot prevent SQL Injection when using PDO.', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/pdo.quote.php', "label": 'PDO::quote'},
            {"url": 'https://www.php.net/manual/en/pdo.prepared-statements.php', "label": 'Prepared statements'},
        ],
    },
    {
        "prompt": '[Q27] Which of the following does NOT help to protect against session hijacking and fixation\nattacks?',
        "explanation": 'XSS protection, HTTPS + Secure cookies, session.use_only_cookies=1, and session_regenerate_id() all reduce hijacking/fixation risk.\nsession.cookie_lifetime=0 only makes the cookie a browser-session cookie; it does not protect against hijacking or fixation.\nCorrect answer: Set the session.cookie_lifetime php.ini parameter to 0.',
        "options": [
            ('Protect against XSS vulnerabilities in the application.', False),
            ('Use HTTPS and set the secure cookie flag.', False),
            ('Set the session.use_only_cookies php.ini parameter to 1.', False),
            ('Set the session.cookie_lifetime php.ini parameter to 0.', True),
            ('Rotate the session id on successful login and logout using\nsession_regenerate_id().', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/session.security.php', "label": 'Session security'},
            {"url": 'https://www.php.net/manual/en/function.session-regenerate-id.php', "label": 'session_regenerate_id'},
        ],
    },
    {
        "prompt": '[Q28] Are PHP constants case-sensitive?',
        "explanation": 'PHP constants created with const or define() are always case-sensitive.\n(define() used to allow case-insensitive constants via a third argument; that behavior is removed in modern PHP.)\nCorrect answer: Yes, they are always case-sensitive.',
        "options": [
            ('They are not by default, but it is possible to create case-sensitive constants.', False),
            ('No, they are always case-insensitive.', False),
            ('They are by default, but it is possible to create case-insensitive constants.', False),
            ('Yes, they are always case-sensitive.', True),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/language.constants.php', "label": 'Constants'},
            {"url": 'https://www.php.net/manual/en/function.define.php', "label": 'define'},
        ],
    },
    {
        "prompt": '[Q29] What is the output of the following code?\n\n```php\necho "22" + "0.2", 23 . 1;\n```',
        "explanation": '"22" + "0.2" uses numeric addition → 22.2.\n23 . 1 concatenates as strings → \'231\'.\nWith comma in echo, output is 22.2,231.',
        "options": [
            ('56.2', False),
            ('22.2,231', True),
            ('22.2231', False),
            ('220.2231', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/language.operators.arithmetic.php', "label": 'Arithmetic operators'},
            {"url": 'https://www.php.net/manual/en/language.operators.string.php', "label": 'String operators'},
        ],
    },
    {
        "prompt": '[Q30] What are two reasons to use POST instead of GET when submitting a form? (Choose 2)',
        "explanation": 'POST supports much larger payloads than GET and is required for file uploads.\nPOST alone does not prevent CSRF and does not encrypt data (HTTPS does).\nCorrect answers: higher size limits, and possibility to upload files.',
        "options": [
            ('A much higher content size restriction.', True),
            ('Protection from Cross-Site Request Forgery.', False),
            ('POST requests can automatically encrypt data.', False),
            ('Possibility to upload files.', True),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/reserved.variables.post.php', "label": '$_POST'},
            {"url": 'https://www.php.net/manual/en/features.file-upload.post-method.php', "label": 'POST method uploads'},
        ],
    },
    {
        "prompt": '[Q31] What function is best suited for extracting data from a formatted string into an array?',
        "explanation": 'sscanf() parses a formatted string into variables/array values.\nfgetcsv/strtok/sprintf solve different problems.\nCorrect answer: sscanf().',
        "options": [
            ('fgetcsv()', False),
            ('strtok()', False),
            ('sprintf()', False),
            ('sscanf()', True),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/function.sscanf.php', "label": 'sscanf'},
        ],
    },
    {
        "prompt": '[Q32] Which of the following expressions generate a value that is different from the others?',
        "explanation": "(a)(b)(c) all produce ['one','two','three'] with keys 0,1,2.\n(d) uses keys starting at 1, so the array value differs under PHP comparison.\nCorrect answer: [1 => 'one', 2 => 'two', 3 => 'three'].",
        "options": [
            ("explode(',', 'one,two,three')", False),
            ("array('one', 'two', 'three')", False),
            ("['one', 'two', 'three']", False),
            ("[1 => 'one', 2 => 'two', 3 => 'three']", True),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/function.explode.php', "label": 'explode'},
            {"url": 'https://www.php.net/manual/en/language.types.array.php', "label": 'Arrays'},
        ],
    },
    {
        "prompt": "[Q33] Which of these PHP values may NOT be encoded to a JavaScript literal using PHP's ext/json capabilities?",
        "explanation": 'json_encode() can encode strings and arrays/objects.\nA function/closure cannot be represented as a JSON literal.\nCorrect answer: function(){ alert("Hello, world!"); }',
        "options": [
            ("'Hello, world!'", False),
            ("['Hello, world!']", False),
            ('function(){ alert("Hello, world!"); }', True),
            ("['message' => 'Hello, world!']", False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/function.json-encode.php', "label": 'json_encode'},
            {"url": 'https://www.php.net/manual/en/book.json.php', "label": 'JSON extension'},
        ],
    },
    {
        "prompt": '[Q34] How can you define array constants with PHP?',
        "explanation": 'Since PHP 5.6, both const and define() can define array constants.\nCorrect answer: With const and define().',
        "options": [
            ('With const and define().', True),
            ('Only with const.', False),
            ('Only primitive types may be used for constants.', False),
            ('Only with define().', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/language.constants.syntax.php', "label": 'Constant syntax'},
            {"url": 'https://www.php.net/manual/en/function.define.php', "label": 'define'},
        ],
    },
    {
        "prompt": "[Q35] What will the following code print out?\n\n```php\n$str = '✓ one of the following';\necho str_replace('✓', 'Check', $str);\n```",
        "explanation": "str_replace('✓', 'Check', $str) replaces the check mark with 'Check'.\nThe string '✓ one of the following' becomes 'Check one of the following'.\nCorrect answer: Check one of the following.",
        "options": [
            ('Check one of the following', True),
            ('✓ one of the following', False),
            ('one of the following', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/function.str-replace.php', "label": 'str_replace'},
        ],
    },
    {
        "prompt": '[Q36] The class Person should have the two protected properties lastName and\nfirstName. The class should allow setting both properties upon object instantiation. You\nwant to write as little code as possible to achieve this.\nWhich of the following approaches satisfies these requirements?\n\n```php\nparent::__construct();\n    }\n}\nclass Person {\n    public function __construct($firstName, $lastName) {\n        $this->firstName = $firstName;\n        $this->lastName = $lastName;\n    }\n}\nclass Person {\n    public function __construct(protected string $firstName,\nprotected string  $lastName) {\n    }\n}\nclass Person {\n    public function __construct(protected $firstName: string,\nprotected $lastName: string) {\n    }\n}\n```',
        "explanation": 'Constructor property promotion (PHP 8+) declares and initializes protected properties with minimal code.\nCorrect answer: the promoted-constructor approach.',
        "options": [
            ('protected $firstName;', False),
            ('protected $lastName;', False),
            ('public function __construct($firstName, $lastName) {', True),
            ('class Person {', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion', "label": 'Constructor property promotion'},
        ],
    },
    {
        "prompt": '[Q37] How many elements does the array $matches from the following code contain?\n\n```php\n$str = "The cat sat on the roof of their house.";\n$matches = preg_split(\'/(the)/i\', $str, -1,\nPREG_SPLIT_DELIM_CAPTURE);\n```',
        "explanation": 'preg_split(\'/(the)/i\', ..., PREG_SPLIT_DELIM_CAPTURE) splits on \'the\' (case-insensitive) and keeps the captured delimiters.\nFor "The cat sat on the roof of their house." the pieces are:\n[\'\', \'The\', \' cat sat on \', \'the\', \' roof of \', \'the\', \'ir house.\']\n(note: \'their\' also matches the leading \'the\').\nThat is 7 elements.\nCorrect answer: 7.',
        "options": [
            ('2', False),
            ('9', False),
            ('3', False),
            ('7', True),
            ('4', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/function.preg-split.php', "label": 'preg_split'},
        ],
    },
    {
        "prompt": "[Q38] What is the output of the following code?\n\n```php\nclass Bar {\n    private $a = 'b';\n    public $c = 'd';\n}\n$x = (array) new Bar();\necho array_key_exists('a', $x) ? 'true' : 'false';\necho '-';\necho array_key_exists('c', $x) ? 'true' : 'false';\n```",
        "explanation": 'Casting an object to array exposes public properties by name.\nPrivate properties become keys like "\\0Class\\0prop".\narray_keys() therefore includes the mangled private key and the public one.',
        "options": [
            ('true-false', False),
            ('false-true', True),
            ('false-false', False),
            ('true-true', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/language.types.array.php#language.types.array.casting', "label": 'Converting to array'},
            {"url": 'https://www.php.net/manual/en/function.array-keys.php', "label": 'array_keys'},
        ],
    },
    {
        "prompt": '[Q39] Consider the following code:\n\n```php\n$xml = simplexml_load_string(\'<?xml version="1.0"?><root><language>PHP</language></root>\');\n$lang = $xml->xpath(\'//language\');\n```\n\nWhich of the following commands will output "PHP"?',
        "explanation": "xpath('//language') returns an array of nodes.\necho $lang[0]; prints the first node string value 'PHP'.\nechoing the array / strval(array) / toString() are invalid here.\nCorrect answer: echo $lang[0];",
        "options": [
            ('echo $lang[0];', True),
            ('echo $lang;', False),
            ('echo strval($lang);', False),
            ('echo $lang->toString();', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/simplexmlelement.xpath.php', "label": 'SimpleXMLElement::xpath'},
        ],
    },
    {
        "prompt": '[Q40] What can prevent PHP from being able to open a file on the hard drive? (Choose 2)',
        "explanation": 'open_basedir restrictions and filesystem permissions can block opening a file.\nBeing under /tmp or running as CGI does not inherently prevent file access.\nCorrect answers: outside open_basedir, and filesystem permissions.',
        "options": [
            ('File is inside the /tmp directory.', False),
            ('PHP is running in CGI mode.', False),
            ('File is outside of open_basedir.', True),
            ('File system permissions.', True),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/ini.core.php#ini.open-basedir', "label": 'open_basedir'},
            {"url": 'https://www.php.net/manual/en/function.fopen.php', "label": 'fopen'},
        ],
    },
    {
        "prompt": "[Q41] What is the output of the following code?\n\n```html\n<?php\ndeclare(strict_types=1);\nfunction add (int $a, int $b) {\n    return $a + $b;\n}\ntry {\n    echo add(1, 2.0);\n} catch (Exception $ex) {\n    echo 'Exception';\n} catch (Error $err) {\n    echo 'Error';\n} catch (Throwable $e) {\n    echo 'Throwable';\n}\n```",
        "explanation": 'With declare(strict_types=1), float 2.0 is not accepted for int $b.\nThat raises TypeError, which is caught by catch (Error $err).\nOutput: Error.',
        "options": [
            ('Exception', False),
            ('3', False),
            ('Error', True),
            ('Throwable', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/language.types.declarations.php#language.types.declarations.strict', "label": 'Strict typing'},
            {"url": 'https://www.php.net/manual/en/class.error.php', "label": 'Error'},
        ],
    },
    {
        "prompt": '[Q42] What is the purpose of the never return type?',
        "explanation": 'never means the function never returns normally (always throws or exits).\nCorrect answer: It indicates that a function will never return a value.',
        "options": [
            ('It indicates that there will never be a type restriction on the value that the function\nreturns.', False),
            ('It indicates that a variable will never have a value.', False),
            ('It indicates that a function will never return a value.', True),
            ('It indicates that a function will never be run.', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/language.types.declarations.php#language.types.declarations.return-only', "label": 'never return type'},
        ],
    },
    {
        "prompt": '[Q43] Given a PHP value, which of these code samples shows how to convert the value to\nJSON?\n\n```php\n$string = $value->__toJson();\n$string = json_encode($value);\n```',
        "explanation": 'The native way to convert a PHP value to JSON is json_encode($value).\nCorrect answer: json_encode(...).',
        "options": [
            ('$json = new Json($value);', False),
            ('$string = $json->__toString();', False),
            ('$value = (object) $value;', False),
            ('$string = Json::encode($value);', True),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/function.json-encode.php', "label": 'json_encode'},
        ],
    },
    {
        "prompt": "[Q44] What is the output of the following code?\n\n```php\n$a = ['apples', 'bananas', 'clementines'];\nunset($a[1]);\nprint_r($a);\n```",
        "explanation": 'unset($a[1]) removes key 1 and does not reindex the array.\nRemaining keys are 0 => apples and 2 => clementines.\nCorrect print_r output is the array with keys 0 and 2.',
        "options": [
            ('Array\n(\n    [1] => apples\n    [2] => clementines\n)', False),
            ('Array\n(\n    [0] => apples\n    [2] => clementines\n)', True),
            ('Array\n(\n    [0] => apples\n    [1] =>\n    [2] => clementines\n)', False),
            ('Array\n(\n    [0] => apples\n    [1] => clementines\n)', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/function.unset.php', "label": 'unset'},
            {"url": 'https://www.php.net/manual/en/function.print-r.php', "label": 'print_r'},
        ],
    },
    {
        "prompt": '[Q45] Consider the following table data and PHP code. What is the outcome?\n\nTable data (table name "users" with primary key "id"):\n\n```text\nid  name   email\n1   anna   alpha@example.com\n2   betty  beta@example.org\n3   clara  gamma@example.net\n5   sue    sigma@example.info\n```\n\nPHP code (assume the PDO connection is correctly established):\n\n```php\n$dsn  = \'mysql:host=localhost;dbname=exam\';\n$user = \'username\';\n$pass = \'********\';\n$pdo  = new PDO($dsn, $user, $pass);\ntry {\n    $cmd  = "INSERT INTO users (id, name, email) VALUES\n(:id, :name, :email)";\n    $stmt = $pdo->prepare($cmd);\n    $stmt->bindValue(\':id\', 1);\n    $stmt->bindValue(\':name\', \'anna\');\n    $stmt->bindValue(\':email\', \'alpha@example.com\');\n    $stmt->execute();\n    echo "Success!";\n} catch (PDOException $e) {\n    echo "Failure!";\n    throw $e;\n}\n```',
        "explanation": 'The table already has id=1, so INSERT id=1 fails with a primary key violation.\nPDO defaults to ERRMODE_SILENT: execute() returns false and does not throw.\nThe catch block never runs, so the script still prints "Success!".\nCorrect answer: PK violation + "Success!" message.',
        "options": [
            ('The INSERT will fail because of a primary key violation, and the user will see the "Success!" message.', True),
            ('The INSERT will succeed and the user will see the "Success!" message.', False),
            ('The INSERT will fail because of a primary key violation, and the user will see a PDO warning message.', False),
            ('The INSERT will fail because of a primary key violation, and the user will see the "Failure!" message.', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/pdo.error-handling.php', "label": 'PDO error handling'},
            {"url": 'https://www.php.net/manual/en/pdo.setattribute.php', "label": 'PDO::setAttribute'},
        ],
    },
    {
        "prompt": '[Q46] What is the output of the following code?\n\n```php\nfunction increment ($val) {\n    ++$val;\n}\n$val = 1;\nincrement ($val);\necho $val;\n```',
        "explanation": '++$val inside the function still uses pass-by-value, so the outer $val stays 1.\nOutput: 1.',
        "options": [
            ('1', True),
            ('2', False),
            ('parse error', False),
            ('undefined variable', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/functions.arguments.php#functions.arguments.passing', "label": 'Passing arguments by value'},
            {"url": 'https://www.php.net/manual/en/language.operators.increment.php', "label": 'Increment/decrement'},
        ],
    },
    {
        "prompt": '[Q47] The following form is loaded in a recent browser. The user selects the second option and submits the form:\n\n```html\n<form method="post">\n  <select name="list">\n    <option>one</option>\n    <option>two</option>\n    <option>three</option>\n  </select>\n</form>\n```\n\nIn the server-side PHP code that handles the form data, what is the value of $_POST[\'list\']?',
        "explanation": "Without a value attribute, the browser submits the option's text content.\nSelecting the second option submits 'two'.\nCorrect answer: two.",
        "options": [
            ('2', False),
            ('1', False),
            ('null', False),
            ('two', True),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/reserved.variables.post.php', "label": '$_POST'},
            {"url": 'https://developer.mozilla.org/en-US/docs/Web/HTML/Element/option', "label": 'HTML option element'},
        ],
    },
    {
        "prompt": '[Q48] What are two differences between "print" and "echo"? (Choose 2)',
        "explanation": 'print returns 1; echo does not return a value.\necho can take multiple arguments; print cannot.\nCorrect answers: those two differences.',
        "options": [
            ('Echo buffers the output, while print does not.', False),
            ('Print has a return value, echo does not.', True),
            ('Print can accept multiple arguments, echo does not.', False),
            ('Echo can accept multiple arguments, print does not.', True),
            ('Print buffers the output, while echo does not.', False),
            ('Echo has a return value, print does not.', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/function.echo.php', "label": 'echo'},
            {"url": 'https://www.php.net/manual/en/function.print.php', "label": 'print'},
        ],
    },
    {
        "prompt": '[Q49] Before the headers are sent, how can you remove a previously set header?',
        "explanation": 'header_remove() removes a previously set header before headers are sent.\nCorrect answer: Use the header_remove() function.',
        "options": [
            ('Use the die() function to abort the PHP script.', False),
            ('Use the headers_list() function, providing the name of the header as the second\nargument.', False),
            ('Not possible.', False),
            ('Use the header_remove() function, providing the name of the header.', True),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/function.header-remove.php', "label": 'header_remove'},
        ],
    },
    {
        "prompt": '[Q50] What is the output of the following code?\n\n```php\nclass Base {\n    protected static function whoami() {\n        echo "Base ";\n    }\n    public static function whoareyou() {\n        static::whoami();\n    }\n}\nclass A extends Base {\n    public static function test() {\n        Base::whoareyou();\n        self::whoareyou();\n        parent::whoareyou();\n        A::whoareyou();\n        static::whoareyou();\n    }\n    public static function whoami() {\n        echo "A ";\n    }\n}\nclass B extends A {\n    public static function whoami() {\n        echo "B ";\n    }\n}\nB::test();\n```',
        "explanation": 'Late static binding with B::test() yields:\nBase::whoareyou() → Base\nself::whoareyou() → B\nparent::whoareyou() → B\nA::whoareyou() → A\nstatic::whoareyou() → B\nOutput: Base B B A B.',
        "options": [
            ('Base B B A B', True),
            ('Base A Base A B', False),
            ('B B B B B', False),
            ('Base B A A B', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/language.oop5.late-static-bindings.php', "label": 'Late static bindings'},
        ],
    },
    {
        "prompt": '[Q51] Which class of HTTP status codes is used for server error conditions?',
        "explanation": '5xx status codes represent server error conditions.\nCorrect answer: 5xx.',
        "options": [
            ('2XX', False),
            ('3XX', False),
            ('4XX', False),
            ('5XX', True),
        ],
        "references": [
            {"url": 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#server_error_responses', "label": 'HTTP 5xx status codes'},
            {"url": 'https://www.php.net/manual/en/function.http-response-code.php', "label": 'http_response_code'},
        ],
    },
    {
        "prompt": "[Q52] Which key of $_FILES['field'] contains the provisional name/path of the uploaded file on the server?",
        "explanation": 'tmp_name is the temporary path of the uploaded file on the server.\nname is the original client filename.\nCorrect answer: tmp_name.',
        "options": [
            ('name', False),
            ('tmp_name', True),
            ('tmp', False),
            ('file', False),
            ('path', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/features.file-upload.php', "label": 'Handling file uploads'},
            {"url": 'https://www.php.net/manual/en/reserved.variables.files.php', "label": '$_FILES'},
        ],
    },
    {
        "prompt": '[Q53] How many times will the function counter() be executed in the following code?\n\n```php\nfunction counter($start, &$stop)\n{\n    if ($stop > $start) {\n        return;\n    }\n    counter($start--, ++$stop);\n}\n$start = 5;\n$stop = 2;\ncounter($start, $stop);\n```',
        "explanation": 'counter($start--, ++$stop) passes the current $start, then increments $stop.\nCalls with ($start=5, $stop): (5,2) → (5,3) → (5,4) → (5,5) → (5,6).\nOn (5,6), $stop > $start and it returns.\nThat is 5 executions.\nCorrect answer: 5.',
        "options": [
            ('5', True),
            ('6', False),
            ('4', False),
            ('3', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/functions.user-defined.php', "label": 'User-defined functions'},
            {"url": 'https://www.php.net/manual/en/language.operators.increment.php', "label": 'Increment/decrement'},
        ],
    },
    {
        "prompt": '[Q54] Which of the following statements about anonymous functions in PHP are NOT true?\n(Choose 2)',
        "explanation": 'Statements that are NOT true:\nAnonymous functions created in object context are not automatically bound.\nAssigning a Closure to an object property does not bind it by itself.\nCorrect answers: those two false statements.',
        "options": [
            ('Anonymous functions can be bound to objects.', False),
            ('Binding defines the value of $this and the scope for a closure.', False),
            ('Anonymous functions created within object context are always bound to that object.', True),
            ('Assigning closure to a property of an object binds it to that object.', True),
            ('Methods bind() and bindTo() of the Closure object provide means to create\nclosures with different binding and scope.', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/functions.anonymous.php', "label": 'Anonymous functions'},
            {"url": 'https://www.php.net/manual/en/class.closure.php', "label": 'Closure'},
        ],
    },
    {
        "prompt": '[Q55] Which of these statements about PHP is false? (Choose 2)',
        "explanation": 'False statements:\nA final class cannot be extended.\nPHP does not allow multiple inheritance of classes (a class may extend only one parent).\nNote: since PHP 8.4, properties can be final — so that is no longer a false statement.\nCorrect answers: (c) and (d).',
        "options": [
            ('A class with a final function may be extended.', False),
            ('A final class may be instantiated.', False),
            ('A final class can be extended.', True),
            ('A class may extend more than one parent class.', True),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/language.oop5.final.php', "label": 'Final Keyword'},
            {"url": 'https://www.php.net/manual/en/language.oop5.inheritance.php', "label": 'Object Inheritance'},
        ],
    },
    {
        "prompt": '[Q56] What is the preferred method for preventing SQL injection?',
        "explanation": 'Prepared statements with bound parameters are the preferred SQL injection defense.\nCorrect answer: Always using prepared statements when available.',
        "options": [
            ('Always using prepared statements for all SQL queries when available.', True),
            ('Always using the available database-specific escaping functionality on all variables prior\nto building the SQL query.', False),
            ('Using addslashes() to escape variables to be used in a query.', False),
            ('Using htmlspecialchars() and the available database-specific escaping\nfunctionality to escape variables to be used in a query.', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/pdo.prepared-statements.php', "label": 'Prepared statements'},
            {"url": 'https://www.php.net/manual/en/security.database.sql-injection.php', "label": 'SQL injection'},
        ],
    },
    {
        "prompt": '[Q57] What is the name of the method that can be used to provide read access to virtual\nproperties in a class?',
        "explanation": '__get() provides read access to inaccessible/virtual properties.\nCorrect answer: __get.',
        "options": [
            ('__wakeup()', False),
            ('__fetch()', False),
            ('__get()', True),
            ('__call()', False),
            ('__set()', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/language.oop5.overloading.php#object.get', "label": '__get'},
        ],
    },
    {
        "prompt": "[Q58] What will the following function call print?\n\n```php\nprintf('%010.6f', 22);\n```",
        "explanation": '%010.6f formats 22 as 22.000000 (9 chars) and left-pads with 0 to width 10.\nResult: 022.000000.',
        "options": [
            ('22', False),
            ('22.000000', False),
            ('022.000000', True),
            ('22.00', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/function.printf.php', "label": 'printf'},
            {"url": 'https://www.php.net/manual/en/function.sprintf.php', "label": 'sprintf format'},
        ],
    },
    {
        "prompt": "[Q59] Given the following, what is the result of running test.php?\nArquivo functions.php:\nArquivo test.php:\n\n```php\nfunction oops(string $input)\n{\n    return $input;\n}\ninclude 'functions.php';\nvar_dump(oops(12));\n```",
        "explanation": 'With strict_types=1, oops(12) passes an int to string and raises TypeError.\nCorrect answer: Fatal error: Uncaught TypeError.',
        "options": [
            ('Fatal error: Uncaught TypeError', True),
            ('string(2) "12"', False),
            ("Parse error: syntax error, unexpected 'string'", False),
            ('Recoverable fatal error\ndeclare(strict_types=1);', False),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/language.types.declarations.php#language.types.declarations.strict', "label": 'Strict typing'},
            {"url": 'https://www.php.net/manual/en/class.typeerror.php', "label": 'TypeError'},
        ],
    },
    {
        "prompt": '[Q60] Given the following PHP function:\nWhich of the following values for the $s parameter do NOT throw a type error when calling\nthe doSomething() function?\n\n```php\nfunction doSomething(?string $s) {\n   // ...\n}\n```',
        "explanation": "?string accepts null, '' and 'null' without a TypeError.\nCorrect answer: All of the above.",
        "options": [
            ("'null'", False),
            ('null', False),
            ('""', False),
            ('All of the above', True),
        ],
        "references": [
            {"url": 'https://www.php.net/manual/en/language.types.declarations.php#language.types.declarations.nullable', "label": 'Nullable types'},
        ],
    },
]

_assigned = [n for theme in THEME_QUIZZES for n in theme["question_numbers"]]
if sorted(_assigned) != list(range(1, len(QUESTIONS_DATA) + 1)):
    missing = set(range(1, len(QUESTIONS_DATA) + 1)) - set(_assigned)
    dupes = [n for n in _assigned if _assigned.count(n) > 1]
    raise RuntimeError(
        f"Theme assignment incomplete: missing={sorted(missing)} dupes={sorted(set(dupes))}"
    )
