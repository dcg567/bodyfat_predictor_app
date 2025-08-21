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

  function handleChange(e) {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  }

  function toggleDarkMode() {
    setDarkMode(prev => !prev);
    document.body.classList.toggle("dark-mode", !darkMode);
  }

  async function handleSubmit(e) {
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
  }

  return (
    <>
      {/* Toggle Button OUTSIDE the container */}
      <button className="toggle-btn" onClick={toggleDarkMode}>
        {darkMode ? "🌞" : "🌙"}
      </button>

      <div className="container">
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
          <p className="result">Predicted Body Fat: {prediction.toFixed(2)}%</p>
        )}
      </div>
    </>
  );
}
