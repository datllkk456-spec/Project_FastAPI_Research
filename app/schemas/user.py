from pydantic import BaseModel
from datetime import datetime

# Base
class UserBase(BaseModel):
    email: str

# Create
class UserCreate(UserBase):
    password: str

# Update
class UserUpdate(BaseModel):
    email: str | None = None
    is_active: bool | None = None

# Response
class UserResponse(UserBase):
    id: int
    role_id: int | None = None
    is_active: bool
    created_at: datetime

    class Config:
            # Pydantic V2 cấu hình từ form_attributes (ở V1 là orm_mode = True)
            # Giúp Pydantic có thể đọc dữ liệu trực tiếp từ SQLAlchemy Model object
            from_attributes = True