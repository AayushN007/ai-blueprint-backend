from fastapi import APIRouter
from app.services.ai_agent import get_blueprint

router = APIRouter(
    prefix="/blueprint",
    tags=["Blueprint"]
)


@router.post("/generate")
def generate_blueprint():

    return get_blueprint()
