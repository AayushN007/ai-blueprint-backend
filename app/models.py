from sqlalchemy import Column, Integer, String

from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)

    project = Column(String, nullable=False)
    dataset = Column(String, nullable=False)
    target = Column(String, nullable=False)
    model = Column(String, nullable=False)
