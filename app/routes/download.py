from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import Project, User
import io
import json

router = APIRouter(
    prefix="/download",
    tags=["Download"]
)


def get_latest_project(db, user_id):
    return (
        db.query(Project)
        .filter(Project.user_id == user_id)
        .order_by(Project.id.desc())
        .first()
    )


@router.get("/")
def download_blueprint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    project = get_latest_project(
        db,
        current_user.id
    )

    if not project:
        return {"error": "No blueprint found"}

    blueprint = json.loads(
        project.blueprint_json
    ) if project.blueprint_json else {}

    content = json.dumps(
        blueprint,
        indent=2
    )

    buffer = io.BytesIO(
        content.encode()
    )

    return StreamingResponse(
        buffer,
        media_type="application/json",
        headers={
            "Content-Disposition":
            "attachment; filename=blueprint.json"
        }
    )


@router.get("/preview")
def preview_blueprint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    project = get_latest_project(
        db,
        current_user.id
    )

    if not project:
        return {"error": "No blueprint found"}

    if not project.blueprint_json:
        return {
            "error": "No full blueprint stored"
        }

    return json.loads(
        project.blueprint_json
    )
