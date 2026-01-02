import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    Pclass: 3,
    Sex: "male",
    Age: 22,
    Fare: 7.25
  });

  const [prediction, setPrediction] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [errorModel, setError] = useState(null);
  const [selectedModel, setSelectedModel] = useState("decision_tree");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // Clear errors when user types
    if (errorModel) setError(null);
  };

  const validateInput = () => {
    if (formData.Age < 0 || formData.Age > 120) return "Age must be between 0 and 120.";
    if (formData.Fare < 0 || formData.Fare > 10000) return "Fare must be a positive number."; // Assuming 10000 as a reasonable technical max
    return null;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const validationError = validateInput();
    if (validationError) {
      alert(validationError); // Or UI error
      return;
    }

    setIsLoading(true);
    setPrediction(null); // Reset previous prediction to show loading effectively if needed, though we persist result area
    try {
      const response = await axios.post(
        `/predict?model_type=${selectedModel}`,
        formData
      );
      setPrediction(response.data);
    } catch (error) {
      console.error(error);
      alert("Error contacting backend!");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1 className="title">Titanic Survival Prediction</h1>
        <p className="subtitle">
          Compare predictions from different Machine Learning models based on historical data.
        </p>
      </header>

      <form onSubmit={handleSubmit} className="prediction-form">
        <div className="form-group">
          <label>
            Passenger Class
            <span
              className="info-icon"
              data-tooltip="1 = First Class (Upper)&#10;2 = Second Class (Middle)&#10;3 = Third Class (Lower)"
            >
              ⓘ
            </span>
          </label>
          <select
            name="Pclass"
            value={formData.Pclass}
            onChange={handleChange}
          >
            <option value="1">1st Class</option>
            <option value="2">2nd Class</option>
            <option value="3">3rd Class</option>
          </select>
        </div>

        <div className="form-group">
          <label>Sex</label>
          <select
            name="Sex"
            value={formData.Sex}
            onChange={handleChange}
          >
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Age (Years)</label>
            <input
              type="number"
              name="Age"
              value={formData.Age}
              onChange={handleChange}
              min="0"
              max="120"
              step="0.1"
              required
            />
          </div>
          <div className="form-group">
            <label>Fare ($)</label>
            <input
              type="number"
              name="Fare"
              value={formData.Fare}
              onChange={handleChange}
              min="0"
              step="0.01"
              required
            />
          </div>
        </div>

        <div className="form-group">
          <label>Algorithm / Model</label>
          <select
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
          >
            <option value="decision_tree">Decision Tree</option>
            <option value="logistic_regression">Logistic Regression</option>
          </select>
        </div>

        <button
          type="submit"
          className="predict-button"
          disabled={isLoading}
        >
          {isLoading ? "Predicting..." : "Predict Survival Outcome"}
        </button>
      </form>

      <div className="result-area">
        {isLoading && (
          <div className="result-card loading">
            <p>Processing passenger data...</p>
          </div>
        )}

        {!isLoading && prediction && (
          <div className={`result-card ${prediction.prediction === 'yes' ? 'survived' : 'not-survived'}`}>
            <h2 className="result-title">
              {prediction.prediction === 'yes' ? "Survived" : "Did Not Survive"}
            </h2>
            <p className="result-prob">
              Probability: <strong>{(prediction.survival_probability * 100).toFixed(1)}%</strong>
            </p>
          </div>
        )}

        {!isLoading && !prediction && (
          <div style={{ color: '#bdc3c7' }}>
            Results will appear here
          </div>
        )}
      </div>

      <footer className="footer">
        <p>Created by King Kunta aka Kena | <a href="#">View Source</a></p>
      </footer>
    </div>
  );
}

export default App;
