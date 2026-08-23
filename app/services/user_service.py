from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserCreate, UserLogin
from app.core.security import hash_password, verify_password

# Nghiệp vụ register(router/auth.py)
def create_user(db: Session, user_data: UserCreate) -> User:
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email đã tồn tại"
        )
    
    # Lấy role USER mặc định
    default_role = (db.query(Role).filter(Role.name == "USER").first())
    if default_role is None:
        raise HTTPException(
            status_code=500,
            detail="Role USER chưa được cấu hình"
        )

    hashed_password = hash_password(user_data.password)
    # Tạo user
    new_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        role_id=default_role.id,
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# Nghiệp vụ Login(router/auth.py)
def authenticate_user(db: Session, user_data: UserLogin) -> User:

    # Tìm user theo email
    user = (db.query(User).filter(User.email == user_data.email).first())

    # Kiểm tra email + password
    if user is None or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Email hoặc mật khẩu không đúng"
        )

    # Ktra tài khoản có hoạt động ko
    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Tài khoản không hoạt động"
        )
    return user

# task 7 buổi 2: GET /users: chỉ Admin; có search theo tên/email và trạng thái.
def search_users(db: Session, name_search: str | None = None, email_search: str | None = None, status_active: bool | None = None) -> list[User]:
    query = db.query(User)

    if name_search:
        query = query.filter(User.full_name.ilike(f"%{name_search}%"))
    if email_search:
        query = query.filter(User.email.ilike(f"%{email_search}%"))
    if status_active is not None:
        query = query.filter(User.is_active == status_active)

    return query.all()
