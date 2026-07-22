from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.models import FlashcardRating, QuizMode
from app.schemas import AnswerSubmit, FlashcardReviewSubmit, SessionCreate
from app.services import sessions as session_service
from app.services.references import references_payload
from app.utils.hateoas import link, with_links

router = APIRouter(prefix="/sessions", tags=["Sessions"])


class FinishRequest(BaseModel):
    force: bool = False


def _session_payload(session) -> dict:
    settings = get_settings()
    limit_minutes = getattr(session, "time_limit_minutes", None) or settings.session_time_limit_minutes
    limit_seconds = limit_minutes * 60
    created = session.created_at
    expires_at = None
    remaining_seconds = limit_seconds
    if created is not None:
        start = created if created.tzinfo else created.replace(tzinfo=UTC)
        expires = start + timedelta(seconds=limit_seconds)
        expires_at = expires.isoformat()
        now = datetime.now(UTC)
        remaining_seconds = max(0, int((expires - now).total_seconds()))

    return {
        "id": session.id,
        "quiz_id": session.quiz_id,
        "mode": session.mode.value,
        "status": session.status.value,
        "current_index": session.current_index,
        "score": session.score,
        "total_questions": session.total_questions,
        "created_at": session.created_at.isoformat() if session.created_at else None,
        "completed_at": session.completed_at.isoformat() if session.completed_at else None,
        "time_limit_minutes": limit_minutes,
        "time_limit_seconds": limit_seconds,
        "expires_at": expires_at,
        "remaining_seconds": remaining_seconds,
    }


def _session_links(session) -> dict:
    links = {
        "self": link(f"/api/sessions/{session.id}"),
        "quiz": link(f"/api/quizzes/{session.quiz_id}"),
    }
    if session.status.value == "in_progress":
        links["current"] = link(f"/api/sessions/{session.id}/current")
        links["previous"] = link(f"/api/sessions/{session.id}/previous", "POST")
        links["next"] = link(f"/api/sessions/{session.id}/next", "POST")
        links["finish"] = link(f"/api/sessions/{session.id}/finish", "POST")
        if session.mode == QuizMode.FLASHCARD:
            links["review"] = link(f"/api/sessions/{session.id}/flashcard-reviews", "POST")
        else:
            links["answer"] = link(f"/api/sessions/{session.id}/answers", "POST")
    if session.status.value == "completed" or session.mode != QuizMode.PRACTICE:
        links["result"] = link(f"/api/sessions/{session.id}/result")
    return links


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
def start_session(body: SessionCreate, db: Session = Depends(get_db)) -> dict:
    mode = QuizMode(body.mode.value)
    session = session_service.create_session(
        db,
        body.quiz_id,
        mode,
        question_count=body.question_count,
        time_limit_minutes=body.time_limit_minutes,
        theme=body.theme,
    )
    return with_links(_session_payload(session), _session_links(session))


@router.get("/{session_id}", response_model=dict)
def get_session(session_id: int, db: Session = Depends(get_db)) -> dict:
    session = session_service.get_session(db, session_id)
    return with_links(_session_payload(session), _session_links(session))


@router.get("/{session_id}/current", response_model=dict)
def current_item(session_id: int, db: Session = Depends(get_db)) -> dict:
    session = session_service.get_session(db, session_id)
    if session.status.value == "completed":
        return with_links(
            {"completed": True, "message": "Sessão finalizada"},
            {
                "self": link(f"/api/sessions/{session.id}/current"),
                "result": link(f"/api/sessions/{session.id}/result"),
                "session": link(f"/api/sessions/{session.id}"),
            },
        )

    remaining = session_service.remaining_questions(db, session)
    answered = session.total_questions - remaining
    nav = {
        "can_go_previous": session.current_index > 0,
        "can_go_next": session.current_index < session.total_questions - 1,
        "answered_count": answered,
        "remaining": remaining,
    }

    if session.mode == QuizMode.FLASHCARD:
        card = session_service.get_current_flashcard(session)
        if card is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sem flashcards")
        payload = {
            "type": "flashcard",
            "index": session.current_index,
            "total": session.total_questions,
            "flashcard": {"id": card.id, "front": card.front},
            **nav,
        }
        return with_links(
            payload,
            {
                "self": link(f"/api/sessions/{session.id}/current"),
                "reveal": link(f"/api/sessions/{session.id}/flashcards/{card.id}"),
                "review": link(f"/api/sessions/{session.id}/flashcard-reviews", "POST"),
                "previous": link(f"/api/sessions/{session.id}/previous", "POST"),
                "finish": link(f"/api/sessions/{session.id}/finish", "POST"),
            },
        )

    question = session_service.get_current_question(session)
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sem questões")

    options = [
        {"id": opt.id, "text": opt.text, "position": opt.position}
        for opt in sorted(question.options, key=lambda o: o.position)
    ]
    existing = session_service.get_answer_for_question(db, session.id, question.id)
    correct_ids = [
        opt.id
        for opt in sorted(question.options, key=lambda o: o.position)
        if opt.is_correct
    ]
    selected_ids = (
        session_service.decode_option_ids(existing) if existing is not None else []
    )
    payload: dict = {
        "type": "question",
        "index": session.current_index,
        "total": session.total_questions,
        "question": {
            "id": question.id,
            "prompt": question.prompt,
            "options": options,
            "is_multi": len(correct_ids) > 1,
            "correct_count": len(correct_ids),
        },
        "selected_option_id": selected_ids[0] if selected_ids else None,
        "selected_option_ids": selected_ids,
        "already_answered": existing is not None,
        **nav,
    }
    if existing and session.mode == QuizMode.STUDY:
        payload["is_correct"] = existing.is_correct
        payload["correct_option_id"] = correct_ids[0] if correct_ids else None
        payload["correct_option_ids"] = correct_ids
        payload["explanation"] = question.explanation
        payload["references"] = references_payload(question)

    return with_links(
        payload,
        {
            "self": link(f"/api/sessions/{session.id}/current"),
            "answer": link(f"/api/sessions/{session.id}/answers", "POST"),
            "previous": link(f"/api/sessions/{session.id}/previous", "POST"),
            "next": link(f"/api/sessions/{session.id}/next", "POST"),
            "finish": link(f"/api/sessions/{session.id}/finish", "POST"),
            "session": link(f"/api/sessions/{session.id}"),
        },
    )


