from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.security import create_access_token, verify_password
from app.models import User
from app.schemas import LoginRequest, TokenResponse, UserOut
from app.utils.hateoas import link, with_links

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=dict)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> dict:
    user = db.query(User).filter(User.email == form_data.username).first()
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos",
        )
    token = create_access_token(user.email, extra={"role": user.role.value})
    payload = TokenResponse(access_token=token).model_dump()
    return with_links(
        payload,
        {
            "self": link("/api/auth/login", "POST"),
            "me": link("/api/auth/me"),
            "quizzes": link("/api/quizzes"),
        },
    )


@router.post("/token", response_model=dict, include_in_schema=False)
def login_json(body: LoginRequest, db: Session = Depends(get_db)) -> dict:
    user = db.query(User).filter(User.email == body.email).first()
    if user is None or not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos",
        )
    token = create_access_token(user.email, extra={"role": user.role.value})
    payload = TokenResponse(access_token=token).model_dump()
    return with_links(
        payload,
        {
            "self": link("/api/auth/token", "POST"),
            "me": link("/api/auth/me"),
        },
    )


@router.get("/me", response_model=dict)
def me(user: User = Depends(get_current_user)) -> dict:
    payload = UserOut(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role.value,
    ).model_dump()
    return with_links(
        payload,
        {
            "self": link("/api/auth/me"),
            "admin_quizzes": link("/api/admin/quizzes"),
        },
    )
