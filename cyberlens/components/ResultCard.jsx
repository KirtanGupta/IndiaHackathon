function StatCard({ label, value, hint }) {
  return (
    <div className="stat-card">
      <span className="stat-label">{label}</span>
      <strong className="stat-value">{value}</strong>
      <span className="stat-hint">{hint}</span>
    </div>
  );
}

import { useEffect, useState } from "react";

function ProbabilityBar({ label, value, tone }) {
  return (
    <div className="probability-item compact">
      <div className="probability-label-row">
        <span>{label}</span>
        <strong>{Math.round(value * 100)}%</strong>
      </div>
      <div className="probability-track compact">
        <div className={`probability-fill ${tone}`} style={{ width: `${Math.max(6, value * 100)}%` }} />
      </div>
    </div>
  );
}

export default function ResultCard({ result, scanDuration }) {
  const [animate, setAnimate] = useState(false);

  useEffect(() => {
    if (!result) return;
    setAnimate(true);
    const timer = window.setTimeout(() => setAnimate(false), 800);
    return () => window.clearTimeout(timer);
  }, [result]);
  const emailModule = result.modules?.email || {};
  const probabilities = emailModule.probabilities || { benign: 0, phishing: 0 };
  const reasoning = result.module_reasoning?.email || [];
  const matchedSignals = emailModule.matched_signals || [];
  const detected = emailModule.label === "phishing";

  return (
    <section className={`scanner-panel scanner-results ${animate ? "scan-complete" : ""}`}>
      <div className="results-topbar">
        <h2 className="panel-title small">Scan results</h2>
        <span className={`result-pill ${detected ? "danger" : "safe"}`}>
          {detected ? "Phishing detected" : "Looks legitimate"}
        </span>
      </div>

      <div className="stats-grid">
        <StatCard
          label="Confidence"
          value={`${Math.round((emailModule.confidence || 0) * 100)}%`}
          hint={detected ? "High risk" : "Model output"}
        />
        <StatCard
          label="Signals found"
          value={matchedSignals.length}
          hint={matchedSignals.length > 0 ? "Matched patterns" : "No clear flags"}
        />
        <StatCard
          label="Scan time"
          value={`${scanDuration || "0.0"}s`}
          hint="Last run now"
        />
      </div>

      <div className="panel-block">
        <h3 className="section-title">Probability breakdown</h3>
        <ProbabilityBar label="Phishing" value={probabilities.phishing || 0} tone="danger" />
        <ProbabilityBar label="Legitimate" value={probabilities.benign || 0} tone="safe" />
      </div>

      <div className="panel-block">
        <h3 className="section-title">Matched signals</h3>
        <div className="signal-chips compact">
          {matchedSignals.length > 0 ? (
            matchedSignals.map((signal) => (
              <span key={signal} className="signal-chip compact">{signal}</span>
            ))
          ) : (
            <span className="signal-chip compact">No suspicious signals found</span>
          )}
        </div>
      </div>

      <div className="panel-block">
        <h3 className="section-title">Reasoning</h3>
        <div className="reasoning-list compact">
          {reasoning.length > 0 ? (
            reasoning.slice(0, 4).map((item) => (
              <div key={item} className="reasoning-item compact">{item}</div>
            ))
          ) : (
            <div className="reasoning-item compact">Run a scan to generate detailed reasoning.</div>
          )}
        </div>
      </div>
    </section>
  );
}
