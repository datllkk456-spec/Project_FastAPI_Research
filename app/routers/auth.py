from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import hash_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=UserResponse)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    # Kiểm tra email đã tồn tại
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email đã tồn tại"
        )

    # Hash password
    hashed_password = hash_password(user_data.password)

    # Tạo user
    user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        is_active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user