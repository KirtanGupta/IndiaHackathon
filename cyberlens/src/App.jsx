import { useState } from "react";
import InputPanel from "../components/InputPanel";
import ResultCard from "../components/ResultCard";
import IncidentLog from "../components/IncidentLog";
import { scan } from "../api/scan";

const initialResult = {
  score: 18,
  severity: "low",
  explanation: "Run a scan to see risk analysis.",
  signals: {
    email_length: 0,
    url_present: false,
    media_type: "audio"
  }
};

export default function App() {
  const [result, setResult] = useState(initialResult);
  const [incidentLog, setIncidentLog] = useState([]);
  const [loading, setLoading] = useState(false);

  async function handleScan(payload) {
    setLoading(true);
    try {
      const data = await scan(payload);
      setResult(data);
      setIncidentLog((current) => [
        {
          id: Date.now(),
          severity: data.severity,
          score: data.score,
          summary: data.explanation
        },
        ...current
      ].slice(0, 5));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page-shell">
      <section className="hero">
        <p className="eyebrow">IndiaHackathon 2026</p>
        <h1>CyberLens Threat Triage Console</h1>
        <p className="subtitle">
          Scan suspicious content, score cyber risk, and surface a quick explanation for analysts.
        </p>
      </section>
      <div className="content-grid">
        <InputPanel onScan={handleScan} loading={loading} />
        <ResultCard result={result} />
      </div>
      <IncidentLog items={incidentLog} />
    </div>
  );
}