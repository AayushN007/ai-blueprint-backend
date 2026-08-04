import os
import json
import logging
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


def clean_json(text: str):
    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]

    if text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


def get_blueprint(project: str, dataset: str, target: str, model_name: str):

    prompt = f"""
You are a senior machine learning architect.

Generate a COMPLETE production-ready ML blueprint.

PROJECT:
{project}

DATASET:
{dataset}

TARGET:
{target}

MODEL:
{model_name}

Return ONLY VALID JSON.

{{
  "project_name": "",
  "problem_type": "",
  "goal": "",

  "dataset": {{
    "name": "",
    "description": "",
    "source": "",
    "size_estimate": "",
    "preprocessing_steps": []
  }},

  "target_column": "",

  "feature_engineering": [],

  "model": {{
    "name": "",
    "library": "",
    "hyperparameters": {{}},
    "training_steps": []
  }},

  "evaluation_metrics": [],

  "pipeline_steps": [],

  "deployment_suggestions": [],

  "next_steps": []
}}
"""

    try:
        response = model.generate_content(prompt)

        data = json.loads(clean_json(response.text))

        return data

    except Exception as e:
        logger.error(f"Blueprint generation error: {e}")

        return {
            "project_name": project,
            "problem_type": "Unknown",
            "goal": "",

            "dataset": {
                "name": dataset,
                "description": "",
                "source": "",
                "size_estimate": "",
                "preprocessing_steps": []
            },

            "target_column": target,

            "feature_engineering": [],

            "model": {
                "name": model_name,
                "library": "",
                "hyperparameters": {},
                "training_steps": []
            },

            "evaluation_metrics": [],

            "pipeline_steps": [],

            "deployment_suggestions": [],

            "next_steps": []
        }


def get_dataset_recommendations(project: str, target: str = None):

    prompt = f"""
Recommend exactly 5 REAL datasets for this ML project.

Project:
{project}

Target:
{target}

Return ONLY valid JSON.

{{
  "datasets": [
    {{
      "name": "",
      "source": "",
      "description": "",
      "why_fit": "",
      "size": "",
      "link": ""
    }}
  ]
}}
"""

    try:
        response = model.generate_content(prompt)

        return json.loads(
            clean_json(response.text)
        )

    except Exception as e:
        logger.error(f"Dataset recommendation error: {e}")

        return {"datasets": []}


def get_model_recommendations(
    project: str,
    dataset: str = None,
    target: str = None
):

    prompt = f"""
Recommend exactly 5 ML models.

Project:
{project}

Dataset:
{dataset}

Target:
{target}

Return ONLY valid JSON.

{{
  "models": [
    {{
      "name": "",
      "type": "",
      "library": "",
      "reason": "",
      "pros": "",
      "cons": ""
    }}
  ]
}}
"""

    try:
        response = model.generate_content(
            prompt
        )

        return json.loads(
            clean_json(response.text)
        )

    except Exception as e:
        logger.error(f"Model recommendation error: {e}")

        return {"models": []}

from app.services.history_service import save_project

def generate_ai_response(message, db, user_id):
    prompt = f"""
You are an expert AI Machine Learning Architect.

The user says:

{message}

From the user's request, identify:

1. Project name
2. Dataset
3. Target column
4. Best ML model

Then generate a complete ML blueprint.

Return ONLY valid JSON in this format:

{{
  "project_name": "",
  "problem_type": "",
  "goal": "",

  "dataset": {{
    "name": "",
    "description": "",
    "source": "",
    "size_estimate": "",
    "preprocessing_steps": []
  }},

  "target_column": "",

  "feature_engineering": [],

  "model": {{
    "name": "",
    "library": "",
    "hyperparameters": {{}},
    "training_steps": []
  }},

  "evaluation_metrics": [],

  "pipeline_steps": [],

  "deployment_suggestions": [],

  "next_steps": []
}}
"""

    try:
        response = model.generate_content(prompt)

        blueprint = json.loads(
            clean_json(response.text)
        )

        save_project(
            db=db,
            blueprint=blueprint,
            user_id=user_id
        )

        return {
            "reply": "Blueprint generated successfully.",
            "blueprint_ready": True,
            "blueprint": blueprint
        }

    except Exception as e:
        logger.error(e)

        return {
            "error": str(e)
        }
