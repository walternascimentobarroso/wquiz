from sqlalchemy import inspect, text
from sqlalchemy.orm import Session, joinedload

from app.core.config import get_settings
from app.core.database import Base, SessionLocal, engine
from app.core.security import hash_password, verify_password
from app.models import (
    Flashcard,
    FlashcardReview,
    Option,
    Question,
    QuestionReference,
    Quiz,
    QuizSession,
    SessionAnswer,
    User,
    UserRole,
)
from app.services.php_seed_data import (
    SAMPLE_QUIZ_CATEGORY,
    SAMPLE_QUIZ_DESCRIPTION,
    SAMPLE_QUIZ_TITLE,
    seeded_questions,
)


def get_quiz_with_questions(db: Session, quiz_id: int) -> Quiz | None:
    return (
        db.query(Quiz)
        .options(joinedload(Quiz.questions).joinedload(Question.options))
        .filter(Quiz.id == quiz_id)
        .first()
    )


def ensure_admin(db: Session) -> None:
    settings = get_settings()
    admin = db.query(User).filter(User.role == UserRole.ADMIN).first()
    if admin:
        changed = False
        if admin.email != settings.admin_email:
            admin.email = settings.admin_email
            changed = True
        if not verify_password(settings.admin_password, admin.hashed_password):
            admin.hashed_password = hash_password(settings.admin_password)
            changed = True
        if changed:
            db.commit()
        return
    db.add(
        User(
            email=settings.admin_email,
            hashed_password=hash_password(settings.admin_password),
            full_name="Administrador",
            role=UserRole.ADMIN,
        )
    )
    db.commit()


def _add_question(db: Session, quiz_id: int, item: dict, position: int) -> None:
    question = Question(
        quiz_id=quiz_id,
        prompt=item["prompt"],
        explanation=item["explanation"],
        theme=item.get("theme", ""),
        position=position,
    )
    db.add(question)
    db.flush()
    for opt_index, (text_opt, is_correct) in enumerate(item["options"]):
        db.add(
            Option(
                question_id=question.id,
                text=text_opt,
                is_correct=is_correct,
                position=opt_index,
            )
        )
    for ref_index, ref in enumerate(item.get("references") or []):
        if isinstance(ref, dict):
            url = str(ref.get("url", "")).strip()
            label = str(ref.get("label", "")).strip()
        else:
            url = str(ref).strip()
            label = ""
        if not url:
            continue
        db.add(
            QuestionReference(
                question_id=question.id,
                url=url,
                label=label,
                position=ref_index,
            )
        )
    correct_texts = [text for text, ok in item["options"] if ok]
    correct = "\n".join(f"• {text}" for text in correct_texts) if correct_texts else ""
    db.add(
        Flashcard(
            question_id=question.id,
            front=item["prompt"],
            back=f"{correct}\n\n{item['explanation']}".strip(),
        )
    )


def reset_quiz_content(db: Session) -> None:
    """Remove quizzes/sessions so seed can be reapplied cleanly."""
    db.query(FlashcardReview).delete()
    db.query(SessionAnswer).delete()
    db.query(QuizSession).delete()
    db.query(Flashcard).delete()
    db.query(QuestionReference).delete()
    db.query(Option).delete()
    db.query(Question).delete()
    db.query(Quiz).delete()
    db.commit()


def seed_sample_quiz(db: Session, *, force: bool = False) -> None:
    """Seed the single Zend PHP quiz with themed questions."""
    admin = db.query(User).filter(User.role == UserRole.ADMIN).first()
    quiz = db.query(Quiz).filter(Quiz.title == SAMPLE_QUIZ_TITLE).first()

    if force or quiz is None:
        if force:
            reset_quiz_content(db)
            quiz = None
        if quiz is None:
            quiz = Quiz(
                title=SAMPLE_QUIZ_TITLE,
                description=SAMPLE_QUIZ_DESCRIPTION,
                category=SAMPLE_QUIZ_CATEGORY,
                is_published=True,
                author_id=admin.id if admin else None,
            )
            db.add(quiz)
            db.flush()

    existing_prompts = {q.prompt for q in quiz.questions}
    next_position = len(quiz.questions)

    for item in seeded_questions():
        if item["prompt"] in existing_prompts:
            continue
        _add_question(db, quiz.id, item, next_position)
        existing_prompts.add(item["prompt"])
        next_position += 1

    quiz.description = SAMPLE_QUIZ_DESCRIPTION
    quiz.category = SAMPLE_QUIZ_CATEGORY
    quiz.is_published = True
    db.commit()


def init_db(*, force_reseed: bool = False) -> None:
    Base.metadata.create_all(bind=engine)
    _ensure_schema_columns()
    db = SessionLocal()
    try:
        ensure_admin(db)
        seed_sample_quiz(db, force=force_reseed)
    finally:
        db.close()


def _ensure_schema_columns() -> None:
    """Add missing columns on existing databases (SQLite or PostgreSQL)."""
    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    def add_column(table: str, column_sql: str) -> None:
        with engine.begin() as conn:
            conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column_sql}"))

    if "quiz_sessions" in table_names:
        columns = {col["name"] for col in inspector.get_columns("quiz_sessions")}
        if "time_limit_minutes" not in columns:
            add_column("quiz_sessions", "time_limit_minutes INTEGER DEFAULT 120")
        if "question_ids" not in columns:
            add_column("quiz_sessions", "question_ids TEXT")

    if "session_answers" in table_names:
        columns = {col["name"] for col in inspector.get_columns("session_answers")}
        if "selected_option_ids" not in columns:
            add_column("session_answers", "selected_option_ids TEXT DEFAULT '[]'")

    if "questions" in table_names:
        columns = {col["name"] for col in inspector.get_columns("questions")}
        if "theme" not in columns:
            add_column("questions", "theme VARCHAR(120) DEFAULT ''")
