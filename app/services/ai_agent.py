from app.services.gemini_service import ask_gemini
import json
import re
from app.database import SessionLocal
from app.services.history_service import save_project


conversation_history = []

blueprint = {
    "project": "",
    "dataset": "",
    "target": "",
    "model": "XGBoost"
}


def generate_ai_response(message: str):

    global conversation_history
    global blueprint

    conversation_history.append(
        f"User: {message}"
    )

    prompt = f"""
You are an expert Machine Learning Architect.

Conversation:
{chr(10).join(conversation_history)}

Your task:
Collect:
1. Project name
2. Dataset information
3. Prediction target

Rules:
- Infer project name automatically.
- Ask only one question at a time.
- Do not ask for project name.
- When enough information is available write:

BLUEPRINT_READY

Then provide JSON:

{{
"project":"",
"dataset":"",
"target":"",
"model":"XGBoost"
}}
"""

    reply = ask_gemini(prompt)

    ready = False

    if "BLUEPRINT_READY" in reply:

        ready = True

        try:
            match = re.search(
                r"\{[\s\S]*\}",
                reply
            )

            if match:
                data = json.loads(match.group())
                blueprint.update(data)
                db = SessionLocal()
                save_project(db, blueprint)
                db.close()

        except Exception:
            pass


        reply = reply.split(
            "BLUEPRINT_READY"
        )[0].strip()


        if not reply:
            reply = (
                "Excellent! Your AI blueprint is ready."
            )


    conversation_history.append(
        f"Assistant: {reply}"
    )


    return {
        "reply": reply,
        "blueprint_ready": ready
    }



def get_blueprint():

    return {
        "project": blueprint["project"],
        "dataset": blueprint["dataset"],
        "target": blueprint["target"],
        "model": blueprint["model"],
        "pipeline": [
            "Data Collection",
            "Data Cleaning",
            "Feature Engineering",
            "Model Training",
            "Model Evaluation",
            "Deployment"
        ]
    }
