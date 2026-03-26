export default function IncidentLog({ items }) {
  return (
    <section className="panel timeline-panel" style={{ marginTop: 20 }}>
      <div className="result-header-row">
        <div>
          <h2>Recent Scans</h2>
          <p>Quick history of the latest phishing checks in this session.</p>
        </div>
      </div>
      <div className="incident-list">
        {items.length === 0 ? (
          <div className="incident-item">No scans yet. Run the phishing scanner to start building a history.</div>
        ) : (
          items.map((item) => (
            <div key={item.id} className="incident-item">
              <strong>{(item.label || "unknown").toUpperCase()} • {(item.severity || "low").toUpperCase()} • {item.score || 0}/100</strong>
              <p>{item.summary || "No summary available."}</p>
            </div>
          ))
        )}
      </div>
    </section>
  );
}
