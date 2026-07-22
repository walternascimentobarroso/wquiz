#!/usr/bin/env python3
"""Add PHP.net (and related) references to every seed question, then rewrite seed."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "app" / "services" / "php_seed_data.py"

# 1-based question number -> list of {url, label}
REFERENCES: dict[int, list[dict[str, str]]] = {
    1: [
        {
            "url": "https://www.php.net/manual/en/features.file-upload.php",
            "label": "Handling file uploads",
        },
        {
            "url": "https://www.php.net/manual/en/function.move-uploaded-file.php",
            "label": "move_uploaded_file",
        },
    ],
    2: [
        {"url": "https://www.php.net/manual/en/language.enumerations.php", "label": "Enumerations"},
        {
            "url": "https://www.php.net/manual/en/language.enumerations.basics.php",
            "label": "Enum basics",
        },
    ],
    3: [
        {
            "url": "https://www.php.net/manual/en/function.file-get-contents.php",
            "label": "file_get_contents",
        },
        {
            "url": "https://www.php.net/manual/en/context.http.php",
            "label": "HTTP context options",
        },
    ],
    4: [
        {
            "url": "https://www.php.net/manual/en/session.security.php",
            "label": "Sessions and security",
        },
        {
            "url": "https://www.php.net/manual/en/session.configuration.php#ini.session.cookie-samesite",
            "label": "session.cookie_samesite",
        },
    ],
    5: [
        {
            "url": "https://www.php.net/manual/en/language.oop5.magic.php",
            "label": "Magic methods",
        },
    ],
    6: [
        {
            "url": "https://www.php.net/manual/en/language.oop5.basic.php#language.oop5.basic.class.class",
            "label": "::class",
        },
        {
            "url": "https://www.php.net/manual/en/language.namespaces.basics.php",
            "label": "Namespaces",
        },
    ],
    7: [
        {"url": "https://getcomposer.org/doc/", "label": "Composer documentation"},
    ],
    8: [
        {
            "url": "https://www.php.net/manual/en/language.oop5.visibility.php#language.oop5.visibility-asymmetric",
            "label": "Asymmetric property visibility",
        },
    ],
    9: [
        {
            "url": "https://www.php.net/manual/en/pdo.connections.php",
            "label": "PDO connections",
        },
        {
            "url": "https://www.php.net/manual/en/features.persistent-connections.php",
            "label": "Persistent connections",
        },
    ],
    10: [
        {
            "url": "https://www.php.net/manual/en/reference.pcre.pattern.syntax.php",
            "label": "PCRE pattern syntax",
        },
        {
            "url": "https://www.php.net/manual/en/function.preg-match.php",
            "label": "preg_match",
        },
    ],
    11: [
        {
            "url": "https://www.php.net/manual/en/pdostatement.fetchall.php",
            "label": "PDOStatement::fetchAll",
        },
        {
            "url": "https://www.php.net/manual/en/pdo.constants.php#pdo.constants.fetch-both",
            "label": "PDO::FETCH_BOTH",
        },
    ],
    12: [
        {
            "url": "https://www.php.net/manual/en/language.types.object.php#language.types.object.casting",
            "label": "Converting to object",
        },
    ],
    13: [
        {
            "url": "https://www.php.net/manual/en/function.http-response-code.php",
            "label": "http_response_code",
        },
        {
            "url": "https://www.php.net/manual/en/function.header.php",
            "label": "header",
        },
    ],
    14: [
        {
            "url": "https://www.php.net/manual/en/language.oop5.properties.php#language.oop5.properties.dynamic-properties",
            "label": "Dynamic properties",
        },
        {
            "url": "https://www.php.net/manual/en/class.allowdynamicproperties.php",
            "label": "AllowDynamicProperties",
        },
    ],
    15: [
        {
            "url": "https://www.php.net/manual/en/simplexml.examples-basic.php",
            "label": "SimpleXML basic usage",
        },
        {
            "url": "https://www.php.net/manual/en/function.simplexml-load-string.php",
            "label": "simplexml_load_string",
        },
    ],
    16: [
        {
            "url": "https://www.php.net/manual/en/functions.arguments.php#functions.arguments.passing",
            "label": "Passing arguments by value",
        },
    ],
    17: [
        {
            "url": "https://www.php.net/manual/en/language.operators.array.php",
            "label": "Array operators",
        },
        {
            "url": "https://www.php.net/manual/en/function.implode.php",
            "label": "implode",
        },
    ],
    18: [
        {
            "url": "https://www.php.net/manual/en/control-structures.match.php",
            "label": "match",
        },
    ],
    19: [
        {
            "url": "https://www.php.net/manual/en/function.array-rand.php",
            "label": "array_rand",
        },
    ],
    20: [
        {
            "url": "https://www.php.net/manual/en/class.throwable.php",
            "label": "Throwable",
        },
        {
            "url": "https://www.php.net/manual/en/language.exceptions.php",
            "label": "Exceptions",
        },
    ],
    21: [
        {
            "url": "https://www.php.net/manual/en/language.operators.bitwise.php",
            "label": "Bitwise operators",
        },
    ],
    22: [
        {
            "url": "https://www.php.net/manual/en/language.namespaces.rationale.php",
            "label": "Namespaces rationale",
        },
    ],
    23: [
        {
            "url": "https://www.php.net/manual/en/language.types.string.php#language.types.string.syntax.heredoc",
            "label": "Heredoc syntax",
        },
    ],
    24: [
        {
            "url": "https://www.php.net/manual/en/language.types.declarations.php",
            "label": "Type declarations",
        },
        {
            "url": "https://www.php.net/manual/en/class.typeerror.php",
            "label": "TypeError",
        },
    ],
    25: [
        {
            "url": "https://www.php.net/manual/en/function.file-get-contents.php",
            "label": "file_get_contents",
        },
        {
            "url": "https://www.php.net/manual/en/function.file-put-contents.php",
            "label": "file_put_contents",
        },
        {
            "url": "https://www.php.net/manual/en/function.readfile.php",
            "label": "readfile",
        },
    ],
    26: [
        {
            "url": "https://www.php.net/manual/en/pdo.quote.php",
            "label": "PDO::quote",
        },
        {
            "url": "https://www.php.net/manual/en/pdo.prepared-statements.php",
            "label": "Prepared statements",
        },
    ],
    27: [
        {
            "url": "https://www.php.net/manual/en/session.security.php",
            "label": "Session security",
        },
        {
            "url": "https://www.php.net/manual/en/function.session-regenerate-id.php",
            "label": "session_regenerate_id",
        },
    ],
    28: [
        {
            "url": "https://www.php.net/manual/en/language.constants.php",
            "label": "Constants",
        },
        {
            "url": "https://www.php.net/manual/en/function.define.php",
            "label": "define",
        },
    ],
    29: [
        {
            "url": "https://www.php.net/manual/en/language.operators.arithmetic.php",
            "label": "Arithmetic operators",
        },
        {
            "url": "https://www.php.net/manual/en/language.operators.string.php",
            "label": "String operators",
        },
    ],
    30: [
        {
            "url": "https://www.php.net/manual/en/reserved.variables.post.php",
            "label": "$_POST",
        },
        {
            "url": "https://www.php.net/manual/en/features.file-upload.post-method.php",
            "label": "POST method uploads",
        },
    ],
    31: [
        {
            "url": "https://www.php.net/manual/en/function.sscanf.php",
            "label": "sscanf",
        },
    ],
    32: [
        {
            "url": "https://www.php.net/manual/en/function.explode.php",
            "label": "explode",
        },
        {
            "url": "https://www.php.net/manual/en/language.types.array.php",
            "label": "Arrays",
        },
    ],
    33: [
        {
            "url": "https://www.php.net/manual/en/function.json-encode.php",
            "label": "json_encode",
        },
        {
            "url": "https://www.php.net/manual/en/book.json.php",
            "label": "JSON extension",
        },
    ],
    34: [
        {
            "url": "https://www.php.net/manual/en/language.constants.syntax.php",
            "label": "Constant syntax",
        },
        {
            "url": "https://www.php.net/manual/en/function.define.php",
            "label": "define",
        },
    ],
    35: [
        {
            "url": "https://www.php.net/manual/en/function.str-replace.php",
            "label": "str_replace",
        },
    ],
    36: [
        {
            "url": "https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion",
            "label": "Constructor property promotion",
        },
    ],
    37: [
        {
            "url": "https://www.php.net/manual/en/function.preg-split.php",
            "label": "preg_split",
        },
    ],
    38: [
        {
            "url": "https://www.php.net/manual/en/language.types.array.php#language.types.array.casting",
            "label": "Converting to array",
        },
        {
            "url": "https://www.php.net/manual/en/function.array-keys.php",
            "label": "array_keys",
        },
    ],
    39: [
        {
            "url": "https://www.php.net/manual/en/simplexmlelement.xpath.php",
            "label": "SimpleXMLElement::xpath",
        },
    ],
    40: [
        {
            "url": "https://www.php.net/manual/en/ini.core.php#ini.open-basedir",
            "label": "open_basedir",
        },
        {
            "url": "https://www.php.net/manual/en/function.fopen.php",
            "label": "fopen",
        },
    ],
    41: [
        {
            "url": "https://www.php.net/manual/en/language.types.declarations.php#language.types.declarations.strict",
            "label": "Strict typing",
        },
        {
            "url": "https://www.php.net/manual/en/class.error.php",
            "label": "Error",
        },
    ],
    42: [
        {
            "url": "https://www.php.net/manual/en/language.types.declarations.php#language.types.declarations.return-only",
            "label": "never return type",
        },
    ],
    43: [
        {
            "url": "https://www.php.net/manual/en/function.json-encode.php",
            "label": "json_encode",
        },
    ],
    44: [
        {
            "url": "https://www.php.net/manual/en/function.unset.php",
            "label": "unset",
        },
        {
            "url": "https://www.php.net/manual/en/function.print-r.php",
            "label": "print_r",
        },
    ],
    45: [
        {
            "url": "https://www.php.net/manual/en/pdo.error-handling.php",
            "label": "PDO error handling",
        },
        {
            "url": "https://www.php.net/manual/en/pdo.setattribute.php",
            "label": "PDO::setAttribute",
        },
    ],
    46: [
        {
            "url": "https://www.php.net/manual/en/functions.arguments.php#functions.arguments.passing",
            "label": "Passing arguments by value",
        },
        {
            "url": "https://www.php.net/manual/en/language.operators.increment.php",
            "label": "Increment/decrement",
        },
    ],
    47: [
        {
            "url": "https://www.php.net/manual/en/reserved.variables.post.php",
            "label": "$_POST",
        },
        {
            "url": "https://developer.mozilla.org/en-US/docs/Web/HTML/Element/option",
            "label": "HTML option element",
        },
    ],
    48: [
        {
            "url": "https://www.php.net/manual/en/function.echo.php",
            "label": "echo",
        },
        {
            "url": "https://www.php.net/manual/en/function.print.php",
            "label": "print",
        },
    ],
    49: [
        {
            "url": "https://www.php.net/manual/en/function.header-remove.php",
            "label": "header_remove",
        },
    ],
    50: [
        {
            "url": "https://www.php.net/manual/en/language.oop5.late-static-bindings.php",
            "label": "Late static bindings",
        },
    ],
    51: [
        {
            "url": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#server_error_responses",
            "label": "HTTP 5xx status codes",
        },
        {
            "url": "https://www.php.net/manual/en/function.http-response-code.php",
            "label": "http_response_code",
        },
    ],
    52: [
        {
            "url": "https://www.php.net/manual/en/features.file-upload.php",
            "label": "Handling file uploads",
        },
        {
            "url": "https://www.php.net/manual/en/reserved.variables.files.php",
            "label": "$_FILES",
        },
    ],
    53: [
        {
            "url": "https://www.php.net/manual/en/functions.user-defined.php",
            "label": "User-defined functions",
        },
        {
            "url": "https://www.php.net/manual/en/language.operators.increment.php",
            "label": "Increment/decrement",
        },
    ],
    54: [
        {
            "url": "https://www.php.net/manual/en/functions.anonymous.php",
            "label": "Anonymous functions",
        },
        {
            "url": "https://www.php.net/manual/en/class.closure.php",
            "label": "Closure",
        },
    ],
    55: [
        {
            "url": "https://www.php.net/manual/en/language.oop5.final.php",
            "label": "Final Keyword",
        },
        {
            "url": "https://www.php.net/manual/en/language.oop5.inheritance.php",
            "label": "Object Inheritance",
        },
    ],
    56: [
        {
            "url": "https://www.php.net/manual/en/pdo.prepared-statements.php",
            "label": "Prepared statements",
        },
        {
            "url": "https://www.php.net/manual/en/security.database.sql-injection.php",
            "label": "SQL injection",
        },
    ],
    57: [
        {
            "url": "https://www.php.net/manual/en/language.oop5.overloading.php#object.get",
            "label": "__get",
        },
    ],
    58: [
        {
            "url": "https://www.php.net/manual/en/function.printf.php",
            "label": "printf",
        },
        {
            "url": "https://www.php.net/manual/en/function.sprintf.php",
            "label": "sprintf format",
        },
    ],
    59: [
        {
            "url": "https://www.php.net/manual/en/language.types.declarations.php#language.types.declarations.strict",
            "label": "Strict typing",
        },
        {
            "url": "https://www.php.net/manual/en/class.typeerror.php",
            "label": "TypeError",
        },
    ],
    60: [
        {
            "url": "https://www.php.net/manual/en/language.types.declarations.php#language.types.declarations.nullable",
            "label": "Nullable types",
        },
    ],
}


def main() -> None:
    assert set(REFERENCES) == set(range(1, 61)), "Need refs for Q1–Q60"
    for n, refs in REFERENCES.items():
        assert 1 <= len(refs) <= 5, n
        for ref in refs:
            assert ref["url"].startswith("http"), (n, ref)
            assert ref["label"].strip(), (n, ref)

    # Import after path setup when run inside container; for local rewrite we
    # mutate the QUESTIONS_DATA literals in the seed file via exec.
    text = SEED.read_text(encoding="utf-8")

    # Build new QUESTIONS_DATA section by executing current module pieces.
    import sys

    sys.path.insert(0, str(ROOT))
    from app.services import php_seed_data as seed

    items = []
    for index, item in enumerate(seed.QUESTIONS_DATA, start=1):
        refs = [
            {"url": r["url"], "label": r["label"]}
            for r in REFERENCES[index]
        ]
        items.append(
            {
                "prompt": item["prompt"],
                "explanation": item["explanation"],
                "options": item["options"],
                "references": refs,
            }
        )

    # Preserve header through QUESTIONS_DATA = [
    match = re.search(r"QUESTIONS_DATA: list\[dict\] = \[", text)
    if not match:
        raise SystemExit("QUESTIONS_DATA marker not found")
    header = text[: match.end()]
    footer_match = re.search(
        r"\]\n\n_assigned = \[n for theme in THEME_QUIZZES",
        text,
    )
    if not footer_match:
        raise SystemExit("footer marker not found")
    footer = text[footer_match.start() :]

    lines = [header]
    for item in items:
        lines.append("    {")
        lines.append(f"        \"prompt\": {item['prompt']!r},")
        lines.append(f"        \"explanation\": {item['explanation']!r},")
        lines.append("        \"options\": [")
        for text_opt, ok in item["options"]:
            lines.append(f"            ({text_opt!r}, {ok}),")
        lines.append("        ],")
        lines.append("        \"references\": [")
        for ref in item["references"]:
            lines.append(
                "            {"
                f"\"url\": {ref['url']!r}, \"label\": {ref['label']!r}"
                "},"
            )
        lines.append("        ],")
        lines.append("    },")
    lines.append(footer)
    # footer already starts with ]\n\n_assigned...
    # but we appended footer which starts with ], so the lines currently end with
    # "    }," then footer "]\n\n_assigned..." — need one closing ] only once.
    # Actually header ends with "QUESTIONS_DATA: list[dict] = [" and we add items
    # then footer starts with "]\n\n_assigned" — correct.

    SEED.write_text("\n".join(lines), encoding="utf-8")
    print(f"Updated {SEED} with references for {len(items)} questions")
    total_refs = sum(len(i["references"]) for i in items)
    print(f"Total reference links: {total_refs}")


if __name__ == "__main__":
    main()
