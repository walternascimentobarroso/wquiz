from datetime import UTC, datetime
import json
import random

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.services.references import references_payload
from app.core.config import get_settings
from app.models import (
    Flashcard,
    FlashcardRating,
    FlashcardReview,
    Option,
    Question,
    Quiz,
    QuizMode,
    QuizSession,
    SessionAnswer,
    SessionStatus,
)

RATING_INTERVALS = {
    FlashcardRating.AGAIN: 0,
    FlashcardRating.HARD: 1,
    FlashcardRating.GOOD: 3,
    FlashcardRating.EASY: 7,
}

RATING_EASE_DELTA = {
    FlashcardRating.AGAIN: -0.2,
    FlashcardRating.HARD: -0.15,
    FlashcardRating.GOOD: 0.0,
    FlashcardRating.EASY: 0.15,
}


def _published_quiz_or_404(db: Session, quiz_id: int) -> Quiz:
    quiz = (
        db.query(Quiz)
        .options(joinedload(Quiz.questions).joinedload(Question.options))
        .options(joinedload(Quiz.questions).joinedload(Question.flashcard))
        .options(joinedload(Quiz.questions).joinedload(Question.references))
        .filter(Quiz.id == quiz_id)
        .first()
    )
    if quiz is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz não encontrado")
    if not quiz.is_published:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz não publicado")
    if not quiz.questions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quiz sem questões",
        )
    return quiz


def create_session(
    db: Session,
    quiz_id: int,
    mode: QuizMode,
    *,
    question_count: int | None = None,
    time_limit_minutes: int | None = None,
    theme: str | None = None,
) -> QuizSession:
    quiz = _published_quiz_or_404(db, quiz_id)
    settings = get_settings()
    all_questions = sorted(quiz.questions, key=lambda q: q.position)

    if theme:
        theme_name = theme.strip()
        all_questions = [q for q in all_questions if (q.theme or "").strip() == theme_name]
        if not all_questions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Nenhuma questão no tema '{theme_name}'",
            )

    available = len(all_questions)

    if question_count is None:
        selected = all_questions
    else:
        count = min(max(1, question_count), available)
        selected = random.sample(all_questions, k=count)

    limit_minutes = (
        time_limit_minutes
        if time_limit_minutes is not None
        else settings.session_time_limit_minutes
    )
    if limit_minutes < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tempo limite inválido",
        )

    session = QuizSession(
        quiz_id=quiz.id,
        mode=mode,
        status=SessionStatus.IN_PROGRESS,
        current_index=0,
        score=0,
        total_questions=len(selected),
        time_limit_minutes=limit_minutes,
        question_ids=json.dumps([q.id for q in selected]),
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_session(db: Session, session_id: int) -> QuizSession:
    session = (
        db.query(QuizSession)
        .options(
            joinedload(QuizSession.quiz)
            .joinedload(Quiz.questions)
            .joinedload(Question.options)
        )
        .options(
            joinedload(QuizSession.quiz)
            .joinedload(Quiz.questions)
            .joinedload(Question.flashcard)
        )
        .options(
            joinedload(QuizSession.quiz)
            .joinedload(Quiz.questions)
            .joinedload(Question.references)
        )
        .options(joinedload(QuizSession.answers))
        .filter(QuizSession.id == session_id)
        .first()
    )
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sessão não encontrada")
    return session


def _sorted_questions(session: QuizSession) -> list[Question]:
    by_id = {q.id: q for q in session.quiz.questions}
    if session.question_ids:
        try:
            ids = json.loads(session.question_ids)
        except json.JSONDecodeError:
            ids = []
        ordered = [by_id[qid] for qid in ids if qid in by_id]
        if ordered:
            return ordered
    return sorted(session.quiz.questions, key=lambda q: q.position)


def get_current_question(session: QuizSession) -> Question | None:
    questions = _sorted_questions(session)
    if session.current_index >= len(questions):
        return None
    return questions[session.current_index]


def get_current_flashcard(session: QuizSession) -> Flashcard | None:
    question = get_current_question(session)
    if question is None:
        return None
    return question.flashcard


def _encode_option_ids(option_ids: list[int]) -> str:
    return json.dumps(option_ids)


def _decode_option_ids(answer: SessionAnswer) -> list[int]:
    raw = getattr(answer, "selected_option_ids", None) or ""
    if raw:
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list) and parsed:
                return [int(x) for x in parsed]
        except (json.JSONDecodeError, TypeError, ValueError):
            pass
    if answer.option_id is not None:
        return [answer.option_id]
    return []


