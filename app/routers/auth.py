from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import hash_password
from app.schemas.user import UserLogin
from app.core.security import verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Kiểm tra email đã tồn tại
    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email đã tồn tại"
        )

    # Hash password
    hashed_password = hash_password(user_data.password)

    # Tạo user
    user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        is_active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    # Tìm user theo email
    user = db.query(User).filter(User.email == user_data.email).first()

    # Kiểm tra user và mật khẩu
    if user is None or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Email hoặc mật khẩu không đúng"
        )

    # Kiểm tra tài khoản có đang hoạt động không
    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Tài khoản không hoạt động"
        )

    # Lấy tên role từ object relationship (user.role là object Role, user.role.name là chuỗi)
    role_name = user.role.name if user.role else None

    # Tạo JWT Access Token, nhét role_name vào payload để dùng cho Authorization
    access_token = create_access_token(data={"sub": user.email, "id": user.id, "role": role_name})

    return {
        "message": "Đăng nhập thành công",
        "access_token": access_token,
        "token_type": "bearer",
        "data": {
            "id": user.id,
            "email": user.email,
            "role": role_name,
            "is_active": user.is_active,
            "created_at": user.created_at
        }
    }