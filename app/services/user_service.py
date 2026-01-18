from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user import User
from app.core.security import verify_password, hash_password


def create_user(db: Session, email: str, password: str) -> User:
    existing = db.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()

    if existing:
        raise ValueError("Email already registered")

    user = User(
        email=email,
        hashed_password=hash_password(password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.execute(select(User).where(User.email == email)).scalar_one_or_none()


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()

def update_user(db: Session, user: User, *, email: str | None = None) -> User:
    if email is not None:
        existing = get_user_by_email(db, email)
        if existing and existing.id != user.id:
            raise ValueError("Email already registered")

        user.email = email

    db.add(user)
    db.commit()
    db.refresh(user)
    return user