def _correct_option_ids(question: Question) -> list[int]:
    return [
        opt.id
        for opt in sorted(question.options, key=lambda o: o.position)
        if opt.is_correct
    ]


def submit_answer(
    db: Session,
    session: QuizSession,
    question_id: int,
    option_ids: list[int],
) -> dict:
    if session.status != SessionStatus.IN_PROGRESS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sessão finalizada")
    if session.mode == QuizMode.FLASHCARD:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Use o endpoint de flashcard neste modo",
        )

    current = get_current_question(session)
    if current is None or current.id != question_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Questão fora de ordem",
        )

    if not option_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Selecione pelo menos uma opção",
        )

    valid_ids = {opt.id for opt in current.options}
    if any(oid not in valid_ids for oid in option_ids):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Opção inválida")

    correct_ids = set(_correct_option_ids(current))
    if not correct_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Questão sem resposta correta configurada",
        )

    selected_ids = list(dict.fromkeys(option_ids))
    if len(correct_ids) > 1 and len(selected_ids) != len(correct_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Selecione exatamente {len(correct_ids)} opções",
        )

    is_correct = set(selected_ids) == correct_ids
    primary_option_id = selected_ids[0]
    encoded = _encode_option_ids(selected_ids)

    already = (
        db.query(SessionAnswer)
        .filter(SessionAnswer.session_id == session.id, SessionAnswer.question_id == question_id)
        .first()
    )
    is_last = session.current_index >= session.total_questions - 1

    if already:
        if already.is_correct and not is_correct:
            session.score = max(0, session.score - 1)
        elif not already.is_correct and is_correct:
            session.score += 1
        already.option_id = primary_option_id
        already.selected_option_ids = encoded
        already.is_correct = is_correct
        advanced = False
    else:
        db.add(
            SessionAnswer(
                session_id=session.id,
                question_id=question_id,
                option_id=primary_option_id,
                selected_option_ids=encoded,
                is_correct=is_correct,
            )
        )
        if is_correct:
            session.score += 1
        if is_last:
            advanced = False
        else:
            session.current_index += 1
            advanced = True

    db.commit()
    db.refresh(session)

    result: dict = {
        "is_correct": is_correct,
        "selected_option_id": primary_option_id,
        "selected_option_ids": selected_ids,
        "session_completed": False,
        "advanced": advanced,
        "is_last": is_last,
        "is_multi": len(correct_ids) > 1,
    }

    if session.mode == QuizMode.STUDY:
        ordered_correct = _correct_option_ids(current)
        result["correct_option_id"] = ordered_correct[0] if ordered_correct else None
        result["correct_option_ids"] = ordered_correct
        result["explanation"] = current.explanation
        result["references"] = references_payload(current)

    return result


def go_previous(db: Session, session: QuizSession) -> QuizSession:
    if session.status != SessionStatus.IN_PROGRESS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sessão finalizada")
    if session.current_index <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já está na primeira questão",
        )
    session.current_index -= 1
    db.commit()
    db.refresh(session)
    return session


def go_next(db: Session, session: QuizSession) -> QuizSession:
    if session.status != SessionStatus.IN_PROGRESS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sessão finalizada")
    if session.current_index >= session.total_questions - 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já está na última questão",
        )

    current = get_current_question(session)
    if current is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sem questão atual")

    if session.mode == QuizMode.FLASHCARD:
        if current.flashcard is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Flashcard não encontrado",
            )
        reviewed = (
            db.query(FlashcardReview)
            .filter(
                FlashcardReview.session_id == session.id,
                FlashcardReview.flashcard_id == current.flashcard.id,
            )
            .first()
        )
        if reviewed is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Avalie o flashcard antes de avançar",
            )
    else:
        answered = (
            db.query(SessionAnswer)
            .filter(
                SessionAnswer.session_id == session.id,
                SessionAnswer.question_id == current.id,
            )
            .first()
        )
        if answered is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Responda a questão antes de avançar",
            )

    session.current_index += 1
    db.commit()
    db.refresh(session)
    return session


def _answered_count(db: Session, session: QuizSession) -> int:
    if session.mode == QuizMode.FLASHCARD:
        return (
            db.query(FlashcardReview)
            .filter(FlashcardReview.session_id == session.id)
            .count()
        )
    return (
        db.query(SessionAnswer)
        .filter(SessionAnswer.session_id == session.id)
        .count()
    )


def remaining_questions(db: Session, session: QuizSession) -> int:
    return max(0, session.total_questions - _answered_count(db, session))


