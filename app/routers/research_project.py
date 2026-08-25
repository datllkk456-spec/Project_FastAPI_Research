from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.dependencies.dependencies import get_current_user
from app.schemas.research_project import ResearchProjectResponse, ResearchProjectCreate, ResearchProjectUpdate
from app.schemas.research_member import ResearchMemberCreate, ResearchMemberUpdate
from app.services import project_services

router = APIRouter(
    prefix="/research-projects",
    tags=["Research Projects"]
)

# owner tạo dự án 
@router.post("/", response_model=ResearchProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project_data: ResearchProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return project_services.create_project(
        db=db,
        project_data=project_data,
        current_user=current_user
    )

# danh sách dự án
@router.get("/", response_model=list[ResearchProjectResponse])
def get_research_projects(search: str | None = Query(None, description="Tìm kiếm theo tên đề tài"), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return project_services.get_my_projects(
        db=db,
        current_user=current_user,
        search=search
    )

# chi tiết đề tài nghiên cứu 
@router.get("/{project_id}", response_model=ResearchProjectResponse)
def get_research_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return project_services.get_project_detail(
        db=db,
        project_id=project_id,
        current_user=current_user
    )

@router.put("/{project_id}", response_model=ResearchProjectResponse)
def update_research_project(project_id: int, project_data: ResearchProjectUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return project_services.update_project(
        db=db,
        project_id=project_id,
        project_data=project_data,
        current_user=current_user
    )

@router.delete("/{project_id}")
def delete_research_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return project_services.delete_project(
        db=db,
        project_id=project_id,
        current_user=current_user
    )

# owner thêm thành viên cho dự án 
@router.post("/{project_id}/members")
def add_member(project_id: int, member_data: ResearchMemberCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return project_services.add_member(
        db=db,
        project_id=project_id,
        member_data=member_data,
        current_user=current_user
    )

# owner xóa thành viên
@router.delete("/{project_id}/members/{user_id}")
def remove_member(project_id: int, user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return project_services.remove_member(
        db=db,
        project_id=project_id,
        user_id=user_id,
        current_user=current_user
    )