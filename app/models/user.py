from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Khóa ngoại: Liên kết tới bảng roles
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)

    # 1-N: User có 1 role
    role = relationship("Role", back_populates="users")

    # 1-N: User sở hữu nhiều ResearchProject
    owned_projects = relationship("ResearchProject", back_populates="owner")

    # 1-N: User tham gia nhiều ResearchProject
    memberships = relationship("ResearchMember", back_populates="user")

    # 1-N: User có thể được giao nhiều ResearchTask
    assigned_tasks = relationship("ResearchTask", back_populates="assignee")
