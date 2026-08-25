from pydantic import BaseModel
from datetime import datetime

# Dữ liệu Base
class ResearchMemberBase(BaseModel):
    project_id: int
    user_id: int
    role: str

# Dữ liệu khi thêm thành viên
class ResearchMemberCreate(ResearchMemberBase):
    user_id: int

# Dữ liệu khi cập nhật thành viên
class ResearchMemberUpdate(BaseModel):
    role: str | None = None

# Dữ liệu trả về cho client
class ResearchMemberResponse(ResearchMemberBase):
    joined_at: datetime

    class Config:
        from_attributes = True