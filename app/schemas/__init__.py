from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ProjectCreate(BaseModel):
    project: str
    dataset: Optional[str] = None
    target: Optional[str] = None
    model: Optional[str] = None

class ProjectOut(BaseModel):
    id: int
    project: str
    dataset: Optional[str] = None
    target: Optional[str] = None
    model: Optional[str] = None
    user_id: int

    class Config:
        from_attributes = True

class BlueprintRequest(BaseModel):
    project: str
    dataset: str
    target: str
    model: str

class DatasetRecommendRequest(BaseModel):
    project: str
    target: Optional[str] = None

class ModelRecommendRequest(BaseModel):
    project: str
    dataset: Optional[str] = None
    target: Optional[str] = None
