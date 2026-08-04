from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.services.ai_agent import get_model_recommendations


router = APIRouter(
    prefix="/models",
    tags=["Models"]
)


class ModelRecommendRequest(BaseModel):
    project: str
    dataset: Optional[str] = None
    target: Optional[str] = None


@router.post("/recommend")
def recommend_models(
    request: ModelRecommendRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return get_model_recommendations(
            request.project,
            request.dataset,
            request.target
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
