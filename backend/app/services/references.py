"""Helpers for serializing question references."""

from __future__ import annotations

from app.models import Question


def references_payload(question: Question | None) -> list[dict]:
    if question is None:
        return []
    return [
        {
            "id": ref.id,
            "url": ref.url,
            "label": ref.label or "",
            "position": ref.position,
        }
        for ref in sorted(question.references, key=lambda item: item.position)
    ]