@router.get("/{session_id}/flashcards/{flashcard_id}", response_model=dict)
def reveal_flashcard(
    session_id: int,
    flashcard_id: int,
    db: Session = Depends(get_db),
) -> dict:
    session = session_service.get_session(db, session_id)
    card = session_service.get_current_flashcard(session)
    if card is None or card.id != flashcard_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Flashcard inválido")
    question = card.question
    return with_links(
        {
            "id": card.id,
            "front": card.front,
            "back": card.back,
            "references": references_payload(question),
        },
        {
            "self": link(f"/api/sessions/{session.id}/flashcards/{card.id}"),
            "review": link(f"/api/sessions/{session.id}/flashcard-reviews", "POST"),
            "current": link(f"/api/sessions/{session.id}/current"),
        },
    )


@router.post("/{session_id}/answers", response_model=dict)
def answer_question(
    session_id: int,
    body: AnswerSubmit,
    db: Session = Depends(get_db),
) -> dict:
    session = session_service.get_session(db, session_id)
    result = session_service.submit_answer(
        db,
        session,
        body.question_id,
        body.option_ids or [],
    )
    links = {
        "self": link(f"/api/sessions/{session.id}/answers", "POST"),
        "session": link(f"/api/sessions/{session.id}"),
    }
    if result.get("session_completed"):
        links["result"] = link(f"/api/sessions/{session.id}/result")
    else:
        links["next"] = link(f"/api/sessions/{session.id}/current")
        links["previous"] = link(f"/api/sessions/{session.id}/previous", "POST")
    return with_links(result, links)


@router.post("/{session_id}/previous", response_model=dict)
def previous_item(session_id: int, db: Session = Depends(get_db)) -> dict:
    session = session_service.get_session(db, session_id)
    session = session_service.go_previous(db, session)
    return with_links(
        _session_payload(session),
        {
            **_session_links(session),
            "current": link(f"/api/sessions/{session.id}/current"),
        },
    )


@router.post("/{session_id}/next", response_model=dict)
def next_item(session_id: int, db: Session = Depends(get_db)) -> dict:
    session = session_service.get_session(db, session_id)
    session = session_service.go_next(db, session)
    return with_links(
        _session_payload(session),
        {
            **_session_links(session),
            "current": link(f"/api/sessions/{session.id}/current"),
        },
    )


@router.post("/{session_id}/finish", response_model=dict)
def finish_session(
    session_id: int,
    body: FinishRequest | None = None,
    db: Session = Depends(get_db),
) -> dict:
    session = session_service.get_session(db, session_id)
    force = body.force if body else False
    result = session_service.finish_session(db, session, force=force)
    links = {
        "self": link(f"/api/sessions/{session.id}/finish", "POST"),
        "session": link(f"/api/sessions/{session.id}"),
    }
    if result.get("session_completed"):
        links["result"] = link(f"/api/sessions/{session.id}/result")
    else:
        links["current"] = link(f"/api/sessions/{session.id}/current")
    return with_links(result, links)


@router.post("/{session_id}/flashcard-reviews", response_model=dict)
def review_flashcard(
    session_id: int,
    body: FlashcardReviewSubmit,
    db: Session = Depends(get_db),
) -> dict:
    session = session_service.get_session(db, session_id)
    result = session_service.submit_flashcard_review(
        db,
        session,
        body.flashcard_id,
        FlashcardRating(body.rating.value),
    )
    links = {
        "self": link(f"/api/sessions/{session.id}/flashcard-reviews", "POST"),
        "session": link(f"/api/sessions/{session.id}"),
    }
    if result.get("session_completed"):
        links["result"] = link(f"/api/sessions/{session.id}/result")
    else:
        links["next"] = link(f"/api/sessions/{session.id}/current")
        links["previous"] = link(f"/api/sessions/{session.id}/previous", "POST")
    return with_links(result, links)


@router.get("/{session_id}/result", response_model=dict)
def session_result(session_id: int, db: Session = Depends(get_db)) -> dict:
    session = session_service.get_session(db, session_id)
    result = session_service.build_result(db, session)
    return with_links(
        result,
        {
            "self": link(f"/api/sessions/{session.id}/result"),
            "session": link(f"/api/sessions/{session.id}"),
            "quiz": link(f"/api/quizzes/{session.quiz_id}"),
            "restart": link("/api/sessions", "POST"),
        },
    )
