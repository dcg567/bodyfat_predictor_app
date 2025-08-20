import React, { useState } from "react";

export default function App() {
 const [formData, setFormData] = useState({
  Age: "",
  Weight: "",
  Height: "",
  Neck: "",
  Chest: "",
  Abdomen: "",
  Thigh: "",
  Ankle: "",
  Biceps: "",
  Forearm: "",
});

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  function handleChange(e) {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
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

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setPrediction(data.predicted_bodyfat);
    } catch (err) {
      setError("Failed to get prediction. Is your backend running?");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 400, margin: "2rem auto", fontFamily: "Arial, sans-serif" }}>
      <h1>Body Fat Predictor</h1>
      <form onSubmit={handleSubmit}>
        {Object.entries(formData).map(([key, val]) => (
          <div key={key} style={{ marginBottom: 12 }}>
            <label>
              {key}:
              <input
                type="number"
                name={key}
                value={val}
                onChange={handleChange}
                required
                style={{ marginLeft: 8, width: "100%" }}
              />
            </label>
          </div>
        ))}
        <button type="submit" disabled={loading} style={{ padding: "8px 16px" }}>
          {loading ? "Predicting..." : "Predict Body Fat"}
        </button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {prediction !== null && !error && (
        <p style={{ marginTop: 20 }}>
          Predicted Body Fat: <strong>{prediction.toFixed(2)}%</strong>
        </p>
      )}
    </div>
  );
}
