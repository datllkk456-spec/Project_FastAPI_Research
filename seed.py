# task: Nâng cao - Seed dữ liệu
from datetime import datetime, timedelta, timezone
from app.db.database import SessionLocal, Base, engine
from app.models.user import User
from app.models.role import Role
from app.models.research_project import ResearchProject
from app.models.research_task import ResearchTask
from app.models.research_member import ResearchMember
from app.core.security import hash_password


def seed_data():
    db = SessionLocal()
    try:
        if db.query(User).first():
            print("Database đã có dữ liệu. Bỏ qua seed.")
            return

        print("Đang chèn dữ liệu mẫu vào Database...")

        role_user = Role(name="USER", description="Người dùng thường")
        role_admin = Role(name="ADMIN", description="Quản trị viên")
        db.add_all([role_user, role_admin])
        db.commit()
        db.refresh(role_user)
        db.refresh(role_admin)

        user1 = User(
            email="leader@research.com",
            full_name="Nguyễn Văn Leader",
            hashed_password=hash_password("password123"),
            role_id=role_admin.id,
            is_active=True,
        )
        user2 = User(
            email="researcher@research.com",
            full_name="Trần Thị Researcher",
            hashed_password=hash_password("password123"),
            role_id=role_user.id,
            is_active=True,
        )

        db.add_all([user1, user2])
        db.commit()
        db.refresh(user1)
        db.refresh(user2)

        project1 = ResearchProject(
            name="Nghiên cứu AI Y Tế",
            description="Ứng dụng AI vào chẩn đoán bệnh.",
            owner_id=user1.id
        )
        db.add(project1)
        db.commit()
        db.refresh(project1)

        member1 = ResearchMember(project_id=project1.id, user_id=user1.id, role="OWNER")
        member2 = ResearchMember(project_id=project1.id, user_id=user2.id, role="MEMBER")
        db.add_all([member1, member2])
        db.commit()

        task1 = ResearchTask(
            project_id=project1.id,
            title="Thu thập data",
            assignee_id=user2.id,
            status="IN_PROGRESS",
            priority="HIGH",
            due_date=datetime.now(timezone.utc) + timedelta(days=7)
        )
        db.add(task1)
        db.commit()

        print("Seed dữ liệu mẫu thành công!")

    except Exception as e:
        print(f"Lỗi khi seed: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    # task: Database - Khởi tạo bảng
    Base.metadata.create_all(bind=engine)
    seed_data()
