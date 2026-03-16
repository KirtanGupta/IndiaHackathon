import { useState } from "react";

const defaultState = {
  email_text: "Your account will be suspended unless you verify your password today.",
  url: "http://secure-login-example.com/reset",
  media_type: "audio"
};

export default function InputPanel({ onScan, loading }) {
  const [form, setForm] = useState(defaultState);

  function updateField(event) {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  }

  function submitForm(event) {
    event.preventDefault();
    onScan(form);
  }

  return (
    <form className="panel form-grid" onSubmit={submitForm}>
      <div>
        <h2>Threat Inputs</h2>
        <p>Paste suspicious content and run a fast heuristic scan.</p>
      </div>
      <label>
        Suspicious Email Text
        <textarea name="email_text" value={form.email_text} onChange={updateField} />
      </label>
      <label>
        Suspicious URL
        <input name="url" value={form.url} onChange={updateField} />
      </label>
      <label>
        Media Type
        <select name="media_type" value={form.media_type} onChange={updateField}>
          <option value="audio">Audio</option>
          <option value="video">Video</option>
        </select>
      </label>
      <button className="primary-button" type="submit" disabled={loading}>
        {loading ? "Scanning..." : "Run Scan"}
      </button>
    </form>
  );
}