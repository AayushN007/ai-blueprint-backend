from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
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
def register(data: dict, db: Session = Depends(get_db)):

    if db.query(User).filter(User.email == data["email"]).first():
        return {"message": "Email already exists"}

    user = User(
        username=data["username"],
        email=data["email"],
        password=hash_password(data["password"])
    )

    db.add(user)
    db.commit()

    return {"message": "Registration successful"}


@router.post("/login")
def login(data: dict, db: Session = Depends(get_db)):

    user = db.query(User).filter(
        User.email == data["email"]
    ).first()

    if not user:
        return {"message": "Invalid credentials"}

    if not verify_password(
        data["password"],
        user.password
    ):
        return {"message": "Invalid credentials"}

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
