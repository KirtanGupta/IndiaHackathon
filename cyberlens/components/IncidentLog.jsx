export default function IncidentLog({ items }) {
  return (
    <section className="panel" style={{ marginTop: 20 }}>
      <h2>Demo Timeline</h2>
      <div className="incident-list">
        {items.length === 0 ? (
          <div className="incident-item">No scans run yet.</div>
        ) : (
          items.map((item) => (
            <div key={item.id} className="incident-item">
              <strong>{(item.phase || "phase").toUpperCase()} - {(item.severity || "low").toUpperCase()} - {item.score || 0}/100</strong>
              <p>{item.summary || "No summary available."}</p>
            </div>
          ))
        )}
      </div>
    </section>
  );
}