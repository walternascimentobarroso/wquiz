from typing import Any


def link(href: str, method: str = "GET", rel: str | None = None) -> dict[str, str]:
    item = {"href": href, "method": method}
    if rel:
        item["rel"] = rel
    return item


def with_links(payload: dict[str, Any], links: dict[str, dict[str, str]]) -> dict[str, Any]:
    return {**payload, "_links": links}
