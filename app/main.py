from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
import app.models

from app.routes import projects
from app.routes import datasets
from app.routes import models
from app.routes import blueprint
from app.routes import chat
from app.routes import download

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Blueprint API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(projects.router)
app.include_router(datasets.router)
app.include_router(models.router)
app.include_router(blueprint.router)
app.include_router(chat.router)
app.include_router(download.router)


@app.get("/")
def home():
    return {
        "message": "AI Blueprint Backend Running"
    }
