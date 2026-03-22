import { formatRisk } from "../utils/formatRisk";
import { severityColor } from "../utils/severityColor";

export default function UrlPhaseGuide({ urlResult }) {
  if (!urlResult || urlResult.source === "inactive") {
    return null;
  }

  const severity = urlResult.severity || "low";

  return (
    <section className="panel" style={{ marginBottom: 20 }}>
      <h2>URL Phase Walkthrough</h2>
      <p>
        This panel only reflects the URL detector. It scores risky URL patterns like insecure protocol,
        suspicious terms, long links, and login-style domains.
      </p>
      <div className="metric-row">
        <div className="metric">
          <strong>{formatRisk(urlResult.score || 0)}</strong>
          <div>URL Risk</div>
        </div>
        <div className="metric">
          <strong>{severity.toUpperCase()}</strong>
          <div>Severity</div>
        </div>
        <div className="metric">
          <strong>{(urlResult.matched_signals || []).length}</strong>
          <div>Matched Signals</div>
        </div>
      </div>
      <div style={{ marginTop: 16 }}>
        <span className="badge" style={{ background: severityColor(severity), color: "#08110d" }}>
          {severity.toUpperCase()}
        </span>
      </div>
      <div style={{ marginTop: 16 }}>
        <h3>How to test</h3>
        <p>1. Click `Load Suspicious URL` and run the URL phase.</p>
        <p>2. Click `Load Safe URL` and run it again.</p>
        <p>3. Compare the score and matched signals.</p>
      </div>
      <div style={{ marginTop: 16 }}>
        <h3>Matched Signals</h3>
        <div className="signal-chips">
          {(urlResult.matched_signals || []).map((signal) => (
            <span key={signal} className="signal-chip">{signal}</span>
          ))}
        </div>
      </div>
    </section>
  );
}