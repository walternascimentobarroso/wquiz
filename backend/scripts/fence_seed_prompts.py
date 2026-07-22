#!/usr/bin/env python3
"""Wrap code regions in seed prompts with Markdown fences."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "app" / "services" / "php_seed_data.py"

sys.path.insert(0, str(ROOT))

CODE_START = re.compile(
    r"^(<\?php|<\?xml|<!DOCTYPE|"
    r"<input\b|<form\b|<select\b|<option\b|<document\b|<root\b|<section\b|"
    r"namespace\s|class\s|function\s|enum\s|\$[A-Za-z_]|declare\s*\(|"
    r"//|/\*|public\s|private\s|protected\s|parent::|try\s*\{|catch\s*\(|"
    r"move_uploaded_file\s*\(|echo\s|print(?:f|_r)?\s*\(|include\s|require\s|"
    r"return\s|new\s|unset\s*\(|var_dump\s*\(|\$dsn\b|\$str\b|\$a\b|\$xml\b|"
    r"\$array\b|\$matches\b|\$rnd\b|\$text\b|\$pdo\b|\$cmd\b|\$handle\b|"
    r"\$string\b)",
    re.I,
)

TABLE_HINT = re.compile(
    r"^(id\s+name|-{3,}|\d+\s+[a-z]+\s+\S+@)",
    re.I,
)


def detect_lang(block: str) -> str:
    s = block.lstrip()
    if s.startswith("<?xml") or s.startswith("<document") or s.startswith("<root"):
        return "xml"
    if s.startswith("<"):
        return "html"
    if TABLE_HINT.match(s.split("\n", 1)[0].strip()):
        return "text"
    return "php"


def is_code_paragraph(paragraph: str) -> bool:
    lines = [line for line in paragraph.split("\n") if line.strip()]
    if not lines:
        return False
    first = lines[0].strip()
    if TABLE_HINT.match(first):
        return True
    if len(lines) > 1 and re.match(r"^-{3,}$", lines[1].strip()):
        return True
    if CODE_START.match(first):
        return True
    hits = sum(1 for line in lines if CODE_START.match(line.strip()))
    return hits >= 2


def fence_prompt(prompt: str) -> str:
    if "```" in prompt:
        return prompt

    # Keep leading [Qn] with the first text block
    parts = re.split(r"\n\s*\n", prompt.strip())
    if len(parts) == 1:
        # Single block: maybe "intro\n\ncode" without double newline variants
        return prompt if not is_code_paragraph(parts[0]) else (
            f"```{detect_lang(parts[0])}\n{parts[0].strip()}\n```"
        )

    out: list[str] = []
    for part in parts:
        chunk = part.strip("\n")
        if not chunk.strip():
            continue
        if is_code_paragraph(chunk):
            lang = detect_lang(chunk)
            out.append(f"```{lang}\n{chunk.strip()}\n```")
        else:
            out.append(chunk.strip())
    return "\n\n".join(out)


def main() -> None:
    from app.services import php_seed_data as seed

    text = SEED.read_text(encoding="utf-8")
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

    items = []
    changed = 0
    for index, item in enumerate(seed.QUESTIONS_DATA, start=1):
        original = item["prompt"]
        fenced = fence_prompt(original)
        if fenced != original:
            changed += 1
            print(f"Q{index}: fenced")
        items.append(
            {
                "prompt": fenced,
                "explanation": item["explanation"],
                "options": item["options"],
                "references": item.get("references") or [],
            }
        )

    lines = [header]
    for item in items:
        lines.append("    {")
        lines.append(f"        \"prompt\": {item['prompt']!r},")
        lines.append(f"        \"explanation\": {item['explanation']!r},")
        lines.append("        \"options\": [")
        for text_opt, ok in item["options"]:
            lines.append(f"            ({text_opt!r}, {ok}),")
        lines.append("        ],")
        if item["references"]:
            lines.append('        "references": [')
            for ref in item["references"]:
                lines.append(
                    "            {"
                    f"\"url\": {ref['url']!r}, \"label\": {ref['label']!r}"
                    "},"
                )
            lines.append("        ],")
        lines.append("    },")
    lines.append(footer)
    SEED.write_text("\n".join(lines), encoding="utf-8")
    print(f"Updated {changed}/{len(items)} prompts with fences")


if __name__ == "__main__":
    main()
