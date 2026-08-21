from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.db.database import get_db
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

# --- TASK 3: API Lấy danh sách (Có Search/Lọc) ---
@router.get("/", response_model=list[UserResponse])
def get_all_users(
    email_search: str | None = Query(None, description="Tìm kiếm theo email"),
    status_active: bool | None = Query(None, description="Lọc theo trạng thái hoạt động"),
    db: Session = Depends(get_db), 
    current_user: User = Depends(require_admin)
):
    query = db.query(User)
    
    if email_search:
        query = query.filter(User.email.ilike(f"%{email_search}%"))
    if status_active is not None:
        query = query.filter(User.is_active == status_active)
        
    return query.all()