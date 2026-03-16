export default function IncidentLog({ items }) {
  return (
    <section className="panel" style={{ marginTop: 20 }}>
      <h2>Recent Incidents</h2>
      <div className="incident-list">
        {items.length === 0 ? (
          <div className="incident-item">No incidents logged yet.</div>
        ) : (
          items.map((item) => (
            <div key={item.id} className="incident-item">
              <strong>{item.severity.toUpperCase()} - {item.score}/100</strong>
              <p>{item.summary}</p>
            </div>
          ))
        )}
      </div>
    </section>
  );
}