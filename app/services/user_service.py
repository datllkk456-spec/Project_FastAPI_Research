from sqlalchemy.orm import Session
from app.models.user import User

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
