
import React, { useState } from "react";
import axios from "axios";

const API = "https://datapulse-backend-kedv.onrender.com";

function CsvCleaner() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    setResult(null);
    setError("");

    if (!selectedFile) {
      setFile(null);
      return;
    }

    if (!selectedFile.name.toLowerCase().endsWith(".csv")) {
      setError("Please select a CSV file.");
      setFile(null);
      return;
    }

    setFile(selectedFile);
  };

  const cleanCsv = async () => {
    if (!file) {
      setError("Please select a CSV file first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await axios.post(
        `${API}/csv/clean`,
        formData
      );

      setResult(response.data);
    } catch (err) {
      console.error("CSV cleaning error:", err);

      if (err.response) {
        setError(
          err.response.data?.detail ||
            err.response.data?.message ||
            `Server error: ${err.response.status}`
        );
      } else if (err.request) {
        setError(
          "Unable to connect to the backend server. Please try again."
        );
      } else {
        setError("Failed to clean CSV file.");
      }
    } finally {
      setLoading(false);
    }
  };

  const downloadCleanedFile = () => {
    if (!result?.download_url) {
      return;
    }

    const downloadUrl = result.download_url.startsWith("http")
      ? result.download_url
      : `${API}${result.download_url}`;

    window.open(downloadUrl, "_blank");
  };

  return (
    <div className="csv-cleaner">
      <div className="csv-cleaner-header">
        <h2>CSV Cleaner</h2>
        <p>
          Upload your CSV file and automatically clean missing and
          invalid values.
        </p>
      </div>

      <div className="csv-upload-box">
        <input
          type="file"
          accept=".csv,text/csv"
          onChange={handleFileChange}
        />

        {file && (
          <div className="selected-file">
            <strong>Selected file:</strong> {file.name}
          </div>
        )}

        <button
          type="button"
          onClick={cleanCsv}
          disabled={!file || loading}
        >
          {loading ? "Cleaning CSV..." : "Clean CSV"}
        </button>
      </div>

      {error && (
        <div className="csv-error">
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && result.success && (
        <div className="csv-result">
          <h3>CSV Cleaned Successfully ✅</h3>

          <p>{result.message}</p>

          {result.statistics && (
            <div className="csv-statistics">
              <div className="stat-card">
                <span>Original Records</span>
                <strong>
                  {result.statistics.original_records}
                </strong>
              </div>

              <div className="stat-card">
                <span>Cleaned Records</span>
                <strong>
                  {result.statistics.cleaned_records}
                </strong>
              </div>

              <div className="stat-card">
                <span>Missing Values</span>
                <strong>
                  {result.statistics.missing_values}
                </strong>
              </div>

              <div className="stat-card">
                <span>Invalid Values</span>
                <strong>
                  {result.statistics.invalid_values}
                </strong>
              </div>
            </div>
          )}

          <button
            type="button"
            onClick={downloadCleanedFile}
          >
            Download Cleaned CSV
          </button>
        </div>
      )}
    </div>
  );
}

export default CsvCleaner;

