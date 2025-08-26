import React, { useState } from "react";
import "./style.css";

export default function App() {
  const [formData, setFormData] = useState({
    Age: "", Weight: "", Height: "", Neck: "", Chest: "", Abdomen: "",
    Thigh: "", Ankle: "", Biceps: "", Forearm: ""
  });

  const [darkMode, setDarkMode] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const toggleDarkMode = () => {
    setDarkMode(prev => !prev);
    document.body.classList.toggle("dark-mode", !darkMode);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();
      setPrediction(data.predicted_bodyfat);
    } catch {
      setError("Failed to get prediction. Is your backend running?");
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = () => {
    setFormData({
      Age: "", Weight: "", Height: "", Neck: "", Chest: "", Abdomen: "",
      Thigh: "", Ankle: "", Biceps: "", Forearm: ""
    });
    setPrediction(null);
    setError(null);
  };

  return (
    <>
      <button className="toggle-btn" onClick={toggleDarkMode}>
        {darkMode ? "🌞" : "🌙"}
      </button>

      <div className="app-flex-container">
        {/* Left Section */}
        <div className="left-container">
          <div className="info-section">
            <h2>How to Use</h2>
            <p>Simply input your measurements into the fields and click 'predict'.</p>
            <p>All measurements should be in centimeters, kilograms, and years.</p>
            <p>This is an estimate, not a diagnosis.</p>
          </div>

          <div className="info-section">
            <h2>About the Model</h2>
            <p>My dataset is sourced from Kaggle. It has been cleaned and modified to remove any 
            outliers and ensure high-quality data for accurate predictions</p>
            <p>My model uses a decision tree to predict body fat percentage based on measurements like age, weight, height, and several body circumferences. 
            It learns from existing data by splitting features into different ranges 
            and uses these rules to make accurate predictions on new inputs.</p>
          </div>
        </div>

        {/* Middle Section (Form) */}
        <div className="middle-container">
          <h1>Body Fat Predictor</h1>

          <form onSubmit={handleSubmit}>
            {Object.entries(formData).map(([key, val]) => (
              <div className="form-group" key={key}>
                <label htmlFor={key}>{key}</label>
                <input
                  id={key}
                  type="number"
                  name={key}
                  value={val}
                  min="1"
                  onChange={handleChange}
                  required
                />
              </div>
            ))}
            <button type="submit" disabled={loading}>
              {loading ? "Predicting..." : "Predict Body Fat"}
            </button>
          </form>

          {error && <p className="error">{error}</p>}
          {prediction !== null && !error && (
            <div className="result-container">
              <p className="result">Predicted Body Fat: {prediction.toFixed(2)}%</p>
              <button className="refresh-btn" onClick={handleRefresh}>Refresh</button>
            </div>
          )}
        </div>

        {/* Right Section */}
        <div className="right-container">
          <div className="right-top">
            <h3>Body Fat Percentage Chart</h3>
            <table className="fat-table">
              <thead>
                <tr>
                  <th>BF%</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>&lt;10%</td>
                  <td><span className="status-dot lean"></span>Extremely lean, pro athletes or bodybuilders</td>
                </tr>
                <tr>
                  <td>10–15%</td>
                  <td><span className="status-dot fit"></span>Fit and healthy, some muscle definition visible</td>
                </tr>
                <tr>
                  <td>15–20%</td>
                  <td><span className="status-dot average"></span>Average, healthy for most people</td>
                </tr>
                <tr>
                  <td>20–25%</td>
                  <td><span className="status-dot soft"></span>Soft appearance, approaching overweight</td>
                </tr>
                <tr>
                  <td>25%+</td>
                  <td><span className="status-dot obese"></span>Get yo ass to the gym</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="right-bottom">
            <h3>Additional Info</h3>
            <p>If you like this project and want to learn more or check out my other projects, check out my GitHub, website, or email me directly:</p>

            <div className="link-buttons">
              <a href="https://github.com/yourusername" target="_blank" rel="noopener noreferrer" className="link-btn">
                <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="GitHub" /> GitHub
              </a>
              <a href="https://yourwebsite.com" target="_blank" rel="noopener noreferrer" className="link-btn">
                <img src="https://cdn-icons-png.flaticon.com/512/841/841364.png" alt="Website" /> Website
              </a>
              <a href="mailto:youremail@example.com" className="link-btn">
                <img src="https://cdn-icons-png.flaticon.com/512/732/732200.png" alt="Email" /> Email Me
              </a>
            </div>

            <div className="extra-info">
              <h4>Technologies Used:</h4>
              <div className="tech-icons">
                <div className="tech-item">
                  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg" alt="React" />
                  <span>React</span>
                </div>
                <div className="tech-item">
                  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg" alt="FastAPI" />
                  <span>FastAPI</span>
                </div>
                <div className="tech-item">
                  <img src="/py.svg" alt="Python" />
                  <span>Python</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}