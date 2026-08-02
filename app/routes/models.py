from fastapi import APIRouter

router = APIRouter(
    prefix="/models",
    tags=["Models"]
)

@router.post("/recommend")
def recommend_model():
    return {
        "models": [
            {
                "name": "XGBoost",
                "accuracy": "96%",
                "reason": "Best for structured tabular datasets with excellent predictive performance."
            },
            {
                "name": "Random Forest",
                "accuracy": "95%",
                "reason": "Robust against overfitting and performs well on medium-sized datasets."
            },
            {
                "name": "LightGBM",
                "accuracy": "95%",
                "reason": "Very fast training with excellent scalability for large datasets."
            }
        ]
    }
