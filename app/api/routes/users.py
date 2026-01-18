from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.api.schemas.user import UserOut, UserUpdate
from app.api.deps.auth import get_current_user
from app.db.deps import get_db
from app.services.user_service import update_user

router = APIRouter(prefix="/users", tags=["users"])


from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.api.schemas.user import UserOut, UserUpdate
from app.db.deps import get_db
from app.services.user_service import update_user
from app.api.deps.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
def me(current_user=Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserOut)
def update_me(
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return update_user(
            db,
            current_user,
            email=str(payload.email) if payload.email else None,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


print("✅ users.py loaded")

print("✅ users router routes:")
for r in router.routes:
    print("   ", r.path, r.methods)