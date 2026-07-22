from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_current_admin
from app.core.database import get_db
from app.models import Flashcard, Option, Question, QuestionReference, Quiz, User
from app.schemas import (
    QuestionCreate,
    QuestionOut,
    QuestionUpdate,
    QuizCreate,
    QuizDetailOut,
    QuizOut,
    QuizUpdate,
    ReferenceCreate,
    ReferenceOut,
)
from app.utils.hateoas import link, with_links

router = APIRouter(prefix="/admin", tags=["Admin"])


def _sync_flashcard(db: Session, question: Question) -> None:
    correct_texts = [o.text for o in question.options if o.is_correct]
    back = "\n".join(f"• {text}" for text in correct_texts)
    if question.explanation:
        back = f"{back}\n\n{question.explanation}" if back else question.explanation
    if question.flashcard:
        question.flashcard.front = question.prompt
        question.flashcard.back = back
    else:
        db.add(Flashcard(question_id=question.id, front=question.prompt, back=back))


def _sync_references(
    db: Session,
    question: Question,
    references: list[ReferenceCreate],
) -> None:
    for ref in list(question.references):
        db.delete(ref)
    db.flush()
    for index, ref in enumerate(references):
        db.add(
            QuestionReference(
                question_id=question.id,
                url=ref.url,
                label=ref.label,
                position=ref.position if ref.position else index,
            )
        )


def _references_out(question: Question) -> list[ReferenceOut]:
    return [
        ReferenceOut(
            id=ref.id,
            url=ref.url,
            label=ref.label or "",
            position=ref.position,
        )
        for ref in sorted(question.references, key=lambda item: item.position)
    ]


def _question_out(question: Question, *, reveal_correct: bool = True) -> dict:
    options = []
    for opt in sorted(question.options, key=lambda o: o.position):
        item = {"id": opt.id, "text": opt.text, "position": opt.position}
        if reveal_correct:
            item["is_correct"] = opt.is_correct
        options.append(item)
    return QuestionOut(
        id=question.id,
        prompt=question.prompt,
        explanation=question.explanation,
        theme=question.theme or "",
        position=question.position,
        options=options,
        references=_references_out(question),
    ).model_dump()


def _load_question(db: Session, question_id: int) -> Question | None:
    return (
        db.query(Question)
        .options(
            joinedload(Question.options),
            joinedload(Question.references),
            joinedload(Question.flashcard),
        )
        .filter(Question.id == question_id)
        .first()
    )


