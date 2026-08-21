from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base

class ResearchProject(Base):
    __tablename__ = "research_projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Khóa ngoại: Người sở hữu project
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Quan hệ 1-N: Một User có thể sở hữu nhiều Project
    owner = relationship("User", back_populates="owned_projects")

    # Quan hệ 1-N: Một Project có nhiều Member
    members = relationship("ResearchMember", back_populates="project")

    # Quan hệ 1-N: Một Project có nhiều Task
    tasks = relationship("ResearchTask", back_populates="project")
    
