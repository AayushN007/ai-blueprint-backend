from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Project

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_project(data: dict, db: Session = Depends(get_db)):

    project = Project(
        project=data.get("project", ""),
        dataset=data.get("dataset", ""),
        target=data.get("target", ""),
        model=data.get("model", ""),
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return {
        "message": "Project saved successfully",
        "id": project.id,
    }


@router.get("/")
def get_projects(db: Session = Depends(get_db)):

    projects = db.query(Project).all()

    return projects

@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        return {"message": "Project not found"}

    db.delete(project)
    db.commit()

    return {"message": "Deleted successfully"}