def finish_session(db: Session, session: QuizSession, *, force: bool = False) -> dict:
    if session.status == SessionStatus.COMPLETED:
        return {
            "session_completed": True,
            "remaining": 0,
            "needs_confirmation": False,
        }

    remaining = remaining_questions(db, session)
    if remaining > 0 and not force:
        return {
            "session_completed": False,
            "needs_confirmation": True,
            "remaining": remaining,
            "answered": session.total_questions - remaining,
            "total_questions": session.total_questions,
        }

    session.status = SessionStatus.COMPLETED
    session.completed_at = datetime.now(UTC)
    db.commit()
    db.refresh(session)
    return {
        "session_completed": True,
        "needs_confirmation": False,
        "remaining": remaining,
        "answered": session.total_questions - remaining,
        "total_questions": session.total_questions,
    }


def decode_option_ids(answer: SessionAnswer) -> list[int]:
    return _decode_option_ids(answer)


def get_answer_for_question(db: Session, session_id: int, question_id: int) -> SessionAnswer | None:
    return (
        db.query(SessionAnswer)
        .filter(
            SessionAnswer.session_id == session_id,
            SessionAnswer.question_id == question_id,
        )
        .first()
    )


def submit_flashcard_review(
    db: Session,
    session: QuizSession,
    flashcard_id: int,
    rating: FlashcardRating,
) -> dict:
    if session.status != SessionStatus.IN_PROGRESS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sessão finalizada")
    if session.mode != QuizMode.FLASHCARD:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sessão não é de flashcard",
        )

    current_card = get_current_flashcard(session)
    if current_card is None or current_card.id != flashcard_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Flashcard fora de ordem",
        )

    ease = max(1.3, 2.5 + RATING_EASE_DELTA[rating])
    interval = RATING_INTERVALS[rating]
    already = (
        db.query(FlashcardReview)
        .filter(
            FlashcardReview.session_id == session.id,
            FlashcardReview.flashcard_id == flashcard_id,
        )
        .first()
    )

    positive = rating in {FlashcardRating.GOOD, FlashcardRating.EASY}
    is_last = session.current_index >= session.total_questions - 1

    if already:
        was_positive = already.rating in {FlashcardRating.GOOD, FlashcardRating.EASY}
        if was_positive and not positive:
            session.score = max(0, session.score - 1)
        elif not was_positive and positive:
            session.score += 1
        already.rating = rating
        already.ease_factor = ease
        already.interval_days = interval
        advanced = False
    else:
        db.add(
            FlashcardReview(
                session_id=session.id,
                flashcard_id=flashcard_id,
                rating=rating,
                ease_factor=ease,
                interval_days=interval,
            )
        )
        if positive:
            session.score += 1
        if is_last:
            advanced = False
        else:
            session.current_index += 1
            advanced = True

    db.commit()
    db.refresh(session)
    return {
        "rating": rating.value,
        "ease_factor": ease,
        "interval_days": interval,
        "session_completed": False,
        "advanced": advanced,
        "is_last": is_last,
    }


def build_result(db: Session, session: QuizSession) -> dict:
    if session.status != SessionStatus.COMPLETED and session.mode == QuizMode.PRACTICE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resultado disponível apenas ao final do teste",
        )

    answers_out = []
    for answer in session.answers:
        question = db.query(Question).filter(Question.id == answer.question_id).first()
        correct_ids = (
            _correct_option_ids(question) if question is not None else []
        )
        selected_ids = _decode_option_ids(answer)
        answers_out.append(
            {
                "question_id": answer.question_id,
                "prompt": question.prompt if question else "",
                "selected_option_id": selected_ids[0] if selected_ids else answer.option_id,
                "selected_option_ids": selected_ids,
                "correct_option_id": correct_ids[0] if correct_ids else None,
                "correct_option_ids": correct_ids,
                "is_correct": answer.is_correct,
                "is_multi": len(correct_ids) > 1,
                "explanation": question.explanation if question else "",
                "references": references_payload(question),
            }
        )

    percentage = (session.score / session.total_questions * 100) if session.total_questions else 0.0
    duration_seconds = 0
    if session.created_at:
        end = session.completed_at or datetime.now(UTC)
        start = session.created_at
        if start.tzinfo is None:
            start = start.replace(tzinfo=UTC)
        if end.tzinfo is None:
            end = end.replace(tzinfo=UTC)
        duration_seconds = max(0, int((end - start).total_seconds()))

    return {
        "session_id": session.id,
        "quiz_id": session.quiz_id,
        "mode": session.mode.value,
        "score": session.score,
        "total_questions": session.total_questions,
        "percentage": round(percentage, 2),
        "duration_seconds": duration_seconds,
        "answers": answers_out,
    }
