from fastapi import APIRouter

router = APIRouter(
    prefix="/datasets",
    tags=["Datasets"]
)

@router.post("/recommend")
def recommend_dataset():

    return {
        "datasets": [
            {
                "name":"Student Performance Dataset",
                "url":"https://www.kaggle.com/datasets/spscientist/students-performance-in-exams"
            },
            {
                "name":"UCI Student Dataset",
                "url":"https://archive.ics.uci.edu/ml/datasets/student+performance"
            },
            {
                "name":"Academic Success Dataset",
                "url":"https://www.openml.org/"
            }
        ]
    }
