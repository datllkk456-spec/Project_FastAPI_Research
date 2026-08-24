from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text 
from app.db.database import Base, engine, get_db
from app.models.user import User
from app.models.role import Role
from app.models.research_project import ResearchProject
from app.models.research_member import ResearchMember
from app.models.research_task import ResearchTask
from app.routers.auth import router
from app.core.exceptions import register_exception_handlers
from app.routers import users, research_project

app = FastAPI(
    title="Research Group Management API"
)

# task: Core - Exception & response (format lỗi thống nhất)
register_exception_handlers(app)

# task: Database - Khởi tạo bảng
Base.metadata.create_all(bind=engine)

app.include_router(router)
app.include_router(users.router)
app.include_router(research_project.router)

@app.get("/")
def root():
    return {"message": "Research Group Management API"}

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": "connected"
        }
    except Exception:
        return {
            "status": "error",
            "database": "disconnected"
        }
