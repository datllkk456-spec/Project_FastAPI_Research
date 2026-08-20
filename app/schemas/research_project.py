from pydantic import BaseModel
from datetime import datetime

# Dữ liệu Base
class ResearchProjectBase(BaseModel):
    name: str
    description: str | None = None

# Dữ liệu khi tạo đề tài
class ResearchProjectCreate(ResearchProjectBase):
    pass

# Dữ liệu khi cập nhật đề tài
class ResearchProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

# Dữ liệu trả về cho client
class ResearchProjectResponse(ResearchProjectBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True