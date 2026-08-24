from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.user import UserResponse
from app.db.database import get_db
from app.dependencies.dependencies import RoleChecker, get_current_user
from app.models.user import User
from app.services import user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# task: Authorization - Role guard
# tạo một bộ kiểm tra quyền, yêu cầu người gọi endpoint phải có role ADMIN
require_admin = RoleChecker(["ADMIN"])

# task: User - Profile
@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    # return current_user
    return { 
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role_id": current_user.role_id,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at
    }

# task: User - Danh sách user
# Chỉ dành cho role có quyền Quản trị viên (Admin)
@router.get("/", response_model=list[UserResponse])
def get_all_users(
    name_search: str | None = Query(None, description="Tìm kiếm theo họ tên"),
    email_search: str | None = Query(None, description="Tìm kiếm theo email"),
    status_active: bool | None = Query(None, description="Lọc theo trạng thái hoạt động"),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    return user_service.search_users(
        db=db,
        name_search=name_search,
        email_search=email_search,
        status_active=status_active,
    )
