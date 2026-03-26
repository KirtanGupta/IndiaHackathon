import { useState } from "react";
import InputPanel from "../components/InputPanel";
import ResultCard from "../components/ResultCard";
import { scan } from "../api/scan";

const initialResult = {
  active_phase: "email",
  score: 0,
  severity: "low",
  explanation: "Paste an email and run the phishing scan to see the risk analysis.",
  module_explanations: { email: "" },
  module_reasoning: { email: [] },
  modules: {
    email: {
      module: "email",
      score: 0,
      severity: "low",
      source: "inactive",
      label: "-",
      confidence: 0,
      probabilities: { benign: 0, phishing: 0 },
      matched_signals: [],
      score_breakdown: {
        model_component: 0,
        heuristic_component: 0,
        raw_heuristic_score: 0,
      },
    },
  },
  signals: { email_length: 0 },
};

export default function App() {
  const [result, setResult] = useState(initialResult);
  const [loading, setLoading] = useState(false);
  const [scanDuration, setScanDuration] = useState(null);
  const [scanComplete, setScanComplete] = useState(false);

  async function handleScan(emailText) {
    setLoading(true);
    const start = performance.now();
    try {
      const data = await scan({
        active_phase: "email",
        email_text: emailText,
        url: "",
        media_type: "audio",
      });
      setResult(data);
      setScanDuration(((performance.now() - start) / 1000).toFixed(1));
      setScanComplete(true);
      window.setTimeout(() => setScanComplete(false), 800);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page-shell scanner-page">
      <section className="scanner-shell">
        <InputPanel onScan={handleScan} loading={loading} />
        <ResultCard result={result} scanDuration={scanDuration} />
      </section>
    </main>
  );
}
