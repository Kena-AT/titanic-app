# Titanic Survival Prediction

A full-stack machine learning application that predicts the survival probability of passengers on the Titanic based on their profile (Class, Sex, Age, Fare). This project implements two different classification models for comparison: Logistic Regression and Decision Tree.

## 🚀 Features

- **Interactive UI**: A clean, modern web interface to input passenger details.
- **Multiple Models**: Compare predictions from Logistic Regression and Decision Tree models.
- **Survival Probability**: Get not just a 'yes/no' prediction, but also the calculated probability.
- **RESTful API**: Fast and robust backend powered by FastAPI.
- **Data-Driven**: Trained on the classic Titanic dataset (Kaggle).

## 🛠️ Technology Stack

### Frontend
- **React 19** with **Vite** for a fast development experience.
- **Axios** for API communication.
- **Vanilla CSS** for premium, custom styling.

### Backend
- **FastAPI**: Modern, high-performance web framework.
- **Pandas**: Efficient data manipulation and preprocessing.
- **Scikit-learn**: Machine learning model implementation and inference.
- **Joblib/Pickle**: Model serialization.
- **Uvicorn**: ASGI server for production-ready performance.

## 📁 Project Structure

```text
Titanic Survival Prediction/
├── backend/                # FastAPI Application
│   └── app/
│       ├── main.py         # Entry point & Static serving logic
│       ├── models.py       # ML Model loading logic
│       ├── routes.py       # API Endpoint definitions
│       └── transformers.py # Data preprocessing & transformations
├── frontend/               # React Application (Vite)
│   ├── src/
│   │   ├── App.jsx         # Main application logic
│   │   └── index.css       # Custom styling
│   └── dist/               # Built frontend assets (served by backend)
├── data/                   # Dataset files (train.csv, test.csv)
├── models/                 # Pre-trained .pkl model files
├── notebooks/              # Jupyter notebooks for EDA
└── requirements.txt        # Python dependencies
```

## ⚙️ Installation & Setup

### 1. Prerequisites
- Python 3.8+
- Node.js & npm

### 2. Backend Setup
Navigate to the project root and install the required Python packages:
```bash
pip install -r requirements.txt
```

### 3. Frontend Setup
Navigate to the `frontend` directory and install the dependencies:
```bash
cd frontend
npm install
```

## 🏃 Running the Application

### Option A: Unified Mode (Recommended)
You can run the entire application (frontend + backend) from a single command. First, build the frontend:
```bash
cd frontend
npm run build
```
Then, start the FastAPI server from the project root:
```bash
uvicorn backend.app.main:app --reload
```
The application will be available at `http://localhost:8000`.

### Option B: Development Mode (Separate)
Useful for frontend development with Hot Module Replacement (HMR).

1. **Start Backend**:
   ```bash
   uvicorn backend.app.main:app --reload
   ```
2. **Start Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```
The frontend dev server typically runs on `http://localhost:5173`. Make sure the backend port matches the API configuration in `frontend/src/App.jsx`.

## 📡 API Documentation

Once the backend is running, you can access the interactive API documentation at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Primary Endpoint
`POST /predict`
- **Payload**:
  ```json
  {
    "Pclass": 1,
    "Sex": "female",
    "Age": 29.0,
    "Fare": 71.28
  }
  ```
- **Query Params**: `model_type` ("logistic_regression" or "decision_tree")
