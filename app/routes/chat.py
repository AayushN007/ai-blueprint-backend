from fastapi import APIRouter
from app.services.ai_agent import generate_ai_response

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post("/")
def chat(data: dict):

    message = data.get("message", "")

    return generate_ai_response(message)
