from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app.models import User
from app.services.ai_agent import get_blueprint
from app.services.history_service import save_project


router = APIRouter(
    prefix="/blueprint",
    tags=["Blueprint"]
)


class BlueprintRequest(BaseModel):
    project: str
    dataset: str
    target: str
    model: str = "XGBoost"


@router.post("/generate")
def generate_blueprint(
    request: BlueprintRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    blueprint = get_blueprint(
        project=request.project,
        dataset=request.dataset,
        target=request.target,
        model_name=request.model
    )

    save_project(
        db=db,
        blueprint=blueprint,
        user_id=current_user.id
    )

    return blueprint
