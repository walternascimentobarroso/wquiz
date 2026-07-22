from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

MAX_REFERENCES = 5


class QuizModeSchema(str, Enum):
    PRACTICE = "practice"
    STUDY = "study"
    FLASHCARD = "flashcard"


class FlashcardRatingSchema(str, Enum):
    AGAIN = "again"
    HARD = "hard"
    GOOD = "good"
    EASY = "easy"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    full_name: str
    role: str


class OptionCreate(BaseModel):
    text: str = Field(min_length=1)
    is_correct: bool = False
    position: int = 0


class OptionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str
    position: int
    is_correct: bool | None = None


class ReferenceCreate(BaseModel):
    url: str = Field(min_length=1, max_length=500)
    label: str = Field(default="", max_length=120)
    position: int = 0

    @field_validator("url")
    @classmethod
    def validate_http_url(cls, value: str) -> str:
        cleaned = value.strip()
        if not (cleaned.startswith("http://") or cleaned.startswith("https://")):
            raise ValueError("URL must start with http:// or https://")
        return cleaned

    @field_validator("label")
    @classmethod
    def strip_label(cls, value: str) -> str:
        return value.strip()


class ReferenceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    label: str = ""
    position: int


def _normalize_references(
    refs: list[ReferenceCreate] | None,
) -> list[ReferenceCreate] | None:
    if refs is None:
        return None
    if len(refs) > MAX_REFERENCES:
        raise ValueError(f"At most {MAX_REFERENCES} references are allowed")
    seen: set[str] = set()
    normalized: list[ReferenceCreate] = []
    for index, ref in enumerate(refs):
        key = ref.url.rstrip("/").lower()
        if key in seen:
            continue
        seen.add(key)
        normalized.append(
            ReferenceCreate(url=ref.url, label=ref.label, position=ref.position or index)
        )
    return normalized


class QuestionCreate(BaseModel):
    prompt: str = Field(min_length=1)
    explanation: str = ""
    theme: str = ""
    position: int = 0
    options: list[OptionCreate] = Field(min_length=2)
    references: list[ReferenceCreate] = Field(default_factory=list, max_length=MAX_REFERENCES)

    @field_validator("references")
    @classmethod
    def dedupe_references(cls, value: list[ReferenceCreate]) -> list[ReferenceCreate]:
        return _normalize_references(value) or []


class QuestionUpdate(BaseModel):
    prompt: str | None = None
    explanation: str | None = None
    theme: str | None = None
    position: int | None = None
    options: list[OptionCreate] | None = None
    references: list[ReferenceCreate] | None = None

    @field_validator("references")
    @classmethod
    def dedupe_references(
        cls, value: list[ReferenceCreate] | None
    ) -> list[ReferenceCreate] | None:
        return _normalize_references(value)


class QuestionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    prompt: str
    explanation: str | None = None
    theme: str = ""
    position: int
    options: list[OptionOut]
    references: list[ReferenceOut] = []


class ThemeCount(BaseModel):
    name: str
    question_count: int


class QuizCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = ""
    category: str = "Geral"
    is_published: bool = False


class QuizUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    category: str | None = None
    is_published: bool | None = None


class QuizOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    category: str
    is_published: bool
    created_at: datetime
    question_count: int = 0
    themes: list[ThemeCount] = []


class QuizDetailOut(QuizOut):
    questions: list[QuestionOut] = []


class SessionCreate(BaseModel):
    quiz_id: int
    mode: QuizModeSchema
    question_count: int | None = Field(default=None, ge=1)
    time_limit_minutes: int | None = Field(default=None, ge=1, le=600)
    theme: str | None = Field(default=None, min_length=1, max_length=120)


class AnswerSubmit(BaseModel):
    question_id: int
    option_id: int | None = None
    option_ids: list[int] | None = None

    @model_validator(mode="after")
    def normalize_option_ids(self) -> "AnswerSubmit":
        ids = list(self.option_ids or [])
        if not ids and self.option_id is not None:
            ids = [self.option_id]
        # unique preserve order
        seen: set[int] = set()
        normalized: list[int] = []
        for oid in ids:
            if oid not in seen:
                seen.add(oid)
                normalized.append(oid)
        if not normalized:
            raise ValueError("Informe option_ids ou option_id")
        self.option_ids = normalized
        self.option_id = normalized[0]
        return self


class FlashcardReviewSubmit(BaseModel):
    flashcard_id: int
    rating: FlashcardRatingSchema


class FlashcardOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    front: str
    back: str | None = None


class SessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    quiz_id: int
    mode: QuizModeSchema
    status: str
    current_index: int
    score: int
    total_questions: int


class AnswerResultOut(BaseModel):
    is_correct: bool
    correct_option_id: int | None = None
    correct_option_ids: list[int] = []
    explanation: str | None = None
    references: list[ReferenceOut] = []
    selected_option_id: int | None = None
    selected_option_ids: list[int] = []


class SessionResultOut(BaseModel):
    session_id: int
    quiz_id: int
    mode: QuizModeSchema
    score: int
    total_questions: int
    percentage: float
    answers: list[dict]
