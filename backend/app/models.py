import joblib
import os

# Load models from the root 'models/' folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# BASE_DIR is backend/app, so ../../models is the root models folder
DT_MODEL_PATH = os.path.abspath(os.path.join(BASE_DIR, '../../models/decision_tree_model.pkl'))
LR_MODEL_PATH = os.path.abspath(os.path.join(BASE_DIR, '../../models/logistic_regression_model.pkl'))

decision_tree_model = joblib.load(DT_MODEL_PATH)
logistic_regression_model = joblib.load(LR_MODEL_PATH)
