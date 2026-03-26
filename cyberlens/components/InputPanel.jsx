import { useEffect, useState } from "react";

const defaultEmail = "We detected unusual activity on your account and need you to confirm your identity immediately.";

const presets = {
  suspicious: "We detected unusual activity on your account and need you to confirm your identity immediately.",
  benign: "Your interview is confirmed for Monday at 11 AM in the main office.",
  borderline: "Your refund request is ready but we need account verification before release.",
};

export default function InputPanel({ onScan, loading }) {
  const [emailText, setEmailText] = useState(defaultEmail);

  useEffect(() => {
    setEmailText(defaultEmail);
  }, []);

  function submitForm(event) {
    event.preventDefault();
    onScan(emailText);
  }

  return (
    <form className="panel form-grid scan-panel" onSubmit={submitForm}>
      <div className="scan-header">
        <h2>Scan Email Text</h2>
        <p>
          Paste the body of an email and run a phishing-only scan. The dashboard will show the label, confidence,
          suspicious signals, and the blended risk score.
        </p>
      </div>

      <div className="preset-row">
        <button type="button" className="secondary-button" onClick={() => setEmailText(presets.suspicious)}>
          Suspicious
        </button>
        <button type="button" className="secondary-button" onClick={() => setEmailText(presets.benign)}>
          Legit
        </button>
        <button type="button" className="secondary-button" onClick={() => setEmailText(presets.borderline)}>
          Borderline
        </button>
      </div>

      <label className="email-box">
        <span>Email Content</span>
        <textarea
          name="email_text"
          value={emailText}
          onChange={(event) => setEmailText(event.target.value)}
          placeholder="Paste suspicious email text here"
        />
      </label>

      <div className="helper-grid compact-helper-grid">
        <div className="helper-card">
          <strong>Tip</strong>
          <span>Use the full message body for a more realistic result.</span>
        </div>
        <div className="helper-card">
          <strong>Compare</strong>
          <span>Check how confidence and signals change across examples.</span>
        </div>
      </div>

      <button className="primary-button compact-submit" type="submit" disabled={loading}>
        {loading ? "Scanning..." : "Run phishing scan"}
      </button>
    </form>
  );
}
