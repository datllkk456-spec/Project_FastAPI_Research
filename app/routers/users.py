from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.db.database import get_db
from app.services import user_service
from app.core.security import create_access_token
from app.dependencies.dependencies import RoleChecker, get_current_user
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

# KHAI BÁO CÁC CHỐT CHẶN BẢO VỆ
# Chốt chặn chỉ cho phép ADMIN
require_admin = RoleChecker(["ADMIN"])

# API lấy profile
@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user
