from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
from .models import decision_tree_model, logistic_regression_model

router = APIRouter()

# Input schema
# Input schema
class Passenger(BaseModel):
    Pclass: int
    Sex: str
    Age: float | None = None
    Fare: float | None = None

# Prediction route
@router.post("/predict")
def predict_survival(passenger: Passenger, model_type: str = "random_forest"):
    # Convert input to DataFrame
    input_data = passenger.dict()
    
    input_df = pd.DataFrame([input_data])
    
    # Select model
    if model_type == "logistic_regression":
        model = logistic_regression_model
    elif model_type == "decision_tree":
        model = decision_tree_model
    else:
        # Fallback
        model = decision_tree_model
    try:
        pred = model.predict(input_df)[0]
        proba = model.predict_proba(input_df)[0][1]  # Probability of survival
    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}
    
    model_names = {
        "decision_tree": "Decision Tree",
        "logistic_regression": "Logistic Regression"
    }
    
    return {
        "prediction": "yes" if pred == 1 else "no",
        "survival_probability": round(proba, 2),
        "model_used": model_names.get(model_type, model_type)
    }
