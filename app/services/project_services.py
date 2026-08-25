from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.research_project import ResearchProjectCreate
from app.models.user import User
from app.models.research_project import ResearchProject
from app.models.research_member import ResearchMember

# logic nghiệp vụ của ResearchProject
def create_project(db: Session, project_data: ResearchProjectCreate, current_user: User):
    # tạo project
    project = ResearchProject(
        name=project_data.name,
        description=project_data.description,
        owner_id=current_user.id
    )

    db.add(project)
    db.flush()

    membership = ResearchMember(
        project_id=project.id,
        user_id=current_user.id,
        role="OWNER"
    )

    db.add(membership)
    db.commit()
    db.refresh(project)

    return project

def get_my_projects(db: Session, current_user: User, search: str | None = None):
    query = (db.query(ResearchProject).join(ResearchMember, ResearchMember.project_id == ResearchProject.id).filter(ResearchMember.user_id == current_user.id))

    if search:
        query = query.filter(ResearchProject.name.ilike(f"%{search}%"))

    return query.all()

# Chi tiết đề tài nghiên cứu
def get_project_detail(db: Session, project_id: int, current_user: User):
    project = (
        db.query(ResearchProject).join(
            ResearchMember,
            ResearchMember.project_id == ResearchProject.id
        ).filter(
            ResearchProject.id == project_id,
            ResearchMember.user_id == current_user.id
        ).first()
    )

    if not project:
        raise HTTPException(
            status_code=403,
            detail="Bạn không phải thành viên của dự án này"
        )

    return project