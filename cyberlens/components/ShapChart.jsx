export default function ShapChart({ score }) {
  const bars = [
    { label: "Email", value: Math.min(score, 40) },
    { label: "URL", value: Math.max(score - 20, 10) },
    { label: "Media", value: Math.max(score - 35, 6) }
  ];

  return (
    <div>
      <h3>Signal Contribution</h3>
      {bars.map((bar) => (
        <div key={bar.label} style={{ marginBottom: 10 }}>
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <span>{bar.label}</span>
            <span>{bar.value}</span>
          </div>
          <div style={{ height: 10, background: "rgba(255,255,255,0.08)", borderRadius: 999 }}>
            <div
              style={{
                height: "100%",
                width: `${Math.min(bar.value, 100)}%`,
                background: "linear-gradient(90deg, #8ef0b5, #ffd166)",
                borderRadius: 999
              }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}