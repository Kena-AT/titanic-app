import joblib
import os

# Load models from 'models/' folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DT_MODEL_PATH = os.path.join(BASE_DIR, '../models/decision_tree_model.pkl')
LR_MODEL_PATH = os.path.join(BASE_DIR, '../models/logistic_regression_model.pkl')

decision_tree_model = joblib.load(DT_MODEL_PATH)
logistic_regression_model = joblib.load(LR_MODEL_PATH)
