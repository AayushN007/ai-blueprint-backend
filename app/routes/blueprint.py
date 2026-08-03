from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Project
from app.services.ai_agent import get_blueprint

router = APIRouter(
    prefix="/blueprint",
    tags=["Blueprint"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/generate")
def generate_blueprint(db: Session = Depends(get_db)):

    blueprint = get_blueprint()

    project = Project(
        project=blueprint.get("project", ""),
        dataset=blueprint.get("dataset", ""),
        target=blueprint.get("target", ""),
        model=blueprint.get("model", ""),
    )

    db.add(project)
    db.commit()

    return blueprint
