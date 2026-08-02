from sqlalchemy.orm import Session
from app.models import Project

def save_project(db: Session, blueprint):
    project = Project(
        title=blueprint["project"],
        description=blueprint["target"]
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project
