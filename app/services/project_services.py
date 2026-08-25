from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.research_project import ResearchProjectCreate, ResearchProjectUpdate
from app.schemas.research_member import ResearchMemberCreate, ResearchMemberUpdate
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


# Owner mới được phép sửa dự án. Member chỉ được xem, không được sửa.
def update_project(db: Session, project_id: int, project_data: ResearchProjectUpdate, current_user: User):
    project = (
        db.query(ResearchProject)
        .join(
            ResearchMember,
            ResearchMember.project_id == ResearchProject.id
        )
        .filter(
            ResearchProject.id == project_id,
            ResearchMember.user_id == current_user.id,
            ResearchMember.role == "OWNER"
        )
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=403,
            detail="Chỉ OWNER mới được sửa đề tài"
        )

    if project_data.name is not None:
        project.name = project_data.name

    if project_data.description is not None:
        project.description = project_data.description

    db.commit()
    db.refresh(project)

    return project


# Owner mới được phép xóa đề tài. Member chỉ được xem, không được xóa.
def delete_project(db: Session, project_id: int, current_user: User):
    project = (
        db.query(ResearchProject)
        .join(
            ResearchMember,
            ResearchMember.project_id == ResearchProject.id
        )
        .filter(
            ResearchProject.id == project_id,
            ResearchMember.user_id == current_user.id,
            ResearchMember.role == "OWNER"
        )
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=403,
            detail="Chỉ OWNER mới được xóa đề tài"
        )

    db.delete(project)
    db.commit()

    return {
        "message": "Xóa đề tài thành công"
    }


def add_member(db: Session, project_id: int, member_data: ResearchMemberCreate, current_user: User):
    # Kiểm tra người đang thực hiện có phải OWNER không
    owner = (
        db.query(ResearchMember)
        .filter(
            ResearchMember.project_id == project_id,
            ResearchMember.user_id == current_user.id,
            ResearchMember.role == "OWNER"
        )
        .first()
    )

    if not owner:
        raise HTTPException(
            status_code=403,
            detail="Chỉ OWNER mới được thêm thành viên"
        )

    # Kiểm tra user cần thêm có tồn tại không
    user = (
        db.query(User)
        .filter(User.id == member_data.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User không tồn tại"
        )

    # Kiểm tra user đã có trong project chưa
    existing_member = (
        db.query(ResearchMember)
        .filter(
            ResearchMember.project_id == project_id,
            ResearchMember.user_id == member_data.user_id
        )
        .first()
    )

    if existing_member:
        raise HTTPException(
            status_code=400,
            detail="User đã là thành viên của đề tài"
        )

    # Thêm member
    new_member = ResearchMember(
        project_id=project_id,
        user_id=member_data.user_id,
        role="MEMBER"
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return new_member


def remove_member(
    db: Session,
    project_id: int,
    user_id: int,
    current_user: User
):
    # Kiểm tra người thực hiện có phải OWNER không
    owner = (
        db.query(ResearchMember)
        .filter(
            ResearchMember.project_id == project_id,
            ResearchMember.user_id == current_user.id,
            ResearchMember.role == "OWNER"
        )
        .first()
    )

    if not owner:
        raise HTTPException(
            status_code=403,
            detail="Chỉ OWNER mới được xóa thành viên"
        )

    # Tìm member cần xóa
    member = (
        db.query(ResearchMember)
        .filter(
            ResearchMember.project_id == project_id,
            ResearchMember.user_id == user_id
        )
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="User không phải thành viên của đề tài"
        )

    # Không cho xóa OWNER
    if member.role == "OWNER":
        raise HTTPException(
            status_code=400,
            detail="Không thể xóa OWNER"
        )

    # Xóa member
    db.delete(member)
    db.commit()

    return {
        "message": "Xóa thành viên thành công"
    }