import { useState } from "react";
import axios from "axios";

const API = "https://datapulse-backend-kedv.onrender.com/csv/clean";

function CsvCleaner() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const cleanCsv = async () => {
    if (!file) {
      alert("Please select a CSV file");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setResult(null);

      const formData = new FormData();
      formData.append("file", file);

      const response = await axios.post(
        `${API}/csv/clean`,
        formData
      );

      console.log("CSV Clean Result:", response.data);

      setResult(response.data);
    } catch (err) {
      console.error("CSV cleaning error:", err);

      setError(
        err.response?.data?.detail ||
        "Failed to clean CSV file"
      );
    } finally {
      setLoading(false);
    }
  };

  const downloadCsv = () => {
    if (!result?.download_url) {
      return;
    }

    window.open(
      `${API}${result.download_url}`,
      "_blank"
    );
  };

  return (
    <section className="csv-cleaner">

      <div className="csv-header">
        <div>
          <h2>CSV Cleaner</h2>
          <p>
            Upload your CSV file and automatically
            clean missing and invalid data.
          </p>
        </div>
      </div>

      <div className="csv-upload-card">

        <div className="upload-area">

          <div className="upload-icon">
            📄
          </div>

          <h3>
            Upload CSV File
          </h3>

          <p>
            Select a CSV file from your computer
          </p>

          <input
            type="file"
            accept=".csv"
            onChange={(e) => {
              setFile(e.target.files[0]);
              setResult(null);
              setError("");
            }}
          />

          {file && (
            <div className="selected-file">
              <strong>
                Selected:
              </strong>{" "}
              {file.name}
            </div>
          )}

        </div>

        <button
          className="clean-button"
          onClick={cleanCsv}
          disabled={loading || !file}
        >
          {loading
            ? "Cleaning..."
            : "Clean CSV"}
        </button>

      </div>

      {error && (
        <div className="csv-error">
          {error}
        </div>
      )}

      {result && (
        <div className="csv-result">

          <div className="result-header">
            <div>
              <h3>
                Cleaning Completed
              </h3>

              <p>
                {result.filename}
              </p>
            </div>

            <span className="success-badge">
              SUCCESS
            </span>
          </div>

          <div className="csv-stats">

            <div className="csv-stat">
              <span>
                Original Records
              </span>

              <strong>
                {result.statistics?.original_records || 0}
              </strong>
            </div>

            <div className="csv-stat">
              <span>
                Cleaned Records
              </span>

              <strong>
                {result.statistics?.cleaned_records || 0}
              </strong>
            </div>

            <div className="csv-stat">
              <span>
                Missing Values
              </span>

              <strong>
                {result.statistics?.missing_values || 0}
              </strong>
            </div>

            <div className="csv-stat">
              <span>
                Invalid Values
              </span>

              <strong>
                {result.statistics?.invalid_values || 0}
              </strong>
            </div>

          </div>

          <button
            className="download-button"
            onClick={downloadCsv}
          >
            Download Cleaned CSV
          </button>

        </div>
      )}

    </section>
  );
}

export default CsvCleaner;