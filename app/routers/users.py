from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.db.database import get_db
from app.services import user_service
from app.core.security import create_access_token

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

