from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.user import UserResponse
from app.db.database import get_db
from app.services import user_service
from app.dependencies.dependencies import RoleChecker, get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# task: Authorization - Role guard
require_admin = RoleChecker(["ADMIN"])

# task: User - Profile
@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user

# task: User - Danh sách user
@router.get("/", response_model=list[UserResponse])
def get_all_users(
    name_search: str | None = Query(None, description="Tìm kiếm theo họ tên"),
    email_search: str | None = Query(None, description="Tìm kiếm theo email"),
    status_active: bool | None = Query(None, description="Lọc theo trạng thái hoạt động"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return user_service.search_users(
        db,
        name_search=name_search,
        email_search=email_search,
        status_active=status_active,
    )
