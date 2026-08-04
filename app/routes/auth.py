from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.auth import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(
    data: dict,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == data["email"]
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        username=data["username"],
        email=data["email"],
        password=hash_password(data["password"])
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        "message": "Registration successful"
    }

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == form_data.username
    ).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(
        form_data.password,
        user.password
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(
        {
            "user_id": user.id,
            "email": user.email
        }
    )
    return {
        "access_token": token,
        "token_type": "bearer"
    }
