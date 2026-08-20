from fastapi import FastAPI
from fastapi import FastAPI
from app.db.database import Base, engine
from app.models.user import User
from app.models.role import Role
from app.models.research_project import ResearchProject
from app.models.research_member import ResearchMember
from app.models.research_task import ResearchTask

app = FastAPI(
    title="Research Group Management API"
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Research Group Management API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
