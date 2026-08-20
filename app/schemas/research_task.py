from pydantic import BaseModel
from datetime import datetime

# Dữ liệu Base
class ResearchTaskBase(BaseModel):
    title: str
    description: str | None = None
    status: str = "TODO"
    priority: str = "MEDIUM"
    due_date: datetime | None = None

# Dữ liệu khi tạo nhiệm vụ
class ResearchTaskCreate(ResearchTaskBase):
    project_id: int
    assignee_id: int | None = None

# Dữ liệu khi cập nhật nhiệm vụ
class ResearchTaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    assignee_id: int | None = None
    status: str | None = None
    priority: str | None = None
    due_date: datetime | None = None

# Dữ liệu trả về cho client
class ResearchTaskResponse(ResearchTaskBase):
    id: int
    project_id: int
    assignee_id: int | None = None
    created_at: datetime

    class Config:
        from_attributes = True