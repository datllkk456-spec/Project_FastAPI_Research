from datetime import datetime, timedelta, timezone
from app.db.database import SessionLocal, Base, engine
from app.models.user import User
from app.models.role import Role
from app.models.research_project import ResearchProject
from app.models.research_task import ResearchTask
from app.models.research_member import ResearchMember

def seed_data():
    db = SessionLocal()
    try:
        # Nếu bảng User đã có data rồi thì bỏ qua không tạo nữa
        if db.query(User).first():
            print("Database đã có dữ liệu. Bỏ qua seed.")
            return

        print("Đang chèn dữ liệu mẫu vào Database...")
        
        # 1. Tạo User mẫu
        user1 = User(email="leader@research.com", hashed_password="fake_hash_1", is_active=True)
        user2 = User(email="researcher@research.com", hashed_password="fake_hash_2", is_active=True)
        
        db.add_all([user1, user2])
        db.commit() 

        # 2. Tạo Đề tài nghiên cứu (Project) mẫu
        project1 = ResearchProject(
            name="Nghiên cứu AI Y Tế", 
            description="Ứng dụng AI vào chẩn đoán bệnh.",
            owner_id=user1.id
        )
        db.add(project1)
        db.commit()

        # 3. Thêm Thành viên (Members)
        member1 = ResearchMember(project_id=project1.id, user_id=user1.id, role="LEADER")
        member2 = ResearchMember(project_id=project1.id, user_id=user2.id, role="RESEARCHER")
        db.add_all([member1, member2])
        db.commit()

        # 4. Tạo Nhiệm vụ (Tasks) mẫu
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
    # Đảm bảo các bảng đã được khởi tạo
    Base.metadata.create_all(bind=engine)
    seed_data()