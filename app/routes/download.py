from fastapi import APIRouter
from app.services.ai_agent import get_blueprint

router = APIRouter(
    prefix="/download",
    tags=["Download"]
)

@router.get("/")
def download_blueprint():
    return get_blueprint()
