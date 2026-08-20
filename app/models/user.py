from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Khóa ngoại: Liên kết tới bảng roles
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)

    # Quan hệ với Role
    role = relationship("Role", back_populates="users")

    # Quan hệ: User sở hữu nhiều ResearchProject
    owned_projects = relationship(
        "ResearchProject",
        back_populates="owner"
    )

    # Quan hệ: User tham gia nhiều ResearchProject
    # thông qua bảng ResearchMember
    memberships = relationship("ResearchMember", back_populates="user")

    # Quan hệ: User có thể được giao nhiều ResearchTask
    assigned_tasks = relationship("ResearchTask", back_populates="assignee")