@router.get("/quizzes", response_model=dict)
def admin_list_quizzes(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> dict:
    quizzes = db.query(Quiz).order_by(Quiz.created_at.desc()).all()
    items = []
    for quiz in quizzes:
        payload = QuizOut(
            id=quiz.id,
            title=quiz.title,
            description=quiz.description,
            category=quiz.category,
            is_published=quiz.is_published,
            created_at=quiz.created_at,
            question_count=len(quiz.questions),
        ).model_dump()
        items.append(
            with_links(
                payload,
                {
                    "self": link(f"/api/admin/quizzes/{quiz.id}"),
                    "questions": link(f"/api/admin/quizzes/{quiz.id}/questions"),
                    "update": link(f"/api/admin/quizzes/{quiz.id}", "PUT"),
                    "delete": link(f"/api/admin/quizzes/{quiz.id}", "DELETE"),
                },
            )
        )
    return with_links(
        {"items": items, "count": len(items)},
        {
            "self": link("/api/admin/quizzes"),
            "create": link("/api/admin/quizzes", "POST"),
        },
    )


@router.post("/quizzes", response_model=dict, status_code=status.HTTP_201_CREATED)
def admin_create_quiz(
    body: QuizCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
) -> dict:
    quiz = Quiz(
        title=body.title,
        description=body.description,
        category=body.category,
        is_published=body.is_published,
        author_id=admin.id,
    )
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    payload = QuizOut(
        id=quiz.id,
        title=quiz.title,
        description=quiz.description,
        category=quiz.category,
        is_published=quiz.is_published,
        created_at=quiz.created_at,
        question_count=0,
    ).model_dump()
    return with_links(
        payload,
        {
            "self": link(f"/api/admin/quizzes/{quiz.id}"),
            "questions": link(f"/api/admin/quizzes/{quiz.id}/questions"),
            "collection": link("/api/admin/quizzes"),
        },
    )


@router.get("/quizzes/{quiz_id}", response_model=dict)
def admin_get_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> dict:
    quiz = (
        db.query(Quiz)
        .options(
            joinedload(Quiz.questions).joinedload(Question.options),
            joinedload(Quiz.questions).joinedload(Question.references),
        )
        .filter(Quiz.id == quiz_id)
        .first()
    )
    if quiz is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz não encontrado")

    payload = QuizDetailOut(
        id=quiz.id,
        title=quiz.title,
        description=quiz.description,
        category=quiz.category,
        is_published=quiz.is_published,
        created_at=quiz.created_at,
        question_count=len(quiz.questions),
        questions=[_question_out(q) for q in sorted(quiz.questions, key=lambda x: x.position)],
    ).model_dump()
    return with_links(
        payload,
        {
            "self": link(f"/api/admin/quizzes/{quiz.id}"),
            "update": link(f"/api/admin/quizzes/{quiz.id}", "PUT"),
            "delete": link(f"/api/admin/quizzes/{quiz.id}", "DELETE"),
            "add_question": link(f"/api/admin/quizzes/{quiz.id}/questions", "POST"),
            "collection": link("/api/admin/quizzes"),
        },
    )


@router.put("/quizzes/{quiz_id}", response_model=dict)
def admin_update_quiz(
    quiz_id: int,
    body: QuizUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> dict:
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if quiz is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz não encontrado")

    data = body.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(quiz, key, value)
    db.commit()
    db.refresh(quiz)
    payload = QuizOut(
        id=quiz.id,
        title=quiz.title,
        description=quiz.description,
        category=quiz.category,
        is_published=quiz.is_published,
        created_at=quiz.created_at,
        question_count=len(quiz.questions),
    ).model_dump()
    return with_links(
        payload,
        {
            "self": link(f"/api/admin/quizzes/{quiz.id}"),
            "collection": link("/api/admin/quizzes"),
        },
    )


@router.delete("/quizzes/{quiz_id}", response_model=dict)
def admin_delete_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> dict:
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if quiz is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz não encontrado")
    db.delete(quiz)
    db.commit()
    return with_links(
        {"deleted": True, "id": quiz_id},
        {"collection": link("/api/admin/quizzes")},
    )


@router.post(
    "/quizzes/{quiz_id}/questions",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
)
def admin_add_question(
    quiz_id: int,
    body: QuestionCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> dict:
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if quiz is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz não encontrado")
    if not any(opt.is_correct for opt in body.options):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Informe ao menos uma opção correta",
        )

    question = Question(
        quiz_id=quiz.id,
        prompt=body.prompt,
        explanation=body.explanation,
        theme=body.theme,
        position=body.position if body.position else len(quiz.questions),
    )
    db.add(question)
    db.flush()
    for index, opt in enumerate(body.options):
        db.add(
            Option(
                question_id=question.id,
                text=opt.text,
                is_correct=opt.is_correct,
                position=opt.position if opt.position else index,
            )
        )
    _sync_references(db, question, body.references)
    db.flush()
    question = _load_question(db, question.id)
    if question is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Falha ao carregar questão",
        )
    _sync_flashcard(db, question)
    db.commit()
    question = _load_question(db, question.id)
    if question is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Falha ao carregar questão",
        )

    payload = _question_out(question)
    return with_links(
        payload,
        {
            "self": link(f"/api/admin/questions/{question.id}"),
            "quiz": link(f"/api/admin/quizzes/{quiz_id}"),
            "update": link(f"/api/admin/questions/{question.id}", "PUT"),
            "delete": link(f"/api/admin/questions/{question.id}", "DELETE"),
        },
    )


@router.put("/questions/{question_id}", response_model=dict)
def admin_update_question(
    question_id: int,
    body: QuestionUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> dict:
    question = _load_question(db, question_id)
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Questão não encontrada")

    if body.prompt is not None:
        question.prompt = body.prompt
    if body.explanation is not None:
        question.explanation = body.explanation
    if body.theme is not None:
        question.theme = body.theme
    if body.position is not None:
        question.position = body.position

    if body.options is not None:
        if not any(opt.is_correct for opt in body.options):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Informe ao menos uma opção correta",
            )
        for opt in list(question.options):
            db.delete(opt)
        db.flush()
        for index, opt in enumerate(body.options):
            db.add(
                Option(
                    question_id=question.id,
                    text=opt.text,
                    is_correct=opt.is_correct,
                    position=opt.position if opt.position else index,
                )
            )

    if body.references is not None:
        _sync_references(db, question, body.references)

    db.flush()
    question = _load_question(db, question.id)
    if question is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Falha ao carregar questão",
        )
    _sync_flashcard(db, question)
    db.commit()
    question = _load_question(db, question.id)
    if question is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Falha ao carregar questão",
        )

    return with_links(
        _question_out(question),
        {
            "self": link(f"/api/admin/questions/{question.id}"),
            "quiz": link(f"/api/admin/quizzes/{question.quiz_id}"),
        },
    )


@router.delete("/questions/{question_id}", response_model=dict)
def admin_delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> dict:
    question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Questão não encontrada")
    quiz_id = question.quiz_id
    db.delete(question)
    db.commit()
    return with_links(
        {"deleted": True, "id": question_id},
        {"quiz": link(f"/api/admin/quizzes/{quiz_id}")},
    )
