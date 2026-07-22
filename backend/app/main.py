from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import admin, auth, quizzes, sessions
from app.core.config import get_settings
from app.services.bootstrap import init_db
from app.utils.hateoas import link, with_links

settings = get_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    description=(
        "API RESTful de quizzes com HATEOAS. "
        "Modos: practice (resultado no fim), study (explicação por questão) "
        "e flashcard (revisão estilo Anki)."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(quizzes.router, prefix=settings.api_prefix)
app.include_router(sessions.router, prefix=settings.api_prefix)
app.include_router(admin.router, prefix=settings.api_prefix)


@app.get("/", tags=["Root"])
def root() -> dict:
    return with_links(
        {
            "name": settings.app_name,
            "version": "1.0.0",
            "docs": "/docs",
        },
        {
            "self": link("/"),
            "docs": link("/docs"),
            "quizzes": link("/api/quizzes"),
            "login": link("/api/auth/login", "POST"),
            "sessions": link("/api/sessions", "POST"),
            "admin_quizzes": link("/api/admin/quizzes"),
        },
    )


@app.get("/health", tags=["Root"])
def health() -> dict:
    return {"status": "ok"}
