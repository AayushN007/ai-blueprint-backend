import json
from sqlalchemy.orm import Session
from app.models import Project


def save_project(db: Session, blueprint, user_id):

    project = Project(
        project=blueprint.get(
            "project_name",
            blueprint.get("project", "Untitled")
        ),

        dataset=json.dumps(
            blueprint.get("dataset", {})
        ),

        target=blueprint.get(
            "target_column",
            blueprint.get("target", "")
        ),

        model=json.dumps(
            blueprint.get("model", {})
        ),

        blueprint_json=json.dumps(
            blueprint
        ),

        user_id=user_id
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project
