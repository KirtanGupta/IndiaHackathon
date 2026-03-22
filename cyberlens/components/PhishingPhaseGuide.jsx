import { formatRisk } from "../utils/formatRisk";
import { severityColor } from "../utils/severityColor";

function PercentageBar({ label, value, color }) {
  return (
    <div style={{ marginBottom: 12 }}>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
        <span>{label}</span>
        <span>{value}%</span>
      </div>
      <div style={{ height: 10, background: "rgba(255,255,255,0.08)", borderRadius: 999 }}>
        <div
          style={{
            height: "100%",
            width: `${Math.min(value, 100)}%`,
            background: color,
            borderRadius: 999
          }}
        />
      </div>
    </div>
  );
}

export default function PhishingPhaseGuide({ emailResult }) {
  if (!emailResult || emailResult.source === "inactive") {
    return null;
  }

  const phishingProbability = Math.round((emailResult.probabilities?.phishing || 0) * 100);
  const benignProbability = Math.round((emailResult.probabilities?.benign || 0) * 100);
  const severity = emailResult.severity || "low";
  const label = emailResult.label || "unknown";
  const breakdown = emailResult.score_breakdown || {
    model_component: 0,
    heuristic_component: 0,
    raw_heuristic_score: 0,
  };

  return (
    <section className="panel" style={{ marginBottom: 20 }}>
      <h2>Phishing Phase Walkthrough</h2>
      <p>
        This panel only reflects the phishing model. Nothing from URL or deepfake is included here.
      </p>
      <div className="metric-row">
        <div className="metric">
          <strong>{label.toUpperCase()}</strong>
          <div>Predicted Label</div>
        </div>
        <div className="metric">
          <strong>{Math.round((emailResult.confidence || 0) * 100)}%</strong>
          <div>Model Confidence</div>
        </div>
        <div className="metric">
          <strong>{formatRisk(emailResult.score || 0)}</strong>
          <div>Email Risk</div>
        </div>
      </div>
      <div style={{ marginTop: 16 }}>
        <PercentageBar label="Phishing probability" value={phishingProbability} color="linear-gradient(90deg, #ff6b6b, #ff9f68)" />
        <PercentageBar label="Benign probability" value={benignProbability} color="linear-gradient(90deg, #8ef0b5, #d6ff8b)" />
      </div>
      <div style={{ marginTop: 16 }}>
        <span className="badge" style={{ background: severityColor(severity), color: "#08110d" }}>
          {severity.toUpperCase()}
        </span>
      </div>
      <div className="score-breakdown" style={{ marginTop: 16 }}>
        <div className="metric">
          <strong>{breakdown.model_component}/100</strong>
          <div>Model Contribution</div>
        </div>
        <div className="metric">
          <strong>{breakdown.heuristic_component}/100</strong>
          <div>Signal Contribution</div>
        </div>
        <div className="metric">
          <strong>{breakdown.raw_heuristic_score}/100</strong>
          <div>Raw Heuristic Strength</div>
        </div>
      </div>
      <div style={{ marginTop: 16 }}>
        <h3>Why this score happened</h3>
        <p>The model contribution comes from the phishing probability.</p>
        <p>The signal contribution comes from suspicious phrases, threats, urgency, and risky links found in the email body.</p>
        <p>The final score is a weighted blend of both, so obvious fraud emails can score high even if the model alone is cautious.</p>
      </div>
      <div style={{ marginTop: 16 }}>
        <h3>How to test</h3>
        <p>1. Click `Load Suspicious Email` and run the email phase.</p>
        <p>2. Click `Load Legit Email` and run it again.</p>
        <p>3. Compare the label, probabilities, contributions, and final risk score.</p>
      </div>
      <div style={{ marginTop: 16 }}>
        <h3>Matched Signals</h3>
        <div className="signal-chips">
          {(emailResult.matched_signals || []).map((signal) => (
            <span key={signal} className="signal-chip">{signal}</span>
          ))}
        </div>
      </div>
    </section>
  );
}