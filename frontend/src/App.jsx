import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";
import CsvCleaner from "./CsvCleaner";

const API = "http://127.0.0.1:8000";

function App() {
  const [pipelines, setPipelines] = useState([]);
  const [error, setError] = useState("");

  const [showForm, setShowForm] = useState(false);
  const [name, setName] = useState("");
  const [sourceType, setSourceType] = useState("REST_API");
  const [sourcePath, setSourcePath] = useState("");
  const [loading, setLoading] = useState(false);

  const [showRuns, setShowRuns] = useState(false);
  const [selectedPipeline, setSelectedPipeline] = useState(null);
  const [runs, setRuns] = useState([]);
  const [runsLoading, setRunsLoading] = useState(false);

  const loadPipelines = async () => {
    try {
      setError("");

      const response = await axios.get(`${API}/pipelines`);

      setPipelines(response.data.pipelines || []);
    } catch (err) {
      console.error("Load pipelines error:", err);
      setError("Failed to load pipelines");
    }
  };

  useEffect(() => {
    loadPipelines();
  }, []);

  const createPipeline = async (e) => {
    e.preventDefault();

    if (!name.trim() || !sourcePath.trim()) {
      alert("Please fill all fields");
      return;
    }

    try {
      setLoading(true);

      const response = await axios.post(`${API}/pipelines`, {
        name: name.trim(),
        source_type: sourceType,
        source_path: sourcePath.trim(),
      });

      console.log("Created:", response.data);

      alert("Pipeline created successfully!");

      setName("");
      setSourceType("REST_API");
      setSourcePath("");
      setShowForm(false);

      await loadPipelines();
    } catch (err) {
      console.error("Create pipeline error:", err);

      if (err.response) {
        alert(
          err.response.data?.detail ||
          "Failed to create pipeline"
        );
      } else {
        alert("Backend server is not running");
      }
    } finally {
      setLoading(false);
    }
  };

  const runPipeline = async (pipeline) => {
    try {
      const response = await axios.post(
        `${API}/pipelines/${pipeline.id}/run`
      );

      console.log("Run response:", response.data);

      if (response.data.success) {
        const records =
          response.data.result?.records_cleaned || 0;

        alert(
          `Pipeline completed successfully!\nRecords: ${records}`
        );
      } else {
        alert("Pipeline failed");
      }

      await loadPipelines();
    } catch (err) {
      console.error("Run pipeline error:", err);

      alert(
        err.response?.data?.detail ||
        "Failed to run pipeline"
      );
    }
  };

  const viewRuns = async (pipeline) => {
    try {
      setSelectedPipeline(pipeline);
      setShowRuns(true);
      setRunsLoading(true);
      setRuns([]);

      const response = await axios.get(
        `${API}/pipelines/${pipeline.id}/runs`
      );

      console.log("Runs:", response.data);

      setRuns(response.data.runs || []);
    } catch (err) {
      console.error("View runs error:", err);

      alert(
        err.response?.data?.detail ||
        "Failed to load pipeline runs"
      );
    } finally {
      setRunsLoading(false);
    }
  };

  const closeRuns = () => {
    setShowRuns(false);
    setSelectedPipeline(null);
    setRuns([]);
  };

  const totalPipelines = pipelines.length;

  const successfulPipelines = pipelines.filter(
    (pipeline) => pipeline.status === "SUCCESS"
  ).length;

  const failedPipelines = pipelines.filter(
    (pipeline) => pipeline.status === "FAILED"
  ).length;

  return (
    <div className="app">

      <header>
        <h1>DataPulse</h1>
        <p>Data Pipeline Management</p>
      </header>
<CsvCleaner />

      <main>

        <div className="dashboard">

          <div className="stat-card">
            <h3>Total Pipelines</h3>
            <strong>{totalPipelines}</strong>
          </div>

          <div className="stat-card">
            <h3>Successful</h3>
            <strong>{successfulPipelines}</strong>
          </div>

          <div className="stat-card">
            <h3>Failed</h3>
            <strong>{failedPipelines}</strong>
          </div>

        </div>

        <div className="page-header">

          <h2>Pipelines</h2>

          <button
            onClick={() => setShowForm(!showForm)}
          >
            + Create Pipeline
          </button>

        </div>

        {showForm && (
          <div className="create-form">

            <h3>Create New Pipeline</h3>

            <form onSubmit={createPipeline}>

              <label>Pipeline Name</label>

              <input
                type="text"
                placeholder="Example: Customer Data Pipeline"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />

              <label>Source Type</label>

              <select
                value={sourceType}
                onChange={(e) =>
                  setSourceType(e.target.value)
                }
              >
                <option value="REST_API">
                  REST API
                </option>

                <option value="CSV">
                  CSV
                </option>
              </select>

              <label>Source Path</label>

              <input
                type="text"
                placeholder="Enter URL or file path"
                value={sourcePath}
                onChange={(e) =>
                  setSourcePath(e.target.value)
                }
              />

              <div className="form-buttons">

                <button
                  type="submit"
                  disabled={loading}
                >
                  {loading
                    ? "Creating..."
                    : "Create Pipeline"}
                </button>

                <button
                  type="button"
                  onClick={() => setShowForm(false)}
                >
                  Cancel
                </button>

              </div>

            </form>

          </div>
        )}

        {error && (
          <p className="error-message">
            {error}
          </p>
        )}

        <div className="pipeline-grid">

          {pipelines.map((pipeline) => (

            <div
              className="pipeline-card"
              key={pipeline.id}
            >

              <h3>{pipeline.name}</h3>

              <p>
                <strong>ID:</strong> {pipeline.id}
              </p>

              <p>
                <strong>Source:</strong>{" "}
                {pipeline.source_type}
              </p>

              <p>
                <strong>Status:</strong>{" "}

                <span
                  className={
                    pipeline.status === "SUCCESS"
                      ? "status-success"
                      : pipeline.status === "FAILED"
                      ? "status-failed"
                      : "status-created"
                  }
                >
                  {pipeline.status}
                </span>

              </p>

              <p>
                <strong>Path:</strong>{" "}
                {pipeline.source_path}
              </p>

              <div className="card-buttons">

                <button
                  onClick={() =>
                    runPipeline(pipeline)
                  }
                >
                  Run Pipeline
                </button>

                <button
                  onClick={() =>
                    viewRuns(pipeline)
                  }
                >
                  View Runs
                </button>

              </div>

            </div>

          ))}

        </div>

      </main>

      {showRuns && selectedPipeline && (

        <div
          className="modal-overlay"
          onClick={closeRuns}
        >

          <div
            className="runs-modal"
            onClick={(e) => e.stopPropagation()}
          >

            <div className="modal-header">

              <div>

                <h2>Pipeline Runs</h2>

                <p>
                  {selectedPipeline.name}
                  {" "}
                  (ID: {selectedPipeline.id})
                </p>

              </div>

              <button
                className="close-button"
                onClick={closeRuns}
              >
                ×
              </button>

            </div>

            {runsLoading ? (

              <p className="loading-text">
                Loading runs...
              </p>

            ) : runs.length === 0 ? (

              <p className="no-runs">
                No runs found for this pipeline.
              </p>

            ) : (

              <div className="runs-list">

                {runs.map((run) => (

                  <div
                    className="run-card"
                    key={run.run_id}
                  >

                    <div className="run-header">

                      <h3>
                        Run #{run.run_id}
                      </h3>

                      <span
                        className={
                          run.status === "SUCCESS"
                            ? "status-success"
                            : "status-failed"
                        }
                      >
                        {run.status}
                      </span>

                    </div>

                    <p>
                      <strong>Attempt:</strong>{" "}
                      {run.attempt}
                    </p>

                    <p>
                      <strong>Records:</strong>{" "}
                      {run.records_processed}
                    </p>

                    <p>
                      <strong>Started:</strong>{" "}
                      {run.started_at || "-"}
                    </p>

                    <p>
                      <strong>Completed:</strong>{" "}
                      {run.completed_at || "-"}
                    </p>

                    {run.error && (
                      <div className="run-error">

                        <strong>Error:</strong>

                        <p>
                          {run.error}
                        </p>

                      </div>
                    )}

                  </div>

                ))}

              </div>

            )}

          </div>

        </div>

      )}

    </div>
  );
}

export default App;