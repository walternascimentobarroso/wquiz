from collections import Counter

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Quiz
from app.schemas import QuizOut, ThemeCount
from app.services.bootstrap import get_quiz_with_questions
from app.services.php_seed_data import THEME_QUIZZES
from app.utils.hateoas import link, with_links

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])

_THEME_ORDER = {theme["title"]: index for index, theme in enumerate(THEME_QUIZZES)}


def _quiz_themes(quiz: Quiz) -> list[ThemeCount]:
    counts = Counter(
        (question.theme or "").strip()
        for question in quiz.questions
        if (question.theme or "").strip()
    )
    ordered = sorted(
        counts.items(),
        key=lambda item: (_THEME_ORDER.get(item[0], 999), item[0]),
    )
    return [ThemeCount(name=name, question_count=count) for name, count in ordered]


def _quiz_summary(quiz: Quiz) -> dict:
    return QuizOut(
        id=quiz.id,
        title=quiz.title,
        description=quiz.description,
        category=quiz.category,
        is_published=quiz.is_published,
        created_at=quiz.created_at,
        question_count=len(quiz.questions),
        themes=_quiz_themes(quiz),
    ).model_dump()


@router.get("", response_model=dict)
def list_quizzes(db: Session = Depends(get_db)) -> dict:
    quizzes = (
        db.query(Quiz)
        .filter(Quiz.is_published.is_(True))
        .order_by(Quiz.id.asc())
        .all()
    )
    items = []
    for quiz in quizzes:
        payload = _quiz_summary(quiz)
        items.append(
            with_links(
                payload,
                {
                    "self": link(f"/api/quizzes/{quiz.id}"),
                    "start_practice": link("/api/sessions", "POST"),
                    "start_study": link("/api/sessions", "POST"),
                    "start_flashcard": link("/api/sessions", "POST"),
                },
            )
        )
    return with_links(
        {"items": items, "count": len(items)},
        {"self": link("/api/quizzes")},
    )


@router.get("/{quiz_id}", response_model=dict)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)) -> dict:
    quiz = get_quiz_with_questions(db, quiz_id)
    if quiz is None or not quiz.is_published:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz não encontrado")

    payload = _quiz_summary(quiz)
    payload["modes"] = ["practice", "study", "flashcard"]
    return with_links(
        payload,
        {
            "self": link(f"/api/quizzes/{quiz.id}"),
            "collection": link("/api/quizzes"),
            "start_session": link("/api/sessions", "POST"),
        },
    )
