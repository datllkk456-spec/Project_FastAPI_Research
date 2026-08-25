from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.dependencies.dependencies import get_current_user
from app.schemas.research_project import ResearchProjectResponse, ResearchProjectCreate
from app.services import project_services

router = APIRouter(
    prefix="/research-projects",
    tags=["Research Projects"]
)

@router.post("/", response_model=ResearchProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project_data: ResearchProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return project_services.create_project(
        db=db,
        project_data=project_data,
        current_user=current_user
    )

@router.get("/", response_model=list[ResearchProjectResponse])
def get_research_projects(search: str | None = Query(None, description="Tìm kiếm theo tên đề tài"), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return project_services.get_my_projects(
        db=db,
        current_user=current_user,
        search=search
    )

@router.get(
    "/{project_id}",
    response_model=ResearchProjectResponse
)
def get_research_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return project_services.get_project_detail(
        db=db,
        project_id=project_id,
        current_user=current_user
    )