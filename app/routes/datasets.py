from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.services.ai_agent import get_dataset_recommendations

router = APIRouter(prefix="/datasets", tags=["Datasets"])

class DatasetRecommendRequest(BaseModel):
    project: str
    target: Optional[str] = None

@router.post("/recommend")
def recommend_datasets(
    request: DatasetRecommendRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        result = get_dataset_recommendations(request.project, request.target)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
