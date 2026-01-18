from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.schemas.user import UserCreate, UserOut
from app.api.schemas.auth import TokenResponse
from app.core.jwt import create_access_token
from app.db.deps import get_db
from app.services.user_service import authenticate_user, create_user

from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

expires_seconds = settings.access_token_expire_minutes * 60

@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_user(
            db,
            email=str(payload.email),
            password=payload.password,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # Swagger sends form fields: username + password
    # We treat "username" as the user's email
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(subject=user.id)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=expires_seconds,
    )
