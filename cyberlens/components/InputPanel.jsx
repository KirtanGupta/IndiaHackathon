import { useEffect, useState } from "react";

const phaseDefaults = {
  email: {
    email_text: "Your account will be suspended unless you verify your password today.",
    url: "",
    media_type: "audio"
  },
  url: {
    email_text: "",
    url: "http://secure-login-example.com/reset",
    media_type: "audio"
  },
  deepfake: {
    email_text: "",
    url: "",
    media_type: "audio"
  }
};

const phaseDescriptions = {
  email: "Run only the phishing model and test suspicious vs legitimate email text.",
  url: "Run only the URL detector without mixing email or deepfake scores.",
  deepfake: "Run only the deepfake phase using the selected media type."
};

export default function InputPanel({ onScan, loading, activePhase, onPhaseChange }) {
  const [forms, setForms] = useState(phaseDefaults);

  useEffect(() => {
    setForms((current) => ({ ...phaseDefaults, ...current }));
  }, []);

  function updateField(event) {
    const { name, value } = event.target;
    setForms((current) => ({
      ...current,
      [activePhase]: {
        ...current[activePhase],
        [name]: value,
      },
    }));
  }

  function applyExample(kind) {
    const examples = {
      email: {
        suspicious: "Urgent verify your password immediately or your account will be suspended",
        benign: "Weekly team meeting tomorrow at 10 AM in the conference room"
      },
      url: {
        suspicious: "http://secure-bank-verification-update.com/login",
        benign: "https://docs.python.org/3/tutorial/"
      }
    };

    if (activePhase === "email") {
      setForms((current) => ({
        ...current,
        email: {
          ...current.email,
          email_text: examples.email[kind],
        },
      }));
    }

    if (activePhase === "url") {
      setForms((current) => ({
        ...current,
        url: {
          ...current.url,
          url: examples.url[kind],
        },
      }));
    }
  }

  function submitForm(event) {
    event.preventDefault();
    onScan({
      active_phase: activePhase,
      ...forms[activePhase],
    });
  }

  const form = forms[activePhase];

  return (
    <form className="panel form-grid" onSubmit={submitForm}>
      <div>
        <h2>Demo Inputs</h2>
        <p>{phaseDescriptions[activePhase]}</p>
      </div>
      <div className="phase-switcher">
        <button type="button" className={activePhase === "email" ? "phase-pill active" : "phase-pill"} onClick={() => onPhaseChange("email")}>
          1. Email
        </button>
        <button type="button" className={activePhase === "url" ? "phase-pill active" : "phase-pill"} onClick={() => onPhaseChange("url")}>
          2. URL
        </button>
        <button type="button" className={activePhase === "deepfake" ? "phase-pill active" : "phase-pill"} onClick={() => onPhaseChange("deepfake")}>
          3. Deepfake
        </button>
      </div>

      {activePhase === "email" ? (
        <>
          <div className="phase-actions">
            <button type="button" className="secondary-button" onClick={() => applyExample("suspicious")}>Load Suspicious Email</button>
            <button type="button" className="secondary-button" onClick={() => applyExample("benign")}>Load Legit Email</button>
          </div>
          <label>
            Email Text
            <textarea name="email_text" value={form.email_text} onChange={updateField} />
          </label>
        </>
      ) : null}

      {activePhase === "url" ? (
        <>
          <div className="phase-actions">
            <button type="button" className="secondary-button" onClick={() => applyExample("suspicious")}>Load Suspicious URL</button>
            <button type="button" className="secondary-button" onClick={() => applyExample("benign")}>Load Safe URL</button>
          </div>
          <label>
            Suspicious URL
            <input name="url" value={form.url} onChange={updateField} />
          </label>
        </>
      ) : null}

      {activePhase === "deepfake" ? (
        <label>
          Media Type
          <select name="media_type" value={form.media_type} onChange={updateField}>
            <option value="audio">Audio</option>
            <option value="video">Video</option>
          </select>
        </label>
      ) : null}

      <button className="primary-button" type="submit" disabled={loading}>
        {loading ? "Scanning..." : `Run ${activePhase} phase`}
      </button>
    </form>
  );
}