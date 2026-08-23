from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.core.security import hash_password, verify_password, create_access_token
from app.services import user_service

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# task: Authentication - Register
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(
        db=db,
        user_data=user_data
    )

# task: Authentication - Login
@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = user_service.authenticate_user(db=db, user_data=user_data)

    role_name = user.role.name if user.role else None

    access_token = create_access_token(
        data={
            "sub": user.email,
            "id": user.id,
            "role": role_name
        }
    )

    return {
        "message": "Đăng nhập thành công",
        "access_token": access_token,
        "token_type": "bearer",
        "data": {
            "id": user.id,
            "email": user.email,
            "role": role_name,
            "is_active": user.is_active,
            "created_at": user.created_at
        }
    }
