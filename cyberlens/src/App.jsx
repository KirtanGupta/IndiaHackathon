import { useEffect, useState } from "react";
import InputPanel from "../components/InputPanel";
import PhishingPhaseGuide from "../components/PhishingPhaseGuide";
import UrlPhaseGuide from "../components/UrlPhaseGuide";
import ResultCard from "../components/ResultCard";
import IncidentLog from "../components/IncidentLog";
import { fetchRoadmap, scan } from "../api/scan";

const initialResult = {
  active_phase: "email",
  score: 0,
  severity: "low",
  explanation: "Run a phase to see isolated analysis.",
  module_explanations: {
    email: "",
    url: "",
    deepfake: ""
  },
  modules: {
    email: { score: 0, severity: "low", source: "inactive" },
    url: { score: 0, severity: "low", source: "inactive" },
    deepfake: { score: 0, severity: "low", source: "inactive" }
  },
  ordered_modules: [],
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
  const [activePhase, setActivePhase] = useState("email");
  const [roadmap, setRoadmap] = useState({ phases: [], demo_order: ["email", "url", "deepfake"] });

  useEffect(() => {
    fetchRoadmap().then(setRoadmap).catch(() => undefined);
  }, []);

  async function handleScan(payload) {
    setLoading(true);
    try {
      const data = await scan(payload);
      setResult(data);
      const activeModule = data.modules[data.active_phase];
      setIncidentLog((current) => [
        {
          id: Date.now(),
          phase: data.active_phase,
          severity: activeModule.severity,
          score: activeModule.score,
          summary: data.module_explanations[data.active_phase]
        },
        ...current
      ].slice(0, 6));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page-shell">
      <section className="hero">
        <p className="eyebrow">IndiaHackathon 2026</p>
        <h1>CyberLens Build-by-Phase Demo</h1>
        <p className="subtitle">
          Each model now runs separately. Select one phase, test it in isolation, and compare suspicious vs legitimate inputs clearly.
        </p>
      </section>
      <section className="panel roadmap-panel">
        <h2>Project Roadmap</h2>
        <div className="phase-roadmap">
          {roadmap.phases.map((phase, index) => (
            <div key={phase} className="roadmap-step">
              <span className="roadmap-index">{index + 1}</span>
              <span>{phase}</span>
            </div>
          ))}
        </div>
        <p className="roadmap-note">Demo order: {roadmap.demo_order.join(" -> ")}</p>
      </section>
      {activePhase === "email" ? <PhishingPhaseGuide emailResult={result.modules?.email} /> : null}
      {activePhase === "url" ? <UrlPhaseGuide urlResult={result.modules?.url} /> : null}
      <div className="content-grid">
        <InputPanel onScan={handleScan} loading={loading} activePhase={activePhase} onPhaseChange={setActivePhase} />
        <ResultCard result={result} activePhase={activePhase} />
      </div>
      <IncidentLog items={incidentLog} />
    </div>
  );
}